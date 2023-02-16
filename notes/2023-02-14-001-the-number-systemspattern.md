# The Number Systems Pattern

tags: math

In school, I learned about the progression ℕ → ℤ → ℚ → ℝ → ℂ.
In time, I have come to dislike this particular pattern: I don't think it is a real pattern.
It tells a story, but a more historical one than a mathematical one, and I'm not even sure the historical one is entirely accurate.

## Discrete Mathematics

Let's take it from the top and start with ℕ.
This seems to be the root of all number systems, (or is at least embedded into all of them), and is necessary to formalize quite a bit of basic mathematics.
This system is characterized by the successor function, which will be the seed for our story today.

The successor function is an interesting one however, because it has no inverse: you can't always "go back".
This is really due to only one thing: zero is not the successor of any ℕ.
One could extend the number system, adding an extra pre-zero element: we might call this 𝟙 + ℕ.
This is a little bit fruitless though, not only is there an isomorphism ℕ ≃ 𝟙 + ℕ, but this isomorphism preserves the structure of successor/predecessor.
That is, we could have defined successor on 𝟙 + ℕ to begin with, and successor on ℕ would just be a restriction of its domain.
Additionally, predecessor on 𝟙 + ℕ would have the same properties as predecessor on ℕ, so should we actually use 𝟚 + ℕ?, but that has the same problems _again_.

Instead, let's think about another interesting function: repeated successor.
This is just addition plain and simple.
Addition also has an inverse, subtraction, which like successor is partial in ℕ.
But the fact that it is repeated brings us a solution to the infinite regress we faced with successor.
If a and b ∈ ℕ, we'll write a - b to stand for an integer in ℤ; importantly, we won't actually subtract b from a, we're just using the subtraction sign as notation.
Now, we'll say that two integers a - b and c - d are equal exactly when a + d = c + b.
Both a + d and c + b can be reduced to natural numbers, and equality is defined on ℕ, so now we have an equivalence class between these numbers.
We now have a number system closed under addition and its inverse, subtraction.

If you haven't seen this construction before, it might seem a bit strange, but trust me it's more elegant than what you're used to.
If you think of ℤ as ±ℕ, then here's a question: is +0 the same as -0?
There's a weird special equivalence rule when you write integers as naturals with a sign, whereas in the equivalence-based definition puts the equivalence classes up-front and center.
And actually, you've seen the same construction before…

Now we consider multiplication, which is repeated addition.
Unfortunately, multiplication in ℤ has no inverse: you sometimes get a remainder after division (and the same problem would happen in ℕ as well).
What if we use that same equivalence class trick as before?
Let's take two numbers a, b ∈ ℤ and write a ÷ b to stand for a number in ℚ; again, we don't actually divide a by b, we're just using the division sign as notation.
Now, we'll say that two rationals a ÷ b and c ÷ d are equal exactly when a × d = b × c.
Notice the similarity with the definition of ℤ?
At least you should be familiar with this definition of ℚ from school, and it turns out that the definition of ℤ has exactly the same structure: just swap addition and subtraction for multiplication and division!

One might think the next step in the pattern is repeated exponentiation, and in one sense it is, but exponentiation brings some new problems.
For one, it is not commutative like addition and multiplication before it.
But that just means it has left- and right-inverses rather than a single inverse; maybe that's not a problem?
Unfortunately, exponentiation doesn't have unique inverses, which makes them not really inverses at all!
The obvious example is solving x² = a, where square root (the right "inverse" of 2) leads to two solutions x = ±√a.
There is of course the construction of ℂ which uses ordered pairs of ℝ, but then it has the same ugly special equivalence at zero that the 𝔹×ℕ-based representation of ℤ has, and also we face a choice of rectangular or polar coordinates, not to mention that we haven't even defined ℝ yet!

I guess the story stops here then: ℕ → ℤ → ℚ.
It does seem strange that we couldn't even continue on to ℝ, since they're so relevant to geometry.
However, there's an important property that all of these systems hold that ℝ doesn't: countability.
Essentially, this is the story of number theory, and ℝ doesn't belong here.

## Finite Extensions

