import sys
sys.path.append('./board')
sys.path.append('./piece')

import Board
import Rook
import Queen
import King
import Bishop
import Pawn
import Knight

def choose_game_variant():
    print("Choisissez une variante de jeu :")
    print("1. Reine - Tour - Fou - Cavalier")
    print("2. Tour - Fou - Cavalier - Reine-Pion")
    print("3. Tour - Fou - Cavalier - Reine-Roi")
    
    while True:
        choice = input("Entrez le numéro de votre choix (1, 2, ou 3) : ")
        if choice in ['1', '2', '3']:
            return int(choice)
        else:
            print("Choix invalide. Veuillez entrer 1, 2, ou 3.")

variant = choose_game_variant()

def player_turn(board, variant):
    print("Votre tour.")

    present_pieces = board.get_present_pieces('B')  # Supposons que 'B' représente le joueur humain

    if variant == 1:
        options = "".join([p for p in ['Q', 'T', 'F', 'C'] if p in present_pieces])
    elif variant == 2:
        options = "".join([p for p in ['T', 'F', 'C', 'P'] if p in present_pieces])
    elif variant == 3:
        options = "".join([p for p in ['T', 'F', 'C', 'K'] if p in present_pieces])
    
    print(f"Choisissez une pièce à déplacer ({options}): ")

    while True:
        piece_choice = input().strip().upper()

        if piece_choice not in present_pieces:
            print("Pièce non valide ou non présente sur le plateau. Veuillez choisir une pièce valide.")
            continue  # Demander à nouveau

        start_row, start_col = get_valid_coords("Entrez la position actuelle de la pièce (format: ligne,colonne): ")

        end_row, end_col = get_valid_coords("Entrez la nouvelle position de la pièce (format: ligne,colonne): ")

        piece = board.get_piece(start_row, start_col)
        if piece and piece.name == piece_choice and (end_row, end_col) in piece.get_moves(board, start_row, start_col):
            board.move_piece(start_row, start_col, end_row, end_col)
            print("Mouvement effectué.")
            break
        else:
            print("Mouvement invalide. Veuillez essayer à nouveau.")

    board.display()

def is_piece_threatened(board, row, col, color):
    opponent_color = 'N' if color == 'B' else 'B'
    for move in board.get_all_possible_moves(opponent_color):
        if move['end_row'] == row and move['end_col'] == col:
            return True
    return False

def evaluate_threats_and_protections(board):
    threats_and_protections = {
        'N': {'threatened': [], 'protected': [], 'threatened_protected': [], 'safe_captures': [], 'risky_captures': []},
        'B': {'threatened': [], 'protected': [], 'threatened_protected': [], 'safe_captures': [], 'risky_captures': []}
    }

    for row in range(4):
        for col in range(4):
            piece = board.get_piece(row, col)
            if not piece:
                continue
            
            # Check for threats and protections
            for move in piece.get_moves(board, row, col):
                target_row, target_col = move
                target_piece = board.get_piece(target_row, target_col)
                if target_piece and target_piece.color != piece.color:
                    if target_piece not in threats_and_protections[target_piece.color]['protected']:
                        threats_and_protections[target_piece.color]['threatened'].append(target_piece)
                    else:
                        if target_piece not in threats_and_protections[target_piece.color]['threatened_protected']:
                            threats_and_protections[target_piece.color]['threatened_protected'].append(target_piece)
                elif target_piece and target_piece.color == piece.color:
                    threats_and_protections[piece.color]['protected'].append(target_piece)

    for row in range(4):
        for col in range(4):
            piece = board.get_piece(row, col)
            if not piece:
                continue
            
            potential_moves = piece.get_moves(board, row, col)
            for move in potential_moves:
                target_row, target_col = move
                target_piece = board.get_piece(target_row, target_col)
                if not target_piece:
                    continue
                if target_piece.color != piece.color:
                    # Vérifie si la pièce attaquante serait menacée après avoir effectué la capture
                    board_copy = board.copy()
                    board_copy.move_piece(row, col, target_row, target_col)
                    if is_piece_threatened(board_copy, target_row, target_col, target_piece.color):
                        # Si la pièce serait menacée, c'est une capture risquée
                        threats_and_protections[piece.color]['risky_captures'].append(target_piece)
                    else:
                        # Sinon, c'est une capture sans risque
                        threats_and_protections[piece.color]['safe_captures'].append(target_piece)

    return threats_and_protections

