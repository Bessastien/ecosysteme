if str(input('Voulez-vous parametrer votre écosytème ? (Oui ou Non)\n')) == 'Oui':
    nb_mouton = int(input('Avec combien de moutons débute votre écosysteme ?  '))
    nb_loup = int(input('Et combien de loups ? '))

    taille_grille = int(input('Votre prairie fera combien de côté ?  '))
    herbe_depart = int(input("L'herbe de votre prairie sera à combien de hauteur au premier tour ? (Chiffre entre 0 et 9)  "))
    herbe_minimale = int(input("Votre mouton mangera l'herbe à partir de quelle hauteur ? (Chiffre entre 0 et 9)  "))

    energie_mouton = int(input('Vos moutons débuterons avec combien de santé ? (0 = mort et 50 = pleine forme)  '))
    faim_mouton = int(input('Vos moutons ont faim et perdent de la vie à chaque tour, combien ?  '))

    energie_loup = int(input('Vos loups débuterons avec combien de santé ? (0 = mort et 50 = pleine forme)  '))
    faim_loup = int(input('Vos loups ont faim et perdent de la vie à chaque tour, combien ?  '))

else :
    nb_mouton = 30
    nb_loup = 5

    taille_grille = 30
    herbe_depart = herbe_minimale = 4  # Âge minimal de l’herbe pour qu'un mouton puisse la manger (< 9)

    energie_mouton = 5  # Énergie initiale d’un mouton (< 50)
    faim_mouton = 2  # Énergie dépensée par un mouton à chaque tour

    energie_loup = 10  # Énergie initiale d’un loup (< 50)
    faim_loup = 2  # Énergie dépensée par un loup à chaque tour
