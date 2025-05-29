from copy import deepcopy

def srt_schedule(processes):
    n = len(processes)
    processes = deepcopy(processes)  # Evitar modificar el original
    processes.sort(key=lambda p: p.at)  # Orden inicial por llegada

    timeline = []
    remaining_times = {p.pid: p.bt for p in processes}
    completed = 0
    current_time = 0
    last_pid = None

    ready_queue = []
    index = 0

    while completed < n:
        # Agregar procesos disponibles
        while index < n and processes[index].at <= current_time:
            ready_queue.append(processes[index])
            index += 1

        # Filtrar los que aún no terminaron
        available = [p for p in ready_queue if remaining_times[p.pid] > 0]

        if not available:
            current_time += 1
            continue

        # Seleccionar el de menor tiempo restante
        available.sort(key=lambda p: remaining_times[p.pid])
        current = available[0]
        pid = current.pid

        if last_pid != pid:
            timeline.append((pid, current_time))  # Comienzo nuevo bloque

        # Ejecutar un ciclo
        remaining_times[pid] -= 1
        current_time += 1
        last_pid = pid

        if remaining_times[pid] == 0:
            current.completion_time = current_time
            current.start_time = current.completion_time - current.bt
            current.waiting_time = current.start_time - current.at
            completed += 1

    # Convertir timeline en (pid, start, end) bloques
    final_timeline = []
    for i in range(len(timeline)):
        pid, start = timeline[i]
        end = timeline[i + 1][1] if i + 1 < len(timeline) else current_time
        final_timeline.append((pid, start, end))

    return final_timeline, processes
