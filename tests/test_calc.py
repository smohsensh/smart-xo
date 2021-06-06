from unittest import TestCase

import numpy as np

from xo.calc import get_next_turn, get_best_move_score
from xo.model import Board


class PredictionTestCase(TestCase):

    def test_next_turn(self):
        self.assertEqual(get_next_turn(1), 2)
        self.assertEqual(get_next_turn(2), 1)
        with self.assertRaises(AssertionError):
            get_next_turn(0)

    def test_board_result_winner(self):
        b = Board()
        b.b[1, :] = 1

        _, score = get_best_move_score(b, 1, 1)
        self.assertEqual(score, 1)

        _, score = get_best_move_score(b, 1, 2)
        self.assertEqual(score, -1)

    def test_board_result_full(self):
        b = Board(np.array([[1, 2, 1], [2, 1, 2], [2, 1, 2]]))
        _, score = get_best_move_score(b, 1, 1)
        self.assertEqual(score, 0)

    def test_board_result_1(self):
        b = Board(np.array([[1, 2, 1], [2, 1, 2], [2, 1, 0]]))
        m, s = get_best_move_score(b, 2, 1)
        self.assertTupleEqual(m, (2, 2))
        self.assertEqual(s, 0)

        m, s = get_best_move_score(b, 1, 1)
        self.assertTupleEqual(m, (2, 2))
        self.assertEqual(s, 1)

    def test_board_result_2(self):
        b = Board(np.array([[1, 2, 0], [2, 1, 2], [2, 1, 0]]))

        m, s = get_best_move_score(b, 1, 1)
        self.assertTupleEqual(m, (2, 2))
        self.assertEqual(s, 1)

        m, s = get_best_move_score(b, 2, 1)
        self.assertTupleEqual(m, (2, 2))
        self.assertEqual(s, 0)

    def test_board_result_3(self):
        b = Board(np.array([[1, 2, 0], [1, 1, 2], [0, 2, 0]]))

        m, s = get_best_move_score(b, 1, 1)
        self.assertEqual(s, 1)

        m, s = get_best_move_score(b, 2, 1)
        self.assertEqual(s, 1)