# Use-case for Higher Inductive Types
tags: dependent-types, higher-inductive-types

I've been skeptical of higher inductive types (HITs) since I couldn't find a practical use for them.
Sure, you could represent integers and rationals with them, but the equivalence classes are so simple I don't mind not having HITs.

However, I just stumbled across a practical use-case for HITs (while, of all things, programming in Bash):
  syntactic normalization of filepaths.
This type leverages plain text and regex replacements.
I've written all the higher-order constructors (in this case, all ctors for identity types)
  so that the rhs is simpler than the lhs.

data FilePath where
  FilePath :: { unPath :: Text } -> FilePath
  -- the dot crumb is a no-op
  Dot :: { ∀p :: FilePath } -> p = overFilePath (Text.replace r'./' "" p)
  - the dot-dot crumb erases any previous crumb
  DotDot :: { ∀p :: FilePath } -> p = overFilePath (RE.replace r'[^/]+/\.\./' "" "" p)
  -- empty crumbs are ignored
  SlashSlash :: { ∀p :: FilePath } -> p = overFilePath (Text.replace r'//' "/" "" p)
  -- trailing slashes are ignored
  TrailSlash :: { ∀p :: FilePath } -> p = overFilePath (RE.replace r'/$' "" "" p)

overFilePath :: (Text -> Text) -> (FilePath -> FilePath)
overFilePath f = FilePath . f . unPath
```

Of course, the representation of such a type is still unknown to me.
  * Should it be normalized on construction?, on deconstruction?, whenever the runtime system finds it convenient?, never unless specifically instructed?
  * Where do I specify a normalization procedure (and prove it sound)?

Depending on the problem, the choice of representation could have meaningful performance impacts.
