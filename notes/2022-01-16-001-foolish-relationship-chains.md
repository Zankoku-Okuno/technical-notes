# A Foolish Solution for Chaining Relational Operators

tags: haskell, api-design, mixfixes

Fist, let's work not with `Bool` but `Booly` everywhere.
```
if :: Booly b -> b -> -> Lazy a -> Lazy a -> a
(&&) :: Booly b => b -> b -> b
-- and so on
```

Then, we have a chained relationship type, which is booly:
```
type RelationChain a = (a, b, Bool)
instance Booly (RelationChain a) where
  toBool = _.3
```

Then, we redefine relational operators to produce `RelationChain`s, either from others, or from a base data type:
```
class RelLt a where
  rawLt :: a -> a -> Bool

  let t = a | RelationChain a
  (<) :: t -> t -> RelationChain a
  (n|) < (m|) = (n, m, rawLt n m)
  (n|) < (|(m, u, b)) = b && (n, u, rawLt n m)
  (|(l, n, b)) < (m|) = b && (l, m, rawLt n m)
  (|(l, n, b)) < (|(m, u, b)) = b && (l, u, rawLt n m)
```
