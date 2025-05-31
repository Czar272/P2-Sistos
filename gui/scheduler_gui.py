import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from utils.parser import parse_processes
from algorithms.fifo import fifo_schedule
from algorithms.sjf import sjf_schedule
from algorithms.srt import srt_schedule
from algorithms.round_robin import round_robin_schedule
from algorithms.priority import priority_schedule
import subprocess, sys


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class SchedulerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Algoritmos de Calendarización")
        self.geometry("900x600")

        self.is_paused = False
        self.restart_requested = False


        self.file_path = None
        self.selected_algo = tk.StringVar()
        self.quantum = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Dropdown de algoritmo
        ttk.Label(self, text="Algoritmo:").pack(pady=5)
        algo_menu = ttk.Combobox(self, textvariable=self.selected_algo, state="readonly")
        algo_menu["values"] = ["FIFO", "SJF", "SRT", "Round Robin", "Priority"]
        algo_menu.pack()

        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(pady=5)

        ttk.Button(self, text="⬅ Regresar al Menú Principal", command=self.back_to_menu).pack(pady=5)
        ttk.Button(self.control_frame, text="⏸ Pausar/Reanudar", command=self.toggle_pause).pack(side="left", padx=5)
        ttk.Button(self.control_frame, text="🔄 Reiniciar", command=self.restart_animation).pack(side="left", padx=5)
        ttk.Button(self.control_frame, text="💾 Exportar PNG", command=self.export_image).pack(side="left", padx=5)


        # Campo de quantum
        self.quantum_frame = ttk.Frame(self)
        ttk.Label(self.quantum_frame, text="Quantum:").pack(side="left", padx=5)
        ttk.Entry(self.quantum_frame, textvariable=self.quantum, width=5).pack(side="left")
        self.quantum_frame.pack(pady=5)

        # Ocultar quantum si no es RR
        self.selected_algo.trace_add("write", self.toggle_quantum)

        # Botón cargar archivo
        ttk.Button(self, text="Cargar archivo de procesos", command=self.load_file).pack(pady=5)

        self.file_label = ttk.Label(self, text="Archivo no cargado", foreground="gray")
        self.file_label.pack(pady=2)


        # Botón de simulación
        ttk.Button(self, text="Simular", command=self.run_simulation).pack(pady=10)
        ttk.Button(self, text="Limpiar Campos", command=self.clear_fields).pack(pady=5)


        # Área para gráficos
        self.graph_frame = ttk.Frame(self)
        self.graph_frame.pack(fill="both", expand=True)

    def toggle_quantum(self, *args):
        if self.selected_algo.get() == "Round Robin":
            self.quantum_frame.pack(pady=5)
        else:
            self.quantum_frame.forget()
    
    def clear_fields(self):
        self.selected_algo.set("")
        self.quantum.set("")
        self.file_path = None
        self.file_label.config(text="Archivo no cargado", foreground="gray")


    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if path:
            self.file_path = path
            filename = os.path.basename(path)
            self.file_label.config(text=f"📄 {filename} cargado", foreground="green")


    def run_simulation(self):
        if not self.file_path or not self.selected_algo.get():
            messagebox.showerror("Error", "Selecciona un algoritmo y carga un archivo.")
            return

        processes = parse_processes(self.file_path)
        algo = self.selected_algo.get()
        if algo == "FIFO":
            timeline, updated = fifo_schedule(processes)
        elif algo == "SJF":
            timeline, updated = sjf_schedule(processes)
        elif algo == "SRT":
            timeline, updated = srt_schedule(processes)
        elif algo == "Round Robin":
            try:
                q = int(self.quantum.get())
            except ValueError:
                messagebox.showerror("Error", "Quantum inválido.")
                return
            timeline, updated = round_robin_schedule(processes, q)
        elif algo == "Priority":
            timeline, updated = priority_schedule(processes)
        else:
            return

        self.show_gantt(timeline, updated)

    def show_gantt(self, timeline, processes):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        self.fig, self.ax = plt.subplots(figsize=(10, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.timeline = timeline
        self.process_names = sorted({pid for pid, _, _ in timeline})
        self.process_map = {pid: i for i, pid in enumerate(self.process_names)}
        self.max_time = max(end for _, _, end in timeline)

        self.current_segment = 0
        self.prepare_axes()
        self.animate_schedule()

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def restart_animation(self):
        self.restart_requested = True
        self.current_segment = 0
        self.ax.cla()
        self.prepare_axes()
        self.canvas.draw()
        self.restart_requested = False
        self.animate_schedule()

    def export_image(self):
        from tkinter import filedialog, messagebox
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if path:
            self.fig.savefig(path)
            messagebox.showinfo("Exportado", f"Gráfico guardado en:\n{path}")

    def prepare_axes(self):
        self.ax.set_yticks([i * 10 + 4.5 for i in range(len(self.process_names))])
        self.ax.set_yticklabels(self.process_names)
        self.ax.set_xticks(range(0, self.max_time + 2))
        self.ax.set_xlabel("Ciclos")
        self.ax.set_title("Simulación Calendarización Paso a Paso")
        self.ax.grid(True)

    def animate_schedule(self):
        if self.is_paused:
            self.after(200, self.animate_schedule)
            return

        if self.restart_requested:
            return

        if self.current_segment >= len(self.timeline):
            self.canvas.draw()
            return

        pid, start, end = self.timeline[self.current_segment]
        y = self.process_map[pid] * 10
        self.ax.broken_barh([(start, end - start)], (y, 9), facecolors="tab:blue")
        self.ax.text(start + 0.2, y + 3, pid, color="white", fontsize=8)

        self.current_segment += 1
        self.canvas.draw()
        self.after(500, self.animate_schedule)
    
    def back_to_menu(self):
        self.destroy()
        subprocess.Popen([sys.executable, "gui/main.py"])



