# Set Theory vs Type Theory or Untyped vs Typed

tags: lang-design, math, rant

The choice of a foundations for mathematics is simultaneously not very important,
  but also fraught with landmines that explode with the force of deeply-held philosophical beliefs.
The dialectic (fancy word for debate that plays out cultural timescales) begins from the start of foundations as a field of study, namely: classical and constructivist mathematicians started it.
The classicists got there first with the development of Zermelo-Fraenkel set theory in 1922.
The constructivists lagged behind, eventually creating Martin-Löf type theory in 1972, fifty years later.

What this has to do with dynamic vs. static typing is not often spelled out clearly.
Nevertheless, it seems important enough for people on both ends of the debate to bring up.
There do seem to be deep parallels between set theory & dynamic typing on the one hand, and type theory & static typing on the other.
Perhaps the least of the parallels is that this debate has gone on for a long time,
  the dynamic typers go there first with Lisp in 1960,
  and the static typers had to catch up with (let's say) Coq in 1989 or perhaps ML in 1973.

Aside:
One could argue with the exact timeline or choices of reference, but for my purposes, these are good enough.
While type theories today are generally modifications to the original Martin-Löf theory,
  these modifications are like the modifications that are commonly done to the lambda calculus.
My primary comparison in this article is between Lisp dialects and HoTT-based languages.
The latter is an active area of research.

## The Educated Uneducated

In some online comments, noted Lisp-enjoyer and static-type-detractor John Schutt brings up set theory.
His words practically jump off the page and demand critique.

> In my math classes I never encountered types as experienced in programming.
> Sets, yes, algebraic structures of various kinds yes, but they lacked some qualitative type-ness.

Indeed, type theory is not taught in mathematics classes at the undergrad level,
  and as far as I can tell, even at the grad level, one has to seek out type theory independently.
This is hardly a point for set theory or a mark against type theory.
Instead, it is simply the historical fact of set theory being created before type theory.
Whether the first thing to arrive on the scene is better is an entirely different question.
In fact, let's apply our [design meta-strategy](2023-02-16-000-predominant-theories-and-local-maxima.md):
  *Set theory became the predominant theory shaping all of mathematics,
  and so nearly all mathematicians fell into the trap of not looking for anything better.*

Dr. Schutt goes on to claim that in set theory, abstraction is "perfect".
He gives an example:
> If just at the moment you're not treating functions as subsets of the cartesian product of domain and codomain,
>   then just at the moment they aren't such subsets.
> Another time they might be.

I'll pick a simpler example, the natural numbers.
Mathematicians often think of the naturals as von Neumann ordinals.
When I say "often", I mean that Wikipedia at time of writing references exactly one alternative,
  Zermelo ordinals, which it says "is nowadays only of historical interest".
Once again, a single theory has become predominant (though at least IMO it probably is the best in ZF).
Of course, when you're working with ℕ, you are probably abstracting the representation away, so it doesn't matter, right?
Well, the issue is that in ZF, everything is a set, so it is grammatically allowed to ask about
  `∃a ∈ ℕ. 5 ∈ a`.
It is allowed because quantifiers always range over sets, and one can ask about the inclusion of an element in a set.
The statement itself has no answer of course, it depends on the representation of ℕ
  (with Zermelo ordinals, it is true for `a = 6`,
  and with von Neumann ordinals, it is true for all `a > 5`,
  and who knows about any of the other representations).
In other words, if a machine were to try computing a truth value for this statement, it would become stuck.
While one can't make a machine that will never get stuck, I believe this point of failure is unnecessary.
In particular, it could have been avoided by a more rigorous application of abstraction barriers.
The abstraction present in set theory _can_ be broken, and therefore isn't "perfect".
Type theory does not have these problems because it rigorously enforces abstraction boundaries.

One more thing of note in Dr. Schutt's discussion of set theory's "advantages":
> If you start with some structure A and use it to define another structure B,
> then use B to define C, and C to define A, you really get back to A,
> not some imperfect simulation/approximation of it.

Well, this is also the case in type theory.
It is called the Univalence Axiom, introduced by Vladimir Voevodsky in 2010.
Working type theorists I have encountered seem to take it for granted that
  univalent type theories are the way that type theory will be in the future.
I won't go into detail, but suffice it to say that this is necessary knowledge to have
  when critiquing type theory as a field.
Nevertheless, even well-educated Lispers such as Dr. Schutt seem to simply
  not be aware of such core ideas.

## Conclusion

I don't know that there is a conclusion.
Look, John Schutt isn't a fool, and I don't mean to pick on him;
  probably anyone could have made these errors
  if they aren't working in foundations of math, logic, and/or computing.

I guess set theory (and recently type theory) are so omnipresent that everyone is exposed to them,
  and their work is based on them, so they feel qualified to share opinions.
At the same time, these theories are quite delicate,
  and so very few people truly understand the context.
Together, these factors create a perfect storm for misinformation and bad opinions,
  whether reporting incorrect things, or failing to report necessary context.
At least with this stuff, the misinformation isn't leading to deaths.
It's just disappointing that the officially card-carrying best-think-people somethings fail to think clearly before spouting uninformed opinions without evidence.
I wonder what hope we have for "yer dad" to stop accidentally sharing misinformation?

Well, to not end on a downer, I do have one thing that's actually relevant to the debates.
Computers are constructive; they don't just conjure infinities out of thin air.
Why shouldn't we be using a theory of computation based more in constructive mathematics?
When you look at proof assistants, they're all type theories, because that's what has been successful.
If one were trying to validate some functionality in your code, wouldn't you like something to help you prove your code right?
And, once you get some experience in dependently-typed, total languages with tactics support,
  you might find you don't pay much as you might think to unlock all the help you might possibly need.
Or, even with a non-dependent, partial language,
  you hardly pay anything, and get the vast majority of the help you might imagine wanting.
