import tkinter as tk
from typing import Tuple


class Board:
    def __init__(self, width, height, n_to_win):
        self.width = width
        self.height = height
        self.n_to_win = n_to_win             # number of chess in a roll needed to win
        self.board = self.get_empty_board()  # 0 for no player, 1 for player1, 2 for player2
        self.last_move = (0, 0)  # TODO: is it necessary to exist?

    def get_board(self):
        return self.board.copy()

    def get_empty_board(self):
        board = {}
        for i in range(self.width):
            for j in range(self.height):
                board[(i+1, j+1)] = 0
        return board

    def get_available_action(self, board=None):
        if board is None:
            board = self.board

        available_action = []
        for action in board:
            if board[action] == 0:
                available_action.append(action)
        return available_action

    def move(self, player, position: Tuple[int, int]):
        """
        For 4x4 board, move would be like
        0 0 0 0
        0 0 0 0
        0 0 0 0
        0 0 1 0
        with position (4, 3)
        """
        if self.board[position] == 0:
            self.board[position] = player
            self.last_move = position
            return self.check_if_game_ends(player, position[0], position[1])
        else:
            raise Exception('Position is not valid!')

    def check_if_game_ends(self, player, row, col, board=None):
        # check the number of chess in each direction
        # left->right | up->bottom | up left-> bottom right | up right-> bottom left
        if board is None:
            board = self.board

        direction = [((0, -1), (0, 1)), ((-1, 0), (1, 0)), ((-1, -1), (1, 1)), ((-1, 1), (1, -1))]
        for dd in direction:
            num = -1  # itself is calculated twice
            for d in dd:
                i = row
                j = col
                while board[(i, j)] == player:
                    num += 1
                    i += d[0]
                    j += d[1]
                    if not (0 < i <= self.height and 0 < j <= self.width):
                        break

            if num == self.n_to_win:
                return True  # Game ends
        return False         # Game not ends


class Game:
    def __init__(self, width, height, n_to_win):
        self.board = None
        self.restart(width, height, n_to_win)
        # TODO: UI is going to be added later

    def restart(self, width, height, n_to_win):
        self.board = Board(width, height, n_to_win)

