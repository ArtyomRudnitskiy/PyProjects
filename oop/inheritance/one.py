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
    def __init__(self, name, breed=None):
        # вызов по MRO, вызывает метод первого в списке
        super().__init__(name, breed)
        #super(ExDog, self).__init__(name)


class WoolenDog(Dog, ExportJSON):
    def __init__(self, name, breed=None):
        # явное указание, от кого наследуем метод
        super(Dog, self).__init__(name)
        self._breed = "Шерстяная собака породы {}".format(breed)


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
    print(eDog.to_json(), end="\n\n")

    print("Порядок наследования для ExDog (MRO): " + str(ExDog.__mro__), end="\n\n")

    wDog = WoolenDog("Жучка", "Такса")
    print(wDog.get_breed())

