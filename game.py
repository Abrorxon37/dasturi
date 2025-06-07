class Game:
    def __init__(self, board):
        self.board = board
        self.turn = 1  # 1=oq, 2=qora
        self.must_continue = False

    def is_jump_forced(self, color):
        # Bu o'yinda majburiy sakrash yo'q.
        return False

    def switch_turn(self):
        self.turn = 2 if self.turn == 1 else 1

    def valid_move(self, src, dst, only_jump=False):
        r1, c1 = src
        r2, c2 = dst
        if self.board.get_piece(r1, c1) != self.turn or self.board.get_piece(r2, c2) != 0:
            return False
        dr, dc = r2 - r1, c2 - c1

        # Faqat to'g'ri yo'nalishlar (yuqori, past, chap, o'ng) va faqat 1 katakli yurish
        if not only_jump and ((abs(dr) == 1 and dc == 0) or (dr == 0 and abs(dc) == 1)):
            return True

        # Sakrash: faqat to'g'ri yo'nalishda, 2 katak, orada istalgan dona bo'lsa bo'ladi
        if ((abs(dr) == 2 and dc == 0) or (dr == 0 and abs(dc) == 2)):
            mid_r, mid_c = (r1 + r2)//2, (c1 + c2)//2
            mid_piece = self.board.get_piece(mid_r, mid_c)
            if mid_piece != 0:
                return True

        return False

    def all_moves(self, pos, only_jump=False):
        r, c = pos
        moves = []
        # To'g'ri yo'nalishlar: yuqori, past, chap, o'ng
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        for dr, dc in directions:
            # Oddiy yurish
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.board.size and 0 <= nc < self.board.size:
                if self.valid_move((r, c), (nr, nc), only_jump=only_jump):
                    moves.append((nr, nc))
            # Sakrash
            nr2, nc2 = r + 2*dr, c + 2*dc
            if 0 <= nr2 < self.board.size and 0 <= nc2 < self.board.size:
                if self.valid_move((r, c), (nr2, nc2), only_jump=only_jump):
                    moves.append((nr2, nc2))
        return moves

    def all_multi_jumps(self, pos, path=None, visited=None):
        if path is None:
            path = [pos]
        if visited is None:
            visited = set()
        moves = []
        r, c = pos
        found = False
        for dr, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            nr, nc = r + dr, c + dc
            mr, mc = r + dr // 2, c + dc // 2
            if 0 <= nr < self.board.size and 0 <= nc < self.board.size:
                if self.board.get_piece(mr, mc) not in (0, self.board.get_piece(r, c)) and self.board.get_piece(nr, nc) == 0 and ((mr, mc), (nr, nc)) not in visited:
                    found = True
                    new_visited = visited.copy()
                    new_visited.add(((mr, mc), (nr, nc)))
                    for sub in self.all_multi_jumps((nr, nc), path + [(nr, nc)], new_visited):
                        moves.append(sub)
        if not found and len(path) > 1:
            moves.append(path)
        
        print(moves)
        return moves

    def move(self, src, dst):
        r1, c1 = src
        r2, c2 = dst
        self.board.set_piece(r2, c2, self.board.get_piece(r1, c1))
        self.board.set_piece(r1, c1, 0)
        dr, dc = r2 - r1, c2 - c1
        # Sakrash bo‘lsa ham, o‘rtadagi dona olib tashlanmaydi!

        # Ko'p sakrashlar uchun: yana sakrash mumkinmi?
        multi_jumps = self.all_multi_jumps((r2, c2))
        if multi_jumps:
            self.must_continue = True
            return (r2, c2)
        self.must_continue = False
        self.switch_turn()
        return None

    def check_game_over(self):
        size = self.board.size
        """# Oqlar uchun o'ng pastki 3x3
        oq_win = True
        for r in range(size-3, size):
            for c in range(size-3, size):
                if self.board.grid[r][c] != 1:
                    oq_win = False
        if oq_win:
            return 1  # Oqlar yutdi

        # Qoralar uchun chap yuqori 3x3
        qora_win = True
        for r in range(3):
            for c in range(3):
                if self.board.grid[r][c] != 2:
                    qora_win = False
        if qora_win:
            return 2  # Qoralar yutdi"""

        return 0  # O'yin davom etmoqda