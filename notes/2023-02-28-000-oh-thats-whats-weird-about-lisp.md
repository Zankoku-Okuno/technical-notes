# Oh, THAT's what's weird about Lisp!

tags: lang-design, lisp, rant

In programming language theory (PLT), we generally work with formal calculi.
Here, we have a syntax, which is just defining a set of admissible terms (a.k.a. well-formed formulae, program fragments that pass the parser, yadda-yadda).
Then, there is a semantics, which is a relation taking elements of the syntax into elements of values
  (a.k.a. reduction relation, interpreter, and so on).
The set of values is often a subset of terms, but it isn't always.

Lisp is described as having s-expressions as its syntax (when it's not busy being described as having no syntax at all).
Instead of stating a whole reduction relation outright, it is often given piecemeal.
In particular, atoms are described as self-evaluating,
  a quote is described as evaluating to its single s-expression argument,
  and so on.
So far, no problem; Lisp can of course include a subset of expressions as values.
However, what does `(lambda (x) x)` evaluate to?

```
> (lambda (x) x)
#<procedure>
```

This presents a problem for Lisp textbooks.
Generally, they only bother to define s-expressions (the things that the programmer can see in the code),
  but don't define values.
The output `#<procedure>` does not reflect an s-expression, but it does (incompletely) reflect a value.
Instead of talking about values, Lisp texts sidestep the issue and instead talk about how function application evaluates to the body of the function with parameters replaced with evaluated arguments.
The student is meant to build their own mental model of whatever internal information the interpreter must keep to execute this replacement.
This is fine, as long as you are only implementing Lisp in Lisp,
  which — to be fair — is unique and fun an awesome.
It's only once you wish to implement Lisp in some other language that there is an issue.

```
eval :: Sexpr -> Value
eval ["lambda", paramlist, body] = Closure ???

data Value
  = Literal Sexpr
  | Closure ???
  | ???
```

The situation is worse when you wish to do macro expansion ahead-of-time
  (perhaps so you can compile Lisp to machine code, or simply look at the result of an expansion to help debug a macro).

```
expand :: Env -> Sexpr -> Sexpr
expand env (macroname : args)
  | Just macro <- env `lookup` macroname =
    let v = macroapply env macro args
     in toSyntax v

toSyntax :: Value -> Sexpr
toSyntax = ???
```

There are a few things I want to see from a formal theory of Lisp:
  1. A notion of concrete syntax (optional, kinda obvious)
  2. A notion of abstract syntax that differentiates special forms from applications
  3. A relation mapping s-expressions into abstract syntax
  4. A notion of value
  5. A reduction relation relating abstract syntax to values
  6. A isolatable subset of reduction relation rules that implement macro expansion

So far, items 2, 3, 4, and 6 are totally absent from my knowledge,
  and 5 is not as well-collected than a usual Plotkin-style calculus.
