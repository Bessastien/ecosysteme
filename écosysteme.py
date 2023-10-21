import random
import time
import colorama
colorama.init()


# Variables de paramètres
taille_grille = 30
herbe_depart = 4 # < 9

energie_mouton = 4 # < 50
faim_mouton = 3

energie_loup = 40 # < 50
faim_loup = 1

taux_reproduction = 1


class Prairie:
    """
    Classe représentant la prairie.
    """

    def __init__(self):
        """
        Initialise la prairie avec une grille de taille taille_grille.
        Chaque case de la grille contient initialement 4, représentant la pousse d'herbe.
        """
        self.grille = [[4 for i in range(taille_grille)] for j in range(taille_grille)]

    def herbe_pousse(self):
        """
        Incrémente de 1 l'âge de l'herbe à chaque case de la grille,
        sauf si l'herbe a déjà atteint sa durée maximale de repousse (9).
        """
        for i in range(len(self.grille)):
            for j in range(len(self.grille[0])):
                if self.grille[i][j] < 9:
                    self.grille[i][j] += 1

    def assez_herbe(self, i, j):
        """
        Vérifie si il y a assez d'herbe à la case (i, j) pour qu'un mouton puisse s'y nourrir.
        Retourne True si l'herbe a un âge supérieur ou égal à herbe_depart, et False sinon.
        """
        return self.grille[i][j] >= herbe_depart

    def mange_herbe(self, i, j):
        """
        Le mouton mange l'herbe à la case (i, j).
        Si il y a assez d'herbe, l'herbe disparaît et l'énergie du mouton est rechargée.
        Retourne l'énergie gagnée par le mouton.
        """
        if self.assez_herbe(i, j):
            self.grille[i][j] = 0
            return energie_mouton
        return 0

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères de la prairie.
        """
        res = ""
        for i in range(len(self.grille)):
            res += "\n"
            res += "|"
            for j in range(len(self.grille[0])):
                res += f"{self.grille[i][j]}"
                res += "|"
        return res


class Mouton:
    """
    Classe représentant un mouton.
    """

    def __init__(self, i, j):
        """
        Initialise un mouton à la case (i, j) de la prairie, avec une énergie initiale de energie_mouton.
        """
        self.i = i
        self.j = j
        self.energie = energie_mouton

    def est_mort(self):
        """
        Vérifie si le mouton est mort.
        Retourne True si l'énergie du mouton est inférieure ou égale à 0, et False sinon.
        """
        return self.energie <= 0

    def a_faim(self):
        """
        Diminue l'énergie du mouton de faim_mouton.
        """
        self.energie -= faim_mouton

    def mange(self, prairie):
        """
        Le mouton mange l'herbe à sa position actuelle.
        L'énergie du mouton est rechargée en conséquence.
        """
        self.energie += prairie.mange_herbe(self.i, self.j)
        if self.energie > 50:
            self.energie = 50

    def deplacement(self, prairie):
        """
        Le mouton se déplace aléatoirement dans une des 8 cases autour de lui.
        Il ne sort pas de la prairie.
        """
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        direction = random.choice(directions)

        nouvelle_i = self.i + direction[0]
        nouvelle_j = self.j + direction[1]

        # Vérifie si la nouvelle position est dans les limites de la prairie
        if 0 <= nouvelle_i < len(prairie.grille) and 0 <= nouvelle_j < len(prairie.grille[0]):
            # Mets à jour les coordonnées du mouton
            self.i = nouvelle_i
            self.j = nouvelle_j


    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères du mouton.
        """
        return f"Mouton: position = (i={self.i}, j={self.j}), energie = {self.energie}"
    
