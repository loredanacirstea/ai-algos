# AI Subject

(in work; this will become a hierarchy of AI subjects)

Constraint Propagation

Monty Hall Problem



Search Algorithm

Depth-First Search
Breath-First Search
A* Search | Best estimated total path cost first
Uniform Cost Search
Bidirectional Search
Greedy Search
Minimax Algorithm

Depth-Limited Search
Alpha-Beta Pruning
Probabilistic Alpha-Beta Pruning | eliminating tree branches based on a minimum and maximum limit for the state score estimation
Forward Pruning | some moves at a given node are pruned immediately without further consideration
Beam Search | forward pruning, remaining with the best moves according to an evaluation function

Breadth-First Search

Quiescent Search | until it gives similar results
Iterative Deepening

Game Play
Adversarial Search
Horizon Effect | algorithm does not see an outcome that is clear for a human player
Killer Move Heuristic | trying the best moves first
Transposition Table | hash table of previously seen positions
Heuristic Evaluation Function | function which returns an estimate of the expected utility of the game from a given position
Iterative Heuristics | static evaluation function results from the successors of a chosen node are used to provide the result for the node

Simulated Annealing
Random Restart
Local Beam Search
Genetic Algorithm
Genetic Algorithm Crossover
Genetic Algorithm Mutation

Constraint Satisfaction
Backtracking
Forward Checking
Minimum Remaining Values | choose the next node based on what node has less options from which we can choose
Least Constraining Value | choose the next node based on the fact that one of his options can be chosen so that you maximize the options for the other graphs
Constraint Hypergraph

Logic and reasoning
First Order Logic | Objects, relations, functions that can be true or false or unknown
Propositional Logic | Facts that can be true or false or unknown
Probability Theory | Facts that can be a real number in the range [0,1]
Resolution Algorithm
Graph Plan

Classical Planning
Progression Search
Regression Search
Plan Space Search
Planning Domain Definition Language

NP Hard Problem

State Space | the space where all the possible states of a problem reside
