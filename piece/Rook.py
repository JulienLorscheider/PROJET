from piece.Piece import Piece

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'T')  # 'T' pour Tour
        self.value = 4

    def __str__(self):
        return '\u2656' if self.color == 'B' else '\u265C'

    def get_moves(self, board, row, col):
        moves = []

        # Les directions possibles pour une Tour (verticalement et horizontalement)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 4 and 0 <= c < 4:
                target = board.get_piece(r, c)
                # Ajouter la position si elle est vide
                if target is None:
                    moves.append((r, c))
                else:
                    # Arrêter si une pièce est rencontrée, mais inclure cette case si c'est une pièce adverse
                    if target.color != self.color:
                        moves.append((r, c))
                    break
                r += dr
                c += dc

        return moves