from piece.Piece import Piece

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 'Q')  # 'Q' pour Queen
        self.value = 5

    def __str__(self):
        return '\u2655' if self.color == 'B' else '\u265B'

    def get_moves(self, board, row, col):
        moves = []

        # Les directions possibles pour une Dame (combinant Tour et Fou)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

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