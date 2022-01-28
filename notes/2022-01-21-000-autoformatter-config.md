# Configureless Formatters
tags: code-style, todo, rant

There's definitely a trend going around of code formatters that don't offer the user any options.
The idea is that if "there can be only one" style across an entire language, then it's possible for a someone to recognize the style of _any_ code written in that language.
If that style has been automated in an official tool that has no configuration options, then that _should_ move the community towards a single style.

This is community management by royal decree.
Which is not to say pure anarchy is the way to go either.
It seems that most ideologies, when allowed to practice to their logical conclusions, eventually fall apart;
  it's almost like the physics of social structure is too complex to be accounted for by a reasonable number of rules and principles.
However, I do have some more proximate causes of concern.

## Sub-Optimality

Fundamentally, code style is a way to describe programmer intension.
This is just like in natural language, where a question can be phrased in a neutral style like "Did you take out the trash?", but when phrased in a different style "Did you really take out the trash?" has a very different intension and message.
A code style standard (as enforced by a formatter) is a way to describe what the neutral style should be.
When that style is deviated from, this shows the reader that something "weird" is going on, and more care should be taken when reading.
A configure-less formatter ensures that everyone speaks the same neutral, but one project's weird is another project's normal.
A configuration file would be able not only allow the weird project to use its own idioms, but also be a place to document how and _why_ the project is weird.

Code formatters generally do four things:
  * make and enforce a trivial decisions,
  * detect and replace known anti-patterns,
  * erase intentional deviations from the neutral standard, and
  * use brackets instead of indentation as ground-truth for nesting intension.



### Trivial Decisions

(How do you pronounce potato?)

The classic example here is how to indent code: tabs or spaces?, how big?

Honestly, if you let people configure indentation size, most everyone will quickly realize that the extra configuration effort for every project is not worth such a trivial payoff.
Instead, they'll configure the language-specific settings in their editor once and be done with it, or maybe install a plugin that can read the formatter configuration and do the project-specific configuration automatically.
For people who haven't yet realized that indentation style is trivial—and they're usually vocal about it—they will spend their efforts configuring their projects, and _not pestering the language/formatter maintainer_ with an unending stream of duplicate, whiny issues to close.
And what's the worst that could happen?, every project has a different preferences over a trivial matter like indentation?, it's a trivial difference.

Whitespace is one of the most controversial things because everyone has preferences, but no natural preference improves/degrades quality.
These trivial decisions are defined by that last point: their inability to influence a general reader's ability comprehend the code.

TODO organize imports, organize pragmas, organize switch/case/match clauses, indentation, trailing whitespace, line-length, organize related declarations/definitions

### Known Anti-Patterns

(…up with which I will not put.)

TODO honestly, use compiler warnings: these are things like variable shadowing, dead code, lack of type signature at top-level, public instance data members, global mutables, and so on; the compiler is the place where the knowledge is

TODO one thing I _would_ like is to automatically detect common todo/fixme/debug/&c tags; maybe even open issues

TODO you might be thinking that "my language is interpreted", but that doesn't mean it doesn't have a compiler: PyPy for example, or even CPython which generates bytecode by default, or the TypeScript which compiles to ECMAScript, or Scheme which has numerous compilers since it's been a fruitful source for compiler experimentation, and I'm sure you can think of your own examples

### Deviations from Neutral

TODO organize switch/case/match clauses, organize related declarations/definitions


TODO
> Many formatters apply what I think of as "niche" rules, for example: no spaces on the inside of brackets.
> This is a fine rule in theory, but in practice it is useless.
> I agree with (apparently) the programming community that spaces inside brackets are generally ugly.
> So I never accidentally put spaces inside my brackets, so the formatter rule never applies.
> However, there are times when brackets have gotten deeply nested, and spaces are essentially _required_ for readability.
> (It doesn't take much: consider the Python `sorted(((p.x, p.y) for point in points3d), reverse=True)` and its ugly triple-open-paren.
>   One of these parenthesis need some space in there, or you'll pay an extra line.)
> It is only at these times—when I specifically want to flaunt the rule—that the formatter changes my code to enforce the rule.
> 
> The one place where niche rules _are_ useful is for the newcomers (and there must always be newcomers).
> Perhaps they saw extra spaces inside parenthesis once and now cargo-cult it into all their code.
> Thankfully, it's pretty easy for a formatter to detect such people, and thus leave the greybeards alone.
> If more than (say) half the parens on a single line have spaces inside them, then that's a noob, and the formatter should
>   _report the community's preferences_ and why following them is important, and
>   offer to reformat all the parenthesis' whitespace.
> That's a policy that doesn't trip anyone up, and can even convert inexperience to knowledge.
> In the absence of a better formatter, the option to turn off such a rule would at least let me stop my intention from getting stepped on.

TODO
> Even these no-config formatters understand that their rules cannot be absolute.
> They will usually offer some comment-based syntax that can turn off rules, all-at-once or piecemeal.
> To be honest, I don't want to be bothered to learn yet another niche-use syntax, and I don't want to stop my flow to google for it just because I've compiled.
> Perhaps it wouldn't be so bad if the formatter could run as I type, though that strategy might lead to other problems (sometimes I move the cursor without looking).
> Additionally, I prefer my comments to do one thing: provide commentary on the reasoning that influenced the code.
> Putting formatter commands in the comments (or commands to the compiler i.e. pragmas, or commands to the documentation generator i.e. doc comments) makes it harder to distinguish code from commentary.
> To be fair, this is not a problem specific to config-free formatters, but a that does increase the chance that I will need to insert a special "comment".


### Bracketing Bugs

### Thoughts on Community Structure

As much as you might wish there to be no options, there are _always_ options.
If the formatter is open-source (and why wouldn't it be?), then someone who wants a different style can fork your formatter and change a few variables; perhaps it'll make a good starter project while they learn the language.
More likely—because it is the laziest option—is to simply not use the formatter at all.
Personally, I'd prefer to use and for people to use at least _part_ of a formatter rather than none of it.

If the officially-sanctioned formatter has no configuration, why not make it part of the language instead of a separate specification?
Obviously, you'd like the formatter implemented in a separate library from the compiler (as a library), so it can be reused across multiple compiler implementations.
In my own parsers, if commas are allowed to separate terms, then I usually require that such commas be followed by whitespace.


## My Wish List


TODO auto-tabulator

TODO remember refusal of a suggestion (preferably outside the source code)




# Rant (FIXME: delete)








How far should formatting extend?
Is there a canonical ordering of import statements?, pattern-match clauses?, language extension pragmas?, canonicalizing types through isomorphisms?
These are things that I often find myself sorting out more-or-less manually (sometimes with the help of my editor's "alphabetize lines" feature).
A formatter that at least allows for _some_ configuration can allow a community to experiment with different cut-off points.
Projects that do want a lot of organization can even opt-in to extra formatting without extra tooling when the community does decide on where to draw the line.






TODO if indents are wrong, that indicates a bug I should look at, not something to be auto-corrected
TODO import organization is mostly taken care of by a non-specific alphabetize and compiler warnings
TODO I need (could use) tables, and this can (mostly) be done language-agnostic, or the lang could integrate its own syntax

