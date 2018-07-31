# John Gresl 7/26/2018

import time
import tkinter as tk

import numpy as np

from GUIDefaults import *
from Connect4Logic import Connect4GameOver, Connect4InvalidMove


class Connect4GUI(object):
    def __init__(self, gamestate):
        self.color_dict = {0: "white", 1: "blue", 2: "red"}
        self.pad = 15
        self.gamestate = gamestate
        self.col_edges = np.zeros(self.gamestate.ncols)
        self.row_edges = np.zeros(self.gamestate.nrows)
        self.root = tk.Tk()
        self.canvas = tk.Canvas(master=self.root)
        self.canvas.pack(fill="both", expand=True)
        self.root.bind("<Configure>", self.update_board)
        self.canvas.tag_bind("clickable", "<1>", self.click)
        self.hold = False
        self.game_over_bool = False
        self.play_again_bool = False
        self.start()
        return

    def start(self):
        self.check_for_cpu_move()
        self.root.minsize(self.canvas.winfo_width(), self.canvas.winfo_height())
        self.root.mainloop()
        return

    def draw_oval_from_center(self, x, y, a, b, color):
        self.canvas.create_oval(x - a, y - b, x + a, y + b, fill=color, tags=("clickable"))
        return

    def make_move(self, clickcol):
        try:
            self.gamestate.drop_piece(clickcol)
        except Connect4GameOver:
            print("it me")
            self.game_over()
            return
        except Connect4InvalidMove:
            pass
        except Exception as e:
            raise e
        if self.gamestate.winner != self.gamestate.emptyk:
            self.game_over()
            self.update_board(None)
            return
        self.update_board(None)
        if self.gamestate.full_board_q():
            self.game_over()
            return
        return

    def check_for_cpu_move(self):
        if self.gamestate.is_cpu_move() and not self.game_over_bool:
            self.hold = True
            time.sleep(WAIT_TIME)
            cpu_move = self.gamestate.computer_move()
            self.make_move(cpu_move)
            if self.gamestate.is_cpu_move():
                self.root.after(10, self.check_for_cpu_move)
            else:
                self.hold = False
        return

    def click(self, ev):
        if self.hold or self.game_over_bool:
            return
        clickrow = np.argmax(self.row_edges > ev.y)
        clickcol = np.argmax(self.col_edges > ev.x)
        self.make_move(clickcol)
        self.check_for_cpu_move()
        return

    def game_over(self):
        self.game_over_bool = True
        top = tk.Toplevel(master=self.root, background=DEFAULT_WIDGET_BG)
        top.protocol("WM_DELETE_WINDOW", self.root.destroy)
        while True:
            try:
                top.grab_set()
                break
            except:
                top.after(100)
        top.geometry("250x215")
        top.resizable(False, False)
        if self.gamestate.winner == self.gamestate.p1k:
            winner_msg = "{} Wins!".format(self.gamestate.player1)
        elif self.gamestate.winner == self.gamestate.p2k:
            winner_msg = "{} Wins!".format(self.gamestate.player2)
        else:
            winner_msg = "It's a tie!"
        top.title(winner_msg)
        message = tk.Message(master=top, text=winner_msg, font=DEFAULT_FONT,
                             width=240, background=DEFAULT_WIDGET_BG)
        message.pack()
        self.quit_button = tk.Button(master=top, text="Quit", command=self.root.destroy,
                                     font=DEFAULT_FONT, background=DEFAULT_WIDGET_BG,
                                     activebackground=DEFAULT_WIDGET_BG)
        def play_again():
            self.play_again_bool = True
            self.root.destroy()
            return

        self.quit_button.pack()
        self.play_again_button = tk.Button(master=top, text="Again!",
                                           command=play_again, font=DEFAULT_FONT,
                                           background=DEFAULT_WIDGET_BG,
                                           activebackground=DEFAULT_WIDGET_BG)
        self.play_again_button.pack()
        return

    def generate_font(self):
        h = self.canvas.winfo_height()
        w = self.canvas.winfo_width()
        info_height = 0.15 * h
        font_size = info_height/1.5
        while (len(self.gamestate.player1) + len(self.gamestate.player2)*(font_size**2))/12 > w:
            font_size -= 1
            if font_size <= 1:
                font_size = 1
                break
        return np.int(np.floor(font_size))

    def update_board(self, ev):
        h = self.canvas.winfo_height()
        w = self.canvas.winfo_width()
        info_height = 0.15 * h
        col_inc = (w - 2 * self.pad) / self.gamestate.ncols
        row_inc = (h - info_height - 2 * self.pad) / self.gamestate.nrows
        self.canvas.delete("all")
        self.col_edges = np.zeros(self.gamestate.ncols)
        self.row_edges = np.zeros(self.gamestate.nrows)

        for r in range(self.gamestate.nrows):
            self.row_edges[r] = row_inc * (r + 1) + self.pad
        for c in range(self.gamestate.ncols):
            self.col_edges[c] = col_inc * (c + 1) + self.pad

        self.canvas.create_rectangle(self.pad, self.pad, w - self.pad, h - self.pad, fill="yellow")
        for row in range(self.gamestate.nrows):
            for col in range(self.gamestate.ncols):
                self.draw_oval_from_center(col_inc * (col + 0.5) + self.pad,
                                           row_inc * (row + 0.5) + self.pad,
                                           col_inc * 0.5 / 1.2,
                                           row_inc * 0.5 / 1.2,
                                           color=self.color_dict[self.gamestate.board[row][col]])
        font_size = self.generate_font()
        self.canvas.create_text(2 * self.pad,
                                row_inc * (row + 0.5) + self.pad + row_inc * 0.5 / 1.2,
                                text=self.gamestate.player1,
                                font=("Courier", font_size, "bold underline" if self.gamestate.current_turn == 1 else "normal"),
                                anchor=tk.NW,
                                fill = self.color_dict[1])
        self.canvas.create_text(w - 2 * self.pad,
                                row_inc * (row + 0.5) + self.pad + row_inc * 0.5 / 1.2,
                                text=self.gamestate.player2,
                                font=("Courier", font_size, "bold underline" if self.gamestate.current_turn == 2 else "normal"),
                                anchor=tk.NE,
                                fill = self.color_dict[2])
        self.canvas.update()
        return
