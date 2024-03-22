from piece.Piece import Piece

class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'K')  # 'K' pour King

    def __str__(self):
        return '\u2654' if self.color == 'B' else '\u265A'

    def get_moves(self, board, row, col):
        moves = []

        # Les directions possibles pour un Roi (incluant horizontales, verticales et diagonales)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 4 and 0 <= c < 4:
                target = board.get_piece(r, c)
                # Ajouter la position si elle est vide ou occupée par une pièce adverse
                if target is None or target.color != self.color:
                    moves.append((r, c))

        return moves