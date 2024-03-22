from piece.Piece import Piece

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'P')  # 'P' pour Pion
        self.value = 1

    def __str__(self):
        return '\u2659' if self.color == 'B' else '\u265F'

    def get_moves(self, board, row, col):
        moves = []
        directions = [1, -1] if self.color == 'B' else [-1, 1]  # Avant et arrière pour chaque couleur

        for direction in directions:
            next_row = row + direction
            if 0 <= next_row < 4 and board.get_piece(next_row, col) is None:
                moves.append((next_row, col))

        for direction in directions:
            for dcol in [-1, 1]:  # Diagonale gauche et droite
                next_row, next_col = row + direction, col + dcol
                if 0 <= next_row < 4 and 0 <= next_col < 4:
                    target = board.get_piece(next_row, next_col)
                    if target is not None and target.color != self.color:
                        moves.append((next_row, next_col))

        return moves