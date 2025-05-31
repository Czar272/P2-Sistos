# P2-Sistos

Sistemas Operativos Proyecto - # 2: Simulador

## Descripción General

Este proyecto implementa un simulador visual interactivo para el curso de Sistemas Operativos. Incluye:

- Simulación de algoritmos de **planificación de procesos**
- Simulación de mecanismos de **sincronización** (mutex y semáforos)
- **Interfaz gráfica** desarrollada con `tkinter`
- **Visualización paso a paso** con animación Gantt usando `matplotlib`

## Archivos de Entrada

### procesos.txt (para planificación)

```
P1, 6, 0, 2     # PID, BurstTime, ArrivalTime, Priority
P2, 2, 1, 1
... etc.
```

### recursos.txt (para sincronización)

```
R1, 2           # Nombre del recurso, cantidad de instancias
R2, 1
```

### acciones.txt (para sincronización)

```
P1, READ, R1, 0     # PID, Acción (READ/WRITE), Recurso, Ciclo
P2, WRITE, R2, 2
```

---

## Instrucciones de Ejecución

### GUI interactiva

```bash
python gui/main_menu.py
```

Desde ahí podrás elegir:

- Planificación de procesos
- Sincronización con recursos

### Modo consola

```bash
python run.py    # Ejecuta el simulador por consola
```

---

## ⚖️ Algoritmos Soportados

### Planificación:

- FIFO
- SJF (no expulsivo)
- SRT (expulsivo)
- Round Robin (cuanto de 2 ciclos)
- Prioridad (no expulsiva)

### Sincronización:

- Mutex (1 instancia)
- Semáforo (múltiples instancias)

---

## Visualización Interactiva

- Paso a paso por ciclo
- Colores: Verde = acceso exitoso, Rojo = esperando
- Exportación a imagen `.png`
- Botones para **pausar**, **reiniciar**, **guardar**
