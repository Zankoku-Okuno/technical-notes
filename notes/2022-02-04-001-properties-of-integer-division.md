# Properties of Integer Division
tags: integer-division, api-design, math

Let `a, b ∈ ℤ`.
We want to compute an integer division `q = a/b` with remainder `r = a%b`.
There are a number of properties we might want.
Obviously we must have:
  1. `q, r ∈ ℤ`
  2. `|r| < |b|`

and most programming languages also require:
  3. `a = b * q + r`

It is usual in modular arithmetic to take residues to be positive:
  4. `0 ≤ r < |b|`
  5. `-a % b ≡ a % -b ≡ -(a % b) (mod b)` for `b > 0`

It would also be intuitive to satisfy some familiar sign cancellation and distribution properties from algebra:
  6. `-a / -b = a / b`
  7. `-a % -b = a % b`
  8. `-a / b = -(a / b)`

Unfortunately, we cannot do all of these.
The problem is with `-a / b = -(a / b)`, and essentially boils down to the fact that
  we do not in general have`floor(-a) = -floor(a)`.
The fact that negation and floor do not commute is fairly obvious, so perhaps it is not so bad if we also drop that last requirement.

## An Algorithm

I propose we use the following algorithm:

```
let n, m ∈ ℕ, m ≠ 0
Then
  n / m = -n / -m = floor(n/m)
  -n / m = n / -m = -ceiling(n/m)
  ±n % ±m = n - m*floor(n/m)
  ±n % ∓m = n + m*ceiling(n/m)
```

and now it's time to prove it satisfies the properties 1–7.

It is trivial to see that `q, r ∈ ℤ`.
It is also easy to see that `±n % ±m ∈ ℕ`, because the rhs is an expression over ℕ,
  and `∓n % ±m ∈ ℕ` for the same reason.
Since `a % b ∈ ℕ`, we also get `0 ≤ a % b` for free.
Further, we get `-a / -b = a / b` and `-a % -b = a % b` by definition.

We how only have two properties left to show.
We will start with `a = b * q + r`.
For `a, b ≥ 0`, we substitute: `a = b * floor(a/b) + a - b*floor(a/b)`,
  then factor `a = a + (b - b)*floor(a/b)`
  and reduce `a = a + 0`.
For `a, b ≤ 0`, we use sign cancellation and reduce to the `a, b ≥ 0` case.
When `b < 0 ≤ a`, we follow a similar path:
  substitute to obtain `a = b * -ceiling(a/b) + a - b*ceiling(a/b)`,
  then factor `a = a + (-b + b)*ceiling(a/b)`
  and reduce `a = a + 0`.
For `a < 0 ≤ b`, we use sign cancellation to multiply `a, b` by `-1`, and reduce to the `b < 0 ≤ a` case.

For the final property, we will also use sign cancellation extensively,
  so it is sufficient to show that `-a % b ≡ -(a % b) (mod b)` for the case `a, b > 0`.
We substitute into the definition of modulus:
  `a + b*ceiling(a/b) ≡ -a + b*floor(a/b) (mod b)`
  and cancel multiple of `b` to obtain `a ≡ -a (mod b)`.
This completes the proof.

## Analysis

My algorithm is, I think, equivalent to Boute's Euclidean division (E-division).
I'm not sure how Boute came to his definition, but the considerations I brought up in the introduction were just a result of
  my experience with elementary algebra (to which I was introduced at a young age in public school) and
  modular arithmetic (to which I was properly introduced in an undergraduate number theory course, though I and everyone I know had already had some practice with it through everyday time arithmetic);
  they are thus readily familiar to programmers (making the intuitions easy to transfer), and readily obtainable (a likely thought process for any other programmer or mathematician, including Boute).
Boute develops his definition according to Euclid's Theorem (with which I was unfamiliar),
  though as for his thought process, I will not presume to have psychic powers.

Though I would not be surprised it Boute is a better mathematician than I, and just knew the theorem,
  or perhaps knew of the Euclidean ring axioms which he mentions.
In any case, the theorem and the ring axioms lend support to the suitability of E-division.
If indeed my proposal is equivalent, then perhaps I have simply contributed a more accessible justification: one which does not require formal geometry and abstract algebra.

Actually, checking the Boute's Fig 3, my definition is indeed equivalent.

## Links

  * [Wikipedia: Modulo operation](https://en.wikipedia.org/wiki/Modulo_operation)
  * ["The Euclidean definition of the functions div and mod", Raymond T. Boute](https://dl.acm.org/doi/pdf/10.1145/128861.128862)
    As far as noting the sorry state of the industry, I couldn't put it better than Boute.
