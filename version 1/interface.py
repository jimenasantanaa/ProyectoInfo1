# Importaciones
import tkinter as tk
from tkinter import messagebox, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import math
from collections import deque
from navPoint import *
from navSegment import *
from path import *
from graph import *
from NavAirport import *
from airSpace import *
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

# Variables globales
grafo = None
airports = []
canvas = None
fig = None
ax = None
selected_node = [None]
origin_node = None
waiting_for_neighbor_selection = False
waiting_for_path_selection = 0
segment_color = 'black'
node_color = 'black'
modo_visualizacion = "completo"


def añadir_icono(ax, image_path, x, y, zoom=0.1, rotation=0, flip=False):
    pil_img = Image.open(image_path).convert("RGBA")

    if flip:
        pil_img = ImageOps.mirror(pil_img)

    pil_img = pil_img.rotate(rotation, expand=True)
    img = np.array(pil_img)

    imagebox = OffsetImage(img, zoom=zoom)
    ab = AnnotationBbox(imagebox, (x, y), frameon=False, zorder=999)
    ax.add_artist(ab)


# Función para dibujar el gráfico completo
def draw_graph(g):
    global canvas, fig, ax, modo_visualizacion
    modo_visualizacion = "completo"

    if canvas:
        canvas.get_tk_widget().destroy()

    fig, ax = plt.subplots(figsize=(8, 6))

    for seg in g.navSegment:
        origin = next((n for n in g.navPoint if n.number == seg.origin_number), None)
        destination = next((n for n in g.navPoint if n.number == seg.destination_number), None)
        if origin and destination:
            ax.plot([origin.longitude, destination.longitude], [origin.latitude, destination.latitude], color=segment_color, linewidth=0.5)

    for n in g.navPoint:
        ax.scatter(n.longitude, n.latitude, color=node_color, s=10)
        ax.text(n.longitude, n.latitude, n.name, fontsize=6, alpha=0.6)

    ax.set_title("Gráfico")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.mpl_connect("button_press_event", on_click)


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


def preparar_mostrar_vecinos():
    global waiting_for_neighbor_selection
    waiting_for_neighbor_selection = True
    messagebox.showinfo("Selecciona nodo", "Haz clic en un nodo para mostrar sus vecinos.")


def mostrar_vecinos():
    global modo_visualizacion
    modo_visualizacion = "vecinos"

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
        ax.scatter(n.longitude, n.latitude, color=node_color, s=8)
        ax.text(n.longitude, n.latitude, n.name, fontsize=6, alpha=0.5)

    for seg in grafo.navSegment:
        origin = next((n for n in grafo.navPoint if n.number == seg.origin_number), None)
        destination = next((n for n in grafo.navPoint if n.number == seg.destination_number), None)
        if origin and destination:
            if origin == nodo or destination == nodo:
                ax.plot([origin.longitude, destination.longitude], [origin.latitude, destination.latitude], 'c-', linewidth=0.5)

    ax.plot(nodo.longitude, nodo.latitude, 'ro')
    ax.text(nodo.longitude, nodo.latitude, nodo.name, fontsize=8, color=node_color)

    for vecino in vecinos:
        ax.plot(vecino.longitude, vecino.latitude, 'bo')
        ax.text(vecino.longitude, vecino.latitude, vecino.name, fontsize=6, alpha=0.6)
        ax.plot([nodo.longitude, vecino.longitude], [nodo.latitude, vecino.latitude], 'c-', linewidth=0.5)

    canvas.draw()

    export_neighbors_to_kml(nodo, vecinos, grafo.navSegment)
    messagebox.showinfo("Exportación KML", "Se ha modificado 'neighbors.kml' con el nodo y los vecinos actuales.")


def preparar_camino_mas_corto():
    global waiting_for_path_selection
    waiting_for_path_selection = 1
    messagebox.showinfo("Selecciona origen", "Haz clic en el nodo de origen del camino más corto.")


