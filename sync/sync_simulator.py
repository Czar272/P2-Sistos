from collections import defaultdict

from matplotlib import pyplot as plt
from utils.sync_parser import parse_resources, parse_actions

def simulate_mutex(resources, actions, max_cycles=20):
    timeline = defaultdict(list)  # ciclo → [acciones]
    held_resources = {}           # recurso → (pid, release_time)

    actions_by_cycle = defaultdict(list)
    for action in actions:
        actions_by_cycle[action.cycle].append(action)

    current_cycle = 0
    pending_actions = []

    print("Simulación de Mutex")

    while current_cycle < max_cycles:
        print(f"\n Ciclo {current_cycle}:")

        # Liberar recursos ocupados si corresponde
        to_release = [res for res, (_, release_time) in held_resources.items() if release_time <= current_cycle]
        for res in to_release:
            resources[res].available += 1
            print(f"Recurso {res} liberado")
            del held_resources[res]

        # Agregar acciones nuevas del ciclo actual
        current_actions = actions_by_cycle[current_cycle] + pending_actions
        pending_actions = []

        for action in current_actions:
            res = action.resource_name
            if resources[res].available > 0:
                # Acceso exitoso
                resources[res].available -= 1
                held_resources[res] = (action.pid, current_cycle + 1)
                timeline[current_cycle].append((action.pid, action.action_type, res, "ACCESSED"))
                print(f"{action.pid} {action.action_type} {res} → ACCESSED")
            else:
                # Espera
                timeline[current_cycle].append((action.pid, action.action_type, res, "WAITING"))
                pending_actions.append(action)
                print(f"{action.pid} {action.action_type} {res} → WAITING")

        current_cycle += 1

    return timeline

def print_mutex_timeline_ascii(timeline, max_cycles=20):
    # Obtener todos los procesos únicos
    process_names = set()
    for entries in timeline.values():
        for pid, *_ in entries:
            process_names.add(pid)

    process_names = sorted(list(process_names))
    process_lines = {pid: ["." for _ in range(max_cycles)] for pid in process_names}

    for cycle in range(max_cycles):
        for entry in timeline.get(cycle, []):
            pid, _, _, status = entry
            symbol = "A" if status == "ACCESSED" else "W"
            process_lines[pid][cycle] = symbol

    print("\n Diagrama de Accesos por Proceso (ASCII):\n")
    print("     " + " ".join(f"{i:>2}" for i in range(max_cycles)))
    for pid in process_names:
        print(f"{pid:>3}:  " + "  ".join(process_lines[pid]))



def plot_mutex_gantt(timeline, max_cycles=20):
    process_names = sorted({entry[0] for actions in timeline.values() for entry in actions})
    process_map = {pid: idx for idx, pid in enumerate(process_names)}
    
    fig, ax = plt.subplots(figsize=(12, 2 + len(process_names)))
    
    for cycle in range(max_cycles):
        for pid, action_type, resource, status in timeline.get(cycle, []):
            y = process_map[pid] * 10
            color = "tab:green" if status == "ACCESSED" else "tab:red"
            ax.broken_barh([(cycle, 1)], (y, 9), facecolors=color)
            ax.text(cycle + 0.1, y + 3.5, f"{action_type}", fontsize=7, color="white", weight="bold")
    
    ax.set_yticks([i * 10 + 4.5 for i in range(len(process_names))])
    ax.set_yticklabels(process_names)
    ax.set_xticks(range(0, max_cycles + 1, 1))
    ax.set_xlabel("Ciclos")
    ax.set_title("Simulación Mutex - Accesos y Esperas")
    ax.grid(True)
    plt.tight_layout()
    plt.show()

def simulate_semaphore(resources, actions, max_cycles=20):
    timeline = defaultdict(list)  # ciclo → [acciones]
    held_resources = defaultdict(list)  # recurso → list of (pid, release_time)

    actions_by_cycle = defaultdict(list)
    for action in actions:
        actions_by_cycle[action.cycle].append(action)

    current_cycle = 0
    pending_actions = []

    print("🔁 Simulación de Semáforos")

    while current_cycle < max_cycles:
        print(f"\n⏱️ Ciclo {current_cycle}:")

        # Liberar recursos ocupados si corresponde
        for res_name, holds in held_resources.items():
            releasing = [entry for entry in holds if entry[1] <= current_cycle]
            held_resources[res_name] = [entry for entry in holds if entry[1] > current_cycle]
            if releasing:
                resources[res_name].available += len(releasing)
                for entry in releasing:
                    print(f"🔓 Recurso {res_name} liberado por {entry[0]}")

        # Agregar acciones nuevas del ciclo actual
        current_actions = actions_by_cycle[current_cycle] + pending_actions
        pending_actions = []

        for action in current_actions:
            res = action.resource_name
            if resources[res].available > 0:
                # Acceso exitoso
                resources[res].available -= 1
                held_resources[res].append((action.pid, current_cycle + 1))
                timeline[current_cycle].append((action.pid, action.action_type, res, "ACCESSED"))
                print(f"✅ {action.pid} {action.action_type} {res} → ACCESSED")
            else:
                # Espera
                timeline[current_cycle].append((action.pid, action.action_type, res, "WAITING"))
                pending_actions.append(action)
                print(f"⛔ {action.pid} {action.action_type} {res} → WAITING")

        current_cycle += 1

    return timeline

