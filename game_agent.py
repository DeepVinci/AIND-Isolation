"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
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
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return together_center(game, player)


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
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return me_opp_distance(game, player)


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
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return own_opp_move_change_weight_inv(game, player)


def own_opp_moves(game, player):
    """ Basic move difference """
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return own_moves - opp_moves


def me_opp_distance(game, player):
    """Distance between player and opponent"""
    opp = game.get_opponent(player)
    oy, ox = game.get_player_location(opp)
    py, px = game.get_player_location(player)

    return float((ox - px) ** 2 + (oy - py) ** 2)


def center_distance(game, player):
    """ Distance between a player and the center of the board """
    py, px = game.get_player_location(player)
    cx, cy = game.width / 2., game.height / 2.

    return float((cx - px)**2 + (cy - py)**2)


def together_moves(game, player):
    """ Keep your enemies close and have more moves """
    return own_opp_moves(game, player) - me_opp_distance(game, player)


def together_center(game, player):
    """ Keep your enemies close but stay in middle """
    return 1 - me_opp_distance(game, player) - 0.5 * center_distance(game, player)


def change_middle_to_moves(game, player):
    """ First try to keep opp from middle, then just try to have more moves """
    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    opp_center_dist = center_distance(game, game.get_opponent(player))

    return 0.2 * (my_moves - opp_moves * 2) + opp_center_dist * blank_spaces_ratio(game)


def block_opp_from_center(game, player):
    """ decrease opp possibilities while dominating middle """
    opp = game.get_opponent(player)
    opp_moves = game.get_legal_moves(opp)
    my_moves = game.get_legal_moves(player)
    block = set(opp_moves) & set(my_moves)
    score = 0

    # I block the opponent
    if game.active_player == player and len(block) > 0:
        score = 2

    return score - center_distance(game, player)


def blank_spaces_ratio(game):
    """" The Ratio of empty fields and dimension of the board """
    blank_spaces = len(game.get_blank_spaces())
    dim = game.width * game.height

    return blank_spaces / dim


def own_opp_move_change_weight(game, player):
    """ Smoothly adjust behaviour to decreasing blank spaces"""
    weight = 1.5 - blank_spaces_ratio(game)
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return own_moves * weight - opp_moves


def own_opp_move_change_weight_inv(game, player):
    """ Smoothly adjust behaviour to decreasing blank spaces"""
    weight = 1.5 - blank_spaces_ratio(game)
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return own_moves - opp_moves * weight


def occupy_middle(game, player):
    """ Higher score if own player is close to middle """
    return float(own_opp_moves(game, player) - center_distance(game, player))


def opp_moves_center_distance(game, player):
    opp_center_dist = center_distance(game, game.get_opponent(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(opp_center_dist - opp_moves)


def opening_book():
    """ Only center of board and direct neighbors. """
    pass


def counter_opening():
    """ Best counter moves without calculation """
    pass


# only useful for depth 1
def copycat(game, player):
    # is the current location the mirror of opponents position?
    if game.get_player_location(player) == mirror(game, player):
        if game.active_player == player:
            return 100  # I mirror
        else:
            return -100  # Opp mirrors me

    return own_opp_moves(game, player)


# Not useful in heuristic, must be played before alphabeta
def mirror(game, player):
    """ Return opponents mirrored position """
    opp = game.get_opponent(player)
    oy, ox = game.get_player_location(opp)

    return game.width - ox, game.height - oy


# Not useful in heuristic, must be played before alphabeta
def avoid_mirror(game, player):
    """ Only allow fields opponent can´t reach """
    opp = game.get_opponent(player)
    opp_moves = game.get_legal_moves(opp)
    my_moves = game.get_legal_moves(player)

    return set(my_moves) - set(opp_moves)


def rotate():
    """ Rotate the board for 90 degrees """
    pass


def check_symetry():
    """ No need for another calculation if a symetric situation is found """
    pass


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

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return -1, -1

        best_move = legal_moves[random.randint(0, len(legal_moves) - 1)]

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            # print('Minimax moves: '+str(game.get_legal_moves()))
            best_move = self.minimax(game, self.search_depth)
            # print('Minimax score: ' + str(score) + ', move ' + str(best_move))

        except SearchTimeout:
            # Handle any actions required after timeout as needed
            return best_move

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
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return -1, -1

        _, best_move = max([(self.mini(game.forecast_move(m), depth - 1), m) for m in legal_moves])

        return best_move

    def maxi(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if depth <= 0 or not legal_moves:
            return self.score(game, self)

        return max([self.mini(game.forecast_move(m), depth - 1) for m in legal_moves])

    def mini(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if depth <= 0 or not legal_moves:
            return self.score(game, self)

        return min([self.maxi(game.forecast_move(m), depth - 1) for m in legal_moves])


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

        # TODO: finish this function!
        best_move = (-1, -1)
        depth = 1
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            while True:
                new_move = self.alphabeta(game, depth)
                if new_move != (-1, -1):
                    best_move = new_move
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
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_move = -1, -1
        legal_moves = game.get_legal_moves()

        # m = mirror(game, self)
        # if legal_moves.count(m) > 0:
        #    return m

        if depth == 0 or not legal_moves:
            return best_move

        best_score = float("-inf")
        # Finally, we are interested in moves not scores, also take care of alpha from the beginning
        for m in legal_moves:
            score = self.mini(game.forecast_move(m), depth - 1, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = m

            alpha = max(alpha, best_score)

        return best_move

    def maxi(self, game, depth, alpha, beta):
        """ Choose max value with regard to beta border determined by mini """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if depth == 0 or not legal_moves:
            return self.score(game, self)

        score = float("-inf")
        for m in legal_moves:
            score = max(score, self.mini(game.forecast_move(m), depth-1, alpha, beta))
            if score >= beta:
                return score  # beta cut

            alpha = max(alpha, score)  # increase alpha border for next min level

        return score

    def mini(self, game, depth, alpha, beta):
        """ Choose min value with regard to alpha border determined by maxi"""
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if depth == 0 or not legal_moves:
            return self.score(game, self)

        score = float("inf")
        for m in legal_moves:
            score = min(score, self.maxi(game.forecast_move(m), depth-1, alpha, beta))
            if score <= alpha:
                return score  # alpha cut

            beta = min(beta, score)  # decrease beta border for next max level

        return score
