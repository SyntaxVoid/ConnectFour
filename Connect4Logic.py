import numpy as np
import random
import time


class Connect4GameOver(Exception):
    pass


class Connect4InvalidMove(Exception):
    pass


class Connect4Logic(object):
    def __init__(self, nrows, ncols, connectn, player1, player2, cpu1, cpu2):
        self.nrows = nrows
        self.ncols = ncols
        self.connectn = connectn
        self.player1 = player1
        self.player2 = player2
        self.cpu1 = cpu1
        self.cpu2 = cpu2
        self.emptyk = np.int8(0)
        self.p1k = np.int8(1)
        self.p2k = np.int8(2)
        self.board = self.new_board(self.nrows, self.ncols)
        self.current_turn = 1  # 1 -> Player 1's turn. 2 -> Player 2's turn.
        self.winner = self.emptyk
        self.check_computer_move()
        return

    def new_board(self, nrow, ncol):
        return np.zeros((nrow, ncol), dtype=np.int8) + self.emptyk

    def copy_board(self):
        return self.board * np.int8(1)

    def check_computer_move(self):
        if self.is_cpu_move():
            self.drop_piece(self.computer_move())
        return

    def is_cpu_move(self):
        return (self.cpu1 and self.current_turn == 1) or (self.cpu2 and self.current_turn == 2)

    def computer_move(self):
        return random.choice(list(range(self.ncols)))

    def valid_move(self, col):
        if col > self.ncols:
            raise Connect4InvalidMove("col is greater than the number of columns ({} > {})".format(col, self.ncols))
        return np.any(self.board[:, col] == self.emptyk)

    def drop_piece(self, col):
        if self.winner != self.emptyk:
            raise Connect4GameOver("Cannot drop piece! Game is already over!")
        if not self.valid_move(col):
            raise Connect4InvalidMove("Placing a piece in column {} is not a valid move!".format(col))
        self.board[np.where(self.board[:, col] == self.emptyk)[0][-1], col] = self.p1k \
            if self.current_turn == 1 else self.p2k
        self.current_turn = 2 if self.current_turn == 1 else 1
        self.check_winner()
        return

    def check_horiz_vert(self, invert=False):
        p1_win_seq = np.zeros(self.connectn, dtype=np.int8) + self.p1k
        p2_win_seq = np.zeros(self.connectn, dtype=np.int8) + self.p2k
        board = self.board if not invert else self.copy_board().T
        rows, cols = board.shape
        for row in range(rows):
            for col in range(self.connectn):
                if np.array_equal(board[row, col:col + self.connectn], p1_win_seq):
                    return self.p1k
                elif np.array_equal(board[row, col:col + self.connectn], p2_win_seq):
                    return self.p2k
        return self.emptyk

    def check_diag(self, invert=False):
        p1_win_seq = np.zeros(self.connectn, dtype=np.int8) + self.p1k
        p2_win_seq = np.zeros(self.connectn, dtype=np.int8) + self.p2k
        board = self.board if not invert else self.board[:, ::-1]
        rows, cols = board.shape
        for d in range(-rows + self.connectn, cols - self.connectn + 1):
            dg = board.diagonal(d)
            if len(dg) == self.connectn:
                if np.array_equal(dg, p1_win_seq):
                    return self.p1k
                elif np.array_equal(dg, p2_win_seq):
                    return self.p2k
            else:
                for i in range(len(dg) - self.connectn + 1):
                    if np.array_equal(dg[i:self.connectn + i], p1_win_seq):
                        return self.p1k
                    elif np.array_equal(dg[i:self.connectn + i], p2_win_seq):
                        return self.p2k
        return self.emptyk

    def check_winner(self):
        self.winner = self.check_horiz_vert()
        if self.winner != self.emptyk:
            return
        self.winner = self.check_horiz_vert(invert=True)
        if self.winner != self.emptyk:
            return
        self.winner = self.check_diag()
        if self.winner != self.emptyk:
            return
        self.winner = self.check_diag(invert=True)
        if self.winner != self.emptyk:
            return
        return

    def full_board_q(self):
        return self.emptyk not in self.board

    def __repr__(self):
        return str(self.board)
