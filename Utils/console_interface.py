from Algorithm.greedy_algorithm import solve_greedy as run_greedy_algorithm
from Algorithm.local_search_algorithm import solve_local_search as run_local_search_algorithm
from Utils.data_handler import generate_random_data, load_data_from_file, load_data_manual
from Utils.experiments import main as run_experiments_menu
from Utils.utils import (
    print_details,
    print_orders,
    print_schedule,
    read_int,
    read_menu_item,
    save_results_to_file,
)


def run():
    main_menu()


def main_menu():
    orders = []
    m = 0
    greedy_result = None
    local_search_result = None
    last_result = None

    while True:
        print()
        print("Головне меню.")
        print_task_status(orders, m)
        print()
        print("Доступні опції:")
        print("1. Внести дані задачі")
        print("2. Розв'язати задачу жадібним алгоритмом")
        print("3. Провести локальний пошук")
        print("4. Вивести дані задачі")
        print("5. Записати результати у файл")
        print("6. Провести експерименти")
        print("0. Завершити роботу")
        print()

        choice = read_menu_item("Введіть число: ", ["1", "2", "3", "4", "5", "6", "0"])

        if choice == "1":
            new_orders, new_m = input_data_menu(orders, m)

            if new_orders != orders or new_m != m:
                orders = new_orders
                m = new_m
                greedy_result = None
                local_search_result = None
                last_result = None
        elif choice == "2":
            greedy_result, last_result = solve_greedy_menu(orders, m, greedy_result, last_result)
        elif choice == "3":
            local_search_result, last_result = solve_local_search_menu(
                orders,
                greedy_result,
                local_search_result,
                last_result
            )
        elif choice == "4":
            output_data_menu(orders, m, last_result)
        elif choice == "5":
            save_results(last_result, orders, m)
        elif choice == "6":
            run_experiments_menu()
        elif choice == "0":
            print()
            print("Роботу програми завершено.")
            return


def print_task_status(orders, m):
    if len(orders) == 0:
        print("Статус задачі: задачу не задано.")
    else:
        print("Статус задачі: задачу задано.")
        print("Кількість замовлень n =", len(orders))
        print("Кількість контейнеровозів m =", m)


def input_data_menu(current_orders, current_m):
    while True:
        print()
        print("Підменю для внесення даних задачі.")
        print()
        print("Доступні опції:")
        print("1. Ввести дані вручну")
        print("2. Згенерувати дані випадковим чином")
        print("3. Зчитати дані з файлу")
        print("0. Повернутись в головне меню")
        print()

        choice = read_menu_item("Введіть число: ", ["1", "2", "3", "0"])

        if choice == "1":
            return load_data_manual()
        elif choice == "2":
            return generate_random_data()
        elif choice == "3":
            return load_data_from_file()
        elif choice == "0":
            return current_orders, current_m


def solve_greedy_menu(orders, m, current_greedy_result, current_last_result):
    if len(orders) == 0:
        print()
        print("Спочатку потрібно внести дані задачі.")
        return current_greedy_result, current_last_result

    greedy_result, rule, all_results = run_greedy_algorithm(orders, m)

    print()
    print("Результат роботи жадібного алгоритму:")
    print("Значення F за правилами:")

    for item in all_results:
        item_rule = item[0]
        item_result = item[1]
        print(item_rule + ": F =", round(item_result.F, 4))

    print()
    print("Обране правило:", rule)
    print_schedule(greedy_result)
    print_details(greedy_result)

    return greedy_result, greedy_result


def solve_local_search_menu(orders, greedy_result, current_local_search_result, current_last_result):
    if len(orders) == 0:
        print()
        print("Спочатку потрібно внести дані задачі.")
        return current_local_search_result, current_last_result

    if greedy_result is None:
        print()
        print("Спочатку потрібно розв'язати задачу жадібним алгоритмом.")
        return current_local_search_result, current_last_result

    max_iterations = int(0.5 * len(orders))
    print()
    print("Максимальна кількість ітерацій K = int(0.5 * n) =", max_iterations)
    local_search_result, start_F, finish_reason, f_history = run_local_search_algorithm(
        greedy_result,
        orders,
        max_iterations,
        return_history=True,
    )

    print()
    print("Результат локального пошуку:")
    print("Початкове значення F =", round(start_F, 4))
    print("Покращене значення F =", round(local_search_result.F, 4))
    print("Причина завершення пошуку:", finish_reason)
    print()
    print("Розклад після локального пошуку:")
    print_schedule(local_search_result)
    print_details(local_search_result)
    plot_local_search_history(f_history)

    return local_search_result, local_search_result


def plot_local_search_history(f_history):
    import matplotlib.pyplot as plt

    iteration_values = list(range(len(f_history)))

    plt.figure()
    plt.plot(iteration_values, f_history, marker="o")
    plt.title("F by local search iteration")
    plt.xlabel("iteration")
    plt.ylabel("F")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def output_data_menu(orders, m, last_result):
    while True:
        print()
        print("Підменю для виведення даних задачі.")
        print()
        print("Доступні опції:")
        print("1. Вивести початкові дані")
        print("2. Вивести останній результат")
        print("0. Повернутись в головне меню")
        print()

        choice = read_menu_item("Введіть число: ", ["1", "2", "0"])

        if choice == "1":
            print_orders(orders, m)
        elif choice == "2":
            if last_result is None:
                print()
                print("Результат ще не отримано.")
            else:
                print_schedule(last_result)
                print_details(last_result)
        elif choice == "0":
            return


def save_results(last_result, orders, m):
    if last_result is None:
        print()
        print("Спочатку потрібно розв'язати задачу.")
        return

    file_name = input("Введіть назву файлу для запису результатів: ")

    if file_name == "":
        file_name = "results.txt"

    save_results_to_file(last_result, orders, m, file_name)
