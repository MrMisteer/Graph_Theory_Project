#récupére les données du tableau de contrainte et de les stock en mémoire
class readfile():
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(self.file_path, 'r')
        self.file_lines = self.file.readlines()
        self.file.close()