def evaluate_board(board, maximizing_player):
    piece_value = {'P': 1, 'C': 3, 'F': 3, 'T': 5, 'Q': 9, 'K': 1000}

    # Paramètres d'évaluation
    threat_penalty = 10  # Pénalité pour une pièce menacée
    protection_bonus = 3  # Bonus pour une pièce protégée
    threatened_protected_bonus = 2  # Bonus pour une pièce menacée mais protégée

    safe_capture_bonus = 10
    risky_capture_penalty = 10

    # Récupération des menaces et protections
    tp_info = evaluate_threats_and_protections(board)

    king_safety_penalty = 100
    black_score, white_score = 0, 0
    friend_proximity_bonus = 5
    pawn_cover_bonus = 10
    mobility_weight = 0.1

    for row in range(4):
        for col in range(4):
            piece = board.get_piece(row, col)
            if not piece:
                continue

            if piece:
                moves = piece.get_moves(board, row, col)
                mobility_score = len(moves) * mobility_weight

                if piece.color == 'N':  # Noir
                    black_score += piece_value[piece.name] + mobility_score
                else:  # Blanc
                    white_score += piece_value[piece.name] + mobility_score

            # Base score
            base_score = piece_value[piece.name]
            color_multiplier = 1 if piece.color == 'N' else -1# Ajustements pour les menaces et protections
            
            if piece in tp_info[piece.color]['threatened']:
                base_score -= threat_penalty
            if piece in tp_info[piece.color]['protected']:
                base_score += protection_bonus
            if piece in tp_info[piece.color]['threatened_protected']:
                base_score += threatened_protected_bonus
            if piece in tp_info[piece.color]['safe_captures']:
                base_score += safe_capture_bonus
            if piece in tp_info[piece.color]['risky_captures']:
                base_score -= risky_capture_penalty

            # Adjust score for proximity of friendly pieces
            for drow in [-1, 0, 1]:
                for dcol in [-1, 0, 1]:
                    if drow == 0 and dcol == 0:
                        continue  # Skip the piece itself
                    adj_row, adj_col = row + drow, col + dcol
                    if 0 <= adj_row < 4 and 0 <= adj_col < 4:
                        adj_piece = board.get_piece(adj_row, adj_col)
                        if adj_piece and adj_piece.color == piece.color:
                            base_score += friend_proximity_bonus

            # King specific checks
            if isinstance(piece, King.King):
                if is_in_check((row, col), board):
                    base_score -= king_safety_penalty

                # Pawn cover bonus
                for cover_row in [row + 1, row - 1]:  # Forward and backward for king
                    for cover_col in [col - 1, col, col + 1]:
                        if 0 <= cover_row < 4 and 0 <= cover_col < 4:
                            cover_piece = board.get_piece(cover_row, cover_col)
                            if isinstance(cover_piece, Pawn.Pawn) and cover_piece.color == piece.color:
                                base_score += pawn_cover_bonus

            # Add to total score
            if piece.color == 'N':
                black_score += base_score * color_multiplier
            else:
                white_score += base_score * color_multiplier

    # Final score adjustment
    if maximizing_player:
        return black_score - white_score if board.ia_color == 'N' else white_score - black_score
    else:
        return white_score - black_score if board.ia_color == 'N' else black_score - white_score

