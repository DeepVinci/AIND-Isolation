"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


# build tree structure, that allows alpha and beta cuts
class Node():

    def __init__(self, value, alpha, beta, children):
        self.value = value
        self.alpha = alpha
        self.beta = beta
        self.children = children

    # get_score
    def get_value(self):
        return self.value

    def get_alpha(self):
        return self.alpha

    def get_beta(self):
        return self.beta

    # get_legal_moves
    def get_children(self):
        return self.children


# https://de.wikipedia.org/wiki/Alpha-Beta-Suche
tree_dict = {'1':12, '11':10, '12':12, '13':3,
            '111':10, '112':12, '121':12, '122':13, '131':3, '132':5,
            '1111':10, '1112':-5, '1113':3, '1121':-6, '1122':12, '1123':3,
            '1211': 10, '1212':12, '1213': 3, '1221': 13, '1222': -6, '1223': 14,
            '1311': 3, '1312': 2, '1313': -4, '1321': -6, '1322': 12, '1323': 3,}

tree_dict_4 = {'1111':5, '1112':6, '1121':7, '1122':4, '1123':5, '1211':3,
             '2111':6, '2121':6, '2122':9, '2211':7,
             '3111':5, '3211':9, '3212':8, '3221':6,}


# get next node, simulate get_legal_moves


if __name__ == '__main__':
    unittest.main()
