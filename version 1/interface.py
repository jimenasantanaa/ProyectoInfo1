import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import math
from collections import deque

from navPoint import load_navpoints
from navSegment import load_navsegment
from path import Path
from graph import Graph, AddNavPoint, GetNavNeighbors

# Variables globales
canvas = None
grafo = None
selected_node = [None]
fig = None
ax = None
waiting_for_neighbor_selection = False
waiting_for_path_selection = 0
origin_node = None

# Selección click
def on_click(event):
    global waiting_for_neighbor_selection, waiting_for_path_selection, selected_node, origin_node

    if grafo is None:
        return
    x, y = event.xdata, event.ydata
    if x is None or y is None:
        return

    closest = min(grafo.navPoint, key=lambda n: math.hypot(n.longitude - x, n.latitude - y))
    selected_node[0] = closest

    if waiting_for_neighbor_selection:
        waiting_for_neighbor_selection = False
        mostrar_vecinos()
    elif waiting_for_path_selection == 1:
        origin_node = closest
        waiting_for_path_selection = 2
        messagebox.showinfo("Destino", f"Nodo origen seleccionado: {closest.name}. Ahora selecciona el nodo destino.")
    elif waiting_for_path_selection == 2:
        destino_node = closest
        waiting_for_path_selection = 0
        mostrar_camino_mas_corto(origin_node, destino_node)
    else:
        messagebox.showinfo("Nodo seleccionado", f"Has seleccionado el nodo: {closest.name}")

# Mostrar vecinos
def mostrar_vecinos():
    if selected_node[0] is None:
        messagebox.showwarning("Advertencia", "Por favor selecciona un nodo haciendo clic en el gráfico.")
        return

    nodo = selected_node[0]
    vecinos = GetNavNeighbors(grafo, nodo)

    ax.clear()
    ax.set_title("Gráfico")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.grid(True)

    for n in grafo.navPoint:
        ax.scatter(n.longitude, n.latitude, color='lightgray', s=8)
        ax.text(n.longitude, n.latitude, n.name, fontsize=6, alpha=0.5)

    for seg in grafo.navSegment:
        origin = next((n for n in grafo.navPoint if n.number == seg.origin_number), None)
        destination = next((n for n in grafo.navPoint if n.number == seg.destination_number), None)
        if origin and destination:
            if origin == nodo or destination == nodo:
                ax.plot([origin.longitude, destination.longitude], [origin.latitude, destination.latitude], 'c-', linewidth=0.5)

    ax.plot(nodo.longitude, nodo.latitude, 'ro')
    ax.text(nodo.longitude, nodo.latitude, nodo.name, fontsize=8, color='red')

    for vecino in vecinos:
        ax.plot(vecino.longitude, vecino.latitude, 'bo')
        ax.text(vecino.longitude, vecino.latitude, vecino.name, fontsize=6, alpha=0.6)
        ax.plot([nodo.longitude, vecino.longitude], [nodo.latitude, vecino.latitude], 'c-', linewidth=0.5)

    canvas.draw()

def preparar_mostrar_vecinos():
    global waiting_for_neighbor_selection
    waiting_for_neighbor_selection = True
    messagebox.showinfo("Selecciona nodo", "Haz clic en un nodo para mostrar sus vecinos.")

def preparar_camino_mas_corto():
    global waiting_for_path_selection
    waiting_for_path_selection = 1
    messagebox.showinfo("Selecciona origen", "Haz clic en el nodo de origen del camino más corto.")

# Mostrar camino más corto
def mostrar_camino_mas_corto(origen, destino):
    visitados = set()
    cola = deque([[origen]])
    camino_final = None

    while cola:
        camino = cola.popleft()
        actual = camino[-1]
        if actual == destino:
            camino_final = camino
            break

        visitados.add(actual)
        for vecino in GetNavNeighbors(grafo, actual):
            if vecino not in visitados:
                nueva_ruta = list(camino)
                nueva_ruta.append(vecino)
                cola.append(nueva_ruta)

    if not camino_final:
        messagebox.showerror("Error", "No se encontró camino entre los puntos seleccionados.")
        return

    ruta = Path(camino_final[0])
    for n in camino_final[1:]:
        ruta.AddNodeToPath(n)

    ax.clear()
    ax.set_title("Camino más corto")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.grid(True)

    for n in grafo.navPoint:
        ax.scatter(n.longitude, n.latitude, color='lightgray', s=8)
        ax.text(n.longitude, n.latitude, n.name, fontsize=6, alpha=0.5)

    for i in range(len(ruta.nodes) - 1):
        n1, n2 = ruta.nodes[i], ruta.nodes[i + 1]
        ax.plot([n1.longitude, n2.longitude], [n1.latitude, n2.latitude], 'r-', linewidth=2)
        ax.annotate('', xy=(n2.longitude, n2.latitude), xytext=(n1.longitude, n1.latitude),
                    arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->'))

    for n in ruta.nodes:
        ax.scatter(n.longitude, n.latitude, color='blue')
        ax.text(n.longitude, n.latitude, n.name, fontsize=8, ha='right')

    canvas.draw()

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

    airport_file = filedialog.askopenfilename(title="Selecciona el archivo de aeropuertos (Cat_aer.txt)", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not airport_file:
        return

    nav_file = filedialog.askopenfilename(title="Selecciona el archivo de puntos (Cat_nav.txt)", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not nav_file:
        return

    # Crear grafo y añadir navpoints
    grafo = Graph()
    navpoints = load_navpoints(nav_file)
    for nav in navpoints:
        AddNavPoint(grafo, nav)

    seg_file = filedialog.askopenfilename(title="Selecciona el archivo de segmentos (Cat_seg.txt)", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not seg_file:
        return

    load_navsegment(seg_file, grafo)
    draw_graph(grafo)

root = tk.Tk()
root.title("Visualizador")
root.geometry("900x700")

btn_cargar = tk.Button(root, text="Cargar archivos", command=load_and_draw)
btn_cargar.pack(pady=10)

btn_vecinos = tk.Button(root, text="Mostrar vecinos ", command=preparar_mostrar_vecinos)
btn_vecinos.pack(pady=5)

btn_camino = tk.Button(root, text="Camino más corto", command=preparar_camino_mas_corto)
btn_camino.pack(pady=5)

btn_todos = tk.Button(root, text="Volver gráfico completo", command=lambda: draw_graph(grafo) if grafo else None)
btn_todos.pack(pady=5)

plot_frame = tk.Frame(root)
plot_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()
