import os


ERROR_MESSAGE = "Введено некоректне значення. Спробуйте ще раз."


def read_int(message, min_value=1):
    while True:
        try:
            value = int(input(message))

            if value >= min_value:
                return value

            print(ERROR_MESSAGE)
        except ValueError:
            print(ERROR_MESSAGE)


def read_menu_item(message, allowed_items):
    while True:
        choice = input(message)

        if choice in allowed_items:
            return choice

        print("Невірний пункт меню. Спробуйте ще раз.")


def order_header():
    return "{:<5}{:<8}{:<8}{:<8}".format("id", "t_i", "d_i", "w_i")


def order_row(order):
    return "{:<5}{:<8}{:<8}{:<8}".format(order.id, order.t, order.d, order.w)


def result_header():
    return "{:<6}{:<8}{:<8}{:<8}{:<8}{:<8}{:<8}".format(
        "Зам.", "Конт.", "S_i", "C_i", "d_i", "w_i", "U_i"
    )


def result_row(item):
    return "{:<6}{:<8}{:<8}{:<8}{:<8}{:<8}{:<8}".format(
        item.order_id,
        item.truck,
        item.start_time,
        item.completion_time,
        item.deadline,
        item.weight,
        item.late
    )


def print_orders(orders, m):
    if len(orders) == 0:
        print()
        print("Дані задачі ще не задано.")
        return

    print()
    print("Початкові дані задачі:")
    print()
    print("Кількість замовлень n =", len(orders))
    print("Кількість контейнеровозів m =", m)
    print()
    print(order_header())

    for order in orders:
        print(order_row(order))


def print_schedule(schedule):
    for i in range(len(schedule.schedule)):
        print("S" + str(i + 1), "=", schedule.schedule[i])


def print_details(schedule):
    print()
    print("Детальна таблиця:")
    print(result_header())

    sorted_results = sorted(schedule.results, key=lambda item: item.order_id)

    for item in sorted_results:
        print(result_row(item))

    print()
    print("Сумарна вага всіх замовлень:", schedule.total_weight)
    print("Сумарна вага запізнілих замовлень:", schedule.late_weight)
    print("F =", round(schedule.F, 4))
    print("F у відсотках =", round(schedule.F * 100, 2), "%")


def save_results_to_file(schedule, orders, m, file_name):
    if os.path.exists(file_name):
        answer = input("Файл уже існує. Перезаписати? (так/ні): ")

        if answer.lower() != "так":
            return

    file = open(file_name, "w", encoding="utf-8")

    file.write("Початкові дані задачі:\n")
    file.write("n = " + str(len(orders)) + "\n")
    file.write("m = " + str(m) + "\n\n")
    file.write("Замовлення:\n")
    file.write(order_header() + "\n")

    for order in orders:
        file.write(order_row(order) + "\n")

    file.write("\nРезультат алгоритму:\n")
    file.write(schedule.algorithm_name + "\n\n")

    for i in range(len(schedule.schedule)):
        file.write("S" + str(i + 1) + " = " + str(schedule.schedule[i]) + "\n")

    file.write("\nДетальна таблиця:\n")
    file.write(result_header() + "\n")

    sorted_results = sorted(schedule.results, key=lambda item: item.order_id)

    for item in sorted_results:
        file.write(result_row(item) + "\n")

    file.write("\nСумарна вага всіх замовлень: " + str(schedule.total_weight) + "\n")
    file.write("Сумарна вага запізнілих замовлень: " + str(schedule.late_weight) + "\n")
    file.write("F = " + str(round(schedule.F, 4)) + "\n")
    file.write("F у відсотках = " + str(round(schedule.F * 100, 2)) + " %\n")
    file.close()

    print()
    print("Результати успішно записано у файл.")
