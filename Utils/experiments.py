import random
import time

import matplotlib.pyplot as plt
import numpy as np

from Algorithm.greedy_algorithm import solve_greedy
from Algorithm.local_search_algorithm import solve_local_search
from Utils.data_handler import generate_orders
from Utils.utils import read_int


ALPHA_VALUES = [0.10, 0.20, 0.30, 0.4, 0.5, 0.6, 0.7]
O_PERCENT_VALUES = [10, 30, 50, 70, 90, 100]

DEFAULT_ALPHA_N = 80
DEFAULT_ALPHA_REPEAT_COUNT = 3

DEFAULT_O_N = 80
DEFAULT_O_REPEAT_COUNT = 10
O_MAX_ITERATIONS_COEFFICIENT = 0.5
DEFAULT_COMPARE_REPEAT_COUNT = 10

RANDOM_SEED = 42


def read_float(message, min_value=0):
    while True:
        try:
            value = float(input(message).replace(",", "."))

            if value >= min_value:
                return value

            print("Введено некоректне значення. Спробуйте ще раз.")
        except ValueError:
            print("Введено некоректне значення. Спробуйте ще раз.")


def read_int_list(message):
    while True:
        text = input(message)
        parts = text.replace(";", ",").split(",")
        values = []

        try:
            for part in parts:
                value_text = part.strip()

                if value_text != "":
                    value = int(value_text)

                    if value <= 0:
                        values = []
                        break

                    values.append(value)

            if len(values) > 0:
                return values

            print("Введено некоректне значення. Спробуйте ще раз.")
        except ValueError:
            print("Введено некоректне значення. Спробуйте ще раз.")


def measure_time(func, *args, **kwargs):
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    finish_time = time.perf_counter()

    return result, finish_time - start_time


def generate_initial_schedule(orders, m):
    return solve_greedy(orders, m)[0]


def calculate_truck_count(n, truck_percent):
    return max(1, int(n * truck_percent / 100))


def run_local_search(orders, m, max_iterations, O_percent=None):
    start_schedule = generate_initial_schedule(orders, m)
    result, start_F, reason = solve_local_search(
        start_schedule,
        orders,
        max_iterations=max_iterations,
        O_percent=O_percent,
    )

    return result.F


def get_seed(repeat):
    return RANDOM_SEED + repeat


def run_alpha_experiment(n=DEFAULT_ALPHA_N, repeat_count=DEFAULT_ALPHA_REPEAT_COUNT, truck_percent=None):
    if truck_percent is None:
        truck_percent = read_float("Введіть кількість контейнеровозів у відсотках від n: ", 0.0001)

    m = calculate_truck_count(n, truck_percent)
    rows = []

    print_experiment_start(
        "Дослідження впливу кількості ітерацій на локальний пошук",
        "alpha",
        {"n": n, "m, % від n": truck_percent, "m": m, "r": repeat_count},
    )

    for alpha in ALPHA_VALUES:
        pi = int(alpha * n)
        f_values = []

        for repeat in range(1, repeat_count + 1):
            seed = get_seed(repeat)
            random.seed(seed)
            orders = generate_orders(n, seed)
            F = run_local_search(orders, m, max_iterations=pi)
            f_values.append(F)

        rows.append({
            "pi": pi,
            "F_avg": float(np.mean(f_values)),
        })

    plot_alpha_experiment(rows)
    return rows


def run_experiment(n=DEFAULT_O_N, truck_percent=10, r=DEFAULT_O_REPEAT_COUNT):
    m = calculate_truck_count(n, truck_percent)
    max_iterations = int(O_MAX_ITERATIONS_COEFFICIENT * n)
    rows = []

    print_experiment_start(
        "Дослідження впливу розміру околу на локальний пошук",
        "O_percent",
        {"n": n, "m, % від n": truck_percent, "m": m, "r": r, "max_iterations": max_iterations},
    )

    for O_percent in O_PERCENT_VALUES:
        f_values = []

        for repeat in range(1, r + 1):
            seed = get_seed(repeat)
            random.seed(seed)
            orders = generate_orders(n, seed)
            F = run_local_search(
                orders,
                m,
                max_iterations=max_iterations,
                O_percent=O_percent,
            )
            f_values.append(F)

        rows.append({
            "O_percent": O_percent,
            "F_avg": float(np.mean(f_values)),
        })

    plot_o_percent_experiment(rows)
    return rows


