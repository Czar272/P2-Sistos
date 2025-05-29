from utils.parser import parse_processes
from algorithms.fifo import fifo_schedule
from algorithms.priority import priority_schedule
from algorithms.sjf import sjf_schedule
from algorithms.srt import srt_schedule
from algorithms.round_robin import round_robin_schedule
from sync.sync_simulator import plot_mutex_gantt, print_mutex_timeline_ascii, simulate_mutex
import matplotlib.pyplot as plt
from utils.sync_parser import parse_actions, parse_resources



def plot_gantt(timeline):
    fig, ax = plt.subplots()
    yticks = []
    
    for i, (pid, start, end) in enumerate(timeline):
        ax.broken_barh([(start, end - start)], (i * 10, 9), facecolors='tab:blue')
        ax.text(start + (end - start)/2 - 0.5, i * 10 + 4, pid, color='white', fontsize=9, fontweight='bold')
        yticks.append((i * 10 + 4, pid))

    ax.set_xlabel('Ciclos')
    ax.set_yticks([y for y, _ in yticks])
    ax.set_yticklabels([label for _, label in yticks])
    ax.grid(True)
    ax.set_title('Diagrama de Gantt')
    plt.tight_layout()
    plt.show()


def print_timeline(timeline):
    print("\n Línea de Tiempo:")
    for pid, start, end in timeline:
        print(f"{pid}: {start} -> {end}")

def print_metrics(processes):
    total_wait = sum(p.waiting_time for p in processes)
    avg_wait = total_wait / len(processes)
    print(f"\n Avg Waiting Time: {avg_wait:.2f} ciclos")



# --------------- FIRST IN FIRST OUT ---------------

# if __name__ == "__main__":
#     file_path = 'data/procesos.txt'
#     processes = parse_processes(file_path)
#     timeline, updated_processes = fifo_schedule(processes)
#     print_timeline(timeline)
#     print_metrics(updated_processes)
#     plot_gantt(timeline)


# --------------- SHORTEST JOB FIRST ---------------

# if __name__ == "__main__":
#     file_path = 'data/procesos.txt'
#     processes = parse_processes(file_path)
#     timeline, updated_processes = sjf_schedule(processes)
#     print_timeline(timeline)
#     print_metrics(updated_processes)
#     plot_gantt(timeline)

# --------------- SHORTEST REMAINING TIME ---------------

# if __name__ == "__main__":
#     file_path = 'data/procesos.txt'
#     processes = parse_processes(file_path)
#     timeline, updated_processes = srt_schedule(processes)
#     print_timeline(timeline)
#     print_metrics(updated_processes)
#     plot_gantt(timeline)


# --------------- ROUND ROBIN ---------------

# if __name__ == "__main__":
#     file_path = 'data/procesos.txt'
#     quantum = 2  # Configurable
#     processes = parse_processes(file_path)
#     timeline, updated_processes = round_robin_schedule(processes, quantum)
#     print_timeline(timeline)
#     print_metrics(updated_processes)
#     plot_gantt(timeline)


# --------------- PRIORITY ---------------

# if __name__ == "__main__":
#     file_path = 'data/procesos.txt'
#     processes = parse_processes(file_path)
#     timeline, updated_processes = priority_schedule(processes)
#     print_timeline(timeline)
#     print_metrics(updated_processes)
#     plot_gantt(timeline)


if __name__ == "__main__":

    resources = parse_resources("data/recursos.txt")
    actions = parse_actions("data/acciones.txt")

    timeline = simulate_mutex(resources, actions)
    print_mutex_timeline_ascii(timeline, max_cycles=20)
    plot_mutex_gantt(timeline, max_cycles=20)


