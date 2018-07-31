import numpy as np
import random
from copy import deepcopy
import time


class Connect4GameOver(Exception):
    pass


class Connect4InvalidMove(Exception):
    pass


class Connect4Logic(object):
    def __init__(self, nrows, ncols, connectn, player1, player2, cpu1, cpu2,
                 emptyk=None, p1k=None, p2k=None, board=None, current_turn=None, winner=None):
        self.nrows = nrows
        self.ncols = ncols
        self.connectn = connectn
        self.player1 = player1
        self.player2 = player2
        self.cpu1 = cpu1
        self.cpu2 = cpu2
        if emptyk is None:
            self.emptyk = np.int8(0)
        else:
            self.emptyk = emptyk
        if p1k is None:
            self.p1k = np.int8(1)
        else:
            self.p1k = p1k
        if p2k is None:
            self.p2k = np.int8(2)
        else:
            self.p2k = p2k
        if board is None:
            self.board = self.new_board(self.nrows, self.ncols)
        else:
            self.board = board
            self.board = self.copy_board()
        if current_turn is None:
            self.current_turn = 1  # 1 -> Player 1's turn. 2 -> Player 2's turn.
        else:
            self.current_turn = current_turn
        if winner is None:
            self.winner = self.emptyk
        else:
            self.winner = winner
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

    def valid_columns(self):
        valid_col_inds =  np.array([self.valid_move(col) for col in range(self.ncols)])
        return np.array(range(self.ncols))[valid_col_inds]

    def computer_move(self):
        # Priorities are:
        #   1. to stop the opponent from winning.
        #   2. to connect as many pieces as he can
        #1.
        valid_moves = self.valid_columns()
        pseudo_object =  deepcopy(self.__dict__)
        pseudo_object["cpu1"] = False
        pseudo_object["cpu2"] = False
        for mv in valid_moves:
            new_state = Connect4Logic(**pseudo_object)
            # Toggle the turn to see if the opponent can win by putting a piece anywhere
            new_state.current_turn = 2 if new_state.current_turn == 1 else 1
            new_state.drop_piece(mv)
            if new_state.winner != new_state.emptyk:
                return mv
        for mv in valid_moves:
            new_state = Connect4Logic(**pseudo_object)
            new_state.drop_piece(mv)
            if new_state.winner != new_state.emptyk:
                return mv
        return random.choice(valid_moves)

    def valid_move(self, col):
        if col > self.ncols:
            raise Connect4InvalidMove("col is greater than the number of columns ({} > {})".format(col, self.ncols))
        return np.any(self.board[:, col] == self.emptyk)

    def drop_piece(self, col, docheck=False):
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
