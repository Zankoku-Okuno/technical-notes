# Core Laziness "Advantage"
tags: lang-design

From What I Wish I Knew When Learning Haskell:
  > The primary advantage of lazy evaluation in the large is that algorithms that operate over both unbounded and bounded data structures can inhabit the same type signatures

Unfortunately, it also means that functions which operate on _only_ bounded data inhabit the same type signatures as those that operate on both bounded and unbounded.
Or more practically: `fmap f . reverse` has the same type as `fmap f`, but the former will enter an unproductive infinite loop given infinite data.

Dependently-typed languages have a distinction between data and codata.
This is theoretically sound (by design), and I think I'd prefer to see this distinction made in any functional programming language.
In particular, `seq` and `deepseq` have extremely unusual semantics for their types (you would normally expect these both to just be `const`).
It seems like data/codata would be able to mostly automatically normalize what the user needs without requiring these oddball functions.