from piece.Piece import Piece

class Board:
    def __init__(self, ia_color='N'):
        self.grid = [[None for _ in range(4)] for _ in range(4)]
        self.moves_without_capture = 0
        self.ia_color = ia_color  # Ajout de l'attribut ia_color

    def display(self):
        for row in self.grid:
            print('|' + '|'.join([' ' if piece is None else str(piece) for piece in row]) + '|')

    def place_piece(self, piece, row, col):
        if 0 <= row < 4 and 0 <= col < 4 and self.grid[row][col] is None and isinstance(piece, Piece):
            self.grid[row][col] = piece
            return True
        return False
    
    def get_piece(self, row, col):
        if 0 <= row < 4 and 0 <= col < 4:
            return self.grid[row][col]
        else:
            return None
        
    def get_present_pieces(self, color):
        pieces = set()
        for row in self.grid:
            for piece in row:
                if piece and piece.color == color:
                    pieces.add(piece.name)
        return pieces

    def move_piece(self, start_row, start_col, end_row, end_col, is_real_move=True):
        if 0 <= start_row < 4 and 0 <= start_col < 4 and 0 <= end_row < 4 and 0 <= end_col < 4:
            moving_piece = self.grid[start_row][start_col]
            target_piece = self.grid[end_row][end_col]

            if moving_piece is not None and (target_piece is None or moving_piece.color != target_piece.color):
                self.grid[end_row][end_col] = moving_piece
                self.grid[start_row][start_col] = None
                    
                if target_piece is None and is_real_move:
                    self.moves_without_capture += 1
                elif target_piece is not None and is_real_move:
                    self.moves_without_capture = 0
                    
                return True
        return False
    
    def copy(self):
        new_board = Board()
        for row in range(4):
            for col in range(4):
                piece = self.get_piece(row, col)
                if piece is not None:
                    # Créer une nouvelle instance de la pièce avec les mêmes attributs
                    copied_piece = type(piece)(piece.color)
                    new_board.place_piece(copied_piece, row, col)
        new_board.moves_without_capture = self.moves_without_capture
        return new_board
    
    def get_all_opponent_moves(self, opponent_color):
        opponent_moves = []
        for row in range(4):
            for col in range(4):
                piece = self.get_piece(row, col)
                if piece and piece.color == opponent_color:
                    moves = piece.get_moves(self, row, col)
                    opponent_moves.extend(moves)
        return opponent_moves
    
    def get_all_possible_moves(self, color):
        """
        Génère tous les mouvements possibles pour le joueur de la couleur spécifiée.
        
        :param color: La couleur du joueur ('B' pour Blanc, 'N' pour Noir)
        :return: Une liste de tous les mouvements possibles. Chaque mouvement est représenté comme un dictionnaire
                 contenant la pièce, la position de départ et la position de fin.
        """
        moves = []
        for row in range(4):
            for col in range(4):
                piece = self.get_piece(row, col)
                if piece and piece.color == color:
                    legal_moves = piece.get_moves(self, row, col)
                    for move in legal_moves:
                        moves.append({
                            'piece': piece,
                            'start_row': row,
                            'start_col': col,
                            'end_row': move[0],
                            'end_col': move[1]
                        })
        return moves
    
    def get_piece_threats(self, piece, row, col, opponent_color):
        saved_piece = self.grid[row][col]

        self.grid[row][col] = None

        threats = piece.get_moves(self, row, col)

        self.grid[row][col] = saved_piece

        valid_threats = []
        for threat_row, threat_col in threats:
            threatened_piece = self.get_piece(threat_row, threat_col)
            if threatened_piece and threatened_piece.color == opponent_color:
                valid_threats.append((threat_row, threat_col))
        
        return valid_threats