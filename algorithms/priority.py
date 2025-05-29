from copy import deepcopy

def priority_schedule(processes):
    n = len(processes)
    processes = deepcopy(processes)
    processes.sort(key=lambda p: p.at)

    current_time = 0
    completed = 0
    timeline = []
    ready_queue = []
    index = 0
    visited = set()

    while completed < n:
        
        # Agregar procesos que han llegado
        while index < n and processes[index].at <= current_time:
            ready_queue.append(processes[index])
            index += 1

        if not ready_queue:
            if index < n:
                current_time = processes[index].at
            continue

        # Esperar si hay un proceso futuro con mejor prioridad
        future_has_better_priority = False
        current_best = min(ready_queue, key=lambda p: p.priority)

        for i in range(index, n):
            if processes[i].priority < current_best.priority:
                current_time += 1
                future_has_better_priority = True
                break

        if future_has_better_priority:
            continue

        # Ejecutar el de mayor prioridad
        current = current_best
        ready_queue.remove(current)


        current.start_time = current_time
        current.completion_time = current_time + current.bt
        current.waiting_time = current.start_time - current.at
        current_time = current.completion_time

        timeline.append((current.pid, current.start_time, current.completion_time))
        visited.add(current.pid)
        completed += 1



    return timeline, processes
