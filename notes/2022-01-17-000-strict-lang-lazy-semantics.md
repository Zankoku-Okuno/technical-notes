# Strict Language, Lazy Semantics

tags: lang-design, lang-impl, lazy-evaluation

There's a strict Haskell variant out there (called mu?) that has a compiler flag that
  allows let-bindings to float down even if they would have caused an exception.
It seems like people just turn this on and don't worry about it.
It breaks the semantics (a non-terminating function becomes terminating), but this is probably because the semantics are too narrowly-defined.
But, how would you formalize it?

I think you would define the semantics of the language to be "lazy".
You would have to be careful of the reduction of mutable cell allocation/control operators/message-passing a-la π-calculus, which are all the same thing anyway.
However, "lazy" semantics does _not_ guarantee a delay of evaluation:
  a compiler/interpreter is allowed evaluate expressions at any time,
  it does not have to _guarantee_ delay to the last possible moment.
So, a compiler for such a language would be allowed—but not required—to force all function arguments before evaluating the body of the invocation.

The reason I've put lazy in quotes above is that laziness seems to relate more to evaluation order than semantics.
At least in my mind, evaluation order is a separate layer from the semantics of functional equivalence.

For example, calling `f 1 (raise FooError)` could result in an error.
However, if `f x y = x`, the compiler could inline `f` and naïvely β-convert, which would result in normalizing to `1`.
Such a strategy would only result in stuck or non-terminating terms becoming terminating.

On the other hand, data constructors are (in a sense) primitives, and so cannot be inlined.
I think we can be sure that a function that returns a datum will evaluate all the arguments to the constructor, and no data type will be accidentally lazy.
Codata of course will have to be lazy (at least at some point), as it's just not feasible to implement codata with anything other than thunks.

Indeed, we can think of all non-termination (infinite loop, exception, deadlock) as the same thing, then an uncaught exception is just the same as the detection of a deadlock that STM can do, or when a "sufficiently smart" compiler detects and removes an infinite no-op loop, and so on.
Altering a non-terminating program to a terminating one is simply an optimization with infinite speedup—if we consider all non-termination equivalent to an infinite loop.

The question perhaps is how to do first-class control (and equivalently mutable state and concurrency) with such semantics.
I think the answer is: those are side-effects, perform them under a monad.
It's the same reasoning that pushed Haskell to do IO under a monad.

## A Sketch for Formalization and Implications

Simply formalize the reduction semantics as you would for a full λ-calculus, but
  be careful not to embed a notion of evaluation order in those semantics.
Evaluation is allowed at _any_ redex _anywhere_ in the program (fragment).
Importantly, exceptions (and the like) are _not_ pure, do not "bubble up" the continuation, and _cannot_ be caught: they are more like Haskell `undefined` or `error`.
An exception is just a specific stuck term.
We already have languages like Rust (and frankly, C) that don't have exception handling anyway, and they work just fine, and can even be speedy.
Rust works around this limitation with the `Result<e, a>` type, and Haskell can do this just as well with `Either`, or `Except`/`ExceptT`, and so on.

I guess this means that if a term has a normal form, not all evaluation strategies will find that normal form (i.e. no Standardization Theorem).
This is perhaps a theoretical downside for the point of view of giving compiler writers as many options as possible to alter expressions.
However, I'm not sure it's a practical downside.
In fact, languages based on λᵥ only have standardization because they have unnecessarily restricted the semantic's equivalence classes.
A normally call-by-value lambda calculus does not have standardization w.r.t. the semantics of full λ
  (which I guess just says that full λ normalizes more terms than λᵥ).
Users might of course expect a certain level of deferred evaluation out of their compilers, and compiler writers might worry if there is no standard for how much laziness they should try to insert.
Then again, compilers are also allowed to just not inline anything, thereby producing low-performance code not suitable for production.
The more terms a compiler can guarantee normalization for, the higher-quality the compiler,
  just like compiler quality is judged on the speedup from optimizations
  (but we don't actually want to treat infinite no-op loop as infinite speedup, b/c that breaks familiar notions of quantification).
This seems to be exactly the case for Mu, since everyone turns on the "higher-quality" version of the compiler.

Unknown function calls are almost certainly going to get a performance regression, though.
If a compiler decides that some of a function's args should be taken lazily, but the function is invoked as statically unknown, how will the unknown call know the laziness of the calling convention?
The only thing I can think is to have every function come along with not just the native number of arguments it takes, but also a bitmap of which args should be lazy.
This would create additional branches before an unknown function call relative to Haskell, degrading performance in those cases.
Frankly, unknown function calls are _already_ bad for performance, so it might not be worth worrying about such cases:
  if you're making an unknown call, you probably don't care to squeeze out that last bit of speed anyway.
It's not like I've given much thought to it, so there might be a solution I don't know about.
At the very least a magic keyword could ensure that a particular invocation (even an unknown one) is always given its arguments by value (which might require emitting an extra entrypoint like worker/wrapper already does).
Or, something like GRIN might be able to optimize these unknown calling-convention calls without much modification.
