import random

from xo.calc import get_next_turn, get_best_move_score
from xo.model import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.play_for = None
        self.starter = None

    def initialize(self):
        print('Playing a Game of X/O')
        print('-' * 50)
        print('Please note that you should tell me your moves by a number between 1-9')
        print('Consider the board is number pad of your phone and tell the number of key you want')
        print('-' * 50)
        op = input('Which symbol you want to play for? X or O? ')
        self.play_for = 2 if op.lower() == 'x' else 1
        print('Flipping a coin to see who starts')
        self.starter = random.randint(1, 2)
        # self.starter = self.play_for
        if self.play_for == self.starter:
            print('Computer will start')
        else:
            print('You start First')

    def play(self):
        self.initialize()
        turn = self.starter
        while not (self.board.get_winner_if_any() or self.board.is_full()):
            m = self.get_next_move(turn)
            self.board.b[m] = turn
            print(self.board)
            turn = get_next_turn(turn)

        if self.board.get_winner_if_any() == self.play_for:
            print('Hooray! I win')
        elif self.board.get_winner_if_any() != 0:
            print('Oh you got me')
        else:
            print("That's a tie")

    def get_next_move(self, turn):
        if turn == self.play_for:
            print('Thinking...')
            m, _ = get_best_move_score(self.board, turn, self.play_for)
            return m
        else:
            m = int(input('Please Enter Your Move '))
            m = self.convert_user_move(m)
            assert self.board.b[m] == 0, 'The cell is already full'
            return m

    @staticmethod
    def convert_user_move(m):
        return (m - 1) // 3, (m - 1) % 3