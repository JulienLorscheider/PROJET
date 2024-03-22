from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, color, name):
        self.color = color  # Couleur de la pièce (par exemple, 'B' pour blanc, 'N' pour noir)
        self.name = name    # Nom ou abréviation de la pièce (par exemple, 'P' pour Pion)

    @abstractmethod
    def get_moves(self, board, row, col):
        """
        Méthode abstraite pour obtenir les mouvements possibles de cette pièce.
        
        :param board: L'instance du plateau de jeu (Board).
        :param row: La ligne actuelle de la pièce.
        :param col: La colonne actuelle de la pièce.
        :return: Une liste de tuples représentant les mouvements possibles (ligne, colonne).
        """
        pass