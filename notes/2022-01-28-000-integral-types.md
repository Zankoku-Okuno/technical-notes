# Stream of Consciousness on Integral Types
tags: lang-design, arithmetic

Consider `((100 : U8) + 100 + 100 ) : U16`, should we understand `+` to mean addition as in elementary school arithmetic, or modulo 256, or modulo 65636, or some mix?

Globally, we can intuit that we want arithmetic to happen in U16 because we know that teh final result will fit there.
The problem is that the compiler doesn't know our intent: perhaps we want to do some ℕ₂₅₆ arithmetic in the middle?
And sometimes we _do_, for bit-manipulation hacks.

The way I see it, programmer mostly assume they are working in ℕ or ℤ, because that's what they want to work in, and are reasonably sure that their arithmetic won't overflow the machine registers.
Unfortunately, every language in the world essentially forces you to actually work in modular arithmetic.
That disconnect is the source of major bugs, right down to security vulnerabilities in memory allocators.
Even in languages that offer ergonomic big integer types, somewhere in the back of your mind is the idea that bigints are slow.

Honestly, I think Zig might be on the right track.
Their `+` operator causes undefined behavior on overflow, but they have `+%` for modular arithmetic and `+|` for saturating arithmetic. I dislike UB, but I can see why they chose it: trapping and revealing an error condition can be expensive, and Zig certainly isn't going to build in bigints (which would require a memory allocator argument to stay oriented to the reusability philosophy).

```
class FiniteNum a where
  -- useful for catching overflow errors that might lead to security vulnerabilities
  (+!) :: a -> a -> Maybe a
  -- useful in crypto and bit-manipulation
  (+%) :: a -> a -> a
  -- useful in graphics and control systems
  (+|) :: a -> a -> a

class Num a where
  toInteger :: a -> Integer
  fromInteger :: Integer -> Maybe a
  -- pay the cost of bigints to make sure _your_ arithmetic works the way _real_ arithmetic works
  (+) :: a -> a -> Integer
  (-) :: a -> a -> Integer

class UNum a where
  toNatural :: a -> Natural
  fromNatural Natural -> a
  (+) :: a -> a -> Natural
  (-) :: a -> a -> Maybe Natural
```

Now, we might wonder about what to do with array indices, since if an index is stored in a proper bigint, it will almost certainly overflow memory, not just the array.
I think we've been complacent in how we use integral types interchangeably for both numerical computations and indexing.
My philosophy is that `ArrayIndexOutOfBounds` (or worse, buffer overrun) should be impossible because the compiler has already checked the invariants at compile time.
What this means in practice is that `type Array :: (n : Natural) -> Type -> Type`, and `index :: Array n a -> Fin n -> a` is a total function, and being total means no runtime bounds checking is required.
`Fin` numbers will allow `FunuteNum` instances, but might also come with their own `(++) :: Fin n -> Fin m -> Fun (n + m)`.
