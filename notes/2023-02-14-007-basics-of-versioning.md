# Basics of Versioning

tags: versioning

Okay, so interfaces...

Someone writes some code and gives it a name.
They later revise it, creating a very similar body of code, but they don't change the name.
This happens multiple times.
Each different-but-similar bit of code is called a "version".

Humans look at the versions, and think they are "the same" software.
Humans usually think in terms of "identity by historical continuity".
Only rarely do humans do humans remember that "you can't step in the same river twice".

Computers look at versions and think they are "not the same" software.
Computers operate in terms of "identity of indiscernibles".
Since there are changes between two versions, they are discernible, and therefore not the same.
Computers know they can't step in the same river twice (and not just because the first time would be lethal).


The same considerations apply for the artifacts and the build flags.


A stranger wants to link to that code from their own.
They download a single version and compile against it, and everything works.
They distribute their work to users.
A user tries to build the code, so they download the dependency, but perhaps a different version.
Will that user's compilation work?
