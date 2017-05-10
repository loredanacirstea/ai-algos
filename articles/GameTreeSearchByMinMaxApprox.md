# Game Tree Searching by Min / Max Approximation
Ronald L. Rivest
Laboratory for Computer Science, MIT, Cambridge,
MA 02139, U.S.A.
https://people.csail.mit.edu/rivest/pubs/Riv87c.pdf

This is a brief summary of:
- the paper's goals or techniques introduced
- the paper's results


## Goals

This paper focuses on a technique for reliably choosing which tree nodes are worth expanding further in a penalty-based iterative search method.

The technique consists in calculating estimates of a node's evaluation score with the help of "min/max approximation", using generalized mean-valued functions.


## Techniques

The paper uses the Connect-Four game with 7 columns and 6 rows. 980 game are played between two players. One player uses the min/max approximation method with a single static evaluation function (MM). The other player uses the minimax algorithm with alpha-beta pruning, iterative deepening and node sorting after a static evaluation function (AB). The implementation was written in C on a DEC MicroVax workstation.

The use of generalized mean-valued functions in MM is meant to improve sensitivity analysis due to the continuity of the derivative, which ranges from 0 to n^{-1/p}. This allows moves that appear sub-optimal at a point in time to be taken into consideration in a later iteration if their penalty is low enough.

The MM technique is using edge and node weights as penalties for representing sub-optimal moves. The tree is expanded one node at a time, by choosing the most promising node (with the smallest penalty).

Each node keeps track of the node's accumulated penalty, memorizing the child node that acts as a root for the subtree with the most promising leaf node. The penalties are backtracked from leaf to root in such a way that the root penalty is a sum of all penalties from the root to the best leaf node.

Leaf node expansion stops when the new leaf nodes do not have enough influence on the penalty of the subtree root. At this point, another root child is explored in the same way.

Nodes that cannot be expanded are given a penalty of Infinity, while expandable nodes are initialized with penalty of 0. Every time a node is expanded, the penalty increases with a chosen value.

## Results

The implementation of the algorithm uses reverse approximation. This means that the value computed for a node is the actual backed-up min/max value from the leaf nodes instead of an approximation. The reason was the computational difficulty in calculating the generalized p-means. The benefit of the approximation method is, after all, the use of derivatives in order to increase sensitivity.

The penalty of an edge between a node and its successor was calculated by adding 0.05 to the absolute difference between the natural logarithms of the node value and its most promising child.

The static evaluation function returns a value in the (1,1023) range for each cell on the board depending on which player has to move and on the scores of the segments (sets of four cells) that contain the cell. A score of 1 means a win for the Min player. A score of 1023 means a win for the Max player.

The results show that the MM technique is superior at choosing a better play move when no time constraint is in place. When the time allocated for a move was a constraint, AB was superior.

Specifically, when the constraint was the number of moves that a player has to make, the MM technique won 50.81% of the 490 games played, with 10.4% of the games resulting in a tie. The 490 games were played in batches of 98 games with the following limits: 1000, 2000, 3000, 4000 and 5000 moves.

When the time resource served as a bound, the 490 games were played in batches of 98 games with the following limits: 1, 2, 3, 4 and 5 seconds per move. The MM technique won 37.96% of the games, with 13.26% of the games resulting in a tie.

Therefore, 980 games were played altogether. The authors observed that AB took into consideration three times more distinct positions than MM when a time bound was in effect. When using a move bound, the numbers were comparable. Noting that MM called the move operator 4.375 times less per second than AB, it is clear that MM is more computationally intensive.

# Conclusion

These initial results show the potential of the min/max approximation method. However, improvements can be done to lower the computational overhead, produced by:
- explicitly storing the game tree
- traversing the subtree up and down multiple times
- exploring options that do not affect the decision made at root of the subtree; penalty-based methods are oriented towards
improving the value of the estimate at the root, rather than towards
selecting the best move to make from the root
- exploring sub-optimal tree branches due to improper evaluation functions that do not increase weights fast enough.
