import Base.simulation as s
from Base.param import nb_loup, nb_mouton

def main() -> None:
    """
    Fonction principale du programme.
    """
    set = s.Simulation(nb_mouton, nb_loup)
    set.partie()


if __name__ == "__main__":
    main()

