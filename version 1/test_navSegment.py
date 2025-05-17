import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import math
from collections import deque

from navPoint import load_navpoints
from navSegment import load_navsegment
from path import Path
from graph import *

# Variables globales
canvas = None
grafo = None
selected_node = [None]
fig = None
ax = None
waiting_for_neighbor_selection = False
waiting_for_path_selection = 0
origin_node = None

# Dibujar gráfico completo
def draw_graph(g):
    global canvas, fig, ax
    if canvas:
        canvas.get_tk_widget().destroy()

    fig, ax = plt.subplots(figsize=(8, 6))

    for seg in g.navSegment:
        origin = next((n for n in g.navPoint if n.number == seg.origin_number), None)
        destination = next((n for n in g.navPoint if n.number == seg.destination_number), None)
        if origin and destination:
            ax.plot([origin.longitude, destination.longitude], [origin.latitude, destination.latitude], 'k-', linewidth=0.5)

    for n in g.navPoint:
        ax.scatter(n.longitude, n.latitude, color='blue', s=10)
        ax.text(n.longitude, n.latitude, n.name, fontsize=6, alpha=0.6)

    ax.set_title("Gráfico")
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
    nav_file = filedialog.askopenfilename(title="Selecciona el archivo de NavPoints (Cat_nav.txt)", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not nav_file:
        return

    grafo = Graph()
    navpoints = load_navpoints(nav_file)
    for np in navpoints:
        AddNavPoint(grafo, np)

    seg_file = filedialog.askopenfilename(title="Selecciona el archivo de segmentos (Cat_seg.txt)", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not seg_file:
        return

    load_navsegment(seg_file, grafo)
    draw_graph(grafo)

root = tk.Tk()
root.title("Visualizador")
root.geometry("900x700")

btn_cargar = tk.Button(root, text="Cargar NavPoints y NavSegmentos", command=load_and_draw)
btn_cargar.pack(pady=10)

btn_todos = tk.Button(root, text="Volver gráfico completo", command=lambda: draw_graph(grafo) if grafo else None)
btn_todos.pack(pady=5)

plot_frame = tk.Frame(root)
plot_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()