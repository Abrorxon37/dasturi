import tkinter as tk
from tkinter import messagebox
from board import Board
from game import Game
from ai import SimpleAI

CELL_SIZE = 64
PADDING = 36

class GameUI:
    def __init__(self, master):
        self.master = master
        self.master.title("8x8 Halma varianti")
        self.BOARD_SIZE = 8
        self.create_menu()
        # Default: Oqlar bilan kompyuterga qarshi
        self.player_color = 1
        self.ai_color = 2
        self.game_mode = "vs_computer"  # options: vs_computer, vs_self, vs_network
        self.setup_board()
        self.draw_game()

    def create_menu(self):
        menubar = tk.Menu(self.master)
        # Tanlash menyusi
        select_menu = tk.Menu(menubar, tearoff=0)
        select_menu.add_command(label="Oqlar bilan o'ynash", command=self.select_white_vs_computer)
        select_menu.add_command(label="Qoralar bilan o'ynash", command=self.select_black_vs_computer)
        select_menu.add_command(label="O'z o'zi bilan o'ynash", command=self.select_self_play)
        select_menu.add_command(label="Kompyuter bilan o'ynash", command=self.select_vs_computer)
        select_menu.add_command(label="Tarmoqda o'ynash", command=self.select_network_play, state="disabled")
        menubar.add_cascade(label="Tanlash", menu=select_menu)
        # O'yin menyusi
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="Yangi o'yin", command=self.restart)
        game_menu.add_separator()
        game_menu.add_command(label="Chiqish", command=self.master.quit)
        menubar.add_cascade(label="O'yin", menu=game_menu)
        # Yordam
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Yordam", command=self.show_help)
        menubar.add_cascade(label="Yordam", menu=help_menu)
        self.master.config(menu=menubar)

    def show_help(self):
        messagebox.showinfo(
            "Yordam",
            "Menyu orqali o'yin turini tanlang.\n"
            "Oq yoki qora donalar bilan o'ynash, yoki kompyuterga qarshi/o'z-o'zi bilan rejimlar mavjud.\n"
            "Donani tanlang, sariq katakka bosing. Agar sakrash mumkin bo‘lsa, barcha sakrashlar bajarilishi majburiy."
        )

    def select_white_vs_computer(self):
        self.player_color = 1
        self.ai_color = 2
        self.game_mode = "vs_computer"
        self.setup_board()
        self.draw_game()

    def select_black_vs_computer(self):
        self.player_color = 2
        self.ai_color = 1
        self.game_mode = "vs_computer"
        self.setup_board()
        self.draw_game()

    def select_self_play(self):
        self.player_color = None
        self.ai_color = None
        self.game_mode = "vs_self"
        self.setup_board()
        self.draw_game()

    def select_vs_computer(self):
        self.player_color = 1
        self.ai_color = 2
        self.game_mode = "vs_computer"
        self.setup_board()
        self.draw_game()

    def select_network_play(self):
        messagebox.showinfo("Tarmoqda o'ynash", "Bu funksiya hozircha yoqilmagan.")

    def setup_board(self):
        self.board = Board(self.BOARD_SIZE)
        # Oqlar/Qoralar tanlanganda joylashishni almashtirish
        if self.game_mode == "vs_computer" and self.player_color == 2:
            # Qora tanlansa: Qoralar o'ng pastki, oqlar chap yuqori
            self.board.clear_pieces()
            for r in range(3):
                for c in range(3):
                    self.board.grid[r][c] = 1  # Oq chap yuqori
            for r in range(self.BOARD_SIZE-3, self.BOARD_SIZE):
                for c in range(self.BOARD_SIZE-3, self.BOARD_SIZE):
                    self.board.grid[r][c] = 2  # Qora o'ng pastki
        elif self.game_mode == "vs_computer" and self.player_color == 1:
            # Oq tanlansa: Oqlar o'ng pastki, qoralar chap yuqori
            self.board.clear_pieces()
            for r in range(3):
                for c in range(3):
                    self.board.grid[r][c] = 2  # Qora chap yuqori
            for r in range(self.BOARD_SIZE-3, self.BOARD_SIZE):
                for c in range(self.BOARD_SIZE-3, self.BOARD_SIZE):
                    self.board.grid[r][c] = 1  # Oq o'ng pastki
        else:
            self.board.setup_pieces()
        self.game = Game(self.board)
        self.selected = None
        self.highlight_moves = []
        self.must_continue_pos = None
        # AI faqat kerak bo'lsa
        if self.game_mode == "vs_computer":
            self.ai = SimpleAI(self.game, self.ai_color)
        else:
            self.ai = None

    def draw_game(self):
        # Eski canvas va status_label ni tozalash
        if hasattr(self, "canvas") and self.canvas is not None:
            self.canvas.pack_forget()
            self.canvas.destroy()
            self.canvas = None
        if hasattr(self, "status_label") and self.status_label is not None:
            self.status_label.pack_forget()
            self.status_label.destroy()
            self.status_label = None

        w = self.BOARD_SIZE*CELL_SIZE+PADDING*2
        h = self.BOARD_SIZE*CELL_SIZE+PADDING*2
        self.canvas = tk.Canvas(self.master, width=w, height=h, bg='bisque')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.status_label = tk.Label(self.master, text=self.get_status_text(), font=('Arial', 12))
        self.status_label.pack()
        self.draw_board()
        # Kompyuter yurishi navbati bo'lsa, avtomatik chaqirish
        if self.game_mode == "vs_computer" and self.game.turn == self.ai_color:
            self.master.after(700, self.make_ai_move)

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

        # O'z o'zi bilan o'ynash rejimi
        if self.game_mode == "vs_self":
            current_color = self.game.turn
            only_jump = self.game.is_jump_forced(current_color)
            if self.selected is None:
                if self.board.get_piece(r, c) == current_color:
                    self.selected = (r, c)
                    # Multi-jumplarni tekshirish
                    multi_jump_paths = self.game.all_multi_jumps(self.selected)
                    if multi_jump_paths:
                        # Faqat multi-jump yo'llarning oxirgi nuqtalarini ko'rsatamiz
                        self.highlight_moves = [path[-1] for path in multi_jump_paths]
                        self.multi_jump_paths = multi_jump_paths
                    else:
                        self.highlight_moves = self.game.all_moves(self.selected, only_jump=only_jump)
                        self.multi_jump_paths = []
                    self.draw_board()
            else:
                src = self.selected
                dst = (r, c)
                # Multi-jump path bor bo'lsa, faqat oxirgi nuqtalarga yurish mumkin
                if hasattr(self, 'multi_jump_paths') and self.multi_jump_paths and dst in [path[-1] for path in self.multi_jump_paths]:
                    # Qaysi path tanlandi
                    for path in self.multi_jump_paths:
                        if path[-1] == dst:
                            cur = path[0]
                            for nxt in path[1:]:
                                self.game.move(cur, nxt)
                                cur = nxt
                            break
                    self.selected = None
                    self.highlight_moves = []
                    self.multi_jump_paths = []
                    self.draw_board()
                    self.status_label.config(text=self.get_status_text())
                    winner = self.game.check_game_over()
                    if winner:
                        messagebox.showinfo("O'yin tugadi!", f"{'Oq' if winner == 1 else 'Qora'} donalar yutdi!")
                        self.restart()
                        return
                elif dst in self.highlight_moves and self.game.valid_move(src, dst, only_jump=only_jump):
                    next_pos = self.game.move(src, dst)
                    if next_pos:
                        self.selected = next_pos
                        # Yangi multi-jumplar tekshiriladi
                        multi_jump_paths = self.game.all_multi_jumps(self.selected)
                        if multi_jump_paths:
                            self.highlight_moves = [path[-1] for path in multi_jump_paths]
                            self.multi_jump_paths = multi_jump_paths
                        else:
                            self.highlight_moves = self.game.all_moves(self.selected, only_jump=True)
                            self.multi_jump_paths = []
                        self.draw_board()
                        self.status_label.config(text=self.get_status_text())
                        winner = self.game.check_game_over()
                        if winner:
                            messagebox.showinfo("O'yin tugadi!", f"{'Oq' if winner == 1 else 'Qora'} donalar yutdi!")
                            self.restart()
                            return
                    else:
                        self.selected = None
                        self.highlight_moves = []
                        self.multi_jump_paths = []
                        self.draw_board()
                        self.status_label.config(text=self.get_status_text())
                        winner = self.game.check_game_over()
                        if winner:
                            messagebox.showinfo("O'yin tugadi!", f"{'Oq' if winner == 1 else 'Qora'} donalar yutdi!")
                            self.restart()
                            return
                else:
                    if self.board.get_piece(r, c) == current_color:
                        self.selected = (r, c)
                        multi_jump_paths = self.game.all_multi_jumps(self.selected)
                        if multi_jump_paths:
                            self.highlight_moves = [path[-1] for path in multi_jump_paths]
                            self.multi_jump_paths = multi_jump_paths
                        else:
                            self.highlight_moves = self.game.all_moves(self.selected, only_jump=only_jump)
                            self.multi_jump_paths = []
                    else:
                        self.selected = None
                        self.highlight_moves = []
                        self.multi_jump_paths = []
                    self.draw_board()

        # Kompyuterga qarshi o'ynash rejimi
        elif self.game_mode == "vs_computer":
            if self.game.turn != self.player_color:
                return
            # Majburiy sakrash davom etyaptimi?
            if self.game.must_continue and self.selected:
                if (r, c) in self.highlight_moves and self.game.valid_move(self.selected, (r, c), only_jump=True):
                    next_pos = self.game.move(self.selected, (r, c))
                    self.selected = next_pos
                    # Multi-jumplarni tekshirish
                    if self.selected:
                        multi_jump_paths = self.game.all_multi_jumps(self.selected)
                        if multi_jump_paths:
                            self.highlight_moves = [path[-1] for path in multi_jump_paths]
                            self.multi_jump_paths = multi_jump_paths
                        else:
                            self.highlight_moves = self.game.all_moves(self.selected, only_jump=True)
                            self.multi_jump_paths = []
                    else:
                        self.highlight_moves = []
                        self.multi_jump_paths = []
                    self.draw_board()
                    self.status_label.config(text=self.get_status_text())
                    winner = self.game.check_game_over()
                    if winner:
                        messagebox.showinfo("O'yin tugadi!", f"{'Oq' if winner == 1 else 'Qora'} donalar yutdi!")
                        self.restart()
                        return
                    if not next_pos:
                        self.selected = None
                        self.highlight_moves = []
                        self.multi_jump_paths = []
                        self.master.after(700, self.make_ai_move)
                else:
                    return
            else:
                only_jump = self.game.is_jump_forced(self.player_color)
                if self.selected is None:
                    if self.board.get_piece(r, c) == self.player_color:
                        self.selected = (r, c)
                        multi_jump_paths = self.game.all_multi_jumps(self.selected)
                        if multi_jump_paths:
                            self.highlight_moves = [path[-1] for path in multi_jump_paths]
                            self.multi_jump_paths = multi_jump_paths
                        else:
                            self.highlight_moves = self.game.all_moves(self.selected, only_jump=only_jump)
                            self.multi_jump_paths = []
                        self.draw_board()
                else:
                    src = self.selected
                    dst = (r, c)
                    if hasattr(self, 'multi_jump_paths') and self.multi_jump_paths and dst in [path[-1] for path in self.multi_jump_paths]:
                        for path in self.multi_jump_paths:
                            if path[-1] == dst:
                                cur = path[0]
                                for nxt in path[1:]:
                                    self.game.move(cur, nxt)
                                    cur = nxt
                                break
                        self.selected = None
                        self.highlight_moves = []
                        self.multi_jump_paths = []
                        self.draw_board()
                        self.status_label.config(text=self.get_status_text())
                        winner = self.game.check_game_over()
                        if winner:
                            messagebox.showinfo("O'yin tugadi!", f"{'Oq' if winner == 1 else 'Qora'} donalar yutdi!")
                            self.restart()
                            return
                        self.master.after(700, self.make_ai_move)
                    elif dst in self.highlight_moves and self.game.valid_move(src, dst, only_jump=only_jump):
                        next_pos = self.game.move(src, dst)
                        if next_pos:
                            self.selected = next_pos
                            multi_jump_paths = self.game.all_multi_jumps(self.selected)
                            if multi_jump_paths:
                                self.highlight_moves = [path[-1] for path in multi_jump_paths]
                                self.multi_jump_paths = multi_jump_paths
                            else:
                                self.highlight_moves = self.game.all_moves(self.selected, only_jump=True)
                                self.multi_jump_paths = []
                            self.draw_board()
                            self.status_label.config(text=self.get_status_text())
                            winner = self.game.check_game_over()
                            if winner:
                                messagebox.showinfo("O'yin tugadi!", f"{'Oq' if winner == 1 else 'Qora'} donalar yutdi!")
                                self.restart()
                                return
                        else:
                            self.selected = None
                            self.highlight_moves = []
                            self.multi_jump_paths = []
                            self.draw_board()
                            self.status_label.config(text=self.get_status_text())
                            winner = self.game.check_game_over()
                            if winner:
                                messagebox.showinfo("O'yin tugadi!", f"{'Oq' if winner == 1 else 'Qora'} donalar yutdi!")
                                self.restart()
                                return
                            self.master.after(700, self.make_ai_move)
                    else:
                        if self.board.get_piece(r, c) == self.player_color:
                            self.selected = (r, c)
                            multi_jump_paths = self.game.all_multi_jumps(self.selected)
                            if multi_jump_paths:
                                self.highlight_moves = [path[-1] for path in multi_jump_paths]
                                self.multi_jump_paths = multi_jump_paths
                            else:
                                self.highlight_moves = self.game.all_moves(self.selected, only_jump=only_jump)
                                self.multi_jump_paths = []
                        else:
                            self.selected = None
                            self.highlight_moves = []
                            self.multi_jump_paths = []
                        self.draw_board()

    def make_ai_move(self):
        if not self.ai or self.game.turn != self.ai_color:
            return
        src, dst = self.ai.get_move()
        if src and dst:
            next_pos = self.game.move(src, dst)
            self.selected = next_pos
            self.highlight_moves = self.game.all_moves(self.selected, only_jump=True) if next_pos else []
            self.draw_board()
            self.status_label.config(text=self.get_status_text())
            winner = self.game.check_game_over()
            if winner:
                messagebox.showinfo("O'yin tugadi!", f"{'Oq' if winner == 1 else 'Qora'} donalar yutdi!")
                self.restart()
                return
            if next_pos:
                self.master.after(500, self.make_ai_move)
            else:
                self.selected = None
                self.highlight_moves = []
        else:
            self.selected = None
            self.highlight_moves = []
            self.draw_board()
            self.status_label.config(text=self.get_status_text())

    def restart(self):
        if hasattr(self, "canvas") and self.canvas is not None:
            self.canvas.pack_forget()
            self.canvas.destroy()
            self.canvas = None
        if hasattr(self, "status_label") and self.status_label is not None:
            self.status_label.pack_forget()
            self.status_label.destroy()
            self.status_label = None
        self.setup_board()
        self.draw_game()

    def get_status_text(self):
        t = self.game.turn
        if self.game_mode == "vs_self":
            who = "Oq" if t == 1 else "Qora"
        elif self.game_mode == "vs_computer":
            who = "Siz (Oq)" if self.player_color == 1 and t == 1 else \
                  "Siz (Qora)" if self.player_color == 2 and t == 2 else \
                  "Kompyuter (Qora)" if self.player_color == 1 else "Kompyuter (Oq)"
        else:
            who = "Navbat"
        return f"Navbat: {who}"