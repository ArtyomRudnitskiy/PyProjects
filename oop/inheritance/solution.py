class FileReader:
    def __init__(self, path: str):
        self.__path = path

    def read(self):
        try:
            with open(self.__path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return ""


if __name__ == '__main__':
    reader = FileReader("C:\PyProjects\ex7.txt")
    print(reader.read())