class Troupeau:
    """
    Classe representant un troupeau de mouton
    """
    def __init__(self, lst=[]):
        """
        Initialise une liste representant le troupeau de mouton
        :type lst: liste
        """
        self.lst = lst
        self.nombre = len(lst)
        self.décès = 0
        self.naissance = 0
        
    def ajoute_mouton(self, mouton):
        """
        Ajoute un mouton, on doit donner ses caracteristiques en parametre
        """
        self.lst.append(mouton)
        self.nombre += 1
        
    def supprime_mouton(self, mouton):
        """
        Supprime le mouton donné en parametre
        """
        self.lst.remove(mouton)
        self.décès += 1
        self.nombre -= 1
        
    def equarrisseur(self):
        """
        Supprime tous les mouton morts
        """
        for mouton in self.lst :
            if mouton.est_mort():
                self.supprime_mouton(mouton)
                
                
    def reproduction(self):
        """
        Si deux mouton sont au même endroit ils procréent.
        Les deux mouotn en question doivent avoir plus de 20 d'énergie et perdent 15 d'énergie.
        """
        for i in range(len(self.lst)):
            mouton1 = self.lst[i]
            for j in range(i + 1, len(self.lst)):
                mouton2 = self.lst[j]
                if mouton1.i == mouton2.i and mouton1.j == mouton2.j and mouton1.energie > 20 and mouton2.energie > 20:
                    self.naissance += 1
                    self.ajoute_mouton(Mouton(mouton1.i,mouton1.j))
                    mouton1.energie -= 15
                    mouton2.energie -= 15
                    
    
    def __str__(self):
        res = f'il y a {self.nombre} moutons. \nIl y a {self.naissance} naissances. \nIl y a {self.décès} décès. \nLes moutons en question :'
        for i in range(self.nombre):
            res += '\n' + self.lst[i].__str__()
        return res


