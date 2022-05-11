class Pet:
    def __init__(self, name=None):
        self._name = name


class Dog(Pet):
    def __init__(self, name, breed=None):
        super().__init__(name)  # вызываем инициализатор у родителя, по-другому нельзя
        self._breed = breed

    def say(self):
        return "{}: waw".format(self._name)

    def get_breed(self):
        return "{}'s порода - {}".format(self._name, self._breed)


if __name__ == '__main__':
    dog = Dog("Шарик", "Доберман")
    print(dog.say())
    print(dog.get_breed())

