I tested several heuristic functions based on `w1 * own_moves - w2 * opponent_moves` and `(0.1 + own_moves * w1) / (0.1 + opponent_moves * w2)`, by changing the w1 and w2 parameters.

With board partitioning in mind, I also wanted to see what happens if a player is encouraged to choose moves close to the center of the board. Therefore, I used a simple evaluation function of the square of the distance between the center of the board and the player's location, with a `-` sign in front. I also combined this distance to center function with previous concepts: using the distance computation as an evaluation function when the board was more than half empty and the other function, based on legal moves, when the board was <= half empty. The reasoning behind this approach was: create a partition first, then find moves that choose the best partition to be in.

Based on the results, I chose three heuristics that proved to have potential and ran `tournament.py` on 200 games. The results are:

Match #   Opponent    AB_Improved   AB_Custom   AB_Custom_2  AB_Custom_3
                       Won | Lost   Won | Lost   Won | Lost   Won | Lost
   1       Random      187 |  13    182 |  18    189 |  11    189 |  11
   2       MM_Open     152 |  48    151 |  49    153 |  47    154 |  46
   3      MM_Center    165 |  35    180 |  20    175 |  25    176 |  24
   4     MM_Improved   139 |  61    150 |  50    149 |  51    152 |  48
   5       AB_Open     107 |  93    101 |  99    99  |  101   92  |  108
   6      AB_Center    113 |  87    110 |  90    119 |  81    101 |  99
   7     AB_Improved   92  |  108   100 |  100   96  |  104   89  |  111
-------------------------------------------------------------------------
          Win Rate:      68.2%        69.6%        70.0%        68.1%


AB_Custom: (0.1 + own_moves) / (0.1 + opp_moves * 1.2)
AB_Custom_2: (0.1 + own_moves) / (0.1 + opp_moves)
AB_Custom_3: if > board/2 empty: (- square distance to center) else: own_moves - opp_moves

The algorithm that had the most wins was AB_Custom_2 with 70%. It surpassed AB_Improved with 1.8% more wins. However, when playing with AB_Improved directly, it only won 48% of the matches.
AB_Custom_2 is also the easiest to implement from the three and has the smallest number of calculations to be performed. Due to these reasons,  AB_Custom_2 was the heuristic ultimately chosen as primary.


Observations:

When I initially tested the different evaluation functions I used only one CPU agent: AB_Improved and only one test agent: the custom evaluation function, with number of games ranging from 10 to 100. This was done to speed up testing different avenues. The scope was to choose a heuristic that managed to beat AB_Improved. The percentage of wins against this agent ranged between 43% and 60%.

I know that this method excludes heuristics that might do much better when confronted with the other CPU agents, therefore having a greater overall percentage of wins.
