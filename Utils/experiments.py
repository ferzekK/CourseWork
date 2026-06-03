import time

from Algorithm.greedy_algorithm import solve_greedy
from Algorithm.local_search_algorithm import solve_local_search
from Utils.data_handler import generate_orders
from Utils.utils import read_int


def read_range(parameter_name):
    print("Вкажіть діапазон зміни " + parameter_name + ":")
    lower = read_int("Введіть нижню межу " + parameter_name + ": ", 1)

    while True:
        upper = read_int("Введіть верхню межу " + parameter_name + ": ", 1)

        if upper >= lower:
            break

        print("Введено некоректне значення. Спробуйте ще раз.")

    step = read_int("Введіть крок зміни " + parameter_name + ": ", 1)

    values = []
    current = lower

    while current <= upper:
        values.append(current)
        current = current + step

    return values


def measure_time(func, *args):
    start_time = time.perf_counter()
    result = func(*args)
    finish_time = time.perf_counter()

    return result, finish_time - start_time


def run_single_test(orders, m, K):
    greedy_data, time_greedy = measure_time(solve_greedy, orders, m)
    greedy_result = greedy_data[0]

    local_data, time_local = measure_time(solve_local_search, greedy_result, orders, K)
    local_result = local_data[0]

    improvement = greedy_result.F - local_result.F

    if greedy_result.F != 0:
        improvement_percent = improvement / greedy_result.F * 100
    else:
        improvement_percent = 0

    return {
        "F_greedy": greedy_result.F,
        "F_local": local_result.F,
        "time_greedy": time_greedy,
        "time_local": time_local,
        "improvement": improvement,
        "improvement_percent": improvement_percent,
    }


def average_results(results):
    average = {}

    for field in results[0]:
        total = 0

        for result in results:
            total = total + result[field]

        average[field] = total / len(results)

    return average


def collect_rows(parameter_name, values, fixed_n, fixed_m, K, repeat_count):
    rows = []

    for value in values:
        if parameter_name == "n":
            n = value
            m = fixed_m
        elif parameter_name == "m":
            n = fixed_n
            m = value
        else:
            n = fixed_n
            m = fixed_m
            K = value

        results = []

        for repeat in range(1, repeat_count + 1):
            if parameter_name == "K":
                seed = repeat
            else:
                seed = value * 1000 + repeat

            orders = generate_orders(n, seed)
            result = run_single_test(orders, m, K)
            results.append(result)

        average = average_results(results)
        average["n"] = n
        average["m"] = m
        average["K"] = K
        average["repeat_count"] = repeat_count
        rows.append(average)

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


def run_n_experiment():
    n_values = read_range("n")
    m = read_int("Введіть фіксовану кількість контейнеровозів m: ", 1)
    K = read_int("Введіть фіксовану кількість ітерацій K: ", 1)
    repeat_count = read_int("Введіть кількість повторів для усереднення: ", 1)

    title = "Дослідження впливу кількості замовлень n на час"
    print_experiment_start(title, "n", {"m": m, "K": K, "Кількість повторів": repeat_count})

    rows = collect_rows("n", n_values, None, m, K, repeat_count)
    plot_time_by_n(rows)


def run_m_experiment():
    n = read_int("Введіть фіксовану кількість замовлень n: ", 1)
    m_values = read_range("m")
    K = read_int("Введіть фіксовану кількість ітерацій K: ", 1)
    repeat_count = read_int("Введіть кількість повторів для усереднення: ", 1)

    title = "Дослідження впливу кількості контейнеровозів m на час"
    print_experiment_start(title, "m", {"n": n, "K": K, "Кількість повторів": repeat_count})

    rows = collect_rows("m", m_values, n, None, K, repeat_count)
    plot_time_by_m(rows)


def run_k_experiment():
    n = read_int("Введіть фіксовану кількість замовлень n: ", 1)
    m = read_int("Введіть фіксовану кількість контейнеровозів m: ", 1)
    k_values = read_range("K")
    repeat_count = read_int("Введіть кількість повторів для усереднення: ", 1)

    title = "Дослідження впливу кількості ітерацій K на час та точність"
    print_experiment_start(title, "K", {"n": n, "m": m, "Кількість повторів": repeat_count})

    rows = collect_rows("K", k_values, n, m, 0, repeat_count)
    plot_k_experiment(rows)


def run_m_accuracy_experiment():
    n = read_int("Введіть фіксовану кількість замовлень n: ", 1)
    m_values = read_range("m")
    K = read_int("Введіть фіксовану кількість ітерацій K: ", 1)
    repeat_count = read_int("Введіть кількість повторів для усереднення: ", 1)

    title = "Дослідження впливу кількості контейнеровозів m на точність"
    print_experiment_start(title, "m", {"n": n, "K": K, "Кількість повторів": repeat_count})

    rows = collect_rows("m", m_values, n, None, K, repeat_count)
    plot_accuracy_by_m(rows)


def plot_time_by_n(rows):
    plot_two_lines(
        rows,
        "n",
        "time_greedy",
        "time_local",
        "greedy",
        "local search",
        "Порівняння часу роботи алгоритмів залежно від n",
        "n",
        "Час роботи, с",
    )


def plot_time_by_m(rows):
    plot_two_lines(
        rows,
        "m",
        "time_greedy",
        "time_local",
        "greedy",
        "local search",
        "Порівняння часу роботи алгоритмів залежно від m",
        "m",
        "Час роботи, с",
    )


def plot_accuracy_by_m(rows):
    plot_two_lines(
        rows,
        "m",
        "F_greedy",
        "F_local",
        "F greedy",
        "F local",
        "Порівняння точності алгоритмів залежно від m",
        "m",
        "F",
    )


def plot_k_experiment(rows):
    import matplotlib.pyplot as plt

    k_values = get_values(rows, "K")
    time_local_values = get_values(rows, "time_local")
    f_local_values = get_values(rows, "F_local")

    figure, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(k_values, time_local_values, marker="o")
    axes[0].set_title("Час локального пошуку від K")
    axes[0].set_xlabel("K")
    axes[0].set_ylabel("Час роботи, с")
    axes[0].grid(True)

    axes[1].plot(k_values, f_local_values, marker="o")
    axes[1].set_title("Точність локального пошуку від K")
    axes[1].set_xlabel("K")
    axes[1].set_ylabel("F local")
    axes[1].grid(True)

    figure.suptitle("Вплив кількості ітерацій K")
    figure.tight_layout()
    plt.show()


def plot_two_lines(rows, x_field, first_field, second_field, first_label, second_label, title, x_label, y_label):
    import matplotlib.pyplot as plt

    x_values = get_values(rows, x_field)
    first_values = get_values(rows, first_field)
    second_values = get_values(rows, second_field)

    plt.figure()
    plt.plot(x_values, first_values, marker="o", label=first_label)
    plt.plot(x_values, second_values, marker="o", label=second_label)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.legend()
    plt.show()


def get_values(rows, field_name):
    values = []

    for row in rows:
        values.append(row[field_name])

    return values


def main():
    while True:
        print("Оберіть експеримент:")
        print("1 - вплив кількості замовлень n на час")
        print("2 - вплив кількості контейнеровозів m на час")
        print("3 - вплив кількості контейнеровозів m на точність")
        print("4 - вплив кількості ітерацій K на час та точність")
        print("0 - вихід")

        choice = input("Введіть число: ")

        if choice == "1":
            run_n_experiment()
        elif choice == "2":
            run_m_experiment()
        elif choice == "3":
            run_m_accuracy_experiment()
        elif choice == "4":
            run_k_experiment()
        elif choice == "0":
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
