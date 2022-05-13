import os
import csv


class CarBase:
    def __init__(self, car_type, brand, photo_file_name, carrying):
        self._car_type = car_type
        self._brand = brand
        self._photo_file_name = photo_file_name
        self._carrying = carrying
        self._extension = os.path.splitext(photo_file_name)[1]

    def get_photo_file_ext(self):
        return self._extension

    def __str__(self):
        return f"Type: {self._car_type}   Brand: {self._brand}   Photo: {self._photo_file_name}   Carrying: {self._carrying}"


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
    extensions = (".jpg", ".jpeg", ".png", ".gif")

    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            if row and row[1] and row[3] and row[5]:

                spl_file_name = os.path.splitext(row[3])
                if spl_file_name[1] not in extensions:
                    continue

                try:
                    carrying = float(row[5])
                except ValueError:
                    continue

                if row[0] == "truck":
                    car_list.append(Truck(row[1], row[3], carrying, row[4]))
                if row[0] == "car" and row[2]:
                    try:
                        passengers = float(row[2])
                    except ValueError:
                        continue
                    car_list.append(Car(row[1], row[3], carrying, passengers))
                if row[0] == "spec_machine" and row[6]:
                    car_list.append(SpecMachine(row[1], row[3], carrying, row[6]))

    return car_list


if __name__ == '__main__':
    cars = get_car_list("D:\Download Yandex\cars.csv")
    for i in cars:
        print(i)

