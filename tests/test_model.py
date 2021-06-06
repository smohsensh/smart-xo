from unittest import TestCase

import numpy as np

from xo.model import Board, Result


class BoardTestCase(TestCase):

    def test_is_full(self):
        b = Board()
        self.assertFalse(b.is_full())
        b.b = np.ones_like(b.b)
        self.assertTrue(b.is_full())

    def test_winner_no_winner(self):
        b = Board()
        self.assertEqual(b.get_winner_if_any(), 0)

        b.b = np.array([
            [1, 2, 0],
            [1, 2, 2],
            [2, 1, 1]
        ])
        self.assertEqual(b.get_winner_if_any(), 0)

    def test_winner_one(self):
        board = Board()
        board.b[1] = [1, 1, 1]
        self.assertEqual(board.get_winner_if_any(), 1)

        board = Board()
        board.b[:, 2] = [2, 2, 2]
        self.assertEqual(board.get_winner_if_any(), 2)

        board = Board()
        board.b[0, 0] = board.b[1, 1] = board.b[2, 2] = 1
        self.assertEqual(board.get_winner_if_any(), 1)

        board = Board()
        board.b[0, 2] = board.b[1, 1] = board.b[2, 0] = 2
        self.assertEqual(board.get_winner_if_any(), 2)

    def test_empty_indices(self):
        board = Board()
        board.b[1] = [1, 1, 1]
        board.b[0, 2] = 2
        board.b[2, 1] = 2

        self.assertSetEqual(
            set(board.generate_empty_indices()),
            {(0, 1), (0, 0), (2, 0), (2, 2)}
        )

    def test_new_from_move(self):
        board = Board()
        board.b[1] = [1, 1, 2]
        b2 = board.new_from_move((2, 2), 2)
        np.testing.assert_array_equal(
            np.array([[0, 0, 0], [1, 1, 2], [0, 0, 2]]),
            b2.b
        )

    def test_invalid_new_move(self):
        board = Board()
        board.b[1] = [1, 1, 2]
        with self.assertRaises(AssertionError):
            board.new_from_move((1, 2), 2)


class ResultTestCase(TestCase):

    def test_add(self):
        r1 = Result(3, 2, 0)
        r2 = Result(0, 2, 1)

        s = r1 + r2
        self.assertEqual(s.x, 3)
        self.assertEqual(s.o, 4)
        self.assertEqual(s.tie, 1)
