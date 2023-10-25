import random
from Base.param import energie_loup, faim_loup
from Animaux.moutons import Mouton

class Loup:
    """
    Classe représentant un loup.
    """

    def __init__(self, i, j) -> None:
        """
        :param i Position i du loup.
        :param j Position j du loup.
        Initialise un loup à la case (i, j) de la prairie, avec une énergie initiale d’energie_loup.
        """
        self.__i = i
        self.__j = j
        self.__energie = energie_loup

    def get_energie(self) -> int:
        """
        Donne l’énergie du mouton
        """
        return self.__energie
    def update_energie(self, up) -> None:
        """
        :param up: Valeur à ajouter à l’énergie du loup.
        Ajoute up à l’énergie du mouton
        """
        self.__energie += up
    def get_i(self) -> int:
        """
        Donne la position i du loup
        """
        return self.__i
    def get_j(self) -> int:
        """
        Donne la position j du loup
        """
        return self.__j

    def est_mort(self) -> bool:
        """
        Vérifie si le loup est mort.
        :return True si l’énergie du loup est inférieure ou égale à 0, et False sinon.
        """
        return self.get_energie() <= 0

    def a_faim(self) -> None:
        """
        Diminue l’énergie du mouton de faim_loup.
        """
        self.update_energie(-faim_loup)

    def mange(self, troupeau) -> None:
        """
        :param troupeau Troupeau de moutons.
        Le loup mange le mouton à sa position actuelle.
        L’énergie du loup augmente de l’énergie qu'avait le mouton.
        Le mouton meurt.
        """
        for mouton in troupeau.get_lst():
            if self.get_i() == mouton.get_i() and self.get_j() == mouton.get_j():
                self.update_energie(mouton.get_energie())
                troupeau.supprime_mouton(mouton)

        if self.get_energie() > 50:
            self.__energie = 50

    def avec_autre_loup(self, horde) -> bool:
        """
        :param horde Horde de loups.
        Vérifie si le loup est sur la même case qu'un autre loup.
        :return True si le loup est sur la même case qu'un autre loup, et False sinon.
        """
        cmp = 0
        for loup in horde.get_lst():
            if self.get_i() == loup.get_i() and self.get_j() == loup.get_j():
                cmp += 1
                if cmp > 1:
                    return True
        return False

    def mouton_plus_proche(self, troupeau) -> Mouton or None:
        """
        :param troupeau Troupeau de moutons.
        :return le mouton le plus proche du loup.
        """
        # Calcule la distance entre le loup et le mouton le plus proche
        lst_distance = []
        for mouton in troupeau.get_lst():
            # ajoute à la liste lst_distance un tuple contenant en premier un mouton et en deuxième sa "distance" avec le loup
            lst_distance.append((mouton, abs(mouton.get_i() - self.get_i()) + abs(mouton.get_j() - self.get_j())))

        # trie la liste lst_distance par rapport à la distance entre le loup et le mouton
        for i in range(len(lst_distance)):
            min_index = i
            for j in range(i + 1, len(lst_distance)):
                if lst_distance[j][1] < lst_distance[min_index][1]:
                    min_index = j

            lst_distance[i], lst_distance[min_index] = lst_distance[min_index], lst_distance[i]

        if len(lst_distance) == 0:
             return None

        return lst_distance[0][0]

    def aller_vers_mouton_plus_proche(self, mouton_plus_proche) -> tuple:
        """
        :param mouton_plus_proche: Mouton le plus proche du loup.
        :return la direction vers laquelle le loup doit aller pour se rapprocher du mouton le plus proche.
        """
        # Le loup choisit si il va en haut, en bas, à gauche ou à droite selon la position du mouton le plus proche
        # Se déplace à la verticale
        if abs(self.get_i() - mouton_plus_proche.get_i()) > abs(self.get_j() - mouton_plus_proche.get_j()):
            # Se déplace en haut ou en bas
            if self.get_i() - mouton_plus_proche.get_i() > 0:
                direction = (-1, 0)
            else:
                direction = (1, 0)
        # se déplace à l’horizontale
        else:
            # Se déplace à gauche ou à droite
            if self.get_j() - mouton_plus_proche.get_j() > 0:
                direction = (0, -1)
            else:
                direction = (0, 1)

        return direction

    def deplacement(self, prairie, troupeau, horde) -> None:
        """
        :param prairie: Prairie.
        :param troupeau: Troupeau de moutons.
        :param horde: Horde de loups.
        Le loup se déplace vers le mouton le plus proche de lui.
        Il peut se déplacer sur les quatres cases autours de lui.
        Il ne sort pas de la prairie.
        """
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        mouton_plus_proche = self.mouton_plus_proche(troupeau)

        #Evite que le loup se déplace sur une case avec un autre loup et qu'ils se reproduisent en boucle
        #Evite aussi que le loup essaye de se deplacer s’il n’y a pas de mouton
        if self.avec_autre_loup(horde) or mouton_plus_proche is None:
            direction = random.choice(directions)

        else :
            # direction vers le mouton le plus proche
            direction = self.aller_vers_mouton_plus_proche(mouton_plus_proche)

        # Calcule la nouvelle position
        nouvelle_i = self.__i + direction[0]
        nouvelle_j = self.__j + direction[1]

        # Vérifie si la nouvelle position est dans les limites de la prairie
        if 0 <= nouvelle_i < len(prairie.get_grille()) and 0 <= nouvelle_j < len(prairie.get_grille()[0]):
            # Mets à jour les coordonnées du mouton
            self.__i = nouvelle_i
            self.__j = nouvelle_j

    def __str__(self) -> str:
        """
        :return une représentation sous forme de chaîne de caractères du loup.
        """
        return f"Loup: position = (i={self.get_i()}, j={self.get_j()}), énergie = {self.get_energie()}"

