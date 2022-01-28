# The Stupidest Parser
tags: lang-impl, metaprogramming, parsers, haskell

Sometimes, you just need a throwaway language.
You'll use it in literally one situation, but a real human will have to read and modify it.

I ran into this at work, where we needed to configure a network performance tool with a simple domain-specific expression language.
At the time, I just did reverse polish notation, but over time the language started to grow.
You think arithmetic is a pain with RPN?, how about relational operators?
We also couldn't fit conditionals into the language itself, since that would requier the parser to find nesting, which we didn't build in at the start.
Instead, the path of least resistance was to implement conditionals at the Json level… yeugh.

I think I'm about to run into this more as I start to use Template Haskell more.
Sometimes, you just need to specify a small domain-specific language to select out or build up some Haskell expression,
  and the Haskell AST is not fun to work with.
In particular, I'd like to implement some of the ideas of the
  [NanoPass Compiler Framework](https://nanopass.org/documentation.html)
  using Template Haskell.
I'm sure I'll need a way to request modifications to mutually-recursive ADTs,
  and I think this stupid parser might actually do the job.


This file is valid Haskell if you only keep the code blocks.
That's why we start with this skip[able preamble garbage:

```
{-# LANGUAGE DeriveFunctor #-}
module Text.Parse.Stupid
  ( Sexpr(..)
  , parse
  , hydrateSpaces
  ) where
import Data.Bifunctor (first)
```

Anyway, what are we parsing into?
All I want is to break up tokens and find nesting structure.
This sounds like a job for sexprs, so we'll use them.

```
data Sexpr a = Atom a | Combo String [Sexpr a]
  deriving (Eq, Ord, Show, Read, Functor)
```

There's an extra string in `Combo`s; this set to the open bracket string that started the combinatino.
This way I later know what bracket pair was used to combine subexpressions.
Speaking of which, here are the bracket pairs I'll be using;
  the `$(` is standard for unquote in Template Haskell, so I stick to that convention.

```
brackPairs :: [(String, String)]
brackPairs =
  [ ( "("  , ")" )
  , ( "$(" , ")" )
  , ( "["  , "]" )
  , ( "{"  , "}" )
  ]
```

This is the bundled parser.
The entire hand-written recursive-decsent parser is just _nine_ lines.
The rest is just tokenizing the input and adapting the output.

```
parse :: String -> Maybe [Sexpr String]
parse = fmap fst . go . tokenize
  where
  go :: [String] -> Maybe ([Sexpr String], [String])
  go [] = Just ([], [])
  go (t:ts) = case t of
    close | close `elem` fmap snd brackPairs -> Just ([], t:ts)
    open | Just close <- lookup open brackPairs -> do
      (inner, rest) <- go ts
      case rest of
        t':rest' | t' == close -> (fmap . first) (Combo open inner :) (go rest')
        _ -> Nothing
    _ -> (fmap . first) (Atom t:) (go ts)
```

Okay, but how do we tokenize?
We want to be as lazy as possible: ideally I'd just use the `words` from the `Prelude`.
However, we do want to detect brackets as separate tokens:
  the tokens from `((a` should be same tokens from `( ( a`.
Also, it might be nice to allow for comments, and we can get line comments with `lines` and a `case`.

```
tokenize :: String -> [String]
tokenize input = do
  line <- lines input
  case line of
    '#':_ -> [] -- remove comment lines
    _ -> do
      word <- words line
      unbracket word
```

Most of the complexity here is just to use an accumulator.
Perhaps I should not use an accumulator, but it seemed easier than a `loop :: String -> ([String], String)`.

```
unbracket :: String -> [String]
unbracket = filter (not . null) . loop ""
  where
  loop acc "" = [reverse acc]
  loop acc ('$':'(':cs) = reverse acc : "$(" : loop "" cs
  loop acc (c:cs)
    | c `elem` "()[]{}" = reverse acc : [c] : loop "" cs
    | otherwise = loop (c:acc) cs
```

The only thing is, tokens aren't allowed to have spaces in them, nor any brackets.
This could a problem if we expect some tokens to be strings, since strings can contain spaces.
However, this can be worked around by using numerical escapes.
I'm okay with doing that for brackets (which might not appear anywhere in a string), but spaces are more common.
I'd prefer to use `\+` for space, if I'm going to use a space at all.
I've therefore included this handy un-escaping function that can be used before passing tokens on to string recognizers.
Of course, the same technique can be used for other string syntaxes,
  but here I'm expecting to use Haskell's `read` method because—again—I am lazy.

```
hydrateSpaces :: String -> String
hydrateSpaces ('\"':content) = go content
  where
  go [] = []
  go ('\\':'\\':rest) = '\\':'\\':go rest
  go ('\\':'+':rest) = ' ':go rest
  go (c:rest) = c:go rest
hydrateSpaces str = str
```
