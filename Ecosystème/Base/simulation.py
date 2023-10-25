import random
import time
import colorama
colorama.init()

from Base.param import taille_grille, herbe_minimale
from Base.prairie import Prairie
from Animaux.moutons import Troupeau, Mouton
from Animaux.loups import Horde, Loup



class Simulation:
    """
    Classe représentant une simulation de moutons et de loups dans une prairie.
    """

    def __init__(self, nb_mouton, nb_loup) -> None:
        """
        :param nb_mouton: Nombre initial de moutons.
        :param nb_loup: Nombre initial de loups.
        Initialise la simulation avec un nombre initial de moutons et de loups.
        """
        self.__nb_mouton = nb_mouton
        self.__p = Prairie()

        # Créer le troupeau
        self.__troupeau = Troupeau()
        for i in range(nb_mouton):
            self.__troupeau.ajoute_mouton(Mouton(random.randint(0, len(self.__p.get_grille()) - 1), random.randint(0, len(self.__p.get_grille()) - 1)))

        # Créer la horde
        self.__horde = Horde()
        for i in range(nb_loup):
            self.__horde.ajoute_loup(Loup(random.randint(0, len(self.__p.get_grille()) - 1), random.randint(0, len(self.__p.get_grille()) - 1)))

        self.__tour = 0

    def get_nb_mouton(self) -> int:
        """
        :return le nombre de moutons dans la simulation.
        """
        return self.__nb_mouton

    def get_tour(self) -> int:
        """
        :return le nombre de tours écoulés dans la simulation.
        """
        return self.__tour

    def affichage(self) -> None:
        """
        :return une représentation sous forme de chaîne de caractères de la prairie et ce qu'il se passe dedans.
        """

        # refait une grille temporaire
        nouvelle_grille = [[4 for i in range(taille_grille)] for j in range(taille_grille)]
        for i in range(len(self.__p.get_grille())):
            for j in range(len(self.__p.get_grille())):
                if self.__p.get_grille()[i][j] <= herbe_minimale:
                    nouvelle_grille[i][j] = colorama.Back.YELLOW + f' {self.__p.get_grille()[i][j]} ' + colorama.Style.RESET_ALL
                else:
                    nouvelle_grille[i][j] = (colorama.Back.GREEN + f' {self.__p.get_grille()[i][j]} ' + colorama.Style.RESET_ALL)

        # Mets les moutons dans la grille
        for mouton in self.__troupeau.get_lst():
            nouvelle_grille[mouton.get_i()][mouton.get_j()] = colorama.Back.WHITE + ' M ' + colorama.Style.RESET_ALL

        # Mets-les loup dans la grille
        for loup in self.__horde.get_lst():
            nouvelle_grille[loup.get_i()][loup.get_j()] = colorama.Back.RED + ' L ' + colorama.Style.RESET_ALL

        # Affiche la grille
        res = "\n" * 50 + f'Tours: {self.__tour}'
        for i in range(len(nouvelle_grille)):
            res += "\n"
            for j in range(len(nouvelle_grille[i])):
                res += f"{nouvelle_grille[i][j]}"
        res += f'\n\nIl y a {self.__troupeau.get_nombre()} moutons, {self.__troupeau.get_naissance()} naissances, {self.__troupeau.get_deces()} décès.\nIl y a {self.__horde.get_nombre()} Loup,  {self.__horde.get_naissance()} naissances, {self.__horde.get_deces()} décès.'

        return print(res)

    def un_tour(self) -> None:
        """
        Effectue un tour de simulation.
        """

        self.affichage()

        self.__tour += 1
        self.__p.herbe_pousse()

        for mouton in self.__troupeau.get_lst():
            mouton.a_faim()
            mouton.deplacement(self.__p)
            mouton.mange(self.__p)
        self.__troupeau.equarrisseur()
        self.__troupeau.reproduction()

        for loup in self.__horde.get_lst():
            loup.a_faim()
            loup.deplacement(self.__p,self.__troupeau,self.__horde)
            loup.mange(self.__troupeau)
        self.__horde.equarrisseur()
        self.__horde.reproduction()

    def partie(self) -> None:
        """
        Commence la simulation et continue les tours jusqu’à ce qu'il ne reste plus de moutons et de loups.
        """

        while self.__troupeau.get_nombre() > 0 and self.__horde.get_nombre() > 0 :
            self.un_tour()
            time.sleep(1)
        self.affichage()