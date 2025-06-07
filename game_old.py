from board import BOARD_SIZE

class Game:
    def __init__(self, board):
        self.board = board
        self.turn = 1  # 1 - oq, 2 - qora
        self.must_continue = False  # Ko‘p martalik sakrash davom etyaptimi?
        self.selected = None        # Faqat shu dona bilan yurish mumkinmi?

    def switch_turn(self):
        self.turn = 2 if self.turn == 1 else 1

    def valid_move(self, src, dst):
        sr, sc = src
        dr, dc = dst
        if self.board.get_piece(sr, sc) != self.turn or self.board.get_piece(dr, dc) != 0:
            return False

        # Agar sakrash zanjiri bo'lsa, faqat selected dona yurishi mumkin
        if self.must_continue and src != self.selected:
            return False

        dir = -1 if self.turn == 1 else 1
        delta_r = dr - sr
        delta_c = dc - sc

        # Oddiy yurish: oldinga, chapga, o'ngga bitta katak
        if (delta_r, delta_c) in [(dir, 0), (0, 1), (0, -1)]:
            if self.must_continue:
                return False
            return True

        # Sakrash: oldinga, chapga, o‘ngga 2 katak
        # Oldinga
        if (delta_r, delta_c) == (2*dir, 0):
            mid_r = sr + dir
            mid_c = sc
            mid_piece = self.board.get_piece(mid_r, mid_c)
            if mid_piece != 0 and self.board.get_piece(dr, dc) == 0:
                return True
        # Chapga
        if (delta_r, delta_c) == (0, -2):
            mid_r = sr
            mid_c = sc - 1
            if 0 <= mid_c < BOARD_SIZE:
                mid_piece = self.board.get_piece(sr, mid_c)
                if mid_piece != 0 and self.board.get_piece(dr, dc) == 0:
                    return True
        # O‘ngga
        if (delta_r, delta_c) == (0, 2):
            mid_r = sr
            mid_c = sc + 1
            if 0 <= mid_c < BOARD_SIZE:
                mid_piece = self.board.get_piece(sr, mid_c)
                if mid_piece != 0 and self.board.get_piece(dr, dc) == 0:
                    return True
        return False

    def can_jump(self, pos):
        """Berilgan dona yana sakrashi mumkinmi?"""
        r, c = pos
        dir = -1 if self.turn == 1 else 1
        # Oldinga
        if 0 <= r + 2*dir < BOARD_SIZE:
            mid = self.board.get_piece(r + dir, c)
            dst = self.board.get_piece(r + 2*dir, c)
            if mid != 0 and dst == 0:
                return True
        # Chapga
        if 0 <= c - 2 < BOARD_SIZE:
            mid = self.board.get_piece(r, c - 1)
            dst = self.board.get_piece(r, c - 2)
            if mid != 0 and dst == 0:
                return True
        # O‘ngga
        if 0 <= c + 2 < BOARD_SIZE:
            mid = self.board.get_piece(r, c + 1)
            dst = self.board.get_piece(r, c + 2)
            if mid != 0 and dst == 0:
                return True
        return False

    def move(self, src, dst):
        sr, sc = src
        dr, dc = dst
        if not self.valid_move(src, dst):
            return False

        delta_r = dr - sr
        delta_c = dc - sc

        self.board.set_piece(dr, dc, self.turn)
        self.board.set_piece(sr, sc, 0)
        self.must_continue = False
        self.selected = None
        self.switch_turn()
        return True

    def get_possible_jumps(self, pos):
        """Berilgan donaning barcha sakrash variantlari"""
        r, c = pos
        dir = -1 if self.turn == 1 else 1
        jumps = []
        # Oldinga
        if 0 <= r + 2*dir < BOARD_SIZE:
            mid = self.board.get_piece(r + dir, c)
            dst = self.board.get_piece(r + 2*dir, c)
            if mid != 0 and dst == 0:
                jumps.append((r + 2*dir, c))
        # Chapga
        if 0 <= c - 2 < BOARD_SIZE:
            mid = self.board.get_piece(r, c - 1)
            dst = self.board.get_piece(r, c - 2)
            if mid != 0 and dst == 0:
                jumps.append((r, c - 2))
        # O‘ngga
        if 0 <= c + 2 < BOARD_SIZE:
            mid = self.board.get_piece(r, c + 1)
            dst = self.board.get_piece(r, c + 2)
            if mid != 0 and dst == 0:
                jumps.append((r, c + 2))
        return jumps
