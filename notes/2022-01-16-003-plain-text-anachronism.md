# Plain Text Anachronism

tags: rant, text-encoding

Tab and CRLF are anachronisms from the age of typewriters and teletypes.

## Tab

The tab key is meant to advance the carriage up to the next tab stop.
Tabs stops are metal pieces that cause the typewriter carriage and body to interact.
They usually can be adjusted, but only in such a way as to stop the carriage at a place that is accessible by pressing other single-character keys.
What all this means is that tab stops _only_ exist for the original author, and
  once written into the document, are exactly equivalent to a _constant_ number of spaces.

Modern computer systems also allow the reader of a document to set tab stops.
What this means is that the author of a document containing tabs does not have a fixed semantics for typesetting, and
  the author of the document will face uncertainties about how their document will be received.
In practice, while separating presentation from content can be advantageous in certain circumstances,
  even where this is promoted (HTML/CSS), authors nevertheless exert firmer controls when it comes to the size of spacing.

The web has a mature system for being responsive to user presentation configuration (i.e. needs).
However, applications which manipulate "plain" text have immature capabilities at best, but more usually non-existent.
Such applications are not limited to text editors, but also include
  terminal emulators, and software which presents information to the user on a terminal:
  essentially every command-line application including compilers, interpreters, and system administration utilities.
No standard has coalesced around providing such support uniformly, and it does not seem likely to happen.

Essentially what I'm saying is: plain text is still the same kind of document that once was spat out of typewriters across the world, it's only the character set that has changed.
Therefore, I will not store tab characters in my plain text document, though I will use the tab key to insert multiple spaces.
This means that my use of the tab key is actually closer to the original purpose: insert an author-configured number of spaces.

It could certainly be (and has been) argued that the typesetting of the document is less important than the reader's ability to configure the document's presentation to fit their needs.
Indeed, I am amenable to the idea of richer formats for editing and displaying source code:
  I want to draw diagrams, flowcharts, link to other bits of code, or to StackOverflow answers, have headings, footnotes, cards of code that can be arranged on a surface, everything!
Unfortunately, _no_ agreement has been reached on supporting a uniform method of configuring _even so much as the size of a tab_.
There's a far better chance of Windows adopting the XDG or SemVer specifications, because at least they _even have a spec_.

Perhaps my rejection of tabs seems callous to those concerned with accessibility.
To that I say: there are _blind_ programmers. _Professional_ *blind* programmers.
It seems like there must already be accessibility solutions that can cope with the size of indentation.

## CRLF

Let me ask you a question: why not LFCR?
Historical accident you say?
Which accident, when, where?

It's teletype time again, and you are trying to command the teleprinter to move down a line, return to the first column, and print some more characters.
It moves down the line nice and quick, then begins moving backwards to the start of the line, but it takes a while to move that heavy carriage such a long distance, and already it's received a command to print a character even though it hasn't made it back!
Suddenly, that character has been smeared across the paper—assuming that the machine didn't jam or rattle out of alignment thanks to the accidental collision.
So, you emit the carriage return first to get it going, then the linefeed—which can safely be executed in parallel with the carriage return— and by the time the linefeed command is complete and the next command arrives, the carriage has successfully returned, allowing that character to be printed correctly.

Phew! Aren't you glad we don't live in the bad old days anymore?
Now computers are so fast that it doesn't matter which order you send the two control characters in.
If I wanted to I could send a LFCR, and that should send me to the same place as a CRLF while printing no content… right?
Nope, your computer chokes, because you computer _doesn't care_ what the old teletype semantics were.
What I'm saying is: I've seen the arguments that "LF is _meant_ to go to next line, wheras LF is _meant_ to go to start of line", but if our systems don't understand them like that, then that's _not_ what they mean.

Apart from the invalid semantic argument, I can see one other: that CRLF adds redundancy and therefore allows checking for corruption.
Then again, CRCs, checksums, and digital signatures all do a _much_ better job of checking for corruption.
Okay, perhaps the corruption was caused by a human: some software developer wrote some code that emits bad bytes.
Obviously a checksum won't pick up on that.
How many times have you run into a bug that would have been detected earlier if we used CRLF instead of plain LF?
On the other hand, how many times has incompatible line endings caused a system to fail?, 'cause I happen to know it regularly causes delays in billing and customer service for at least a certain telecom company.

I'd almost make the argument that CRLF is a waste of space and processing time, but I doubt the space savings are significant in all but the most niche fields—especially after compression—and the time complexity of two-byte lookahead makes no difference when you already have enough lookahead to process a whole unicode character at once.
Long story short: performance is a non-issue here.

We need a single standard for inserting newlines into plain text, and frankly it doesn't much matter which it is.
The only thing driving out selection is: how easy is it to switch the systems that need switching?
Well, LF is overwhelmingly more popular, both counting number of actively-maintained OSes and number of running OSes.
My sense is that by a count of standards for text formats will show plain LF to be more popular when only one of LF or CRLF is accepted.
The one notable exception is HTML, which we don't have to change: humans rarely use text editors to create or read HTML requests; they may as well be a binary format, and sometimes the request/response content is literally just binary.

So, LF it is.
It's better to be unified than right.
