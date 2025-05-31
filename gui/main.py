import tkinter as tk
from scheduler_gui import SchedulerGUI
from sync_gui import SyncGUI

def open_scheduler():
    app.destroy()
    SchedulerGUI().mainloop()

def open_sync():
    app.destroy()
    SyncGUI().mainloop()

app = tk.Tk()
app.title("Simulador 2025 - Sistema Operativo")
app.geometry("400x200")

tk.Label(app, text="Seleccione el tipo de simulación:", font=("Arial", 12)).pack(pady=20)

tk.Button(app, text="Calendarización", width=20, command=open_scheduler).pack(pady=5)
tk.Button(app, text="Sincronización", width=20, command=open_sync).pack(pady=5)

app.mainloop()