class Loup:
    def __init__(self, i, j):
        """
        Initialise un loup à la case (i, j) de la prairie, avec une énergie initiale de energie_loup.
        """
        self.i = i
        self.j = j
        self.energie = energie_loup

    def est_mort(self):
        """
        Vérifie si le loup est mort.
        Retourne True si l'énergie du loup est inférieure ou égale à 0, et False sinon.
        """
        return self.energie <= 0

    def a_faim(self):
        """
        Diminue l'énergie du mouton de faim_loup.
        """
        self.energie -= faim_loup

    def mange(self, troupeau):
        """
        Le loup mange le mouton à sa position actuelle.
        L'énergie du loup augmente de l'energie qu'avait le mouton.
        Le mouton meurt.
        """
        for mouton in troupeau.lst :
            if self.i == mouton.i and self.j == mouton.j:
                self.energie += mouton.energie
                troupeau.supprime_mouton(mouton)

        if self.energie > 50:
            self.energie = 50

    def deplacement(self, prairie):
        """
        Le loup se déplace aléatoirement dans une des 8 cases autour de lui.
        Il ne sort pas de la prairie.
        """
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        direction = random.choice(directions)

        nouvelle_i = self.i + direction[0]
        nouvelle_j = self.j + direction[1]

        # Vérifie si la nouvelle position est dans les limites de la prairie
        if 0 <= nouvelle_i < len(prairie.grille) and 0 <= nouvelle_j < len(prairie.grille[0]):
            # Mets à jour les coordonnées du loup
            self.i = nouvelle_i
            self.j = nouvelle_j

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères du loup.
        """
        return f"Loup: position = (i={self.i}, j={self.j}), energie = {self.energie}"


class Horde:
    def __init__(self, lst=[]):
        """
        Initialise une liste representant la horde de loup
        :type lst: liste
        """
        self.lst = lst
        self.nombre = len(lst)
        self.décès = 0
        self.naissance = 0

    def ajoute_loup(self, loup):
        """
        Ajoute un loup, on doit donner ses caracteristiques en parametre
        """
        self.lst.append(loup)
        self.nombre += 1

    def supprime_loup(self, loup):
        """
        Supprime le loup donné en parametre
        """
        self.lst.remove(loup)
        self.décès += 1
        self.nombre -= 1

    def equarrisseur(self):
        """
        Supprime tous les loup morts
        """
        for loup in self.lst:
            if loup.est_mort():
                self.supprime_loup(loup)

    def reproduction(self):
        """
        Si deux loups sont au même endroit ils procréent.
        Les deux loups en question doivent avoir plus de 20 d'énergie et perdent 15 d'énergie.
        """
        for i in range(len(self.lst)):
            loup1 = self.lst[i]
            for j in range(i + 1, len(self.lst)):
                loup2 = self.lst[j]
                if loup1.i == loup2.i and loup1.j == loup2.j and loup1.energie > 20 and loup2.energie > 20:
                    self.naissance += 1
                    self.ajoute_loup(Loup(loup1.i, loup1.j))
                    loup1.energie -= 15
                    loup2.energie -= 15

    def __str__(self):
        res = f'il y a {self.nombre} loups. \nIl y a {self.naissance} naissances. \nIl y a {self.décès} décès. \nLes loups en question :'
        for i in range(self.nombre):
            res += '\n' + self.lst[i].__str__()
        return res



class Simulation:
    def __init__(self, nb_mouton, nb_loup):
        self.nb_mouton = nb_mouton
        
        self.p = Prairie()
        
        #creer le troupeau
        self.troupeau = Troupeau()
        for i in range(nb_mouton):
            self.troupeau.ajoute_mouton(Mouton(random.randint(0,len(self.p.grille)-1),random.randint(0,len(self.p.grille)-1)))

        #creer la horde
        self.horde = Horde()
        for i in range(nb_loup):
            self.horde.ajoute_loup(Loup(random.randint(0,len(self.p.grille)-1),random.randint(0,len(self.p.grille)-1)))
        
        self.tour = 0
        
    def get_nb_mouton(self):
        return self.nb_mouton
    
    def get_tour(self):
        return self.tour
    
    def affichage(self):
        """
        Retourne une représentation sous forme de chaîne de caractères de la prairie et ce qu'il se passe dedans.
        """
        
        #refait une grille temporaire
        nouvelle_grille = [[4 for i in range(taille_grille)] for j in range(taille_grille)]
        for i in range(len(self.p.grille)):
            for j in range(len(self.p.grille)):
                if self.p.grille[i][j] <= 4 :
                    nouvelle_grille[i][j] = colorama.Back.YELLOW + f' {self.p.grille[i][j]} ' + colorama.Style.RESET_ALL
                else :
                    nouvelle_grille[i][j] = colorama.Back.GREEN + f' {self.p.grille[i][j]} ' + colorama.Style.RESET_ALL
                
        #Mets les moutons dans la grille
        for mouton in self.troupeau.lst:
            nouvelle_grille[mouton.i][mouton.j] = colorama.Back.WHITE + ' M ' + colorama.Style.RESET_ALL

        #Mets les loup dans la grille
        for loup in self.horde.lst:
            nouvelle_grille[loup.i][loup.j] = colorama.Back.RED + ' L ' + colorama.Style.RESET_ALL
            
        #Affiche la grille
        res = "\n"*50
        for i in range(len(nouvelle_grille)):
            res += "\n"
            for j in range(len(nouvelle_grille[i])):
                res += f"{nouvelle_grille[i][j]}"
        res += f'\n\nIl y a {self.troupeau.nombre} moutons, {self.troupeau.naissance} naissances, {self.troupeau.décès} décès.\nIl y a {self.horde.nombre} Loup,  {self.horde.naissance} naissances, {self.horde.décès} décès.'
        return print(res)
    
    def un_tour(self):
        
        self.tour += 1
        self.p.herbe_pousse()
        
        for mouton in self.troupeau.lst:
            mouton.a_faim()
            mouton.mange(self.p)
            mouton.deplacement(self.p)
        self.troupeau.equarrisseur()
        self.troupeau.reproduction()

        for loup in self.horde.lst:
            loup.a_faim()
            loup.mange(self.troupeau)
            loup.deplacement(self.p)
        self.horde.equarrisseur()
        self.horde.reproduction()
        
        self.affichage()
        
    def partie(self):
        
        while len(self.troupeau.lst) >= 0:
            self.un_tour()
            time.sleep(0.2)



s = Simulation(30,5)
s.partie()
