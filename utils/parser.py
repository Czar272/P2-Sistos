class Process:
    def __init__(self, pid, burst_time, arrival_time, priority):
        self.pid = pid
        self.bt = int(burst_time)
        self.at = int(arrival_time)
        self.priority = int(priority)
        self.start_time = None
        self.completion_time = None
        self.waiting_time = None

    def __repr__(self):
        return f"{self.pid}(AT={self.at}, BT={self.bt}, P={self.priority})"

def parse_processes(file_path):
    processes = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip():
                pid, bt, at, priority = line.strip().split(',')
                processes.append(Process(pid.strip(), bt.strip(), at.strip(), priority.strip()))
    return processes
