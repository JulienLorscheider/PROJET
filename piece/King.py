from piece.Piece import Piece

class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'K')  # 'K' pour King

    def __str__(self):
        return '\u2654' if self.color == 'B' else '\u265A'
    
    def is_position_under_direct_threat(self, board, row, col, color):
        directions = {
            'line': [(0, 1), (0, -1), (1, 0), (-1, 0)],
            'diagonal': [(1, 1), (1, -1), (-1, 1), (-1, -1)],
            'knight': [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        }
        
        # Check line and diagonal threats (from queens, rooks, bishops)
        for mode in ['line', 'diagonal']:
            for dx, dy in directions[mode]:
                x, y = row + dx, col + dy
                while 0 <= x < 4 and 0 <= y < 4:
                    piece = board.get_piece(x, y)
                    if piece:
                        if piece.color != color and ((mode == 'line' and piece.name in ['Q', 'T']) or
                                                    (mode == 'diagonal' and piece.name in ['Q', 'F'])):
                            return True
                        break
                    x += dx
                    y += dy
        
        # Check knight threats
        for dx, dy in directions['knight']:
            x, y = row + dx, col + dy
            if 0 <= x < 4 and 0 <= y < 4:
                piece = board.get_piece(x, y)
                if piece and piece.color != color and piece.name == 'C':
                    return True

        # Check pawn threats
        pawn_directions = [-1, 1] if color == 'B' else [1, -1]
        for dy in pawn_directions:
            for dx in [-1, 1]:
                x, y = row + dx, col + dy
                if 0 <= x < 4 and 0 <= y < 4:
                    piece = board.get_piece(x, y)
                    if piece and piece.color != color and piece.name == 'P':
                        return True

        return False
    
    def is_king_too_close(self, board, row, col, color):
        # Vérifie toutes les cases autour de la position pour un autre roi
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1), (0, 0)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 4 and 0 <= c < 4:
                piece = board.get_piece(r, c)
                if piece and piece.name == 'K' and piece.color != color:
                    return True
        return False

    def get_moves(self, board, row, col):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 4 and 0 <= c < 4:
                if not self.is_position_under_direct_threat(board, r, c, self.color) and not self.is_king_too_close(board, r, c, self.color):
                    target = board.get_piece(r, c)
                    if target is None or target.color != self.color:
                        moves.append((r, c))

        return moves