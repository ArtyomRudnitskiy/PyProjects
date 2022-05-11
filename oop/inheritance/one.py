# цепочка наследования: Pet -> Dog -> Cat
import json


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


class Cat(Dog):
    def __init__(self, name, breed=None):
        super().__init__(name, breed)

    def say(self):
        return "{}: meow".format(self._name)


class ExportJSON:
    def to_json(self):
        return json.dumps({
            "name": self._name,
            "breed": self._breed
        }
        )


# примесный класс
class ExDog(Dog, ExportJSON):
    pass


if __name__ == '__main__':
    dog = Dog("Шарик", "Доберман")
    print(dog.say())
    print(dog.get_breed())

    print()

    cat = Cat("Муся", "Сиамская")
    print(cat.say())
    print(cat.get_breed())

    print()

    eDog = ExDog("Белка", breed="Дворняжка")
    print(eDog.to_json())