def alpha_beta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or game_over(board, variant, is_simulation=True):
        return evaluate_board(board, maximizing_player)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.get_all_possible_moves('N'):  # Supposons que 'N' représente l'IA
            board_copy = board.copy()
            board_copy.move_piece(move['start_row'], move['start_col'], move['end_row'], move['end_col'], is_real_move=False)
            eval = alpha_beta(board_copy, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.get_all_possible_moves('B'):  # Supposons que 'B' représente le joueur humain
            board_copy = board.copy()
            board_copy.move_piece(move['start_row'], move['start_col'], move['end_row'], move['end_col'], is_real_move=False)
            eval = alpha_beta(board_copy, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def ai_turn(board):
    best_move = None
    capture_move = None
    best_value = float('-inf')
    for move in board.get_all_possible_moves('N'):  # 'N' pour l'IA
        board_copy = board.copy()
        board_copy.move_piece(move['start_row'], move['start_col'], move['end_row'], move['end_col'], is_real_move=False)
        move_value = alpha_beta(board_copy, 3, float('-inf'), float('inf'), False)
        if move_value > best_value:
            best_value = move_value
            best_move = move

    if capture_move:  # Si un mouvement de capture est disponible, l'exécuter
        best_move = capture_move

    if best_move:
        board.move_piece(best_move['start_row'], best_move['start_col'], best_move['end_row'], best_move['end_col'])
        print("L'IA a effectué son mouvement.")
    
    board.display()


def game_over(board, variant, is_simulation=False):
    white_pieces = []
    black_pieces = []
    for row in range(4):
        for col in range(4):
            piece = board.get_piece(row, col)
            if piece:
                if piece.color == 'N':
                    black_pieces.append(piece)
                else:
                    white_pieces.append(piece)

    if not white_pieces or not black_pieces:
        if not is_simulation:  # Ne pas afficher le message en mode simulation
            winner = 'Noir' if not white_pieces else 'Blanc'
            print(f"Fin de la partie. {winner} gagne par capture de toutes les pièces.")
        return True

    # Conditions spécifiques à chaque variante
    if (variant == 1 or variant == 2) and board.moves_without_capture >= 5:
        # Calculer la somme des valeurs des pièces restantes pour chaque joueur
        white_value = sum(piece.value for piece in white_pieces)
        black_value = sum(piece.value for piece in black_pieces)

        if(white_value == black_value):
            print(f"Fin de la partie après 5 mouvements sans prise. Égalité entre Blanc et Noir.")
            return True

        winner = 'Blanc' if white_value > black_value else 'Noir'
        print(f"Fin de la partie après 5 mouvements sans prise. {winner} gagne avec la plus haute valeur de pièces.")
        return True
    elif variant == 3:
        for row in range(4):
            for col in range(4):
                piece = board.get_piece(row, col)
                if piece and piece.name == 'K':
                    king_position = (row, col)
                    king = piece

        in_check = is_in_check(king_position, board)
        legal_moves = has_legal_moves(board, king, king_position)

        if in_check and not legal_moves:
            print(f"Échec et mat. {'Blanc' if king.color == 'N' else 'Noir'} perd.")
            return True
        elif not in_check and not legal_moves:
            print("Pat. Match nul.")
            return True

    # Aucune condition de fin de jeu n'est remplie
    return False

def evaluate_placement_advanced(board, piece, row, col):
    score = 0

    # Sauvegarde de la pièce originale (peut être None si aucun pièce n'est présente)
    original_piece = board.get_piece(row, col)

    # Placer temporairement la pièce pour évaluation
    board.place_piece(piece, row, col)

    # Notre logique d'évaluation ici
    center_positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
    if (row, col) in center_positions:
        score += 2

    for move in board.get_all_opponent_moves("B"):
        if move == (row, col):
            score -= 3

    offensive_potential = len(board.get_piece_threats(piece, row, col, "B"))
    score += offensive_potential

    # Restaurer la pièce originale après évaluation
    board.grid[row][col] = original_piece

    return score

def initial_piece_placement_ai(board, piece):
    best_score = float('-inf')
    best_move = None
    for row in range(4):
        for col in range(4):
            if board.grid[row][col] is None:
                score = evaluate_placement_advanced(board, piece, row, col)
                if score >= best_score:
                    best_score = score
                    best_move = (row, col)

    if best_move:
        board.place_piece(piece, best_move[0], best_move[1])

def initial_piece_placement(board, variant):
    piece_classes = {'Q': Queen.Queen, 'T': Rook.Rook, 'F': Bishop.Bishop, 'C': Knight.Knight, 'P': Pawn.Pawn, 'K': King.King}
    pieces = {'1': ['Q', 'T', 'F', 'C'],
              '2': ['T', 'F', 'C', 'P'],
              '3': ['T', 'F', 'C', 'K']}

    for piece_symbol in pieces[str(variant)]:
        valid_placement = False
        while not valid_placement:
            board.display()
            row, col = get_valid_coords(f"Où souhaitez-vous placer votre {piece_symbol}? (format: ligne,colonne de 0 à 3): ")
            piece_class = piece_classes[piece_symbol]
            pieceB = piece_class('B')
            pieceN = piece_class('N')
            if board.place_piece(pieceB, row, col):
                valid_placement = True
            else:
                print("Placement invalide, veuillez réessayer.")
        initial_piece_placement_ai(board, pieceN)


def is_in_check(king_position, board):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]  # Directions pour lignes, colonnes, diagonales
    for direction in directions:
        if is_path_clear(king_position, direction, board):
            return True
    return False

def is_path_clear(king_position, direction, board):
    dx, dy = direction
    x, y = king_position
    while 0 <= x < 4 and 0 <= y < 4:
        x += dx
        y += dy
        if 0 <= x < 4 and 0 <= y < 4:
            piece = board.get_piece(x, y)
            if piece is not None:
                if piece.color != board.ia_color and (is_threatening_piece(piece, direction)):
                    return True
                break
    return False

def get_valid_coords(prompt, max_row=3, max_col=3):
    while True:
        user_input = input(prompt)
        try:
            row, col = map(int, user_input.split(','))
            if 0 <= row <= max_row and 0 <= col <= max_col:
                return row, col
            else:
                print(f"Coordonnées hors limites. Veuillez entrer des valeurs entre 0 et {max_row} pour les lignes et entre 0 et {max_col} pour les colonnes.")
        except ValueError:
            print("Format invalide. Veuillez utiliser le format ligne,colonne (par exemple, '1,2').")

def is_threatening_piece(piece, direction):
    # Convertit la direction en vecteur unitaire pour comparaison
    unit_direction = (direction[0] // max(abs(direction[0]), 1), direction[1] // max(abs(direction[1]), 1))

    # Pour les Fous, vérifie si la direction est diagonale
    if isinstance(piece, Bishop.Bishop) and unit_direction in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
        return True

    # Pour les Tours, vérifie si la direction est verticale ou horizontale
    elif isinstance(piece, Rook.Rook) and unit_direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        return True

    # Pour les Dames, vérifie si la direction est verticale, horizontale ou diagonale
    elif isinstance(piece, Queen.Queen) and unit_direction in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
        return True

    # Pour les Cavaliers, vérifie si la direction correspond à un mouvement en L
    # Note: Cette vérification est plus complexe car les Cavaliers sautent
    elif isinstance(piece, Knight.Knight):
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        return direction in knight_moves

    return False

def has_legal_moves(board, king, king_position):
    for move in king.get_moves(board, *king_position):
        if move not in board.get_all_opponent_moves(king.color):
            return True
    return False

def play_game(variant):
    board = Board.Board(ia_color='N')
    player_turn_v = True

    initial_piece_placement(board, variant)
    board.display()

    while not game_over(board, variant):
        if player_turn_v:
            player_turn(board, variant)
        else:
            ai_turn(board)
        
        player_turn_v = not player_turn_v

play_game(variant)