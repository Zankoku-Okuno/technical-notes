# A Specification for Token Streams

  * Version: 0.1.0-alpha
  * Status: experimental
  * Modification Date: 2022-01-15
  * Author: Eric Demko

Part of the Compiler Pipeline series of specifications.

## Frontmatter

### Purpose

The first step of using a formal language (such as a programming language, a configuration language, data storage format, …) is parsing.
In decoding representations of these formal languages, must first perform lexical analysis on the text stream (or sometimes byte stream).
Usually, there are many errors that can only be detected _after_ lexical analysis, but it is important to accurately report the source location of those errors.
This is made difficult because:
  * Fixing the error without precise location information is very difficult.
  * It is sometimes useful to be able to reconstruct a portion of the original source reasonably accurately when reporting such an error.
  * Some tools may wish to modify the original source (e.g. an automatic formatter).
    Without perfect location information, attempts to patch the original source will likely result in the corruption of that source.
  * Tools which alter the display of source (i.e. most text editors) will require data about the source.
    If this data has missing or inaccurate locations, the quality of editor features—such as syntax highlighting, error/warning reporting, go-to definition, and auto-completion suggestions, among others—may suffer, thereby misleading the user and possibly causing mistakes.

This specification provides a baseline for manipulating tokens without losing any data about the original text and the location of tokens within it.
Applications include:
  * interfacing separately-written compiler stages,
    gaining decoupling between compiler subsystems, and
    possibly code reuse if two compilers can make use of the same token streams
  * a standard input format for error reporting tools to prettify and annotate their display
  * interfacing text editors with language servers to provide syntax highlighting, error reporting, and other annotation
  * an interface for code formatting tools that automatically edit the source
  * a data storage format to cache the state of a compiler in-between stages

### Conventions

While this data format could be serialized in a number of different forms, ranging from ABI-dependent structs to data types of a programming language to rows in a relation database, we have chosen to present the format as a subset of JSON.
This has the obvious advantage that JSON is extremely portable between both computing systems and programming languages.
Further, any data type that could be serialized and deserialized to/from json can trivially take advantage of tools that operate on JSON-encoded token streams, at the cost of an additional encoding/decoding step.

The names of data types are written in `UpCamelCase`, except in headers where they are in Title Case.

We use the word "source" a lot.
This can be an input text file, but it could be a transitory stream of character data that is not necessarily stored anywhere (i.e. input from a terminal, or input streamed over a network).
Essentially, we make no assumptions on the origin and storage of the input data, even if it almost always comes from a file.

We abide by the conventions of RFC2119 regarding the use of keywords for requirement levels.

## The Specification

### The Overall Structure

#### Lexical Analysis Results

A `LexicalAnalysisResult` is an object which:
  * MAY contain a `meta` member which is an object that:
    * MAY have a `version` member containing a SemVer version string
      describing a lower bound on the version of this specification that the results object conforms to.
    * MAY have a `lang` member containing a string
      describing the formal language that these results describe.
    * MAY have a `lang-version` member containing a version string
      describing the version of the formal language that these results describe.
    * MAY have a `vendor` member containing a string
  * MAY contain a `files` member, which is an array of strings.
    These may be referenced by locations in the physical or logical streams, and can therefore serve to aid compression and pointer sharing.
  * MUST contain at least a `tokens` member or `err` member.
    It is RECOMMENDED that implementations include both members.
  * SHOULD contain a `tokens` member, which is an object that:
    * MUST contain a `physical` member containing a `PhysicalTokenStream`.
    * MAY contain a `logical` member containing a `LogicalTokenStream`.
  * MAY have an `err` member which contains a non-empty array of `LexingError`s.
    In the following, if we refer to "an error" without further explanation, it is drawn from this member's contents, assuming the object under discussion is a descendant of this `LexicalAnalysisResult` object.
  * MAY have an `warn` member which contains an array of `LexingError`s.
    The phrase "an error" never refers to the content's of this member's array.
    If this member does not appear, it MUST be treated equivalently to if the member contained an empty array.

#### Physical Token Stream

When encoding as standard JSON, a `PhysicalTokenStream` is a possibly mixed array of `PhysicalToken`s and `InvalidInput`s.
If the containing `LexicalAnalysisResult` does not have an `err` member, then the array MUST NOT include any `InvalidInput`s.

