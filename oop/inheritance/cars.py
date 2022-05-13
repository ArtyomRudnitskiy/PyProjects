class CarBase:
    def __init__(self, car_type, photo_file_name, brand,  carrying):

        extensions = ("jpg", "jpeg", "png", "gif")
        spl_file_name = photo_file_name.split(".")
        if spl_file_name[-1] not in extensions:
            raise NameError("Wrong extension")

        self._car_type = car_type
        self.photo_file_name = photo_file_name
        self.brand = brand
        self.carrying = carrying


if __name__ == '__main__':
    car = CarBase(1, "123.jpeg", 3, 4)
