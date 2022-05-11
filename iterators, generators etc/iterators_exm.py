# пример класса итератора

class HelloWorld:
    def __init__(self, num_iters):
        self.num_iters = num_iters
        self.counter = 0

    # делает объект класса итерируемым, получаем итерируемый объект
    def __iter__(self):
        return self

    # позволяет получать итератор
    def __next__(self):
        if self.counter < self.num_iters:
            self.counter += 1
            return "Hello World!"
        raise StopIteration


if __name__ == '__main__':
    greater = HelloWorld(3)

    for item in greater:
        print(item)

    # аналогично
    # print()
    # for item in HelloWorld(5):
    #    print(item)
