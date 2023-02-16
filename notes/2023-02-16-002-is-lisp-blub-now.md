# Is Lisp Blub Now?

tags: lang-design, lisp, haskell

It's quite common for Lispers to outright say that Lisp is the best programming language.
I think most Lispers here would agree with Paul Graham here
  as to why Lisp is best (and that Lisp is best):

> Lisp is so great… because it is simply the most powerful language available.
> Lisp code… is made of data structures that you can traverse.

That is, homoiconicity and macros are extremely good, and Lisp is the only™ language to have them.
I hope that "TM" not some sort of Chekov's gun™.

Anyway all quotes come from a article section called "The Blub Paradox".
He lays out the paradox, which I will condense here:

  > [Consider] a hypothetical language called Blub… falls right in the middle of the [power] continuum.
  >
  > …Our hypothetical Blub programmer wouldn't use [a language lower on the power continuum].
  > …They don't know how anyone can get anything done with it.
  > It doesn't even have x (Blub feature of your choice).
  >
  > …But when our hypothetical Blub programmer looks… up the power continuum… what they see are merely weird languages…
  >   with all this other hairy stuff thrown in as well.
  > They probably consider them about equivalent in power to Blub, but with all this other hairy stuff thrown in as well.
  > Blub is good enough for them.

Interestingly, Graham states something about the opinions of others.
I wonder why one's own opinion is exempt?

> You can't trust the opinions of the others, because of the Blub paradox:
> they're satisfied with whatever language they happen to use,
> because it dictates the way they think about programs.

## Types? Who Needs 'Em?

It seems that Lispers see types as "weird", "hairy", and "thrown-in".
Actually, Haskell's purity is even called a "hair shirt", even by noted Haskell-enjoyers.
Consider a selection of quotes from Lisp-enjoyers in a comment thread online:
  - I'm skeptical of your premise that types are a useful tool for programming.
  - types have turned into red tape and become more of a liability than an asset
  - when you back up enough to extract yourself from the typing tarpit, the definition of "type" starts to wobble.
  - I'd be more inclined to compare programming without types to flying without water.

On the other hand, type-enjoyers are, admittedly, can be pretty snide and derogatory about languages that lack static types.
Consider this quote, from the same thread:

> Programming without types? What next? Breathing without air?

People that use languages with a Hindley-Milner-based type system generally _do_ look down on Lisp.
How does anyone get anything done with Lisp? It doesn't even have types.

So you've got Lisp-enjoyers and Haskell-enjoyers both looking down at each other,
  but which language is the Blub?
Hmm, I wonder why I didn't select any quotes about Haskell not having macros?
It probably™ won't be important.

## Lisp Isn't a Blub!

Well, Lispers certainly don't think their Blub-ites.
After all, they look at something like Haskell and say "It doesn't even have macros, let alone homoiconicity."
When Lispers talk about how "The Parentheses are Good, Actually", this is what they mean.
As Graham says (still this same single section of one article):
  > those parentheses are there for a reason.
  > They are the outward evidence of a fundamental difference between Lisp and other languages.

Just to remind ourselves
  — because homoiconicity is a bit jargon-y for my taste —
  we're talking about when
  the code is made of data structures that you can traverse.

## Revenge of Chekov's TM™

I think sometimes Lispers can get a bit lost looking for the wrong thing, though.
They think they look at other languages to see if they have their favorite feature,
  but what the average Lisper is actually looking for is parenthesis.
Perhaps I'm wring about the cognitive process,
  but Lispers largely just don't admit anything else into the homoiconic club.

Haskell (GHC Haskell anyway, which is the biggest implementation by far, so it's what I'll mean in the following)
  has an extension `TemplateHaskell`.
Okay, so it has macros, but where's the homoiconicity? Shouldn't I see parentheses?
Well, the library `template-haskell` on Hackage has a module `Language.Haskell.TH`,
  which exports a mutually-recursive set of data types
  such as `Dec`, `Exp`, `Pat`, and `Type`, and so on.
If you guessed that these represent declarations, expressions, patterns, types (and so on) as code,
  you've just spotted Haskell's homoiconicity.
These data structures can be spliced in as code, and they are traversable and manipulable,
  just like other Haskell data types.

Let's review:
  - A Lisper looks at Haskell and doesn't see homoiconicity.
    They are factually incorrect.
  - A Lisper looks at Haskell at sees this weird, hairy feature called "types", and don't want it.
    Just like our hypothetical Blub programmer.
  - A Haskeller looks at Lisp, doesn't see static types, and wonders how anyone gets anything done with it.
    Just like they are looking at Blub.

From my perspective of enjoying Lisp first, and Haskell only later, Lisp is looking pretty Blubby.

## Ok, but…

Now, I will fully admit that awareness of Template Haskell is scant,
  documentation even scanter,
  that the error messages you get are pretty gross sometimes,
  that I haven't figured out how to elegantly use quasiquotation in Haskell yet, and
  that the syntax of Haskell is more intricate than the syntax of s-expressions
  (though the syntax of Lisp is also more intricate than just s-expressions).
At the same time, I know that —at time of writing— Template Haskell is getting some improvements.
One will make it possible simplify the implementation internally and keep Template Haskell up-to-date with language extensions.
Another will expose a homoiconic interface that will prevent ill-typed from being constructed in the first place,
  thus mitigating some error message pain.
A recent feature allows for documentation to be generated by macros,
  so now all our generated interfaces can be documented.
None if these issues are really the fault of Template Haskell's design;
  instead, they're caused by a lack of will to exploit these areas.
If only there were some group of people who are passionate about code generation;
  maybe they could get involved and bring their experience with them?

And sure, it's no fun to have one's favorite language called out for being not the best.
Well, if you want to use the best language in the world,
  you don't have time to take these things personally.
Instead, I would focus on grokking some new things:
  types (with inference),
  type classes,
  laziness,
  how to push through Template Haskell's lack of documentation,
  and so on.
Because I'll admit it, going from Lisp to Haskell is a bit of a difficult jump.
Just thank your past self that you don't have to jump all the way from JavaScript.
If you've ever portrayed yourself as smart online, Haskell won't be a problem.
