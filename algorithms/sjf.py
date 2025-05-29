def sjf_schedule(processes):
    processes.sort(key=lambda p: p.at)  # Ordenar por tiempo de llegada
    ready_queue = []
    timeline = []
    current_time = 0
    index = 0
    n = len(processes)

    while len(timeline) < n:
        # Añadir procesos disponibles al tiempo actual
        while index < n and processes[index].at <= current_time:
            ready_queue.append(processes[index])
            index += 1

        if ready_queue:
            # Seleccionar el de menor Burst Time
            ready_queue.sort(key=lambda p: p.bt)
            current = ready_queue.pop(0)
        else:
            # Si no hay procesos listos, avanzar el tiempo
            current_time = processes[index].at
            continue

        current.start_time = current_time
        current.completion_time = current_time + current.bt
        current.waiting_time = current.start_time - current.at
        timeline.append((current.pid, current.start_time, current.completion_time))
        current_time = current.completion_time

    return timeline, processes
