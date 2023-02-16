# A Load of Versioning Notes of Dubious Quality

tags: versioning

Modules can be parameterized not only by other modules/types/values, but also by flags.
Flags are simple booleans (or perhaps strings) passed to the module by the compiler, via the package build system.
These flags can participate in simple boolean/relational operations to guard declarations.

Importantly, it must be possible to compile a module to documentation for all possible flag settings.

==============

A single codebase can provide multiple interfaces.
I'm especially thinking about teh codebase for a unicode-aware text type.
This could export an opaque interface, which should be good enough for most use cases,
  but could also expose a more internal interface for when performance of the internals has a significant impact on the performance of clients.
Additionally, we could even split the opaque interface into "core" and "extras", so that clients who only depend on a few features that are unlikely to change can build against core.
The extras functionality would be for less obviously-correct things: whenever there is a choice in an interface that needed to be made but couldn't be fully thought through at the time.
Being part of the same codebase means it's easy to maintain with changes in the internals, and laying "on top" of the core means breaking changes affect fewer clients (only those which need the extras.



===============

static linking can avoid dependency conflicts at the cost of possibly duplicated code.
Simply find and install/register (sandboxed) every direct dependency of a package.
Each node in the dependency tree does this independently until there are no more dependencies.
If 


Keep a database of code by package-version(-flags).
Register the package to be built in the db.
While there are registered packages in the db that have not been searched:
  Search that package for dependencies:
  If the db already has a package-version that fits the constraints, use the registered one.
  Otherwise, find and register a new package-version in the db for that dependency.
At the end, we may have multiple versions of the same package registered:
  we may try to find a single version that fits all constraints
  if we can't (won't) find a single version, then report that multiple versions are being used


Artifact flags are probably interesting.
I think generally they are products of sums of units, possibly minus invalid combinations.
This way, we can have stuff like `(Unix | Windows) × (Pthreads | ThreadShim) - (Windows × Pthreads)`.

================

Version information should be attached to every function, just like documentation.
This information should say when it was introduced, possibly a prediction of what version it will stick around through, when it was deprecated (if applicable), during what versions was there an incompatible implementation under the same name.

If performance is part of the interface, there should be a way to indicate this as well.


============


build the transitive DAG, then collapse into a table
  rows in this table are marked "weak" if they are only mentioned as optional dependencies
remove weak dependencies (only included optionally) when building with a minimal setup

ah, I was about to say "apply version bounds from each dependency",
  but those version bounds vary based on the version of each dependency
  that's what makes it hard

anyway, I guess we keep the DAG, make a guess at which package versions to start with (at the roots)
thie thing is, I still want to remember which constraints came from where in the dependency tree

ah hell, even the graph itself depends on the selected versions of nodes higher in the graph!




I suppose one way to speed this up is to cache known-good plans
if a dependency has a known-good plan that meets our requriements, we can start dependency solving from there
  if newer versions are available, we can try to use those
  or if we are testing for compatibility with minimum versions, we can work our way backwards

I'm also tempted by the idea of convex hulls:
  if you ask for X version of package P, you won't have to look outside versions Y-Z if P's dependency
then, if we ask for P between A-B, we can overlap these hulls to find the maximum search space
I'm just not sure how much search space that would prune, really


The other thing I'm annoyed by is pre-judged upper version bounds.
If I write software against `text-3.9` and rely only on `Text.pack` and `Text.unpack`, what does it matter that `text-4.0` removed `obsscureFunction`? My software will still build on `text-4.0`, even though that's a "backwards-incompatible" change.
Prematurely adding such pessimisstic version bounds to my package only means that my dependents will have to pester me to update my metadata (with no other code changes) just so that the dependency resolution search space isn't pruned excessively, just to build anything.

The flip side of that is that if I don't constrain my upper bound ahead of time, dependents of my package might end up with failing builds because `text-5.0` altered the functions I _do_ use.
Here though, the builder can add an upper version bound of their own that prunes 5.0 from the search space.
As long as no other packages rely on 5.0+, then the software will build without having to pester upstream.
The trick is getting good error messages to the user when this happens.
I think this will require information about version differences to be _in the source code_, not just in the metadata.
This way, when compilation (or testing) fails, we can hopefully see that the failure was related to xFunction, look up version difference info, and say "hey, xFunction has changed in v5.0, try adding a version bound `text <5.0`".

This especially interacts with deprecation.
The whole point of deprecation is that it is backwards-compatible... but apparently some people refuse to drop `-Werror` from their packages (not their local development flags, the _package itself_).
This means that PVP specifies that deprecation causes a major version bump... exactly the same as if I totally removed it in the first place, so why bother with deprecation at all, especially if we give pessimistic version bounds?
If deprecation is a major version bump, then we should at least not be required to give an upper bound.

For cabal in particular, which seems to prefer newest all the time, with pessimistic version bounds, we get awful dependency solver errors.
  Even for simple incompatibilities we are presented with a mess of backtracking information.
However, with optimistic version bounds we get a build error while build _a particular package_.
Cabal knows which package failed to build, and should know constraints on that package from the dependency solution, and so should be able to detect that the failing build failed to place an upper bound on some other package(s), and should be able to step in and suggest "try placing stricter upper bounds on <failing package> in your package", maybe even with a suggestion of the next lower version number.

The real reason any disagreement exists is because it is infeasible for a single to test every versioning setup.
Even for packages like `text` the sheer number of versions (and options for those versions) is staggering.
What we need to do is distribute the workload, but combine the results in a trustworthy way.
Now, I don't know much about proof-of-work, proof-carrying code, trusted computing, or anything like which might allow untrusted node to do a large amount of work while also supplying an easily-checkable proof that the work was done correctly.
However, we can always implement "reports": "I successfully built/failed to build this package with these versions and configurations of dependency" can automatically be sent to a central server, which find the most popular reports and verifies the claim itself.
This way, we focus on the most popular packages, and can report our results to anyone who finds us trustworthy.
