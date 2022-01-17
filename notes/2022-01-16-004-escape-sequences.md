# Collecting Escape Sequences

tags: parsers, todo

I'll be adding to this list as I find new escape sequences.
Perhaps if they are _too_ obscure I won't bother, but I've at least mentioned some weird ones already
I'm also adding my own proposals anyway, and those are _certainly_ obscure.

## Single-Character Escapes

The necessary C escapes are
  `"`,
  `'`,
  `` ` `` (some languages), and
  `\`.

Beyond that, the most commonly-used C escapes are
  `n`,
  `0`, and
  `t`.
I'll leave my rant about tab elsewhere, but I will note that if tab is not commonly used in text strings, then the use of tab-separated values can become more efficient. Comma is so often used in text that CSVs often have to escape their contents.

Also of note are
  `r` (mostly extra work that Windows imposes, but sometimes used in web formats), and
  `e` (which is actually not C, but very useful for terminal interfaces).

Some escapes in the C standard which I've never used or seen in the wild (outside of escape sequence parsers/printers) are
  `a` (alert),
  `b` (backspace),
  `f` (form feed… now that's a teletype command if ever I saw one), and
  `v` (vertical? tab… does anything still recognize this?).
It may seem like `\a` would be just as useful for terminal interfaces, but most terminal emulators today often just ignore it, so you can't rely on it.
I mean, I'd like to see every computer come with a beeper on the motherboard that the OS can send such alerts to, but it's not going to happen, so this control might fade into obscurity as well.
Backspace I've not seen in the wild, but I wouldn't be surprised if it gets used in terminal interfaces as well (e.g. to display a progress bar); then again, I've seen only `\r` used for such designs.
I could be convinced to move all of `\a`, `\b`, `\r`, and `\e` into a set of escapes for terminal programming.

C also has `?`, but that's very language-specific (and even then is only useful for advanced preprocessor uses, which should be a warning to back away very quickly).

Since spaces are so often invisible, it might be preferable under certain circumstances to _make_ them visible with an escape.
I suggest following url encoding and use `+` as a single-character escape for an Ascii space.
A big one is when a string literal begins or ends in a space: `"[ERROR]:\+" + msg`.

## Byte Escapes

Inputting character codes (bytes) from `0-255` is supported in C as well, going all the way back.
The only form worth keeping is I think the hexadecimal form matched by `\\[xX]\h{2}`.

As far as the octal escape `\\[0-7]+` is concerned, I think it leads to more mistakes than convenience nowadays, and it also fails to conform to the usual syntax for hexadecimal and binary bases.
Look, 36-bit programming is charming, but outside of nice hobbies and systems that brass is too lazy/scared to touch, it's not important anymore.
If it's _really_ needed, I'd suggest `\\[oO][0-7]{3}`; note the _fixed_ number of octal digits.
I recently learned that the `\0` null escape is actually a specific octal escape, but
  I think we can get by with only having the single-character escape.

## Control Characters

Terminal syntax for control codes is stuff like `^C`, `^H`, `^Z`, and so on.
These are already familiar to programmers and could be matched with `\\^[@-_?]`.

## Unicode

From HTML: `&#\d+;`, which could be adapted to backslash-escapes as `\\#\d+;`.

My own from zexprs: `[uU]+\h{1,6};`.

I think I've seen this before: `\\(u\h{4}|U\h{6})`.
It's unambiguous, but I also don't want to have to choose between `u`/`U` based on a character code that I probably haven't looked up yet (or alter the choice later when I'm maintaining the code).

Haskell uses `[uU]\h+`, which has the disadvantage of being ambiguous in front of hexdigits.
Therefore, Haskell also includes a `&` escape meaning "no character", but it just feels like a hack to me.
