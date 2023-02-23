import csv


def inPut(filename):
    jobs = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        return [(int(x[0]), int(x[1]), int(x[2]), int(x[3])) for x in reader]



def fcfs(jobs):
    schedule = []
    current_time = 0
    for pid, _, arrival, duration in jobs:
        if arrival > current_time:
            current_time = arrival
        schedule.append((pid, current_time, current_time + duration))
        current_time += duration

    displaySchedule(schedule, "FCFS")
    compute_metrics(jobs, schedule)
    return schedule


def sjf(jobs):
    schedule = []
    current_time = 0
    jobs = sorted(jobs, key=lambda x: x[3])
    for pid, _, arrival, duration in jobs:
        if arrival > current_time:
            current_time = arrival
        schedule.append((pid, current_time, current_time + duration))
        current_time += duration
    displaySchedule(schedule, "SJF")
    compute_metrics(jobs, schedule)
    return schedule


def stcf(jobs):
    schedule = []
    current_time = 0
    remaining_jobs = jobs.copy()
    while remaining_jobs:
        min_remaining_time = float('inf')
        next_job = None
        for job in remaining_jobs:
            pid, _, arrival, duration = job
            if arrival <= current_time and duration < min_remaining_time:
                min_remaining_time = duration
                next_job = job
        if not next_job:
            current_time = min(remaining_jobs, key=lambda x: x[1])[1]
            continue

        pid, _, arrival, duration = next_job
        if arrival > current_time:
            current_time = arrival
        schedule.append((pid, current_time, current_time + duration))
        current_time += duration
        remaining_jobs.remove(next_job)
    displaySchedule(schedule, "STCF")
    compute_metrics(jobs, schedule)
    return schedule


def rr(jobs, timeslice):
    schedule = []
    current_time = 0
    remaining_jobs = jobs.copy()
    while remaining_jobs:
        if len(remaining_jobs) == 1:
            next_job = remaining_jobs[0]
            pid, _, arrival, duration = next_job
            if arrival > current_time:
                current_time = arrival
            schedule.append((pid, current_time, current_time + duration))
            current_time += duration
            remaining_jobs.remove(next_job)
        else:
            next_job = remaining_jobs.pop(0)
            pid, _, arrival, duration = next_job
            if arrival > current_time:
                current_time = arrival
            if duration > timeslice:
                schedule.append((pid, current_time, current_time + timeslice))
                current_time += timeslice
                remaining_jobs.append((pid, _, arrival, current_time - timeslice))
            else:
                schedule.append((pid, current_time, current_time + duration))
                current_time += duration

    displaySchedule(schedule, "RR")
    compute_metrics(jobs, schedule)
    return schedule


def displaySchedule(schedule, method):
    print(method, "\n")
    for pid, start, end in schedule:
        print(start, ":", "PID", pid, "\n")


def compute_metrics(jobs, schedule):
    ta_times = []
    res_times = []
    wait_times = []
    for pid, _, arrival, duration in jobs:
        for s_pid, start, end in schedule:
            if s_pid == pid:
                ta_time = end - arrival
                ta_times.append(ta_time)
                res_time = start - arrival
                res_times.append(res_time)
                wait_time = start - arrival - duration
                wait_times.append(wait_time)
                break

    avg_ta_time = sum(ta_times) / len(ta_times)
    avg_res_time = sum(res_times) / len(res_times)
    avg_wait_time = sum(wait_times) / len(wait_times)
    print("Time Metics: \n")
    print("Average Turn Around Time: ", avg_ta_time)
    print("Average Response Time: ", avg_res_time)
    print("Average Wait Time: ", avg_wait_time)


def main():
    fcfs(inPut("jobs.csv"))
    sjf(inPut("jobs.csv"))
    stcf(inPut("jobs.csv"))
    rr(inPut("jobs.csv"), 5)



main()
