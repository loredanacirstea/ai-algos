import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    return custom_devide_best(game, player)

def custom_score_2(game, player):
    return custom_divide_opp(game, player)

def custom_score_3(game, player):
    return custom_center_improved(game, player)


# 52  |  48
def custom_devide(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return (0.1 + own_moves) / (0.1 + opp_moves)

def custom_devide_best(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return (0.1 + 0.8 * own_moves) / (0.1 + 0.4 * opp_moves)

# 50  |  50 ; 102 |  98 ;  70.8%
def custom_divide_opp(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return (0.1 + own_moves) / (0.1 + opp_moves * 1.2)

def custom_center_improved(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    blanks = len(game.get_blank_spaces())

    if blanks > (game.width * game.height) / 2:
        # Minimize distance to center square
        w, h = game.width / 2., game.height / 2.
        y, x = game.get_player_location(player)
        return - float((h - y)**2 + (w - x)**2)

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return own_moves - opp_moves

# 46  |  54 ; 56  |  44; 100 |  100 ;  70.8%
def custom_score_1(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return ((0.1 + (own_moves) * 1.5) /
            ((0.1 + opp_moves) * 1.0))

def custom_center_devide(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    blanks = len(game.get_blank_spaces())

    if blanks > (game.width * game.height) / 2:
        # Minimize distance to center square
        w, h = game.width / 2., game.height / 2.
        y, x = game.get_player_location(player)
        return - float((h - y)**2 + (w - x)**2)

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(0.1 + own_moves) / (0.1 + opp_moves * 1.2)

# dist to opp ( 43  |  57 )
def custom_distance_to_opponent(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    y2, x2 = game.get_player_location(game.get_opponent(player))

    # Distance to other opp
    return - float((y2 - y)**2 + (x2 - x)**2)

# center_dist ( 38  |  62 )
def custom_center(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)

    # Distance to center square
    return - float((h - y)**2 + (w - x)**2)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.testTrees = []

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Forfeit game if no legal moves left
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)

        # Initiate depth-first search and store scores & moves
        # Returning the maximum of scores is equivalent to calling maxvalue
        # So we call minvalue inside the for loop
        scores = dict()
        for move in legal_moves:
            scores[move] = self.minvalue(game.forecast_move(move), depth-1)

        # Return move that has the greatest score associated with it
        return max(scores, key=scores.get)

    def maxvalue(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Return the outcome of the game if no legal moves left
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return game.utility(self)

        # Return the result of the evaluation function if we are at a subtree leaf
        if depth <= 0:
            return self.score(game, self)

        # Get the maximum score for each legal move - current player is self
        v = float("-inf")
        for move in legal_moves:
            board = game.forecast_move(move)
            v = max(v, self.minvalue(board, depth-1))

        return v

    def minvalue(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Return the outcome of the game if no legal moves left
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return game.utility(self)

        # Return the result of the evaluation function if we are at a subtree leaf
        if depth <= 0:
            return self.score(game, self)

        # Get the minimum score for each legal move - current player is self's opponent
        v = float("inf")
        for move in legal_moves:
            board = game.forecast_move(move)
            v = min(v, self.maxvalue(board, depth-1))

        return v

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left, tree=None):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        depth = 1

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            while self.time_left() > self.TIMER_THRESHOLD:
                # Memorize last valid move
                best_move = self.alphabeta(game, depth)
                # Increase depth if we still have time
                depth += 1

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), tree=None):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Forfeit game if no legal moves left
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)

        # Initiate best_move with first legal move to avoid forfeiting if all scores = -inf
        best_move = legal_moves[0]
        scores = dict()

        # Initiate depth-first search and store scores & moves
        # Returning the maximum of scores is equivalent to calling maxvalue
        # So we call minvalue inside the for loop
        for move in legal_moves:
            v = self.minvalue(game.forecast_move(move), depth-1, alpha, beta)
            scores[move] = v

            # Memorize move and change lower limit if score is greater that previous ones
            if v > alpha:
                alpha = v
                best_move = move

        # Return move that has the greatest score associated with it
        return best_move

    def maxvalue(self, game, depth, alpha, beta, tree=None):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Return the outcome of the game if no legal moves left
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return game.utility(self)

        # Return the result of the evaluation function if we are at a subtree leaf
        if depth <= 0:
            return self.score(game, self)

        # Get the maximum score for each legal move - current player is self
        v = float("-inf")
        for move in legal_moves:
            v = max(v, self.minvalue(game.forecast_move(move), depth-1, alpha, beta))

            # Prune all branches after this one if score is higher than the top limit
            # Reason: we have to chose the maximum score => if the next scores are greater, they will be > top limit; if they are lower => they do not matter
            # The top limit comes from a previous minvalue calculation
            if v >= beta:
                return v

            # Move lowest limit to current score if the score is higher
            alpha = max(alpha, v)

        return v

    def minvalue(self, game, depth, alpha, beta, tree=None):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Return the outcome of the game if no legal moves left
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return game.utility(self)

        # Return the result of the evaluation function if we are at a subtree leaf
        if depth <= 0:
            return self.score(game, self)

        # Get the minimum score for each legal move - current player is self's opponent
        v = float("inf")
        for move in legal_moves:
            v = min(v, self.maxvalue(game.forecast_move(move), depth-1, alpha, beta))

            # Prune all branches after this one if score is lower than the lowest limit
            # Reason: we have to chose the minimum score => if the next scores are lower, they will be < lowest limit; if they are higher => they do not matter
            # The lowest limit comes from a previous maxvalue calculation
            if v <= alpha:
                return v

            # Move highest limit to current score if the score is lower
            beta = min(beta, v)

        return v
