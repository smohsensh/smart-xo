import random
from typing import Tuple, Union

import numpy as np

from xo.model import Board


def get_next_turn(turn: int):
    assert turn in {1, 2}
    return 2 if turn == 1 else 1


def get_best_move_score(board: Board, turn: int, play_for: int) -> Tuple[Union[None, Tuple[int, int]], float]:
    """turn should be (1, 2) indicating whose turn it is to move"""

    if board.is_empty():
        return random.choice([(0,0), (0, 2), (2, 0), (2,2)]), 1

    winner = board.get_winner_if_any()
    if winner:
        return None, 1 if winner == play_for else -1
    if board.is_full():
        return None, 0

    moves = list(board.generate_empty_indices())
    scores = np.zeros(shape=len(moves))
    for i, move in enumerate(moves):
        new_board = board.new_from_move(move, turn)
        _, s = get_best_move_score(new_board, get_next_turn(turn), play_for)
        scores[i] = s

        if (turn == play_for and s == 1) or (turn != play_for and s == -1):
            break

    if play_for == turn:
        idx = np.random.choice((scores == scores.max()).nonzero()[0])
        return moves[idx], scores.max()
    else:
        idx = np.random.choice((scores == scores.min()).nonzero()[0])
        return moves[idx], scores.min()