# Función para mostrar el camino más corto (con clicks)
def mostrar_camino_mas_corto(origen, destino):
    global modo_visualizacion
    modo_visualizacion = "camino"

    ruta = FindShortestPath(grafo, origen, destino)

    if not ruta:
        messagebox.showerror("Error", "No se encontró camino entre los puntos seleccionados.")
        return

    draw_graph(grafo)

    for i in range(len(ruta.navPoints) - 1):
        n1, n2 = ruta.navPoints[i], ruta.navPoints[i + 1]
        ax.plot([n1.longitude, n2.longitude], [n1.latitude, n2.latitude], 'r-', linewidth=3, zorder=5)
        ax.annotate('', xy=(n2.longitude, n2.latitude), xytext=(n1.longitude, n1.latitude),
                    arrowprops=dict(facecolor=segment_color, edgecolor=segment_color, arrowstyle='->', lw=2), zorder=6)

    for n in ruta.navPoints:
        ax.scatter(n.longitude, n.latitude, color=segment_color, s=40, zorder=7)
        ax.text(n.longitude, n.latitude, n.name, fontsize=9, ha='right', color=segment_color, zorder=8)

    # Coordenadas de inicio y fin del camino
    origen_x, origen_y = ruta.navPoints[0].longitude, ruta.navPoints[0].latitude
    destino_x, destino_y = ruta.navPoints[-1].longitude, ruta.navPoints[-1].latitude

    # Si el destino está a la izquierda del origen, volteamos la imagen
    flip = destino_x < origen_x

    # Avión despegando
    añadir_icono(ax, "avion.png", origen_x, origen_y, zoom=0.06, flip=flip)

    # Avión aterrizando (rotar primero, luego reflejar si hace falta)
    pil_img = Image.open("avion.png").convert("RGBA")
    pil_img = pil_img.rotate(310, expand=True)
    if flip:
        pil_img = ImageOps.mirror(pil_img)

    img = np.array(pil_img)
    imagebox = OffsetImage(img, zoom=0.06)
    ab = AnnotationBbox(imagebox, (destino_x, destino_y), frameon=False, zorder=999)
    ax.add_artist(ab)

    canvas.draw()

    export_path_to_kml(ruta)
    messagebox.showinfo("KML generado", "Se ha modificado 'shortest_path.kml' con el camino más corto actual.")


# Función para mostrar el camino más corto (por aeropuerto)
def camino_mas_corto_por_aeropuerto():
    global airports, grafo

    if not grafo or not airports:
        messagebox.showwarning("Advertencia", "Carga los archivos primero.")
        return

    nombres = [a.name for a in airports]

    origen = simpledialog.askstring("Aeropuerto origen", f"Introduce el aeropuerto de origen: ")
    if origen is None or origen not in nombres:
        messagebox.showerror("Error", "Aeropuerto de origen no válido o cancelado.")
        return

    destino = simpledialog.askstring("Aeropuerto destino", f"Introduce el aeropuerto de destino: ")
    if destino is None or destino not in nombres:
        messagebox.showerror("Error", "Aeropuerto de destino no válido o cancelado.")
        return

    aeropuerto_origen = next(a for a in airports if a.name == origen)
    aeropuerto_destino = next(a for a in airports if a.name == destino)

    if not aeropuerto_origen.sid:
        messagebox.showerror("Error", f"El aeropuerto {aeropuerto_origen.name} no tiene SID asociado.")
        return

    if not aeropuerto_destino.star:
        messagebox.showerror("Error", f"El aeropuerto {aeropuerto_destino.name} no tiene STAR asociado.")
        return

    nodo_sid = aeropuerto_origen.sid[0]
    nodo_star = aeropuerto_destino.star[0]

    ruta = FindShortestPath(grafo, nodo_sid, nodo_star)

    if not ruta:
        messagebox.showerror("Error", "No se encontró camino entre los aeropuertos seleccionados.")
        return

    draw_graph(grafo)

    for i in range(len(ruta.navPoints) - 1):
        n1, n2 = ruta.navPoints[i], ruta.navPoints[i + 1]
        ax.plot([n1.longitude, n2.longitude], [n1.latitude, n2.latitude], 'r-', linewidth=3, zorder=5)
        ax.annotate('', xy=(n2.longitude, n2.latitude), xytext=(n1.longitude, n1.latitude),
                    arrowprops=dict(facecolor=segment_color, edgecolor=segment_color, arrowstyle='->', lw=2), zorder=6)

    for n in ruta.navPoints:
        ax.scatter(n.longitude, n.latitude, color=segment_color, s=40, zorder=7)
        ax.text(n.longitude, n.latitude, n.name, fontsize=9, ha='right', color=segment_color, zorder=8)

    # Coordenadas de inicio y fin del camino
    origen_x, origen_y = ruta.navPoints[0].longitude, ruta.navPoints[0].latitude
    destino_x, destino_y = ruta.navPoints[-1].longitude, ruta.navPoints[-1].latitude

    # Si el destino está a la izquierda del origen, volteamos la imagen
    flip = destino_x < origen_x

    # Avión despegando
    añadir_icono(ax, "avion.png", origen_x, origen_y, zoom=0.06, flip=flip)

    # Avión aterrizando (rotar primero, luego reflejar si hace falta)
    pil_img = Image.open("avion.png").convert("RGBA")
    pil_img = pil_img.rotate(310, expand=True)
    if flip:
        pil_img = ImageOps.mirror(pil_img)

    img = np.array(pil_img)
    imagebox = OffsetImage(img, zoom=0.06)
    ab = AnnotationBbox(imagebox, (destino_x, destino_y), frameon=False, zorder=999)
    ax.add_artist(ab)

    canvas.draw()

    export_path_to_kml(ruta, "shortest_path.kml")
    messagebox.showinfo("KML generado", "Se ha modificado 'shortest_path.kml' con el camino actual.")

