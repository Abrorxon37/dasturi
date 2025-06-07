class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.setup_pieces()

    def setup_pieces(self):
        for r in range(self.size):
            for c in range(self.size):
                self.grid[r][c] = 0
        # Qora chap yuqori 3x3
        for r in range(3):
            for c in range(3):
                self.grid[r][c] = 2
        # Oq o‘ng pastki 3x3
        for r in range(self.size-3, self.size):
            for c in range(self.size-3, self.size):
                self.grid[r][c] = 1

    def clear_pieces(self):
        for r in range(self.size):
            for c in range(self.size):
                self.grid[r][c] = 0

    def get_piece(self, r, c):
        return self.grid[r][c]

    def set_piece(self, r, c, value):
        self.grid[r][c] = value