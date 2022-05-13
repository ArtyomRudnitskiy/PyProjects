import os


class CarBase:
    def __init__(self, car_type, brand, photo_file_name, carrying):
        extensions = (".jpg", ".jpeg", ".png", ".gif")
        spl_file_name = os.path.splitext(photo_file_name)
        if spl_file_name[1] not in extensions:
            raise NameError("Wrong extension")

        self._car_type = car_type
        self._brand = brand
        self._photo_file_name = photo_file_name
        self._carrying = carrying
        self._extension = spl_file_name[1]

    def get_photo_file_ext(self):
        return self._extension


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_lwh):
        super().__init__("Truck", brand, photo_file_name, carrying)
        try:
            body_lwh = body_lwh.split("x")
            body_lwh = map(float, body_lwh)
            self._body_length, self._body_width, self._body_height = body_lwh
        except ValueError:
            self._body_length, self._body_width, self._body_height = 0, 0, 0

    def get_body_volume(self):
        return self._body_length * self._body_width * self._body_height


if __name__ == '__main__':
    car = CarBase(1, 2, "dfsdfs.jpeg", 4)
    print(car.get_photo_file_ext())