The requirements for `PhysicalToken`s already guarantee that `∀(t : PhysicalToken). t.offset[0] <= t.offset[1]`.
The locations of the tokens and invalidity MUST single-cover the source.
In detail, this requirement states that all of the following MUST hold:
  * Let `a`, `b` be adjacent elements in the stream.
    Then `a.offset[1] == b.offset[0]` MUST hold.
  * If `t` is the first element in the stream, then
    `t.offset[0] == 0` MUST hold
  * If `t` is the last element in the stream, and `n` is the length in bytes of the source, then
    `t.offset[1] == n` MUST hold.

#### Logical Token Stream

A `LogicalTokenStream` is an object containing the following members:
  * `physical`: a `PhysicalTokenStream`
  * `logical`: a `LogicalTokenStream`
  * there SHOULD be no other members

#### Logical Token Stream

A `LogicalTokenStream` is a possibly mixed array of `integer`s and `LogicalToken`s.

When an `integer` appears in a logical token stream, this is an index into the physical token stream.
An out-of-bounds index SHOULD indicate a corrupt token stream.
If such an element `n` indexes the physical token `t`, this is equivalent to the situation where the element had been the logical token consisting of the following members:
  * `type` containing `t.type`
  * `orig` containing `[n]`
  * `loc` containing `t.loc`
  * all (valid) additional members of `t`

### Locations

A `Location` is an object which:
  * MUST have a `offset` member, which MUST contain a two-tuple (array) of integers `[a, b]` such that `a <= b`.
  * MAY have a `file` member, which MUST contain either a string or an integer.

    If it contains an integer, then this is an index into the containing `LexicalAnalysisResult`'s `files` member.
    Such a member is equivalent to if the member contained that indexed string.
    An out-of-bounds index SHOULD indicate a corrupt token stream.

    This member is meant for human rather than machine use.
    Implementations MUST allow an option to set this member,
      which can be as simple as taking the name from a command-line argument (the file that will be tokenized).
    This way, if the implementation is used as a subcomponent of a larger compilation system, that system can automatically track the origin across multiple files if data derived from their tokens is mixed together (e.g. as happens in the C Preprocessor, or in most high-level languages, as they usually provide scope analysis/type checking/source maps using multiple files).
    However, if a token stream document is received separately from its originating context, the member MUST NOT be relied on to select a unique source.

  * MAY have a `line` member, which MUST be either:
    * a single integer, or
    * a two-tuple (array) of integers.

    The contents of this member are meant for human rather than machine usage, and so are NOT REQUIRED to unambiguously specify any portion of the source.
    Implementors SHOULD attempt to agree with the line numbering performed by popular text editors, or OPTIONALLY offer configuration to specify particular counting algorithms.
      In particular, the line number(s) SHOULD be one-indexed.

    Despite having no specific formal meaning,
      member is containing a single integer `n` MUST equivalent to containing the tuple `[n, n]`.
    That is: specifying a single one line number selects a full line (however lines are defined).

  * MAY have a `col` member, which MUST be either:
    * a single integer, or
    * a two-tuple (array) of integers.

    This member is like the `line` member.
    They are meant for human usage, and so ideally would count "characters".
    However, there is no notion of "character" in Unicode.
    Implementations MAY choose to use Unicode segmentation algorithms (such as counting grapheme clusters to determine a column),
      or they MAY simply count codepoints,
      or they MAY use some other counting algorithm not listed here.
    Implementors SHOULD attempt to agree with the line numbering performed by popular text editors, or OPTIONALLY offer configuration to specify particular counting algorithms.
      In particular, the the column number(s) SHOULD be one-indexed.

    Despite having no specific formal meaning,
      this member containing the single integer `n` MUST equivalent to containing `[n, n+1]`.
    That is: specifying a single column number selects a full character (however characters are defined).
    A zero-character slice of the source at offset `n` could be specified as `[n, n]`,
      but this is NOT RECOMMENDED except for an "end-of-file" or "start-of-file" token.

  * MAY contain additional members.
    Such additional members MUST NOT have the name `column`,
      and they also MUST NOT not have a name beginning with any of the prefixes `offset_`, `line_`, `col_`, or `column_`.

