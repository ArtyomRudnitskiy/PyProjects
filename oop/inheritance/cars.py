import os
import csv


class CarBase:
    def __init__(self, car_type, brand, photo_file_name, carrying):
        self.car_type = car_type
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying
        self.extension = os.path.splitext(photo_file_name)[1]

    def get_photo_file_ext(self):
        return self.extension

    def __str__(self):
        return f"Type: {self.car_type}   Brand: {self.brand}   Photo: {self.photo_file_name}   Carrying: {self.carrying}"


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_lwh):
        super().__init__("Truck", brand, photo_file_name, carrying)
        try:
            body_lwh = body_lwh.split("x")
            body_lwh = map(float, body_lwh)
            self.body_length, self.body_width, self.body_height = body_lwh
        except ValueError:
            self.body_length, self.body_width, self.body_height = 0, 0, 0

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__("Car", brand, photo_file_name, carrying)
        self.passenger_seats_count = passenger_seats_count


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__("SpecMachine", brand, photo_file_name, carrying)
        self.extra = extra


def get_car_list(csv_filename):
    car_list = []
    extensions = (".jpg", ".jpeg", ".png", ".gif")

    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        for row in reader:
            if row and row[1] and row[3] and row[5]:

                spl_file_name = os.path.splitext(row[3])  # проверяем валидность расширения
                if spl_file_name[1] not in extensions:
                    continue

                if not row[5].isdigit():  # проверяем валидность пассажиров
                    continue

                if row[0] == "truck":
                    car_list.append(Truck(row[1], row[3], row[5], row[4]))

                if row[0] == "car" and row[2]:
                    if not row[2].isdigit():  # проверяем валидность пассажиров
                        continue
                    car_list.append(Car(row[1], row[3], row[5], row[2]))

                if row[0] == "spec_machine" and row[6]:
                    car_list.append(SpecMachine(row[1], row[3], row[5], row[6]))
    return car_list

if __name__ == '__main__':
    cars = get_car_list("D:\Download Yandex\cars.csv")
    for i in cars:
        print(i)