Let's tell another story, again starting with ℕ, but also starting with certain operations: addition, multiplication and exponentiation.
These operations all have very geometrical roots.
We have ℕ to be able to count the number of units, addition to understand placing units next to each other, and multiplication to understand filling out an area with square units (or a volume with cube units, and into higher dimensions with more factors).
The odd one out is exponent, but we can see it sneak in through diagonals: if we form a square (using multiplication), we can ask about the length of its diagonal; this gets us the square root, which is one of the inverses of exponentiation.

It turns out that a lot of physical problems can be solved by solving equations, where each side of the equation models geometrical entity.
We'd like to have the smallest number system capable of solving all these equations, and thus of all these physical problems.
We're already familiar with ℕ from prehistoric times, but is it enough so solve all our equations?
No, we can't solve x + 1 = 0, which we need to understand shifting our origin, so we need to add negative numbers and thus reach ℤ.
Still this isn't enough, because we can't solve x * 2 = 1, which we need to be able to half any distance, so we need to add rational numbers and thus reach ℚ.
And _still_ this isn't enough because we can't solve x² = 2, which we need to quantify diagonals, so we need to add the irrationals.
And finally, it's not quite enough because we can't solve x² = -1, which we need to... do something-something-electrical-engineering?, anyway we add imaginary numbers and arrive at ℂ.

This story is probably the "historical" perspective on our pattern.
The problem is that the Greeks accepted the system with positive ℚ long before anyone in Europe accepted ℤ.
I'm not sure off the top of my head whether negative numbers or positive irrationals or zero were accepted first.

It's true that the number systems in question are ordered by embedding, but the question now is: why these landmarks and not others?
There's a whole lattice (TODO: what's the difference between that and a DAG?) of number systems we could go through.
Sure, ℕ→ℤ→ℚ→ℝ→ℂ is one path, but why not ℕ⁺→ℚ⁺→ℝ→ℂ?
Why did we leave out the Euclidean numbers (numbers that can be created with a compass and unit straightedge)?
Or the origami-constructible numbers (like Euclidean, but your toolset is a sheet of paper with two marked points one unit apart)?
Why did we leave out algebraic numbers (roots of non-zero ℤ-coefficient polynomials)?, or the infinite sub-systems formed by restricting the order of the polynomial?
There are so many interesting paths from ℕ to ℂ that the selection of any particular path does the others a disservice; we may as well drop directly into ℂ.

The choice of "important" operations we choose affects the outcome as well.
If we ignore exponentiation, we can stop at ℚ.
If we didn't think the infinitesimal part of the length of an arc could be tossed aside, we might find ourselves in the hyperreals (I think, though am not sure, that such numbers may be useful in characterizing fractals for example).
If we think functions are useful objects, then we might be able to solve f(x) = x² + 2f(x) for _f_ (btw, f = λx. -x²), but this would require us to include all the terms of the lambda calculus in our system.
Perhaps you think that is getting far away from numbers, but recall that setting 0 = λf,x. x and succ = λn,f,x. n(f(x)), we immediately recover the natural numbers.
All of these choices have real applications, so can we consider any of them primary?

Which naturally brings us to everyone' favorite objection: imaginary numbers aren't real.
That's trite, but there is something to it.
Most humans consider only human-scale pointable-to things to be important.
If you consider orientation as a physical thing, it's easy to see negative numbers: in a building, floors above ground are positive and basement floors are negative.
If you want to find a rational number, cut m pizzas each into n equal slices.
If you want to find an irrational number, you look at the diagonal of a unit square, or the circumference of a circle.
Point at an imaginary number.
The closest thing I can do with everyday human-scale objects is point at a 90° rotation… but 90 ∈ ℕ?

Everyone's favorite counter-objection is modeling electrical circuits.
It's important in the sense that a few people can use complex numbers, and those few can go on to make things the rest of us find useful, but there are _lots_ of special number systems that 
An obvious one is quaternions, ℍ. Why aren't they part of the story?, they would certainly be an interesting addition!
The number systems I've used most often as a physics student are vectors and tensors.
As a computer scientist, I'm much more aware of modular arithmetic: ℤ/nℤ.
Why stop in one particular place and not another?
My point is, importance is contextual, not universal, but it's the only thing this story has going for it.
