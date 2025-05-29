def fifo_schedule(processes):
    processes.sort(key=lambda p: p.at)
    
    current_time = 0
    timeline = []

    for p in processes:
        if current_time < p.at:
            current_time = p.at
        p.start_time = current_time
        p.completion_time = current_time + p.bt
        p.waiting_time = p.start_time - p.at
        timeline.append((p.pid, p.start_time, p.completion_time))
        current_time = p.completion_time
    
    return timeline, processes
