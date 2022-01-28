# Should _I_ Use Containers?
tags: sysadmin, learning, philosophy

If I have to resort to using containers to get software on my server, it means I fundamentally don't understand the system I am administrating.

That's not the only reason to use Docker (sometimes two applications' dependencies on system libraries are just incompatible and you need some sort of isolation), and if you're administrating a dozen or more servers for someone else that just need to be running now and technical debt be damned… well that's a very different situation from the one I find myself in.

I am administrating a single server, that I own, so technical debt is paid by me, deploying new features is not profit-critical, _and_ I want to learn more about how servers and Unix work under the hood.
In addition, the requirements for services the server should provide are reasonably minimal:
  standard sysadmin stuff (sshd, maybe ntp), an http(s) server for static sites/files, and everything else is a standalone application (a statically-linked Haskell library depending only on gmp, or a Factorio/Minecraft server).
Finally, I prefer to install any utilities used to make administration a bit easier to a single user rather than system-wide.
