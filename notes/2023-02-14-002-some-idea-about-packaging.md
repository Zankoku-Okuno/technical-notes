# Some Idea About Packaging

tags: packaging, versioning

```
configuration
╞ a list of repository links: local files, internet sources
├── repository
│   ├── package
│   │   ├── artifact
│   │   │   ╞ semantic version
│   │   │   ╞ artifact type (binary for a given target and flags, source, documentation, headers)
│   │   │   ├── dependency
│   │   │   │   ╞ name of package
│   │   │   │   ╞ name of artifact (or choose the package's default artifact)
│   │   │   │   ╘ semantic version constraint
│   │   │   ┊
│   │   │   └── modules (for artifacts that support them)
│   │   ┊
│   │   └── preferences
│   │       ╘ a list of repo+package names;
│   │         if there are two options when searching for a package, this list is checked to disambiguate
│   ┊
┊
```


What is _not_ exposed by an api can be just as important as what _is_ exposed.
For example, if APIv1.0 does not expose the name `foo`, then a client might define `foo` themself.
Later, when APIv1.1 is released, it _does_ export `foo`, and now the client fails to build (or link) because of a name collision.
It would have been better if APIv1.0 had _reserved_ the name `foo`.
Of course, the names that get reserved are usually ugly (unless there's some way to auto-prefix with the name of the interface, as in GHC package-qualified imports).
Therefore, you may wish to release two versions:
  * one which will not add any unreserved names, so new functions can be added backwards-compatibly
  * one which wraps the other, and just replaces the new interfaces with nicer names
Obviously, the second will climb major version numbers much more quickly.
Nevertheless, this is basically what the C does, by reserving `_*` names, then introducing `_bool`, but you can opt in to `bool = _bool` with `#include <stdbool.h>`.