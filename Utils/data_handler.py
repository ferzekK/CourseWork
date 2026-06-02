import os
import random

from Models.models import Order
from Utils.utils import read_int


DATA_FILE_NAME = "data.txt"


def load_data_manual():
    n = read_int("Введіть кількість замовлень n: ")
    m = read_int("Введіть кількість контейнеровозів m: ")

    orders = []

    for i in range(1, n + 1):
        print()
        print("Замовлення", i)
        t = read_int("Введіть t_i: ")
        d = read_int("Введіть d_i: ")
        w = read_int("Введіть w_i: ")
        orders.append(Order(i, t, d, w))

    if validate_data(orders, m):
        print()
        print("Нові дані задачі збережено успішно!")
        return orders, m

    print("Дані містять помилку. Перевірте їх та повторіть спробу.")
    return [], 0


def generate_random_data():
    n = read_int("Введіть кількість замовлень n: ")
    m = read_int("Введіть кількість контейнеровозів m: ")

    orders = generate_orders(n, 42)

    file_name = input("Введіть назву файлу для запису згенерованих даних: ")

    if file_name == "":
        file_name = DATA_FILE_NAME

    saved = save_data_to_file(orders, m, file_name)

    print()
    print("Нові дані задачі згенеровано успішно!")

    if saved:
        print("Згенеровані дані записано у файл", file_name)
    else:
        print("Згенеровані дані не записано у файл.")

    return orders, m


def generate_orders(n, seed):
    random.seed(seed)
    orders = []

    for i in range(1, n + 1):
        t = random.randint(2, 20)
        w = random.randint(1, 20)
        d = random.randint(t + 2, t * 5 + 20)
        orders.append(Order(i, t, d, w))

    return orders


def load_data_from_file(filename=""):
    if filename == "":
        filename = input("Введіть шлях до файлу, з якого буде зчитано дані: ")

    try:
        file = open(filename, "r", encoding="utf-8")
        lines = file.readlines()
        file.close()

        first_line = lines[0].split()
        n = int(first_line[0])
        m = int(first_line[1])

        if len(lines) < n + 1:
            print("Файл має неправильну структуру.")
            return [], 0

        orders = []

        for i in range(1, n + 1):
            parts = lines[i].split()

            if len(parts) == 4:
                order_id = int(parts[0])
                t = int(parts[1])
                d = int(parts[2])
                w = int(parts[3])
            elif len(parts) == 3:
                order_id = i
                t = int(parts[0])
                d = int(parts[1])
                w = int(parts[2])
            else:
                print("Файл має неправильну структуру.")
                return [], 0

            orders.append(Order(order_id, t, d, w))

        if validate_data(orders, m):
            print()
            print("Нові дані задачі збережено успішно!")
            return orders, m

        print("Файл має неправильну структуру.")
        return [], 0
    except FileNotFoundError:
        print()
        print("Файл не знайдено.")
        return [], 0
    except:
        print()
        print("При зчитуванні виникла помилка. Перевірте файл та повторіть спробу.")
        return [], 0


def save_data_to_file(orders, m, filename):
    if os.path.exists(filename):
        answer = input("Файл уже існує. Перезаписати? (так/ні): ")

        if answer.lower() != "так":
            return False

    file = open(filename, "w", encoding="utf-8")
    file.write(str(len(orders)) + " " + str(m) + "\n")

    for order in orders:
        line = str(order.id) + " " + str(order.t) + " " + str(order.d) + " " + str(order.w) + "\n"
        file.write(line)

    file.close()
    return True


def validate_data(orders, m):
    if len(orders) <= 0 or m <= 0:
        return False

    for order in orders:
        if order.id <= 0 or order.t <= 0 or order.d <= 0 or order.w <= 0:
            return False

    return True
