import itertools
from typing import Tuple

import numpy as np


class Board:
    mapping = {
        0: ' ',
        1: 'X',
        2: 'O'
    }

    def __init__(self, b=None):
        if b is not None:
            self.b = np.copy(b)
        else:
            self.b = np.zeros(shape=(3, 3), dtype=np.int8)
        self.size = self.b.shape[0]

    def new_from_move(self, indices: Tuple[int, int], val: int):
        assert self.b[indices] == 0, 'cell is already full'
        board = Board(self.b)
        board.b[indices] = val
        return board

    def get_winner_if_any(self):
        for row in itertools.chain(self.b, self.b.T, [self.b.diagonal(), np.fliplr(self.b).diagonal()]):
            uniques = np.unique(row)
            if len(uniques) == 1 and uniques[0] != 0:
                return uniques[0]

        return 0

    def is_full(self):
        return not np.any(self.b == 0)

    def is_empty(self):
        return np.all(self.b == 0)

    def generate_empty_indices(self):

        for i, j in itertools.product(range(self.size), range(self.size)):
            if self.b[i, j] == 0:
                yield i, j

    def __str__(self):
        res = ''
        for i, row in enumerate(self.b):
            res += '|'.join([f'{self.mapping[x]} ' for x in row])
            if i != 2:
                res += '\n__|__|__\n'
            else:
                res += '\n  |  |  '
        return res


class Result:
    map = {
        0: 'tie',
        1: 'x',
        2: 'o'
    }

    def __init__(self, x=0, o=0, tie=0):
        self.x = x
        self.o = o
        self.tie = tie

    def get_numeric(self, item):
        return getattr(self, self.map[item])

    @staticmethod
    def from_winner(w):
        if w == 1:
            return Result(x=1)
        if w == 2:
            return Result(o=1)
        if w == 0:
            return Result(tie=1)

    def __add__(self, other):
        return Result(
            x=self.x+other.x,
            o=self.o+other.o,
            tie=self.tie+other.tie
        )

    def __eq__(self, other):
        return self.x == other.x and self.o == other.o and self.tie == other.tie