class Horde:
    """
    Classe représentant une horde de loups.
    """

    def __init__(self, lst=[]) -> None:
        """
        :param lst Liste de loups.
        Initialise une liste représentant la horde de loups.
        """
        self.__lst = lst
        self.__nombre = len(lst)
        self.__deces = 0
        self.__naissance = 0

    def get_lst(self) -> list:
        """
        :return la liste de loups.
        """
        return self.__lst
    def get_nombre(self) -> int:
        """
        :return le nombre de loups.
        """
        return self.__nombre
    def get_deces(self) -> int:
        """
        :return le nombre de loups morts.
        """
        return self.__deces
    def get_naissance(self) -> int:
        """
        :return le nombre de loups nés.
        """
        return self.__naissance

    def ajoute_loup(self, loup) -> None:
        """
        :param loup: Loup à ajouter.
        Ajoute un loup à la horde.
        """
        self.__lst.append(loup)
        self.__nombre += 1

    def supprime_loup(self, loup) -> None:
        """
        :param loup: Loup à supprimer.
        Supprime un loup de la horde.
        """
        self.__lst.remove(loup)
        self.__deces += 1
        self.__nombre -= 1

    def equarrisseur(self) -> None:
        """
        Supprime tous les loups morts de la horde.
        """
        for loup in self.get_lst():
            if loup.est_mort():
                self.supprime_loup(loup)

    def reproduction(self) -> None:
        """
        Permets aux loups de la horde de se reproduire s’ils se trouvent au même endroit
        et ont suffisamment d’énergie.
        Les deux loups en question doivent avoir plus de 20 d’énergie et perdent 15 d’énergie.
        """
        for i in range(len(self.get_lst())):
            loup1 = self.get_lst()[i]
            for j in range(i + 1, len(self.get_lst())):
                loup2 = self.get_lst()[j]
                if loup1.get_i() == loup2.get_i() and loup1.get_j() == loup2.get_j() and loup1.get_energie() > 20 and loup2.get_energie() > 20:
                    self.__naissance += 1
                    self.ajoute_loup(Loup(loup1.get_i(), loup1.get_j()))
                    loup1.update_energie(-15)
                    loup2.update_energie(-15)

    def __str__(self) -> str:
        """
        :return une représentation sous forme de chaîne de caractères de la horde de loups.
        """
        res = f'il y a {self.get_nombre()} loups. \nIl y a {self.get_naissance()} naissances. \nIl y a {self.get_deces()} décès. \nLes loups en question :'
        for i in range(self.get_nombre()):
            res += '\n' + self.get_lst()[i].__str__()
        return res