### The Structure of Tokens

A physical token represents a contiguous sequence of source characters.
The physical tokens in a stream cover the entire stream without overlapping.

A logical token combines zero or more physical tokens.
Logical tokens may overlap with each other, need not cover the source, and a single physical token may be associated with many logical tokens.
Nevertheless, parsers over logical token streams are generally much easier to specify and implement than if they needed to handle physical token streams.

#### Physical Tokens

A `PhysicalToken` is an object which:
  * MUST have a `type` member containing a `string`.

    Within a single token stream, the values of these members are likely to be drawn from a small set of keywords.
    Consumers will likely enjoy performance benefits if it ensures these values are "deduplicated" (arranged so that every appearance of identical such keywords is represented by the same fixed-sized data, usually a pointer to a canonical string).
    Such deduplication can be done on-the-fly, or if the consumer knows the set of `type`s that its producers will create, a symbol table can be pre-built.

  * MUST have a `loc` member containing a `Location`.

  * MUST have an `orig` member containing a `string`.
    This text must be identical (up to a difference of encoding) to the slice of the source between the byte offsets (starting from and including the lower bound, up to but not including the upper bound) specified in this object's `loc.offset` member.
  
  * MAY contain additional members, so long as their names both:
    * do not begin with `type_`, `loc_`, `location_`, `orig_`, or `original_`, and
    * are not one of `location`, `original`, `invalid`, `err`, or `error`.

    Such members may be used to hold the results of preliminary parsing that can be included "for free" by the producer.
    For example, if the lexer recognized the regex `([+-])?([0-9]+(_+[0-9]+))` as a decimal integer, it will likely already have information about the sign and magnitude from the capturing groups.

    Producers that include such additional members MUST ensure that consumers can (knowing the producer) unambiguously identify and process all relevant additional members based on the value of the `type` member.

#### Logical Tokens

A `LogicalToken` is an object which:
  * MUST have a `type` member containing a `string`.
    As with token `type`s, these strings are likely drawn from a small set of keywords.
  * MUST have a `orig` member containing an array (possibly empty) of integers.
    These integers are indexes into the containing `LexicalAnalysisResult`'s `tokens.physical` member.
    An out-of-bounds index SHOULD indicate a corrupt token stream.
  * MAY have a `loc` member containing a `Location`.
    
    The precise method by which this location is synthesized is not specified, but SHOULD conform to these guidelines:
      * If the `orig` tokens are contiguous and no other logical token would overlap, then
        the logical location should be the convex hull of the `orig` token locations.
      * If the `orig` tokens array is empty, then the location should be between the locations of the logical tokens to either side.
      * Otherwise, the logical location should be approximately equal to the convex hull of the `orig` token locations.

  * MAY contain additional members, so long as their names both:
    * do not begin with `type_`, `loc_`, `location_`, `orig_`, or `original_`, and
    * are not one of `location`, `original`, `invalid`, `err`, or `error`.

    These members are intended for the same purposes as additional members of physical tokens.
    Thus, producers that include such additional members MUST ensure that consumers can (knowing the producer) unambiguously identify and process all relevant additional members based on the value of the `type` member.


#### Lexing Errors

A `LexingError` is an object which:
  * MUST have an `err` member containing a string.
    As with token `type`s, these strings are likely drawn from a small set of keywords.
  * MUST have a `loc` member containing a `Location`.
  * MAY contain additional members, so long as their names both:
    * do not begin with `err_`, or `error_`, and
    * are not equal to `error`.

#### Invalid Inputs

An `InvalidInput` is an object which:
  * MUST have an `invalid` member containing an integer.
    This integer is an index into the containing `LexicalAnalysisResult`'s `error` member.
    The error so indexed SHOULD describe the reason for emitting an `InvalidInput` into the token stream.
    An out-of-bounds index SHOULD indicate a corrupt token stream.
  * MUST have a `loc` member containing a `Location`.
  * MUST have a `orig` member containing the non-empty string of bytes from the source that are invalid.
    In JSON, these SHOULD be represented by a string containing the base64 encoding of the binary data as described in RFC4648 section 4.
  * MUST NOT have a `type` member.
  * SHOULD NOT have any other members, as these may be confused for indicators of other types.
