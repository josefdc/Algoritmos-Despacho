def fifo(processes):
    sorted_processes = sorted(processes, key=lambda x: x[1])
    start_time = 0
    gantt_chart = []
    metrics = []

    for process in sorted_processes:
        if start_time < process[1]:
            start_time = process[1]
        end_time = start_time + process[2]
        gantt_chart.append((process[0], start_time, end_time))
        waiting_time = start_time - process[1]
        turnaround_time = waiting_time + process[2]
        metrics.append((process[0], waiting_time, turnaround_time))
        start_time = end_time

    return gantt_chart, metrics

def sjf(processes):
    sorted_processes = sorted(processes, key=lambda x: x[1])
    remaining_processes = sorted_processes.copy()
    start_time = 0
    gantt_chart = []
    metrics = []

    while remaining_processes:
        available_processes = [p for p in remaining_processes if p[1] <= start_time]
        if not available_processes:
            start_time = min(p[1] for p in remaining_processes)
            continue

        next_process = min(available_processes, key=lambda x: x[2])
        remaining_processes.remove(next_process)
        end_time = start_time + next_process[2]
        gantt_chart.append((next_process[0], start_time, end_time))
        waiting_time = start_time - next_process[1]
        turnaround_time = waiting_time + next_process[2]
        metrics.append((next_process[0], waiting_time, turnaround_time))
        start_time = end_time

    return gantt_chart, metrics

def priority_scheduling(processes):
    sorted_processes = sorted(processes, key=lambda x: x[1])
    remaining_processes = sorted_processes.copy()
    start_time = 0
    gantt_chart = []
    metrics = []

    while remaining_processes:
        available_processes = [p for p in remaining_processes if p[1] <= start_time]
        if not available_processes:
            start_time = min(p[1] for p in remaining_processes)
            continue

        next_process = min(available_processes, key=lambda x: x[3])
        remaining_processes.remove(next_process)
        end_time = start_time + next_process[2]
        gantt_chart.append((next_process[0], start_time, end_time))
        waiting_time = start_time - next_process[1]
        turnaround_time = waiting_time + next_process[2]
        metrics.append((next_process[0], waiting_time, turnaround_time))
        start_time = end_time

    return gantt_chart, metrics
