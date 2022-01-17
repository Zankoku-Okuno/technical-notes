# Can a Language be Described as "Complex"?

tags: lang-design, philosophy

There are a lot of words that get used commonly, have no universally-agreed-on definition, and are only ever given explanation about as often people are killed by meteors.
Let's quickly define them:

  * complex: braided (tugging one one thread causes others to move)
  * complicated: includes complexity which is not necessary to solve the problem
  * simple: _not_ braided
  * uncomplicated: _not_ complicated

Also, beware of these:

  * familiar: you've seen/done this before
  * intuitive: you've done this _many_ times before
  * unfamiliar/unintuitive: you haven't worked with this enough to know its advantages or disadvantages
  * easy: that particular speaker didn't have to put much work in to do it, probably because they were adequately prepared by their specific prior knowledge and experiences
  * difficult: not easy, probably because the speaker is missing some relevant background knowledge or experience

Speaking about "easy", I find the λ calculus very easy.
Then again, my first programming language is Scheme, and I learned it when I was ten.
That _maybe_, _might_, _just possibly_ has some _small_, _minor_, _insignificant_ relevance to why I find λ easy.

And finally, a warning about:

  * small: the smaller an idea is, the easier to memorize; sometimes described as "simple", which isn't always also the case
  * big: not small

Something that's bugged me about Haskell is that if I change a type somewhere, not only do I have to change the interior code, but I have to change all the code that uses that type as well.
This seems like complexity (one thing changes means another changes).
However, the type describes an interface. If the upstream interface changes, the downstream users of that interface must also adapt to the new version, obviously.
The nice thing about static typing is that it can automatically identify _all_ the downstream users of an interface in less than a second (up to library boundaries).
Therefore, I don't see Haskell as inherently complicated for requiring downstream to update their code in response to breaking changes; I simply see that it can be tedious to update, and so upstream changes should be avoided so as to not introduce complications (complicatedness).

Complexity is when the interface for a function specifies "calling foFunction before calling fooInit is an error" (looking at you, literally every C library).
If the user of such a library alters the evaluation order of their code, then suddenly an error occurs (or worse, data corruption).
But who controls the evaluation order? The language runtime, a third-party framework, or what?
Suddenly code that doesn't know about (say) OpenGL cannot be used with OpenGL unless it also exposes evaluation order in its interface.
If a language doesn't expose such concerns (e.g. it may optimize computations using lazy evaluation as in Haskell or dynamic linkers, or as part of culling algorithms), then it can't safely be used with OpenGL.
That is: an internal change in one piece (your framework) tugs on some unrelated (i.e. the authors of the pieces don't coordinate with each other) piece (fooInit), and the braid tears apart.

It's entirely possible to write complex Haskell code.
For example, using the `hOpen` and `hClose` actions, or more commonly notably when using the State monad (and its ilk) or unsafe functions.
The first of these can be avoided easily (use the `withFile` interface instead).
Haskell the language mildly steers you away from using `State`, though it's not too hard to use and use it right in a small, internal module.
As far as unsafe functions, they are all specifically named `unsafeFoo` or defined in a module name `Unsafe`: what better way to make sure you actually detect the code smell?, all I have to do is `grep -rF '[Uu]nsafe' src/`.
Haskell doesn't magically make code less complex; instead the ergonomics of the design steer you away from accidentally introducing complexity.
