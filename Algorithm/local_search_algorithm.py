from Models.models import Schedule, ScheduleResult


def solve_local_search(start_schedule, orders, max_iterations):
    current_schedule = copy_schedule(start_schedule.schedule)
    current_result = calculate_result(current_schedule, orders)
    start_F = current_result.F

    iteration = 0
    improvement = True

    while improvement == True and iteration < max_iterations:
        improvement = False
        iteration = iteration + 1

        neighbors = generate_neighbors(current_schedule)

        for neighbor in neighbors:
            neighbor_result = calculate_result(neighbor, orders)

            if neighbor_result.F < current_result.F:
                current_schedule = neighbor
                current_result = neighbor_result
                improvement = True
                break

    if improvement:
        finish_reason = "досягнуто максимальну кількість ітерацій"
    else:
        finish_reason = "неможливо покращити розклад"

    current_result.algorithm_name = "Локальний пошук"
    return current_result, start_F, finish_reason


def copy_schedule(schedule):
    new_schedule = []

    for truck in schedule:
        new_schedule.append(truck.copy())

    return new_schedule


def find_order(orders, order_id):
    for order in orders:
        if order.id == order_id:
            return order

    return None


def calculate_result(schedule, orders):
    results = []
    total_weight = 0
    late_weight = 0

    for order in orders:
        total_weight = total_weight + order.w

    for truck_index in range(len(schedule)):
        truck_time = 0

        for order_id in schedule[truck_index]:
            order = find_order(orders, order_id)

            start_time = truck_time
            completion_time = start_time + order.t

            if completion_time > order.d:
                late = 1
            else:
                late = 0

            late_weight = late_weight + order.w * late

            result = ScheduleResult(
                order.id,
                truck_index + 1,
                start_time,
                completion_time,
                order.d,
                order.w,
                late
            )
            results.append(result)

            truck_time = truck_time + 2 * order.t

    if total_weight == 0:
        F = 0
    else:
        F = late_weight / total_weight

    return Schedule(schedule, results, F, late_weight, total_weight, "Локальний пошук")


def generate_neighbors(schedule):
    neighbors = []

    for truck1 in range(len(schedule)):
        for pos1 in range(len(schedule[truck1])):
            for truck2 in range(len(schedule)):
                for pos2 in range(len(schedule[truck2])):
                    if truck1 == truck2 and pos1 == pos2:
                        continue

                    neighbor = swap_orders(schedule, truck1, pos1, truck2, pos2)
                    neighbors.append(neighbor)

    for truck1 in range(len(schedule)):
        for pos1 in range(len(schedule[truck1])):
            for truck2 in range(len(schedule)):
                if truck1 != truck2:
                    neighbor = move_order(schedule, truck1, pos1, truck2)
                    neighbors.append(neighbor)

    return neighbors


def swap_orders(schedule, truck1, pos1, truck2, pos2):
    new_schedule = copy_schedule(schedule)

    temp = new_schedule[truck1][pos1]
    new_schedule[truck1][pos1] = new_schedule[truck2][pos2]
    new_schedule[truck2][pos2] = temp

    return new_schedule


def move_order(schedule, truck1, pos1, truck2):
    new_schedule = copy_schedule(schedule)
    order_id = new_schedule[truck1].pop(pos1)
    new_schedule[truck2].append(order_id)

    return new_schedule
