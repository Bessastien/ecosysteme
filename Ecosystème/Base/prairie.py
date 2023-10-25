from Base.param import taille_grille, herbe_minimale, energie_mouton, herbe_depart

class Prairie:
    """
    Classe représentant la prairie.
    """

    def __init__(self) -> None:
        """
        Initialise la prairie avec une grille de taille taille_grille.
        Chaque case de la grille contient initialement 4, représentant la pousse d’herbe.
        """
        self.__grille = [[herbe_depart for i in range(taille_grille)] for j in range(taille_grille)]

    def get_grille(self) -> list:
        """
        :return la grille de la prairie.
        """
        return self.__grille

    def herbe_pousse(self) -> None:
        """
        Incrémente de 1 l’âge de l’herbe à chaque case de la grille,
        sauf si l’herbe a déjà atteint sa durée maximale de repousse (9).
        """
        for i in range(len(self.__grille)):
            for j in range(len(self.__grille[0])):
                if self.__grille[i][j] < 9:
                    self.__grille[i][j] += 1

    def assez_herbe(self, i, j) -> bool:
        """
        :param i Position i de la case.
        :param j Position j de la case.
        Vérifie s’il y a assez d’herbe à la case (i, j) pour qu'un mouton puisse s’y nourrir.
        :return True si l’herbe a un âge supérieur ou égal à herbe_minimale, et False sinon.
        """
        return self.__grille[i][j] >= herbe_minimale

    def mange_herbe(self, i, j) -> int:
        """
        :param i Position i de la case.
        :param j Position j de la case.
        Le mouton mange l’herbe à la case (i, j).
        S’il y a assez d’herbe, l’herbe disparaît et l’énergie du mouton est rechargée.
        :return l’énergie gagnée par le mouton.
        """
        tmp = self.get_grille()[i][j]
        if self.assez_herbe(i, j):
            self.__grille[i][j] = 0
            return tmp
        return 0

    def __str__(self) -> str:
        """
        :return une représentation sous forme de chaîne de caractères de la prairie.
        """
        res = ""
        for i in range(len(self.__grille)):
            res += "\n"
            for j in range(len(self.__grille[0])):
                res += f" {self.__grille[i][j]} "
        return res