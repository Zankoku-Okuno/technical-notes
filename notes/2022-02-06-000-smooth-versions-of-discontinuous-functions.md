# Smooth Versions of Discontinuous Functions
tags: math

I've occasionally come across useful but discontinuous functions.

## Sigmoid

Sometimes you just have to condition a term based on whether an input is negative.
This is the Heaviside step function, though there are several variants.
I think I've more often used this one in programming, though `H(-x)` is another contender:

```math
H(x) = \begin{cases}
  1 & \text{if }x > 0 \\
  0 & \text{otherwise}
\end{cases}
```

Fact-checking myself, I did spot notation "indicator function" notation.
This is a nifty little shorthand that lifts a boolean-valued function into a real-valued function:
Given a set `A`, we write:

```math
1_A = \begin{cases}
  1 & \text{if }x ∈ A \\
  0 & \text{if }x ∉ A \\
\end{cases}
```

Or, if `A` is a logical formula with one fresh variable `x`, we also write `1_A` to mean `1_{\{x \mid A\}}`.
This let's us write `H(x) = 1_{x > 0}`.
There's also the less subscript-heavy Iverson bracket notation `⧙x ∈ A⧘`.

Anyway, the smooth version is just the sigmoid function:

```math
S(x) = \frac{1}{1 + e^{-x}}
```

Though the similar `2S(x) - 1` has another natural correspondence in discontinuous functions, the sign function:

```math
sgn(x) = \begin{cases}
  1 & \text{if }x > 0 \\
  0 & \text{if }x = 0 \\
  -1 & \text{if }x < 0 \\
\end{cases}
```

which is related to the half-maximum convention version of the Heaviside step function `\frac{sgn(x) + 1}{2}`.

## Maximum

Another function that gets used a lot is `max`:

```math
max(a, b) = \begin{cases}
  a & \text{if }a > b \\
  b & \text{otherwise} \\
\end{cases}
```

I once came across Albert Bennet's sequence of hyperoperations, which begins from a "smooth maximum" function:

```math
F_0(a, b) = ln(e^a + e^b)
```

Of course, minimum can be defined in terms of maximum: `min(a, b) = -max(-a, -b)`,
and one can do the same for a smooth minimum.

In fact, smooth max is usually understood (if wiki'd focus of discussion is a reliable indicator) as a family of functions tunable by a parameter `α`.
One such family is LogSumExp: `LSE_\alpha(a, b) = \frac{1}{\alpha}ln(e^{\alpha a} + e^{\alpha b})`.
Setting `α = 1` gives the usual `max`, setting `α = -1` gives the usual `min`, and other values vary really only near `x = 0`.


## Ramp

Often, we clamp a value to be at-least or at-most a certain value.
The most common is perhaps `max(a, 0)`, which also happens to be the ramp function:

```
R(x) = \begin{cases}
  0 & \text{if }x < 0 \\
  x & \text{otherwise} \\
\end{cases}
```

There's a similar case, clamping up to zero, which is easy to derive: `min(0, x) = -R(-x)`.
Given `c` a fixed constant, we can also clamp above using `min(c, x) = c - R(c - x)`,
  and we can clamp below with `max(x, c) = R(x - c) + c`.
Swapping `R` out for `F_0(x, 0) `R`, we get smooth versions of these clamping functions.

However, while in the discontinuous version we have `0 ≤ min(max(x, 1), 0) ≤ 1`, this is not the case when we use smooth min/max, since a smooth `max(1, 0) > 1`.
For smooth clamping on both ends, the easiest solution is just to use the sigmoid function.


Regardless of the variation of Heaviside step function selected, we have `H(x) = \frac{d}{dx}R(x)` for `x ≠ 0`.

## Kronecker Delta

Something that comes in handy is the Kronecker delta.
This is especially useful in physics, where it can cut down on the number of functions defines with cases,
though in programming we usually just throw a branch in.

```math
δ_{ij} = \begin{cases}
  1 & \text{if }i = j \\
  0 & \text{otherwise} \\
\end{cases}
```

A particularly common case is `\delta_{i0}`, which just tests if the input is zero.
Iverson brackets were (it seems) developed as a generalization of Kronecker delta, so `\delta_{ij} = ⧙i = j⧘`.

This delta is not to be confused with the Dirac delta (actually a distribution, not a function), which is everywhere zero except at zero, where it is infinity in just the right way so that its integral over the continuum is one.

An obvious choice for a smooth version of `⧙i = j⧘` would be a Gaussian, but exactly which Gaussian could be up for debate.
Since `⧙i = j⧘ = ⧙(i - j) = 0⧘`, I'll center the distribution at zero.
The amplitude also must be 1 to agree with Kronecker δ, so that's another parameter down.
It would be nice if the resulting function were a probability distribution, and that would also nail down the last parameter.
Also, it means the integral of this function is a sigmoid (though I'm not sure if it's _the_ sigmoid above, as I haven't bothered to integrate)
So, I'm left with:

```math
g(x) = e^{-½τx^2}
```

Note that `τ = 2π`, if you haven't seen that already.

## Applications

Ok, so now that we have a bunch of stuff defined, it's time to ask "why?".
Well, consider the Euclidean division we looked at in a recent entry.
It's a very case-by-case definition I gave, which is painful, but there's a better way if we use these functions:

```math
\begin{align*}
  N \mathbin{div} d &= \left\lfloor \frac{N}{d} \right\rfloor + ⧙Nd < 0⧘ \\
  N \mathbin{mod} d &= N - d(N \mathbin{div} d) \\
\end{align*}
```

We can also re-write the properties of how negation interacts with integer division:

```math
\begin{align*}
  N \mathbin{div} (-d) &= -(N \mathbin{div} d) \\
  (-N) \mathbin{div} d &= -(N \mathbin{div} d) - ⧙N/d ∉ ℤ⧘sgn(d) \\
  N \mathbin{mod} (-d) &= N \mathbin{div} d \\
  (-N) \mathbin{mod} d &= N \mathbin{div} d + d⧙N/d ∉ ℤ⧘sgn(d) \\
\end{align*}
```
