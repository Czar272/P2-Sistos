import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from utils.sync_parser import parse_resources, parse_actions
from sync.sync_simulator import simulate_mutex, simulate_semaphore, plot_mutex_gantt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class SyncGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Sincronización")
        self.geometry("900x600")

        self.is_paused = False
        self.restart_requested = False


        self.mode = tk.StringVar()
        self.paths = {
            "recursos": None,
            "acciones": None
        }

        self.create_widgets()

    def create_widgets(self):
        # Selector de modo (mutex / semáforo)
        ttk.Label(self, text="Modo de sincronización:").pack(pady=5)
        mode_menu = ttk.Combobox(self, textvariable=self.mode, state="readonly")
        mode_menu["values"] = ["Mutex", "Semáforo"]
        mode_menu.pack()

        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(pady=5)

        ttk.Button(self.control_frame, text="⏸ Pausar/Reanudar", command=self.toggle_pause).pack(side="left", padx=5)
        ttk.Button(self.control_frame, text="🔄 Reiniciar", command=self.restart_animation).pack(side="left", padx=5)
        ttk.Button(self.control_frame, text="💾 Exportar PNG", command=self.export_image).pack(side="left", padx=5)


        # Botones para cargar archivos
        ttk.Button(self, text="Cargar recursos.txt", command=lambda: self.load_file("recursos")).pack(pady=2)
        ttk.Button(self, text="Cargar acciones.txt", command=lambda: self.load_file("acciones")).pack(pady=2)

        # Botón para ejecutar simulación
        ttk.Button(self, text="Simular", command=self.run_simulation).pack(pady=10)

        # Frame gráfico
        self.graph_frame = ttk.Frame(self)
        self.graph_frame.pack(fill="both", expand=True)

    def load_file(self, file_type):
        path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if path:
            self.paths[file_type] = path
            messagebox.showinfo("Archivo cargado", f"{file_type}.txt cargado:\n{path}")

    def run_simulation(self):
        if not self.mode.get():
            messagebox.showerror("Error", "Selecciona modo: Mutex o Semáforo.")
            return
        if not self.paths["recursos"] or not self.paths["acciones"]:
            messagebox.showerror("Error", "Debes cargar ambos archivos: recursos y acciones.")
            return

        try:
            resources = parse_resources(self.paths["recursos"])
            actions = parse_actions(self.paths["acciones"])

            if self.mode.get() == "Mutex":
                timeline = simulate_mutex(resources, actions)
            else:
                timeline = simulate_semaphore(resources, actions)

            self.show_graph(timeline)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
    
    def animate_cycle(self):
        if self.is_paused:
            self.after(200, self.animate_cycle)
            return

        if self.restart_requested:
            return  # Se reiniciará desde otra función

        if self.current_cycle >= self.max_cycles:
            self.canvas.draw()
            return

        entries = self.timeline.get(self.current_cycle, [])
        for pid, action_type, resource, status in entries:
            y = self.process_map[pid] * 10
            color = "tab:green" if status == "ACCESSED" else "tab:red"
            self.ax.broken_barh([(self.current_cycle, 1)], (y, 9), facecolors=color)
            self.ax.text(self.current_cycle + 0.1, y + 3, action_type, fontsize=7, color="white", weight="bold")

        self.current_cycle += 1
        self.canvas.draw()
        self.after(300, self.animate_cycle)



    def show_graph(self, timeline, max_cycles=20):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # --- Preparar figura y eje
        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # --- Datos necesarios para animación
        self.timeline = timeline
        self.current_cycle = 0
        self.max_cycles = max_cycles

        self.process_names = sorted({entry[0] for actions in timeline.values() for entry in actions})
        self.process_map = {pid: idx for idx, pid in enumerate(self.process_names)}

        self.ax.set_yticks([i * 10 + 4.5 for i in range(len(self.process_names))])
        self.ax.set_yticklabels(self.process_names)
        self.ax.set_xticks(range(0, max_cycles + 1, 1))
        self.ax.set_xlabel("Ciclos")
        self.ax.set_title(f"Gantt Paso a Paso - {self.mode.get()}")
        self.ax.grid(True)

        # Iniciar animación
        self.animate_cycle()

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def restart_animation(self):
        self.restart_requested = True
        self.current_cycle = 0
        self.ax.cla()
        self.ax.set_yticks([i * 10 + 4.5 for i in range(len(self.process_names))])
        self.ax.set_yticklabels(self.process_names)
        self.ax.set_xticks(range(0, self.max_cycles + 1, 1))
        self.ax.set_xlabel("Ciclos")
        self.ax.set_title(f"Gantt Paso a Paso - {self.mode.get()}")
        self.ax.grid(True)
        self.canvas.draw()
        self.restart_requested = False
        self.animate_cycle()

    def export_image(self):
        from tkinter import filedialog
        filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if filepath:
            self.fig.savefig(filepath)
            messagebox.showinfo("Exportado", f"Gráfico guardado en:\n{filepath}")
