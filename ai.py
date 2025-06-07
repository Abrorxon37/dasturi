import random

class SimpleAI:
    def __init__(self, game, color):
        self.game = game
        self.color = color

    def get_move(self):
        # Majburiy sakrash bor bo‘lsa, faqat shuni tanlaydi
        only_jump = self.game.is_jump_forced(self.color)
        candidates = []
        for r in range(self.game.board.size):
            for c in range(self.game.board.size):
                if self.game.board.get_piece(r, c) == self.color:
                    moves = self.game.all_moves((r, c), only_jump=only_jump)
                    for dst in moves:
                        candidates.append(((r, c), dst))
        if not candidates:
            return (None, None)
        return random.choice(candidates)