def seleccionar_espacio_aereo_con_colores():
    seleccion = tk.Tk()
    seleccion.title("Opciones iniciales")
    seleccion.geometry("400x250")

    global segment_color, node_color
    node_color = "black"
    segment_color = "black"

    # === 1. Color de puntos ===
    tk.Label(seleccion, text="1. Elige el color de los puntos:").pack()
    color_punto_frame = tk.Frame(seleccion)
    color_punto_frame.pack()

    def set_node_color(color):
        global node_color
        node_color = color

    def crear_selector_color_punto(frame, color):
        canvas = tk.Canvas(frame, width=30, height=30, highlightthickness=0, bg=seleccion["bg"])
        canvas.pack(side=tk.LEFT, padx=5)
        circle = canvas.create_oval(5, 5, 25, 25, fill=color, outline="black")
        canvas.tag_bind(circle, "<Button-1>", lambda event: set_node_color(color))

    for color in ["black", "red", "blue"]:
        crear_selector_color_punto(color_punto_frame, color)

    # === 2. Color de segmentos ===
    tk.Label(seleccion, text="2. Elige el color de los segmentos:").pack(pady=(10, 0))
    color_segmento_frame = tk.Frame(seleccion)
    color_segmento_frame.pack()

    def set_segment_color(color):
        global segment_color
        segment_color = color

    def crear_selector_color_segmento(frame, color):
        canvas = tk.Canvas(frame, width=30, height=30, highlightthickness=0, bg=seleccion["bg"])
        canvas.pack(side=tk.LEFT, padx=5)
        circle = canvas.create_oval(5, 5, 25, 25, fill=color, outline="black")
        canvas.tag_bind(circle, "<Button-1>", lambda event: set_segment_color(color))

    for color in ["black", "red", "blue"]:
        crear_selector_color_segmento(color_segmento_frame, color)

    # === 3. Selección del espacio aéreo ===
    tk.Label(seleccion, text="3. Elige el espacio aéreo:").pack(pady=(10, 0))
    espacio_frame = tk.Frame(seleccion)
    espacio_frame.pack(pady=5)

    def elegir(prefix):
        seleccion.destroy()
        main_interface(prefix)

    tk.Button(espacio_frame, text="Cataluña", command=lambda: elegir("Cat")).pack(side=tk.LEFT, padx=5)
    tk.Button(espacio_frame, text="España", command=lambda: elegir("Spain")).pack(side=tk.LEFT, padx=5)
    tk.Button(espacio_frame, text="Europa", command=lambda: elegir("ECAC")).pack(side=tk.LEFT, padx=5)

    seleccion.mainloop()

def main_interface(prefix):
    global root, plot_frame, grafo, airports
    grafo, airports_dict = load_airspace(prefix)
    airports = list(airports_dict.values())

    export_navpoints_to_kml(grafo.navPoint, f"points.kml")
    export_navsegments_to_kml(grafo.navSegment, grafo.navPoint, f"segments.kml")

    root = tk.Tk()
    root.title("Visualizador")
    root.geometry("900x700")

    button_frame = tk.Frame(root)
    button_frame.pack(anchor='nw', pady=5, padx=5)

    tk.Button(button_frame, text="Mostrar vecinos", command=preparar_mostrar_vecinos).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Camino más corto", command=preparar_camino_mas_corto).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Volver gráfico completo", command=lambda: draw_graph(grafo)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Camino más corto (por aeropuerto)", command=camino_mas_corto_por_aeropuerto).pack(side=tk.LEFT, padx=5)

    plot_frame = tk.Frame(root)
    plot_frame.pack(fill=tk.BOTH, expand=True)

    draw_graph(grafo)
    root.mainloop()


# Lanzar la interfaz inicial
seleccionar_espacio_aereo_con_colores()