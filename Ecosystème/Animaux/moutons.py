import random
from Base.param import energie_mouton, faim_mouton

class Mouton:
    """
    Classe représentant un mouton.
    """

    def __init__(self, i, j) -> None:
        """
        :param i Position i du mouton.
        :param j Position j du mouton.
        Initialise un mouton à la case (i, j) de la prairie, avec une énergie initiale de energie_mouton.
        """
        self.__i = i
        self.__j = j
        self.__energie = energie_mouton

    def get_energie(self) -> int:
        """
        :return l’énergie du mouton
        """
        return self.__energie
    def update_energie(self, up) -> None:
        """
        :param up Valeur à ajouter à l’énergie du mouton.
        Ajoute up à l’énergie du mouton
        """
        self.__energie += up
    def get_i(self) -> int:
        """
        :return la position i du mouton
        """
        return self.__i
    def get_j(self) -> int:
        """
        :return la position j du mouton
        """
        return self.__j

    def est_mort(self) -> bool:
        """
        Vérifie si le mouton est mort.
        :return True si l’énergie du mouton est inférieure ou égale à 0, et False sinon.
        """
        return self.get_energie() <= 0

    def a_faim(self) -> None:
        """
        Diminue l’énergie du mouton de faim_mouton.
        """
        self.update_energie(-faim_mouton)

    def mange(self, prairie) -> None:
        """
        :param prairie Prairie de la simulation.
        Le mouton mange l’herbe à sa position actuelle.
        L’énergie du mouton est rechargée en conséquence.
        """
        self.update_energie(prairie.mange_herbe(self.__i, self.__j))
        if self.get_energie() > 50:
            self.__energie = 50

    def ou_assez_herbe(self, prairie) -> bool:
        """
        :param prairie Prairie de la simulation.
        :return une liste des directions où il y a assez d'herbe pour le mouton.
        """
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        # Vérifie si les directions sont dans la prairie et si il y a assez d'herbe
        directions_final = []
        for direction in directions:
            nouvelle_i = self.__i + direction[0]
            nouvelle_j = self.__j + direction[1]
            if 0 <= nouvelle_i < len(prairie.get_grille()) and 0 <= nouvelle_j < len(
                    prairie.get_grille()[0]) and prairie.assez_herbe(nouvelle_i, nouvelle_j):
                directions_final.append(direction)

        return directions_final

    def deplacement(self, prairie) -> None:
        """
        :param prairie Prairie de la simulation.
        Le mouton se déplace dans une direction aléatoire où il y a assez d'herbe.
        Il ne sort pas de la prairie.
        """

        direction_assez_herbe = self.ou_assez_herbe(prairie)

        if len(direction_assez_herbe) == 0:
            return None
        direction = random.choice(direction_assez_herbe)

        #Calcule la nouvelle position
        nouvelle_i = self.__i + direction[0]
        nouvelle_j = self.__j + direction[1]

        # Vérifie si la nouvelle position est dans les limites de la prairie
        if 0 <= nouvelle_i < len(prairie.get_grille()) and 0 <= nouvelle_j < len(prairie.get_grille()[0]):
            # Mets à jour les coordonnées du mouton
            self.__i = nouvelle_i
            self.__j = nouvelle_j

    def __str__(self) -> str:
        """
        :return une représentation sous forme de chaîne de caractères du mouton.
        """
        return f"Mouton: position = (i={self.__i}, j={self.__j}), energie = {self.get_energie()}"


class Troupeau:
    """
    Classe représentant un troupeau de mouton
    """

    def __init__(self, lst=[]) -> None:
        """
        :param lst Liste de moutons.
        Initialise une liste représentant le troupeau de mouton
        """
        self.__lst = lst
        self.__nombre = len(lst)
        self.__deces = 0
        self.__naissance = 0

    def get_lst(self) -> list:
        """
        :return la liste de moutons
        """
        return self.__lst
    def get_nombre(self) -> int:
        """
        :return le nombre de moutons
        """
        return self.__nombre
    def get_deces(self) -> int:
        """
        :return le nombre de moutons morts
        """
        return self.__deces
    def get_naissance(self) -> int:
        """
        :return le nombre de naissances
        """
        return self.__naissance

    def ajoute_mouton(self, mouton) -> None:
        """
        :param mouton Mouton à ajouter.
        Ajoute un mouton au troupeau.
        """
        self.__lst.append(mouton)
        self.__nombre += 1

    def supprime_mouton(self, mouton) -> None:
        """
        :param mouton Mouton à supprimer.
        Supprime un mouton du troupeau.
        """
        self.__lst.remove(mouton)
        self.__deces += 1
        self.__nombre -= 1

    def equarrisseur(self) -> None:
        """
        Supprime tous les moutons morts du troupeau.
        """
        for mouton in self.get_lst():
            if mouton.est_mort():
                self.supprime_mouton(mouton)

    def reproduction(self) -> None:
        """
        Permets aux moutons du troupeau de se reproduire s’ils se trouvent au même endroit
        et ont suffisamment d’énergie.
        Les deux moutons en question doivent avoir plus de 20 d’énergie et perdent 15 d’énergie.
        """
        for i in range(len(self.get_lst())):
            mouton1 = self.get_lst()[i]
            for j in range(i + 1, len(self.get_lst())):
                mouton2 = self.get_lst()[j]
                if mouton1.get_i() == mouton2.get_i() and mouton1.get_j() == mouton2.get_j() and mouton1.get_energie() > 20 and mouton2.get_energie() > 20:
                    self.__naissance += 1
                    self.ajoute_mouton(Mouton(mouton1.get_i(), mouton1.get_j()))
                    mouton1.update_energie(-15)
                    mouton2.update_energie(-15)

    def __str__(self) -> str:
        """
        :return une représentation sous forme de chaîne de caractères du troupeau de moutons.
        """
        res = (f'Il y a {self.get_nombre()} moutons.\nIl y a {self.get_naissance()} naissances.\nIl y a {self.get_deces()} décès.\nLes '
               f'moutons en question:')
        for i in range(self.get_nombre()):
            res += '\n' + self.get_lst()[i].__str__()
        return res