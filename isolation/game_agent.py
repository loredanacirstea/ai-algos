import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

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

    player_moves = game.get_legal_moves()
    opponent_moves = game.get_legal_moves(game.inactive_player)

    print('custom_score', len(player_moves) - len(opponent_moves))

    return float(len(player_moves) - len(opponent_moves))


def custom_score_2(game, player):
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

    player_moves = game.get_legal_moves()
    opponent_moves = game.get_legal_moves(game.inactive_player)

    print('custom_score', len(player_moves) - 2 * len(opponent_moves))

    return float(len(player_moves) - 2 * len(opponent_moves))


def custom_score_3(game, player):
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

    return float(len(game.get_legal_moves()))


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
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

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

        scores = dict()
        legal_moves = game.get_legal_moves(self)

        if not legal_moves:
            return (-1, -1)

        print('minimax', depth, legal_moves, game.active_player)
        for move in legal_moves:
            print('MOVE', move);
            board = game.forecast_move(move)
            scores[move] = self.minimax_score(board, depth-1)
            print('SCORE', scores[move])

        print('---scores', scores)
        if game.active_player == self:
            return max(scores, key=scores.get)

        return min(scores, key=scores.get)

    def minimax_score(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Return the actual score of the board if depth is 0
        if depth == 0:
            return self.score(game, self)

        scores = dict()
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return game.utility(self)

        print('minimax_score', depth, legal_moves, game.active_player)

        for move in legal_moves:
            board = game.forecast_move(move)
            print('minimax_score board \n', board.to_string())
            scores[move] = self.minimax_score(board, depth-1)
            print('-move, score', move, scores[move])

        if game.active_player == self:
            return max(scores.values())

        return min(scores.values())


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
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
                best_move = self.alphabeta(game, depth)
                depth += 1

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
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

        # game, depth, alpha, beta
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


        #legal_moves = game.get_legal_moves()

        #if not legal_moves:
        #    return (-1, -1)

        result = self.alphabeta_recurs(game, depth, alpha, beta);

        print('/ALPHABETA', result)
        return result['move']

    def alphabeta_recurs(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


        # If depth is 0, just return the score
        if depth == 0:
            return dict(score = self.score(game, self), alpha = alpha, beta = beta)

        maxval = game.active_player == self
        minval = game.active_player != self
        ab_move = (-1, -1)

        # initialize score
        if maxval:
            score = float("-inf")
            pruning_score = float("inf")
            print('MAXVAL')
        else:
            score = float("inf")
            pruning_score = float("-inf")
            print('MINVAL')

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return dict(move = (-1, -1), score=pruning_score)
            #return dict(score=game.utility(self))

        print('alphabeta_recurs', depth, legal_moves, game.active_player)

        for move in legal_moves:
            board = game.forecast_move(move)
            print('alphabeta_recurs board \n', board.to_string())
            #scores[move] = self.alphabeta_recurs(board, depth-1, alpha, beta)
            result = self.alphabeta_recurs(board, depth-1, alpha, beta)
            print('alphabeta_recurs result', result)

            # If MINVAL and score is lower than lower limit, return (there is a previous MAXVAL with a branch that has a higher score)
            # If MAXVAL and score is higher that the upper limit, return (there is a prev MINVAL with a branch that has a lower score)
            if (minval and result['score'] <= alpha) or (maxval and result['score'] >= beta):
                print('AB pruning', pruning_score, 'alpha', alpha, 'beta', beta)
                return dict(score=pruning_score, alpha=alpha, beta=beta, move=(-1, -1))

            # If MAXVAL and score is higher than others, cache it and the move and replace lower limit
            if maxval and result['score'] > alpha:
                alpha = score = result['score']
                ab_move = move

            # If MINVAL and score is lower than others, cache it and the move and replace upper limit
            if minval and result['score'] < beta:
                beta = score = result['score']
                ab_move = move

            print('-move, score', ab_move, score, 'alpha', alpha, 'beta', beta, 'MAXVAL', maxval)

        return dict(score=score, move=ab_move, alpha=alpha, beta=beta)
