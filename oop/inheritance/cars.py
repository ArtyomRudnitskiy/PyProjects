import os
import csv


class CarBase:
    def __init__(self, car_type, brand, photo_file_name, carrying):
        extensions = (".jpg", ".jpeg", ".png", ".gif")
        spl_file_name = os.path.splitext(photo_file_name)
        if spl_file_name[1] not in extensions:
            raise AttributeError("Wrong extension")

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


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__("Car", brand, photo_file_name, carrying)
        self._passenger_seats_count = passenger_seats_count


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__("SpecMachine", brand, photo_file_name, carrying)
        self._extra = extra


def get_car_list(csv_filename):
    car_list = []

    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            if row and row[1] and row[3] and row[5]:
                if row[0] == "truck":
                    car_list.append(Truck(row[1], row[3], row[5], row[4]))
                if row[0] == "car" and row[2]:
                    car_list.append(Car(row[1], row[3], row[5], row[2]))
                if row[0] == "spec_machine" and row[6]:
                    car_list.append(SpecMachine(row[1], row[3], row[5], row[6]))

    return car_list


if __name__ == '__main__':
    print(get_car_list("D:\Download Yandex\cars.csv"))
