from utils.parser import parse_processes
from algorithms.fifo import fifo_schedule
import matplotlib.pyplot as plt

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
    ax.set_title('Diagrama de Gantt - FIFO')
    plt.tight_layout()
    plt.show()


def print_timeline(timeline):
    print("\n Línea de Tiempo (FIFO):")
    for pid, start, end in timeline:
        print(f"{pid}: {start} -> {end}")

def print_metrics(processes):
    total_wait = sum(p.waiting_time for p in processes)
    avg_wait = total_wait / len(processes)
    print(f"\n Avg Waiting Time: {avg_wait:.2f} ciclos")

if __name__ == "__main__":
    file_path = 'data/procesos.txt'
    processes = parse_processes(file_path)
    timeline, updated_processes = fifo_schedule(processes)
    print_timeline(timeline)
    print_metrics(updated_processes)
    plot_gantt(timeline)

