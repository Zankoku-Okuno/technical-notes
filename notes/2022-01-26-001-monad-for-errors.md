# Monad for Errors: general-purpose, contextualized, fatal/nonfatal/warning

tags: haskell, api-design

## Gather

Step one in reporting errors and warnings is gathering them, along with all information that might be relevant for formatting.

I initially was inspired to add notes to errors as a primitive, but
  honestly the notes should be part of the `err` type, since
  what notes are relevant depend on what kind of error is thrown.

```
data Report ctx err a
  = Ok { warnings :: (RList Err) ; nonfatal :: (RList Err) ; value :: a }
  | Bad { warnings :: (RList Err) ; nonfatal :: (RList Err) ; fatal :: Err }
  where
  Err = Error (RList ctx) err

instance Functor (Report ctx err) where
  fmap f x@Ok{value} = x{value = f value}
  fmap _ x@Bad{} = x

instance Applicative (Report ctx err) where
  pure x = Ok [] x
  f@Ok{} <*> x@Ok{} = Ok
    { warnings = f.warnings <> x.warnings
    , nonfatal = f.nonfatal <> x.nonfatal
    , value = f.value x.value
    }
  f@Ok{} <*> x@Bad{} = x
    { warnings = f.warnings <> x.warnings
    , nonfatal = f.nonfatal <> x.nonfatal
    }
  f@Bad{} <*> x = f
    { warnings = f.warnings <> x.warnings
    , nonfatal = f.nonfatal <> x.nonfatal
    }

instance Monad (Report ctx err) where
  x@Ok{} >>= k = case k x.value of
    y -> y
      { warnings = f.warnings <> x.warnings
      , nonfatal = f.nonfatal <> x.nonfatal
      }
  x@Bad{} >>= _ = x
```

This alternative instance is definitely not what I'd call uncontroversial.
In general, I think when I branch I need to decide:
  * were there any warnings in the first branch that should stick around even if the second succeeds?
  * if neither branch succeeds, which warnings and nonfatals are relevant?

```
instance (Monoid (Error ctx err)) => Alternative (Report ctx err) where
  x@Ok{} <|> _ = x
  x@Bad{} <|> y@Ok{} = y
  x@Bad{} <|> y@Bad{} = Bad
    { warnings = f.warnings <> x.warnings
    , nonfatal = f.nonfatal <> x.nonfatal
    , fatal = x.fatal <> y.fatal
    }
```

It may be better to make you own, custom `Alternative` instance for your `Report`-based `Monad`.
Then, you can do try/catch style alternation, with reporting carried through as you personally see fit/

```
fail :: err -> Report ctx err a
recover :: Report ctx err a -> Report ctx err a -> Report ctx err a
-- ^ if the first fails, it becomes a nonfatal before entering the second
catch :: Report ctx err a -> (Error ctx err -> Report ctx err a) -> Report ctx err a
-- ^ if the first fails, pass the fatal error run the second with the fatal error
withContext :: ctx -> Report ctx err a -> Report ctx err a
-- ^ adds context to all warnings/errors
```

## Present

Once the last section's `Report` has been made, the the warnings and non-fatal errors can be examined.
  * Non-fatal errors may be demoted to warnings.
  * Warnings may be promoted to errors.
  * The distinction beteen fatal and non-fatal is erased:
      all non-fatal errors should now be treated as fatal so that further stages do not generate errors based on possibly-garbage data introduced during recovery.

```
data Report ctx err a
  = Ok { warnings :: [Err] ; value :: a }
  | Bad { warnings :: [Err] ; errors :: NonEmpty Err }
  where
  Err = ([ctx], err)
```

Contexts, by the way, are ordered from smallest-to-largest.
This way, we can traverse the context list only up to the point where the context has gotten "too large".
I've definitely had some GHC error messages go off the screen simply because they report too much context.
