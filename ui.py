import tkinter as tk
from tkinter import messagebox
from board import Board
from game import Game

CELL_SIZE = 64
PADDING = 36

class GameUI:
    def __init__(self, master, allowed_moves_dict=None):
        self.master = master
        self.master.title("Halma — To‘liq Forma")
        self.BOARD_SIZE = 8

        self.allowed_moves_dict = allowed_moves_dict if allowed_moves_dict else {}
        self.create_menu()
        self.create_status_bar()
        self.create_help_frame()
        self.setup_board()
        self.draw_game()

    def create_menu(self):
        menubar = tk.Menu(self.master)
        # O'yin menyusi
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="Yangi o'yin", command=self.restart)
        game_menu.add_separator()
        game_menu.add_command(label="Chiqish", command=self.master.quit)
        menubar.add_cascade(label="O'yin", menu=game_menu)
        # Forma: rang tanlash va rejimlar
        select_menu = tk.Menu(menubar, tearoff=0)
        select_menu.add_command(label="Oqlar bilan o'ynash", command=self.select_white)
        select_menu.add_command(label="Qoralar bilan o'ynash", command=self.select_black)
        select_menu.add_separator()
        select_menu.add_command(label="O'z-o'zi bilan o'ynash", command=self.select_self_play)
        menubar.add_cascade(label="Tanlash", menu=select_menu)
        # Yordam
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Yordam", command=self.show_help)
        menubar.add_cascade(label="Yordam", menu=help_menu)
        self.master.config(menu=menubar)

    def create_status_bar(self):
        self.status_label = tk.Label(self.master, text="", font=('Arial', 12), anchor="w")
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

    def create_help_frame(self):
        self.help_frame = tk.Frame(self.master, borderwidth=2, relief="groove")
        self.help_frame.pack(fill=tk.X, side=tk.TOP)
        self.help_label = tk.Label(self.help_frame, text="Donani tanlang, sariq katakka bosing. Yordam uchun: Menyu > Yordam", font=('Arial', 10))
        self.help_label.pack(padx=5, pady=3)

    def show_help(self):
        messagebox.showinfo(
            "Yordam",
            "Donani tanlang, sariq katakka bosing.\n"
            "Menyu orqali rang va rejimni tanlang.\n"
            "Formadagi har bir element yordamida o‘yin boshqariladi."
        )

    def select_white(self):
        self.player_color = 1
        self.setup_board()
        self.draw_game()

    def select_black(self):
        self.player_color = 2
        self.setup_board()
        self.draw_game()

    def select_self_play(self):
        self.player_color = 0
        self.setup_board()
        self.draw_game()

    def setup_board(self):
        self.board = Board(self.BOARD_SIZE)
        self.board.setup_pieces()
        self.game = Game(self.board, self.allowed_moves_dict)
        self.selected = None
        self.highlight_moves = []

    def draw_game(self):
        if hasattr(self, "canvas") and self.canvas is not None:
            self.canvas.pack_forget()
            self.canvas.destroy()
        w = self.BOARD_SIZE*CELL_SIZE + PADDING*2
        h = self.BOARD_SIZE*CELL_SIZE + PADDING*2
        self.canvas = tk.Canvas(self.master, width=w, height=h, bg='bisque')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.draw_board()
        self.status_label.config(text=self.get_status_text())

    def draw_board(self):
        self.canvas.delete("all")
        font = ("Arial", 14, "bold")
        # Harflar (A-H)
        for c in range(self.BOARD_SIZE):
            x = c*CELL_SIZE + PADDING + CELL_SIZE//2
            self.canvas.create_text(x, PADDING//2, text=chr(ord('A')+c), font=font)
            self.canvas.create_text(x, PADDING + CELL_SIZE*self.BOARD_SIZE + PADDING//2, text=chr(ord('A')+c), font=font)
        # Sonlar (1-8)
        for r in range(self.BOARD_SIZE):
            y = r*CELL_SIZE + PADDING + CELL_SIZE//2
            self.canvas.create_text(PADDING//2, y, text=str(self.BOARD_SIZE-r), font=font)
            self.canvas.create_text(PADDING + CELL_SIZE*self.BOARD_SIZE + PADDING//2, y, text=str(self.BOARD_SIZE-r), font=font)
        # Taxta va donalar
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                x1 = c*CELL_SIZE+PADDING
                y1 = r*CELL_SIZE+PADDING
                x2 = x1+CELL_SIZE
                y2 = y1+CELL_SIZE
                color = "#f0d9b5" if (r+c)%2==0 else "#b58863"
                if (r, c) in self.highlight_moves:
                    color = "#ffe066"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                piece = self.board.get_piece(r, c)
                if piece == 1:
                    self.canvas.create_oval(x1+8, y1+8, x2-8, y2-8, fill="white", outline="gray", width=2)
                elif piece == 2:
                    self.canvas.create_oval(x1+8, y1+8, x2-8, y2-8, fill="black", outline="gray", width=2)
        if self.selected:
            r, c = self.selected
            x1 = c*CELL_SIZE+PADDING
            y1 = r*CELL_SIZE+PADDING
            x2 = x1+CELL_SIZE
            y2 = y1+CELL_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=3)

    def on_canvas_click(self, event):
        c = (event.x - PADDING) // CELL_SIZE
        r = (event.y - PADDING) // CELL_SIZE
        if not (0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE):
            return

        pos = (r, c)
        piece = self.board.get_piece(r, c)
        if self.selected is None:
            if piece == self.game.turn:
                self.selected = pos
                self.highlight_moves = self.game.all_moves(pos)
                self.draw_board()
        else:
            src = self.selected
            dst = pos
            if dst in self.highlight_moves:
                if self.game.move(src, dst):
                    self.selected = None
                    self.highlight_moves = []
                    self.draw_board()
                    self.status_label.config(text=self.get_status_text())
                    winner = self.game.check_game_over()
                    if winner:
                        messagebox.showinfo("O'yin tugadi!", f"Yutuvchi: {'Oq' if winner == 1 else 'Qora'}")
                        self.setup_board()
                        self.draw_game()
                        return
                else:
                    pass
            else:
                if piece == self.game.turn:
                    self.selected = pos
                    self.highlight_moves = self.game.all_moves(pos)
                else:
                    self.selected = None
                    self.highlight_moves = []
                self.draw_board()

    def restart(self):
        self.setup_board()
        self.draw_game()

    def get_status_text(self):
        t = self.game.turn
        if hasattr(self, "player_color"):
            if self.player_color == 1:
                who = "Oq"
            elif self.player_color == 2:
                who = "Qora"
            else:
                who = "Oq/Qora"
        else:
            who = "Oq/Qora"
        return f"Navbat: {'Oq' if t == 1 else 'Qora'}  |  Siz tanlagan: {who}"