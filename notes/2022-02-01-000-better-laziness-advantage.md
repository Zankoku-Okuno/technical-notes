# Better Laziness Advantage and Thoughts
tags: lazy-evaluation, lang-design

I do like that we can re-use lazy functions, as in
  `any = or . map p`.
And we can also do the naïve thing sometimes and let laziness save us:
  `smallest = safeHead . sort`.

I guess my big problem with laziness is that it makes it easy to define partial functions
  `largest = safeLast . sort`
which otherwise look exactly like total functions.

I think this issue might actually disappear once you move to a total language.
Note for example, that (functionally) `safeLast . sort ≡ safeHead . reverse . sort`,
  but attempting to define `reverse` on for a codata list will (I think) be rejected by the termination checker.


In any case, I think it's clear that a language should have the capability for _both_ strict and lazy function arguments.
In cases like `maybe`, it's reasonably easy: `maybe ~z f = \case { Just x -> f x ; Nothing -> z }`.
However, cases like `or . map p` require some more thought: the `or` would prefer its argument to be a stream type, and if this information is not propagated to the `map`, then `map` could generate the whole list anyway, and `or` would receive a pointless iterator.

Perhaps the quickest good solution is to define the common utility functions on streams where possible, but to not define utilities on streams which require the input to be finite.
Utilities that require finite data can be defined on their own, and shared utilities can either be re-implemented when speed can be gained, or the streaming functions can be re-used with appropriate adaptors.
There are two border cases: adapting finite data to infinite, and adapting (possibly) infinite to finite.
The former is trivial, but the latter is technically partial.

As it happens, it may be useful to distinguish FiniteStream from (possibly infinite) Stream.
Or perhaps I am rediscovering why Koka wants to let me write `deepseq :: Stream a -> Diverge (List a)`

Links:
  * http://augustss.blogspot.com/2011/05/more-points-for-lazy-evaluation-in.html
  * https://www.cs.kent.ac.uk/people/staff/dat/miranda/whyfp90.pdf


I had a thought as I was getting up:
> I'm tempted to go with a pure, strict language, and put laziness in a monad,
> but then I remember that laziness is not just about single values but entire data structures.

Here's a stupid idea:
```
type Lazy :: forall k. k -> k
type family Lazy

type instance Lazy (a :: Type) -> Thunk a
type instance Lazy List = Stream
type instance Lazy Tree = GameTree -- or whatever we want to call it


type ListLazy a = List (Lazy a) -- strict list spine with lazy elements
type LazyList a = (Lazy List) a -- lazy list with strict elements
type LazyListLazy a = (Lazy List) (Lazy a) -- lazy list of lazy elements (Haskell lists)
```
