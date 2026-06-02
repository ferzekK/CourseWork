class Order:
    def __init__(self, id, t, d, w):
        self.id = id
        self.t = t
        self.d = d
        self.w = w


class ScheduleResult:
    def __init__(self, order_id, truck, start_time, completion_time, deadline, weight, late):
        self.order_id = order_id
        self.truck = truck
        self.start_time = start_time
        self.completion_time = completion_time
        self.deadline = deadline
        self.weight = weight
        self.late = late


class Schedule:
    def __init__(self, schedule, results, F, late_weight, total_weight, algorithm_name=""):
        self.schedule = schedule
        self.results = results
        self.F = F
        self.late_weight = late_weight
        self.total_weight = total_weight
        self.algorithm_name = algorithm_name
