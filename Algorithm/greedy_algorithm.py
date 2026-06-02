from Models.models import Schedule, ScheduleResult


def get_sort_key(order, rule):
    if rule == "SPTu":
        return order.t / order.w

    return (order.d - order.t) / order.w


def solve_greedy(orders, m):
    result_sptu, rule_sptu = solve_greedy_by_rule(orders, m, "SPTu")
    result_slack, rule_slack = solve_greedy_by_rule(orders, m, "SLACK_OVER_W")

    if result_sptu.F <= result_slack.F:
        best_result = result_sptu
        best_rule = rule_sptu
    else:
        best_result = result_slack
        best_rule = rule_slack

    all_results = [
        [rule_sptu, result_sptu],
        [rule_slack, result_slack]
    ]

    best_result.algorithm_name = "Жадібний алгоритм"
    return best_result, best_rule, all_results


def solve_greedy_by_rule(orders, m, rule):
    sorted_orders = orders.copy()
    sorted_orders.sort(key=lambda order: get_sort_key(order, rule))

    schedule = []
    truck_time = []

    for i in range(m):
        schedule.append([])
        truck_time.append(0)

    results = []
    total_weight = 0
    late_weight = 0

    for order in orders:
        total_weight = total_weight + order.w

    for order in sorted_orders:
        min_time = min(truck_time)
        truck_index = truck_time.index(min_time)

        start_time = truck_time[truck_index]
        completion_time = start_time + order.t

        if completion_time > order.d:
            late = 1
        else:
            late = 0

        late_weight = late_weight + order.w * late
        schedule[truck_index].append(order.id)

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

        truck_time[truck_index] = truck_time[truck_index] + 2 * order.t

    if total_weight == 0:
        F = 0
    else:
        F = late_weight / total_weight

    return Schedule(schedule, results, F, late_weight, total_weight, "Жадібний алгоритм"), rule
