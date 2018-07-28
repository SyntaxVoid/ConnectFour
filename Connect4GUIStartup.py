# John Gresl 7/26/2018
import tkinter as tk
import random

from GUIDefaults import *

class Connect4GUIStartup(object):
    # Performs the 'preamble' for running Connect4 by asking the user(s) for various details about their game.
    # Usage is:
    # c4 = Connect4GUIStartup()
    # c4.start() # <-- mainloop is called in here, so we won't print the next statement till it closes
    # values = c4.outd # <-- Values that the user(s) entered. Empty dict -> fail/they hit quit.
    def __init__(self, **kwargs):
        self.random_names = ["Gerry", "Vicente", "Bert", "Harvey", "Zackary", "Reyes", "Enoch", "Fritz",
                             "Aaron", "Theodore", "Pasquale", "Patrick", "Oswaldo", "Edmond", "Malik",
                             "Alden", "Bernie", "Nathanael", "Charley", "Latoya", "Nery", "Jacquiline",
                             "Shaunta", "Delaine", "Tandra", "Chelsey", "Kellee", "Talia", "Ida", "Eladia",
                             "Wendy", "Siu", "Lavon", "Alysia", "Beulah", "Tabatha", "Lucrecia", "Paulita",
                             "Marlys"]  # Random names generated from listofrandomnames.com
        self.outd = None
        self.root = tk.Tk()
        self.root.configure(background=DEFAULT_WIDGET_BG)

        self.title_lab = tk.Label(master=self.root, text="Welcome to Connect 4\n*-*-*-*-*-*-*-*",
                                  font=("Helvetica", 25),
                                  background=DEFAULT_WIDGET_BG)
        self.title_lab.grid(row=0, column=0, sticky=tk.EW, columnspan=4, padx=[50, 50], pady=[20, 20])

        self.nrow_frame = tk.Frame(master=self.root, background=DEFAULT_WIDGET_BG)
        self.nrow_frame.grid(row=1, column=0, columnspan=4, sticky=tk.N)
        self.nrow_lab = tk.Label(master=self.nrow_frame, text="# Rows:", font=DEFAULT_FONT,
                                 background=DEFAULT_WIDGET_BG)
        self.nrow_lab.grid(row=0, column=0, sticky=tk.E)
        self.nrow_var = tk.IntVar(master=self.nrow_frame, value=6)
        self.nrow_menu = tk.OptionMenu(self.nrow_frame, self.nrow_var, *ROW_OPTIONS)
        self.nrow_menu.config(font=DEFAULT_FONT, background=DEFAULT_WIDGET_BG,
                              activebackground=DEFAULT_HIGHLIGHT_COLOR, highlightthickness=0)
        self.nrow_menu["menu"].config(font=DEFAULT_FONT, background=DEFAULT_WIDGET_BG,
                                      activebackground=DEFAULT_HIGHLIGHT_COLOR,
                                      activeforeground=DEFAULT_ACTIVE_COLOR)
        self.nrow_menu.grid(row=0, column=1, sticky=tk.W)

        self.ncol_lab = tk.Label(master=self.nrow_frame, text="# Cols:", font=DEFAULT_FONT,
                                 background=DEFAULT_WIDGET_BG)
        self.ncol_lab.grid(row=0, column=2, sticky=tk.E)
        self.ncol_var = tk.IntVar(master=self.nrow_frame, value=6)
        self.ncol_menu = tk.OptionMenu(self.nrow_frame, self.ncol_var, *ROW_OPTIONS)
        self.ncol_menu.config(font=DEFAULT_FONT, background=DEFAULT_WIDGET_BG,
                              activebackground=DEFAULT_HIGHLIGHT_COLOR, highlightthickness=0)
        self.ncol_menu["menu"].config(font=DEFAULT_FONT, background=DEFAULT_WIDGET_BG,
                                      activebackground=DEFAULT_HIGHLIGHT_COLOR,
                                      activeforeground=DEFAULT_ACTIVE_COLOR)
        self.ncol_menu.grid(row=0, column=3, sticky=tk.W)

        self.connect_n_frame = tk.Frame(master=self.root, background=DEFAULT_WIDGET_BG)
        self.connect_n_frame.grid(row=2, column=0, columnspan=4, sticky=tk.N)
        self.connect_n_label = tk.Label(master=self.connect_n_frame, text="Connect # to win:", font=DEFAULT_FONT,
                                        background=DEFAULT_WIDGET_BG, )
        self.connect_n_label.grid(row=0, column=0, sticky=tk.E, pady=5)
        self.connect_n_var = tk.IntVar(master=self.connect_n_frame, value=4)
        self.connect_n_menu = tk.OptionMenu(self.connect_n_frame, self.connect_n_var, *CONNECT_OPTIONS)
        self.connect_n_menu.config(font=DEFAULT_FONT, background=DEFAULT_WIDGET_BG,
                                   activebackground=DEFAULT_HIGHLIGHT_COLOR, highlightthickness=0)
        self.connect_n_menu["menu"].config(font=DEFAULT_FONT, background=DEFAULT_WIDGET_BG,
                                           activebackground=DEFAULT_HIGHLIGHT_COLOR,
                                           activeforeground=DEFAULT_ACTIVE_COLOR)
        self.connect_n_menu.grid(row=0, column=1, sticky=tk.W)

        self.players_frame = tk.Frame(master=self.root, background=DEFAULT_WIDGET_BG)
        self.players_frame.grid(row=3, column=0, sticky=tk.EW, columnspan=4, padx=[10, 10], pady=[10, 0])
        self.player1_lab = tk.Label(master=self.players_frame, text="Player 1:", font=DEFAULT_FONT,
                                    background=DEFAULT_WIDGET_BG)
        self.player1_lab.grid(row=0, column=0, sticky=tk.NE)
        self.player1_name = tk.StringVar(master=self.players_frame)
        self.player1_name.trace("w", self.limit_player_len)
        self.player1_entry = tk.Entry(master=self.players_frame, textvariable=self.player1_name, font=DEFAULT_FONT,
                                      background=DEFAULT_ENTRY_COLOR, width=ENTRY_WIDTH)
        self.player1_entry.grid(row=0, column=1, sticky=tk.NW)

        self.cpu1_var = tk.IntVar(master=self.players_frame, value=0)
        self.cpu1_box = tk.Checkbutton(master=self.players_frame, text="CPU?", variable=self.cpu1_var,
                                       background=DEFAULT_WIDGET_BG, font=DEFAULT_FONT,
                                       activebackground=DEFAULT_WIDGET_BG, command=self.cpu1_check)
        self.cpu1_box.grid(row=0, column=2, sticky=tk.NSEW)

        self.player2_lab = tk.Label(master=self.players_frame, text="Player 2:", font=DEFAULT_FONT,
                                    background=DEFAULT_WIDGET_BG)
        self.player2_lab.grid(row=1, column=0, sticky=tk.NE)
        self.player2_name = tk.StringVar(master=self.players_frame)
        self.player2_name.trace("w", self.limit_player_len)
        self.player2_entry = tk.Entry(master=self.players_frame, textvariable=self.player2_name, font=DEFAULT_FONT,
                                      background=DEFAULT_ENTRY_COLOR, width=ENTRY_WIDTH)
        self.player2_entry.grid(row=1, column=1, sticky=tk.NW)

        self.cpu2_var = tk.IntVar(master=self.players_frame, value=0)
        self.cpu2_box = tk.Checkbutton(master=self.players_frame, text="CPU?", variable=self.cpu2_var,
                                       background=DEFAULT_WIDGET_BG, font=DEFAULT_FONT,
                                       activebackground=DEFAULT_WIDGET_BG, command=self.cpu2_check)
        self.cpu2_box.grid(row=1, column=2, sticky=tk.NSEW)

        self.confirm_button = tk.Button(master=self.root, text="Confirm", font=DEFAULT_FONT,
                                        background=DEFAULT_WIDGET_BG, command=self.confirm,
                                        activebackground=DEFAULT_HIGHLIGHT_COLOR)
        self.confirm_button.grid(row=4, column=3, sticky=tk.N)

        self.quit_button = tk.Button(master=self.root, text="Quit", font=DEFAULT_FONT,
                                     background=DEFAULT_WIDGET_BG, command=self.root.destroy,
                                     activebackground=DEFAULT_HIGHLIGHT_COLOR)
        self.quit_button.grid(row=4, column=2, sticky=tk.N)

        if kwargs:
            self.nrow_var.set(kwargs["nrows"])
            self.ncol_var.set(kwargs["ncols"])
            self.connect_n_var.set(kwargs["connectn"])
            self.player1_name.set(kwargs["player1"])
            self.player2_name.set(kwargs["player2"])
            self.cpu1_var.set(kwargs["cpu1"])
            self.cpu2_var.set(kwargs["cpu2"])
            if self.cpu1_var.get():
                self.player1_entry.config(state="disabled")
            if self.cpu2_var.get():
                self.player2_entry.config(state="disabled")

        self.start()
        return

    def limit_player_len(self, *args):
        p1name = self.player1_name.get()
        p2name = self.player2_name.get()
        n = NAME_LIMIT
        if len(p1name) > n: self.player1_name.set(p1name[:n])
        if len(p2name) > n: self.player2_name.set(p2name[:n])
        return

    def confirm(self):
        error = ""
        if self.connect_n_var.get() > self.nrow_var.get() and self.connect_n_var.get() > self.ncol_var.get():
            error += "-Please increase board dimensions or decrease Connect #!\n"
        if self.player1_name.get() == "":
            error += "-Please enter Player 1 name!\n"
        if self.player2_name.get() == "":
            error += "-Please enter Player 2 name!\n"
        if error != "":
            error_color = "firebrick1"
            top = tk.Toplevel(background=error_color)
            top.geometry("250x215")
            top.resizable(False, False)
            top.title("Connect4 Error!")
            message = tk.Message(master=top, text="Fix the following:\n"+error, font=("Helvetica", 14),
                                 background=error_color)
            message.pack()
            button = tk.Button(master=top, text="Dismiss", command=top.destroy, font=("Helvetica", 14),
                               background=error_color, activebackground=error_color)
            button.pack()
            return
        self.outd = {"nrows": self.nrow_var.get(),
                     "ncols": self.ncol_var.get(),
                     "connectn": self.connect_n_var.get(),
                     "player1": self.player1_name.get(),
                     "player2": self.player2_name.get(),
                     "cpu1": self.cpu1_var.get(),
                     "cpu2": self.cpu2_var.get()}
        self.root.destroy()
        return

    def cpu1_check(self):
        if self.cpu1_var.get():
            name = random.choice(self.random_names)
            while name in [self.player1_name.get(), self.player2_name.get()]:
                name = random.choice(self.random_names)
            self.player1_name.set(random.choice(self.random_names))
            self.player1_entry.config(state="disabled")
        else:
            self.player1_entry.config(state="normal")
        return

    def cpu2_check(self):
        if self.cpu2_var.get():
            name = random.choice(self.random_names)
            while name in [self.player1_name.get(), self.player2_name.get()]:
                name = random.choice(self.random_names)
            self.player2_name.set(name)
            self.player2_entry.config(state="disabled")
        else:
            self.player2_entry.config(state="normal")
        return

    def start(self):
        self.root.resizable(False, False)
        self.root.mainloop()
        return
