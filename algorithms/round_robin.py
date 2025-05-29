from copy import deepcopy
from collections import deque

def round_robin_schedule(processes, quantum):
    n = len(processes)
    processes = deepcopy(processes)
    processes.sort(key=lambda p: p.at)

    timeline = []
    current_time = 0
    queue = deque()
    remaining_times = {p.pid: p.bt for p in processes}
    arrival_index = 0
    pid_map = {p.pid: p for p in processes}
    first_execution = {}

    # Función para añadir nuevos procesos al tiempo actual
    def add_new_arrivals():
        nonlocal arrival_index
        while arrival_index < n and processes[arrival_index].at <= current_time:
            queue.append(processes[arrival_index])
            arrival_index += 1

    add_new_arrivals()

    while queue or arrival_index < n:
        if not queue:
            current_time = processes[arrival_index].at
            add_new_arrivals()
            continue

        process = queue.popleft()
        pid = process.pid

        if pid not in first_execution:
            first_execution[pid] = current_time

        run_time = min(quantum, remaining_times[pid])
        start_time = current_time
        end_time = current_time + run_time
        timeline.append((pid, start_time, end_time))

        current_time = end_time
        remaining_times[pid] -= run_time

        add_new_arrivals()

        if remaining_times[pid] > 0:
            queue.append(process)

    # Calcular tiempos finales
    for p in processes:
        p.start_time = first_execution[p.pid]
        p.completion_time = max(t[2] for t in timeline if t[0] == p.pid)
        p.waiting_time = p.completion_time - p.at - p.bt

    return timeline, processes
