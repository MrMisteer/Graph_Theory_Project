class Task(): # représentation d'une tâche dans le graphe
    def __init__(self, name, out_link=0):
        self.name = name
        self.duration = {name: 0}  # dictionnaire stockant les prédecesseurs de notre tâche et la durée du prédecesseur
        self.dependencies = []  # liste qui stocke les prédecesseurs
        self.children = []  # liste qui stocke les sucesseurs
        self.out_link = int(out_link)  # durée de la tâche (indiquée dans le fichier d'entrée)
        self.rank = 0  # rang de la tâche (pour l'ordonnancement)
        self.early_date = 0  # date au plus tôt de la tâche (servira pour après)
        self.late_date = 0  # date au plus tard de la tâche (servira pour après)

    def set_dependencies(self, dependencie): # méthode qui permet d'ajouter les prédécesseurs dans la liste dependencies
        self.dependencies.append(dependencie)  

class Graph:
    def __init__(self, lines):
        self.lines = lines
        self.graph = [] # liste d'objets "Task", représentant les tâches du graphe
        self.create_graph()

    # assigne les valeurs des liens entre les tâches en fonction des dépendances
    def set_link_value(self, task):
        if not task.dependencies:  # si aucune dépendance, la durée depuis α vers notre tâche est 0
            task.duration['0'] = 0
        else:
            for dependencie in task.dependencies: # parcours les tâches dont dépend notre tâche actuelle (les prédecesseurs)
                task.duration[dependencie.name] = dependencie.out_link # associe dans notre dictionnaire la durée de la tâche prédécesseur

    def create_graph(self):
        entry_node = Task('0', 0)  # Sommet α
        self.graph.append(entry_node) #ajoute le sommet 0 (α)

        # Création des tâches
        for line in self.lines: #parcous les lignes du fichier txt
            line_read = line.split() # découpe la ligne en morceaux (indice 0 = nom, indice 1 = durée etc)
            if any(task.name == line_read[0] for task in self.graph):
                continue # évite d'ajouter deux fois la même tâche
            task_obj = Task(line_read[0], line_read[1]) # création de la tâche avec nom (indice 0) + durée (indice 1)
            self.graph.append(task_obj)
            if len(line_read) == 2: #si ya que deux chiffres dans la ligne alors pas de prédecesseurs donc α (0) sera notre prédecesseur
                task_obj.set_dependencies(entry_node)

        # Ajout des dépendances
        for line in self.lines:
            line_read = line.split()
            current_task = next(task for task in self.graph if task.name == line_read[0]) #Parcourt les tâches
            task_read = [int(element) for element in line_read[2:]] # Récupère les prédécesseurs de notre tâche actuelle

            
            # Associe chaque tâche prédécesseur à la tâche actuelle
            for i in task_read: # Parcourt chaque tâche prédécesseur
                for task in self.graph: # Parcourt toutes les tâches du graphe
                    if task.name == str(i): # Cherche la tâche correspondant au prédécesseur
                        current_task.set_dependencies(task) # Ajoute la dépendance
                        break
            self.set_link_value(current_task) # Met à jour les durées des liens entre les tâches

        # Ajout du sommet final ω
        exit_nodes = [node for node in self.graph if not any(node in task.dependencies for task in self.graph)]
        exit_task = Task(str(len(self.graph)), 0)  # Sommet ω (N+1) comme on part de 0 on a pas besoin de faire +1 
        for node in exit_nodes:
            exit_task.set_dependencies(node)
            exit_task.duration[node.name] = node.out_link
        self.graph.append(exit_task)

    def print_graph(self): #choix 1 dans le menu
        for task in self.graph:
            for dependencie in task.dependencies:
                print(dependencie.name, '->', task.name, "=", task.duration[dependencie.name]) # affiche les relations entre tâches sous la forme prédecesseurs -> tâche actuelle = durée prédécesseur

    def print_matrix(self): #choix 2 dans le menu
        print("\nMatrice des valeurs du graphe :")

        # Calcul de la largeur max des colonnes
        max_length = max(len(str(task.name)) for task in self.graph)

        # Affichage de l'en-tête
        header_format = "{:>" + str(max_length) + "}"
        print(header_format.format(""), end=" ")
        for task in self.graph:
            print(header_format.format(task.name), end=" ")
        print()

        # Affichage de la matrice
        for task in self.graph:
            print(header_format.format(task.name), end=" ")
            for target in self.graph:
                if task in target.dependencies:
                    print(header_format.format(target.duration[task.name]), end=" ")
                else:
                    print(header_format.format("-"), end=" ")  # - au lieu de 0 pour par confondre avec la durée du sommet alpha
            print()


    def verify_cycle(self):
        graph_copy = self.graph.copy()  # copie du graphe pour ne pas modifier l'original

        while True:
            entry_nodes = [node for node in graph_copy if not node.dependencies]  # liste qui stocke les tâches sans prédecesseurs
            
            for node in entry_nodes: #boucle qui parcout les tâches sans prédecesseurs 
                graph_copy.remove(node)  #supprime la tâche sans prédecesseur du graphe
                
                for task in graph_copy: #boucle qui supprime les dépendances de notre tâche sans prédecesseurs
                    if node in task.dependencies:
                        task.dependencies.remove(node) 

            if not entry_nodes:  #si plus aucun noeud d'entrée (donc plus de tâches sans prédecesseurs)
                if graph_copy:  #si graphe_copy n'est pas vide => il reste des tâches non supprimées => cycle détecté
                    print("--> Le graphe contient un cycle\n")
                    return False
                print("--> Le graphe ne contient pas de cycle\n")
                return True
            

    def check_negative_val(self):
        for task in self.graph:
            for dependencie in task.dependencies:
                if task.duration[dependencie.name] < 0:
                    print(f"--> Oui, le graphe contient une valeure négative : Tache {task.name} -> {dependencie.name} = {task.duration[dependencie.name]}\n")
                    return False  
        print("--> Non, le graphe ne contient aucune valeure négative\n")
        return True









    #sauvegarde les traces dans un nouveau fichier txt (ne marche pas : donne pas la bonne matrice)
    """def save_results(self, graph_number):
        #Sauvegarde la matrice et les résultats des calculs dans un fichier .txt
        file_name = f"results_table_{graph_number}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(f"Résultats pour le fichier table {graph_number}.txt\n\n")

            f.write("Matrice des valeurs du graphe :\n")
            max_length = max(len(str(task.name)) for task in self.graph)
            header_format = "{:>" + str(max_length) + "}"
            headers = " ".join(header_format.format(task.name) for task in self.graph)
            f.write(" " + headers + "\n")
            for task in self.graph:
                row = " ".join(header_format.format(task.duration.get(target.name, "-")) for target in self.graph)
                f.write(f"{header_format.format(task.name)} {row}\n")
            f.write("\n")

            f.write("Chemin critique :\n")
            self.display_critical_path(f)

            f.write("\nDates au plus tôt :\n")
            self.display_early_start(f)

            f.write("\nDates au plus tard :\n")
            self.display_late_start(f)

            f.write("\nMarges :\n")
            self.compute_floats(f)

        print(f"Les résultats ont été sauvegardés dans {file_name}")"""

