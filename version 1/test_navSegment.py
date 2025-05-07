import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import math

from navPoint import load_navpoints
from navSegment import load_navsegment
from node import *
from segment import *
from graph import *  # <- Aquí ya está importado GetNavNeighbors

# Variables globales
canvas = None
grafo = None
selected_node = [None]
fig = None
ax = None

# Selección por clic
def on_click(event):
    if grafo is None:
        return
    x, y = event.xdata, event.ydata
    if x is None or y is None:
        return

    closest = min(grafo.navPoint, key=lambda n: math.hypot(n.longitude - x, n.latitude - y))
    selected_node[0] = closest
    messagebox.showinfo("Nodo seleccionado", f"Has seleccionado el nodo: {closest.name}")

# Mostrar solo los vecinos del nodo
def mostrar_vecinos():
    if selected_node[0] is None:
        messagebox.showwarning("Advertencia", "Por favor selecciona un nodo haciendo clic en el gráfico.")
        return

    nodo = selected_node[0]
    vecinos = GetNavNeighbors(grafo, nodo)

    # Dibujar vecinos
    global ax, fig, canvas
    ax.clear()
    ax.set_title(f"Vecinos de {nodo.name}")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.grid(True)

    ax.plot(nodo.longitude, nodo.latitude, 'ro')
    ax.text(nodo.longitude, nodo.latitude, nodo.name, fontsize=8, color='red')

    for vecino in vecinos:
        ax.plot(vecino.longitude, vecino.latitude, 'bo')
        ax.text(vecino.longitude, vecino.latitude, vecino.name, fontsize=6, alpha=0.6)
        ax.plot([nodo.longitude, vecino.longitude], [nodo.latitude, vecino.latitude], 'k--', linewidth=0.8)

    canvas.draw()

# Dibujar gráfico completo
def draw_graph(g):
    global canvas, fig, ax
    if canvas:
        canvas.get_tk_widget().destroy()

    fig, ax = plt.subplots(figsize=(8, 6))

    lats = [n.latitude for n in g.navPoint]
    longs = [n.longitude for n in g.navPoint]
    names = [n.name for n in g.navPoint]

    ax.scatter(longs, lats, s=10, c='blue')
    for i, name in enumerate(names):
        ax.text(longs[i], lats[i], name, fontsize=6, alpha=0.6)

    for seg in g.navSegment:
        origin = next((n for n in g.navPoint if n.number == seg.origin_number), None)
        destination = next((n for n in g.navPoint if n.number == seg.destination_number), None)
        if origin and destination:
            ax.plot([origin.longitude, destination.longitude], [origin.latitude, destination.latitude], 'k-', linewidth=0.5)

    ax.set_title("Red de Navegación Aérea")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    canvas.mpl_connect("button_press_event", on_click)

# Cargar y dibujar datos
def load_and_draw():
    global grafo
    nav_file = filedialog.askopenfilename(
        title="Selecciona el archivo de NavPoints (Cat_nav.txt)",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not nav_file:
        return

    grafo = load_navpoints(nav_file)

    seg_file = filedialog.askopenfilename(
        title="Selecciona el archivo de segmentos (Cat_seg.txt)",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not seg_file:
        return

    load_navsegment(seg_file, grafo)
    draw_graph(grafo)

# --- Interfaz ---
root = tk.Tk()
root.title("Visualizador de Rutas Aéreas")
root.geometry("900x700")

btn_cargar = tk.Button(root, text="Cargar NavPoints y Segmentos", command=load_and_draw)
btn_cargar.pack(pady=10)

btn_vecinos = tk.Button(root, text="Mostrar vecinos del nodo seleccionado", command=mostrar_vecinos)
btn_vecinos.pack(pady=5)

btn_todos = tk.Button(root, text="Volver al gráfico completo", command=lambda: draw_graph(grafo) if grafo else None)
btn_todos.pack(pady=5)

plot_frame = tk.Frame(root)
plot_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()
