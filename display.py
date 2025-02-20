import filereader
import graph as graphs
from copy import deepcopy

def Display():
    """Affiche le menu principal permettant de sélectionner et manipuler un graphe."""
    running = True
        
    while running:
        print("\nBienvenue dans notre projet de théorie des graphes !\n")
        print("Choisissez un nombre entre 1 et 14 pour sélectionner un graphe. Pour quitter, tapez 0.")
        
        while True:
            try:
                graph_number = int(input())
                if graph_number == 0:
                    running = False
                    print("Au revoir !")
                    return
                elif graph_number < 1 or graph_number > 14:
                    print("Merci de choisir un nombre entre 1 et 14")
                else:
                    break
            except ValueError:
                print("Merci de choisir un nombre entre 1 et 14 pour sélectionner un graphe")
                
        file = filereader.readfile('tests/table ' + str(graph_number) + '.txt')
        graph = graphs.Graph(file.file_lines)
        check_scheduling = 0

        while True:
            print("\nQue voulez-vous faire ?")
            print("0 - Retour au menu principal")
            print("1 - Afficher le graphe sous forme de lignes")
            print("2 - Afficher la matrice des valeurs")
            print("3 - Vérifier si le graphe est un graphe d'ordonnancement")
            #print("9 - Sauvegarder les résultats dans un fichier")
            if check_scheduling == 1:
                print("4 - Afficher le rang de chaque tâche")
                print("5 - Afficher la date au plus tôt")
                print("6 - Afficher la date au plus tard")
                print("7 - Afficher les marges")
                print("8 - Afficher le chemin critique")

            
            while True: 
                try:
                    choix = int(input("\nChoisissez une option :\n"))  
                    break
                except ValueError:
                    print("Erreur : veuillez entrer un nombre valide.")

            if choix == 0:
                break
            elif choix == 1:
                print("Affichage du graphe sous forme de lignes pour le fichier table "+ str(graph_number))
                graph.print_graph()
            elif choix == 2:
                print("Affichage de la matrice des valeurs")
                graph.print_matrix()
            elif choix == 3:
                print("\nVérification des cycles dans le graphe...\n")
                graph_copy = deepcopy(graph)  # Copie pour éviter de modifier l'original
                cycle = graph_copy.verify_cycle()  # Vérifie l'absence de cycles
    
                print("Le graphe contient-il des valeurs négatives ?\n")
                negative = graph.check_negative_val()  # Vérifie l'absence de valeurs négatives

                if cycle and negative:  # Vérifie que le graphe est bien un graphe d'ordonnancement
                    print("✅ Donc c'est un graphe d'ordonnancement.\n")
                    check_scheduling = 1
                else:
                    print("❌ Donc ce n'est pas un graphe d'ordonnancement.\n")
                    check_scheduling = 0

            elif choix == 9:
                graph.save_results(graph_number) #a activer à la fin pour la sauvegarde 
            
            if check_scheduling != 1:
                print("\nVous ne pouvez pas effectuer d'autres actions sur ce graphe.")
            else:
                if choix == 4:
                    graph_copy = deepcopy(graph)
                    graph_copy.set_rank() # à implémenter
                    for i in range(len(graph_copy.graph)):
                        graph.graph[i].rank = graph_copy.graph[i].rank
                    print("Affichage du rang de chaque tâche")
                    graph.print_rank() # à implémenter

                elif choix == 5:
                    graph.calculate_early_start() # à implémenter
                    print("Affichage de la date au plus tôt")
                    graph.display_early_start() # à implémenter

                elif choix == 6:
                    graph.compute_late_start() # à implémenter
                    print("Affichage de la date au plus tard")
                    graph.display_late_start() # à implémenter

                elif choix == 7:
                    print("Affichage des marges")
                    graph.compute_floats() # à implémenter
                    
                elif choix == 8:
                    print("Affichage du chemin critique")
                    graph.display_critical_path() # à implémenter

                
                

