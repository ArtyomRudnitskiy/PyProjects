class FileReader:
    def __init__(self, path: str):
        self.__path = path

    def read(self):
        try:
            with open(self.__path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return ""