def run_algorithm_comparison_experiment(n_values, truck_percent, r=DEFAULT_COMPARE_REPEAT_COUNT):
    rows = []

    print_experiment_start(
        "Порівняння жадібного алгоритму та локального пошуку",
        "n",
        {"m, % від n": truck_percent, "r": r, "max_iterations": "int(0.5 * n)"},
    )

    for n in n_values:
        m = calculate_truck_count(n, truck_percent)
        max_iterations = int(O_MAX_ITERATIONS_COEFFICIENT * n)
        greedy_f_values = []
        local_f_values = []
        greedy_time_values = []
        local_time_values = []

        for repeat in range(1, r + 1):
            seed = get_seed(repeat)
            random.seed(seed)
            orders = generate_orders(n, seed)

            greedy_data, greedy_time = measure_time(solve_greedy, orders, m)
            greedy_result = greedy_data[0]

            local_data, local_time = measure_time(
                solve_local_search,
                greedy_result,
                orders,
                max_iterations,
            )
            local_result = local_data[0]

            greedy_f_values.append(greedy_result.F)
            local_f_values.append(local_result.F)
            greedy_time_values.append(greedy_time)
            local_time_values.append(local_time)

        rows.append({
            "n": n,
            "m": m,
            "F_greedy": float(np.mean(greedy_f_values)),
            "F_local": float(np.mean(local_f_values)),
            "time_greedy": float(np.mean(greedy_time_values)),
            "time_local": float(np.mean(local_time_values)),
        })

    plot_algorithm_comparison_experiment(rows)
    return rows


def print_experiment_start(title, changed_parameter, fixed_values):
    print()
    print(title)
    print("Змінюється:", changed_parameter)
    print("Фіксовані значення:")

    for name in fixed_values:
        print(name + " =", fixed_values[name])

    print()
    print("Експеримент розпочато. Це може зайняти кілька хвилин...")
    print()


def plot_alpha_experiment(rows):
    pi_values = get_values(rows, "pi")
    f_avg_values = get_values(rows, "F_avg")

    plt.figure()
    plt.plot(pi_values, f_avg_values, marker="o")
    plt.title("F_avg by pi")
    plt.xlabel("pi")
    plt.ylabel("F_avg")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_o_percent_experiment(rows):
    O_percent_values = get_values(rows, "O_percent")
    f_avg_values = get_values(rows, "F_avg")

    plt.figure()
    plt.plot(O_percent_values, f_avg_values, marker="o")
    plt.title("F_avg by O_percent")
    plt.xlabel("O_percent")
    plt.ylabel("F_avg")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_algorithm_comparison_experiment(rows):
    n_values = get_values(rows, "n")
    greedy_time_values = get_values(rows, "time_greedy")
    local_time_values = get_values(rows, "time_local")
    greedy_f_values = get_values(rows, "F_greedy")
    local_f_values = get_values(rows, "F_local")

    plt.figure()
    plt.plot(n_values, greedy_time_values, marker="o", label="greedy")
    plt.plot(n_values, local_time_values, marker="o", label="local search")
    plt.title("Algorithm time by n")
    plt.xlabel("n")
    plt.ylabel("time, s")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.figure()
    plt.plot(n_values, greedy_f_values, marker="o", label="greedy")
    plt.plot(n_values, local_f_values, marker="o", label="local search")
    plt.title("Objective function by n")
    plt.xlabel("n")
    plt.ylabel("F_avg")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def get_values(rows, field_name):
    values = []

    for row in rows:
        values.append(row[field_name])

    return values


def main():
    while True:
        print("Оберіть експеримент:")
        print("1 - вплив коефіцієнта alpha на локальний пошук")
        print("2 - вплив розміру околу на якість локального пошуку")
        print("3 - порівняння жадібного алгоритму та локального пошуку")
        print("0 - вихід")

        choice = input("Введіть число: ")

        if choice == "1":
            n = read_int("Введіть кількість замовлень n: ", 1)
            truck_percent = read_float("Введіть кількість машин у відсотках від n: ", 0.0001)
            r = read_int("Введіть кількість повторів r: ", 1)
            run_alpha_experiment(n=n, repeat_count=r, truck_percent=truck_percent)
        elif choice == "2":
            n = read_int("Введіть кількість замовлень n: ", 1)
            truck_percent = read_float("Введіть кількість машин у відсотках від n: ", 0.0001)
            r = read_int("Введіть кількість повторів r: ", 1)
            run_experiment(n, truck_percent, r)
        elif choice == "3":
            n_values = read_int_list("Введіть значення n через кому, наприклад 20,50,100,150: ")
            truck_percent = read_float("Введіть кількість машин у відсотках від n: ", 0.0001)
            r = read_int("Введіть кількість повторів r: ", 1)
            run_algorithm_comparison_experiment(n_values, truck_percent, r)
        elif choice == "0":
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
