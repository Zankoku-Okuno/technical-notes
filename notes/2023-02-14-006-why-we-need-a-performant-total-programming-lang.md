# Why We Need a Performant, Total Programming Language

tags: lang-design

It's not hard to get programmers on-board with good performance if it means they have to do less work.
Nevertheless, I'll still say that we may be at the point now where hardware improvements will not be so forthcoming,
  and if we want to continue to increase the complexity of our software,
  we will once again need to consider the performance of that software.
Coming from a pure type theory position, this means extending the theory with unboxed and unlifted types.
Haskell has come a long way with this already, though the ecosystem of libraries and knowledge could use plenty of growth.


[The 2003 grid failure](https://www.youtube.com/watch?v=KciAzYfXNwU) was caused by three trees and a computer bug.
Specifically, the bug was an infinite loop.
An infinite loop would not have been possible in a total programming language; without the loop, grid operators would have received alerts and might have been able to minimize the damage of the failure.
This kind of error — like buffer overrun, null pointer dereference, and out of bounds indexing — should be considered unacceptable professionally, especially in such infrastructural systems.

A standard retort about the protection that total languages provide is that total languages still admit infeasibly large computations, which are practically indistinguishable from infinite loops.
However, I think this retort only matters from the viewpoint of total languages' protections against malicious actors.
In language design, we are more concerned with the languages ability to protect against the natural mistakes of trustworthy but flawed programmers.
Infinite loops is a natural mistake, accidentally computing busy-beaver or Ackermann are just not reported to my knowledge.
Basically what I'm saying is that programmers in their day-to-day efforts either write polynomial-time algorithms or infinite loops, but total programming languages would practically leave programmers with only polynomial algorithms with which to accidentally destroy real-time systems.
