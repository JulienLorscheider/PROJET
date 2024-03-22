from piece.Piece import Piece

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'C')  # 'C' pour Cavalier
        self.value = 3

    def __str__(self):
        return '\u2658' if self.color == 'B' else '\u265E'

    def get_moves(self, board, row, col):
        # Définition des mouvements possibles du Cavalier en forme de "L"
        potential_moves = [
            (row + 2, col + 1), (row + 2, col - 1),
            (row - 2, col + 1), (row - 2, col - 1),
            (row + 1, col + 2), (row + 1, col - 2),
            (row - 1, col + 2), (row - 1, col - 2)
        ]

        # Filtrer pour ne garder que les mouvements valides (dans les limites du plateau et sans pièces alliées sur la case d'arrivée)
        moves = []
        for r, c in potential_moves:
            if 0 <= r < 4 and 0 <= c < 4:
                target = board.get_piece(r, c)
                if target is None or target.color != self.color:
                    moves.append((r, c))

        return moves