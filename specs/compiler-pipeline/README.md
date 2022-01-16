# Compiler Pipeline

## Commit/Release Checklist

  - update modification date
  - bump version number
  - update changelog
  - generate pdf

## What is this?

I would like to build programming languages out of tiny parts.
Consider the (reasonably detailed) flow of control through a compiler:
```
parser: physical tokenization → logical tokenization ⮌→ grammatical analysis ⮌→
frontend: scope analysis → type checking →
optimizer ⮌→
backend: target-specific optimizer ⮌→ code generation
```
Of course, individual compilers may merge several steps together, or join two sub-compilers together (e.g. compile to C, then invoke a C compiler).
Even interpreted languages can fit into this framework; they might skip optimization steps, and "generate" code as a no-op by targeting same internal AST format as the parser, or they might actually generate bytecode for a virtual machine.

What is more, I have the idea in my mind that I can build many languages which can share parts of this pipeline.
In particular, I've already implemented eexprs, which takes care of almost the entire parser stage.
(I could split grammatical analysis into two steps: the first creates an general-purpose tree representation, and the second recognizes patterns in that tree to build a language-specific abstract syntax tree. Eexprs do not do that final step.)

If I can share stages of a compiler between different compilation systems, that's code-reuse.
The question is, how do I ensure maximum reusability?
I will have to specify an interface between these stages, which amounts to a data format for each arrow in the diagram above.
The base data format I choose is JSON, since essentially every language speaks it: it's a poor man's FFI.
I could also choose a data format based on the C ABI, which is similarly portable—and much more efficient if all languages involved can speak it—but that requires much more thought as to the specification of the interface and its correct implementation.
Such an in-memory binary format is an additional feature beyond the JSON interface, and of course the JSON interface specification is easily transportable into alternate formats (XML, s-expressions, &c), JSON-based binary formats (SMILE, BSON, &c), or more human-friendly formats (YAML, TOML, &c), depending on the needs of the situation.

Once these data formats are designed, one can also build generic tools that operate on these data formats.
These tools could implement the stages themselves (e.g. most physical tokenizers could be implemented with a few sets of regexes plus some simple state), generate patches for source code (i.e. source formatters), or display nice error messages (i.e. with exact position, colorized snippet of source, relevant definitions, &c).

I have separated each data format into a separate specification.
These specifications should be independent of each other; if they are not, then I have designed them incorrectly.

The roadmap for a minimum viable pipeline specification are:
  - [ ] token streams
    - [x] draft specification
    - [ ] reference implementation
  - [ ] abstract syntax trees
  - [ ] abstract binding trees

The final artifacts I want for each spec are:
  * a written specification (markdown)
  * a reference implementation in Haskell (or Idris, Agda, &co)
  * test cases (input and expected files, with a test script runner)
  * an implementation targeting the C ABI (C, Rust, Zig)

The general-purpose tools I have in mind are:
  - [ ] logical tokenizer: consume by regexes where state is the current regex set and a map(s) of strings
  - [ ] logical token rewrite system: keep a state, match simple linear patterns of tokens, alter the stream by updating/merging/deleting/inserting logical tokens
  - [ ] a syntax tree builder: operate on a token stream with a (mostly) context-free grammar based on extended regex with iterated capturing groups, possibly perform unification on tree attributes
  - [ ] a syntax tree rewriter: match patterns in a tree and re-write them
  - [ ] code formatting to normalize leading/trailing whitespace and line-endings, automatic table alignment, possibly (with the help of later stages) organize imports/pragmas, and so on

I will have to do some more thinking and experimentation before embarking on
  - generalized scope analysis
  - format for a generalized linker
