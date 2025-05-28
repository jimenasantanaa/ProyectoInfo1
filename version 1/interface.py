# Importaciones
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
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
from PIL import Image, ImageOps
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
ruta_manual = []
esperando_ruta_manual = False
selected_node_color_canvas = None
selected_segment_color_canvas = None
añadiendo_navpoint = False
añadiendo_navsegment = 0  # 0 = inactivo, 1 = esperando origen, 2 = esperando destino
navsegment_origen = None
esperando_eliminar_navpoint = False


# Añadir imagen del avión
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

# Función para hacer click en el gráfico
def on_click(event):
    global waiting_for_neighbor_selection, waiting_for_path_selection, selected_node, origin_node, ruta_manual, añadiendo_navpoint, navsegment_origen, añadiendo_navsegment, esperando_eliminar_navpoint

    if grafo is None:
        return
    x, y = event.xdata, event.ydata
    if x is None or y is None:
        return

    if not grafo.navPoint:
        closest = None
    else:
        closest = min(grafo.navPoint, key=lambda n: math.hypot(n.longitude - x, n.latitude - y))

    selected_node[0] = closest

    if esperando_eliminar_navpoint:
        esperando_eliminar_navpoint = False
        navpoint = closest

        confirm = messagebox.askyesno("Confirmar eliminación",
                                      f"¿Eliminar '{navpoint.name}' y sus segmentos?")
        if not confirm:
            return

        grafo.navSegment = [s for s in grafo.navSegment
                            if s.origin_number != navpoint.number and s.destination_number != navpoint.number]
        grafo.navPoint = [n for n in grafo.navPoint if n.number != navpoint.number]
        selected_node[0] = None
        export_navpoints_to_kml(grafo.navPoint)
        export_navsegments_to_kml(grafo.navSegment, grafo.navPoint)
        draw_graph(grafo)
        messagebox.showinfo("Eliminado", f"'{navpoint.name}' y sus segmentos han sido eliminados.")
        return

    elif waiting_for_neighbor_selection:
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

    elif esperando_ruta_manual:
        if len(ruta_manual) == 0:
            ruta_manual.append(closest)
            ax.scatter(closest.longitude, closest.latitude, color=segment_color, s=60, zorder=10)
            ax.text(closest.longitude, closest.latitude, closest.name, fontsize=9, color=segment_color, zorder=11)
        else:
            origen = ruta_manual[-1]
            destino = closest
            subruta = FindShortestPath(grafo, origen, destino)

            if not subruta:
                messagebox.showerror("Error", f"No se encontró camino entre {origen.name} y {destino.name}.")
                return

            for punto in subruta.navPoints[1:]:
                ruta_manual.append(punto)

            for i in range(len(subruta.navPoints) - 1):
                p1 = subruta.navPoints[i]
                p2 = subruta.navPoints[i + 1]
                ax.plot([p1.longitude, p2.longitude], [p1.latitude, p2.latitude], color=segment_color, linewidth=2, zorder=9)
                ax.annotate('', xy=(p2.longitude, p2.latitude), xytext=(p1.longitude, p1.latitude),
                            arrowprops=dict(facecolor=segment_color, edgecolor=segment_color, arrowstyle='->', lw=2), zorder=10)

            for punto in subruta.navPoints[1:]:
                ax.scatter(punto.longitude, punto.latitude, color=segment_color, s=60, zorder=10)
                ax.text(punto.longitude, punto.latitude, punto.name, fontsize=9, color=segment_color, zorder=11)

        canvas.draw()
        return

    elif añadiendo_navpoint:
        nombre = simpledialog.askstring("Nombre", "Introduce el nombre del NavPoint:")
        if not nombre:
            return

        nombre = nombre.strip().upper()

        # Verifica que no existe ya un punto con ese nombre
        if any(p.name.upper() == nombre for p in grafo.navPoint):
            messagebox.showwarning("Nombre duplicado", f"Ya existe un NavPoint con el nombre '{nombre}'.")
            return

        nuevo_numero = max((n.number for n in grafo.navPoint), default=0) + 1
        nuevo = NavPoint(nuevo_numero, nombre, latitude=y, longitude=x)
        grafo.navPoint.append(nuevo)

        ax.scatter(x, y, color=node_color, s=10)
        ax.text(x, y, nombre, fontsize=6, alpha=0.6)
        canvas.draw()
        export_navpoints_to_kml(grafo.navPoint)
        export_navsegments_to_kml(grafo.navSegment, grafo.navPoint)

        añadiendo_navpoint = False
        messagebox.showinfo("NavPoint creado", f"'{nombre}' ha sido añadido correctamente.")
        return

    elif añadiendo_navsegment == 1:
        navsegment_origen = closest
        añadiendo_navsegment = 2
        messagebox.showinfo("Destino", f"Origen: {closest.name}. Ahora haz clic en el destino.")
        return

    elif añadiendo_navsegment == 2:
        navsegment_destino = closest
        nuevo = NavSegment(navsegment_origen.number, navsegment_destino.number, Distance(navsegment_origen, navsegment_destino))
        grafo.navSegment.append(nuevo)
        ax.plot([navsegment_origen.longitude, navsegment_destino.longitude],
                [navsegment_origen.latitude, navsegment_destino.latitude], color=segment_color, linewidth=0.5)
        canvas.draw()
        export_navsegments_to_kml(grafo.navSegment, grafo.navPoint)

        añadiendo_navsegment = 0
        messagebox.showinfo("Segmento creado",f"Segmento añadido entre {navsegment_origen.name} y {navsegment_destino.name}.")
        return

    else:
        messagebox.showinfo("Nodo seleccionado", f"Has seleccionado el nodo: {closest.name}")

# Función para activar el modo mostrar vecinos
def preparar_mostrar_vecinos():
    global waiting_for_neighbor_selection
    waiting_for_neighbor_selection = True
    messagebox.showinfo("Selecciona nodo", "Haz clic en un nodo para mostrar sus vecinos.")

# Función para mostrar vecinos de un punto
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
                ax.plot([origin.longitude, destination.longitude], [origin.latitude, destination.latitude], color=segment_color, linewidth=0.5)

    ax.scatter(nodo.longitude, nodo.latitude, color=node_color, s=40)
    ax.text(nodo.longitude, nodo.latitude, nodo.name, fontsize=8, color=node_color)

    for vecino in vecinos:
        ax.scatter(vecino.longitude, vecino.latitude, color=node_color, s=30)
        ax.text(vecino.longitude, vecino.latitude, vecino.name, fontsize=6, alpha=0.6)
        ax.plot([nodo.longitude, vecino.longitude], [nodo.latitude, vecino.latitude], color=segment_color, linewidth=0.5)

    canvas.draw()

    export_neighbors_to_kml(nodo, vecinos, grafo.navSegment)
    messagebox.showinfo("Exportación KML", "Se ha modificado 'neighbors.kml' con el nodo y los vecinos actuales.")

# Función para activar el modo camino más corto
def preparar_camino_mas_corto():
    global waiting_for_path_selection
    waiting_for_path_selection = 1
    messagebox.showinfo("Selecciona origen", "Haz clic en el nodo de origen del camino más corto.")

# Función para dibujar solo nodos (sin segmentos)
def draw_nodes_only(g):
    global ax
    ax.clear()
    ax.set_title("Gráfico - Solo nodos")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.grid(True)
    for n in g.navPoint:
        ax.scatter(n.longitude, n.latitude, color=node_color, s=10)
        ax.text(n.longitude, n.latitude, n.name, fontsize=6, alpha=0.6)

# Función para mostrar el camino más corto con clicks
def mostrar_camino_mas_corto(origen, destino):
    global modo_visualizacion
    modo_visualizacion = "camino"

    ruta = FindShortestPath(grafo, origen, destino)
    if not ruta:
        messagebox.showerror("Error", "No se encontró camino entre los puntos seleccionados.")
        return

    draw_nodes_only(grafo)

    for i in range(len(ruta.navPoints) - 1):
        n1, n2 = ruta.navPoints[i], ruta.navPoints[i + 1]
        ax.plot([n1.longitude, n2.longitude], [n1.latitude, n2.latitude], 'r-', linewidth=3, zorder=5)
        ax.annotate('', xy=(n2.longitude, n2.latitude), xytext=(n1.longitude, n1.latitude),
                    arrowprops=dict(facecolor=segment_color, edgecolor=segment_color, arrowstyle='->', lw=2), zorder=6)

    for n in ruta.navPoints:
        ax.scatter(n.longitude, n.latitude, color=segment_color, s=40, zorder=7)
        ax.text(n.longitude, n.latitude, n.name, fontsize=9, ha='right', color=segment_color, zorder=8)

    origen_x, origen_y = ruta.navPoints[0].longitude, ruta.navPoints[0].latitude
    destino_x, destino_y = ruta.navPoints[-1].longitude, ruta.navPoints[-1].latitude

    flip = destino_x < origen_x

    añadir_icono(ax, "avion.png", origen_x, origen_y, zoom=0.06, flip=flip)

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
    messagebox.showinfo("KML generado", "Se ha modificado 'path.kml' con el camino más corto actual.")

# Función para activar ruta manual
def preparar_creacion_ruta_manual():
    global esperando_ruta_manual, ruta_manual

    draw_graph(grafo)

    respuesta = messagebox.askquestion(
        "Modo de ruta manual",
        "¿Cómo quieres introducir los navpoints de la ruta?\n\nSí = Clics en el gráfico\nNo = Escribir nombres")

    if respuesta == "yes":
        esperando_ruta_manual = True
        ruta_manual = []
        messagebox.showinfo("Ruta manual", "Haz clic en los navpoints para construir la ruta.\nPulsa ESC para terminar.")
    else:
        introducir_ruta_manual_por_nombres()

# Función para pedir los aeropuertos de origen y destino
def pedir_origen_y_destino(opciones):
    top = tk.Toplevel(root)
    top.title("Seleccionar aeropuertos")
    top.transient(root)
    top.grab_set()

    tk.Label(top, text=" Elige el aeropuerto de origen: ").pack(pady=(10, 0))
    entry_origen = tk.Entry(top)
    entry_origen.pack(pady=(0, 10))
    entry_origen.focus()

    tk.Label(top, text=" Elige el aeropuerto de destino: ").pack(pady=(10, 0))
    entry_destino = tk.Entry(top)
    entry_destino.pack(pady=(0, 10))

    resultado = {}

    # Función para pedir los aeropuertos de origen y destino
    def confirmar():
        origen = entry_origen.get()
        destino = entry_destino.get()

        if origen not in opciones:
            messagebox.showerror("Error", "Aeropuerto de origen no válido.")
            return
        if destino not in opciones:
            messagebox.showerror("Error", "Aeropuerto de destino no válido.")
            return

        resultado["origen"] = origen
        resultado["destino"] = destino
        top.destroy()

    tk.Button(top, text="Aceptar", command=confirmar).pack(pady=10)

    top.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - top.winfo_width()) // 2
    y = root.winfo_y() + (root.winfo_height() - top.winfo_height()) // 2
    top.geometry(f"+{x}+{y}")

    top.wait_window()
    return resultado.get("origen"), resultado.get("destino")

# Función para mostrar el camino más corto por aeropuerto
def camino_mas_corto_por_aeropuerto():
    global airports, grafo

    if not grafo or not airports:
        messagebox.showwarning("Advertencia", "Carga los archivos primero.")
        return

    nombres = [a.name for a in airports]

    origen, destino = pedir_origen_y_destino(nombres)
    if not origen or not destino:
        return

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

    if not ruta or not ruta.navPoints:
        messagebox.showerror("Error", "No se encontró camino entre los aeropuertos seleccionados.")
        return

    draw_nodes_only(grafo)

    for i in range(len(ruta.navPoints) - 1):
        n1, n2 = ruta.navPoints[i], ruta.navPoints[i + 1]
        ax.plot([n1.longitude, n2.longitude], [n1.latitude, n2.latitude], 'r-', linewidth=3, zorder=5)
        ax.annotate('', xy=(n2.longitude, n2.latitude), xytext=(n1.longitude, n1.latitude),
                    arrowprops=dict(facecolor=segment_color, edgecolor=segment_color, arrowstyle='->', lw=2), zorder=6)

    for n in ruta.navPoints:
        ax.scatter(n.longitude, n.latitude, color=segment_color, s=40, zorder=7)
        ax.text(n.longitude, n.latitude, n.name, fontsize=9, ha='right', color=segment_color, zorder=8)

    origen_x, origen_y = ruta.navPoints[0].longitude, ruta.navPoints[0].latitude
    destino_x, destino_y = ruta.navPoints[-1].longitude, ruta.navPoints[-1].latitude

    flip = destino_x < origen_x

    añadir_icono(ax, "avion.png", origen_x, origen_y, zoom=0.06, flip=flip)

    from PIL import ImageOps
    pil_img = Image.open("avion.png").convert("RGBA")
    pil_img = pil_img.rotate(310, expand=True)
    if flip:
        pil_img = ImageOps.mirror(pil_img)
    img = np.array(pil_img)
    imagebox = OffsetImage(img, zoom=0.06)
    ab = AnnotationBbox(imagebox, (destino_x, destino_y), frameon=False, zorder=999)
    ax.add_artist(ab)

    canvas.draw()

    export_path_to_kml(ruta, "path.kml")
    messagebox.showinfo("KML generado", "Se ha modificado 'path.kml' con el camino actual.")

# Función para seleccionar colores y espacio aéreo/crear gráfico
def seleccionar_espacio_aereo_con_colores():
    seleccion = tk.Tk()
    seleccion.title("Opciones iniciales")
    seleccion.geometry("400x250")

    global segment_color, node_color
    node_color = "black"
    segment_color = "black"

    tk.Label(seleccion, text="1. Elige el color de los puntos:").pack()
    color_punto_frame = tk.Frame(seleccion)
    color_punto_frame.pack()

    # Función para poner predetemrminado el color negro en puntos
    def set_node_color(color):
        global node_color
        node_color = color

    # Función para escoger el color de los puntos
    def crear_selector_color_punto(frame, color):
        canvas = tk.Canvas(frame, width=30, height=30, highlightthickness=0, bg=seleccion["bg"])
        canvas.pack(side=tk.LEFT, padx=5)
        circle = canvas.create_oval(5, 5, 25, 25, fill=color, outline="black")
        canvas.tag_bind(circle, "<Button-1>", lambda event: set_node_color(color))

    for color in ["red", "orange", "yellow","green", "blue", "purple"]:
        crear_selector_color_punto(color_punto_frame, color)

    tk.Label(seleccion, text="2. Elige el color de los segmentos:").pack(pady=(10, 0))
    color_segmento_frame = tk.Frame(seleccion)
    color_segmento_frame.pack()

    # Función para poner predetemrminado el color negro en segmentos
    def set_segment_color(color):
        global segment_color
        segment_color = color

    # Función para escoger el color de los segmentos
    def crear_selector_color_segmento(frame, color):
        canvas = tk.Canvas(frame, width=30, height=30, highlightthickness=0, bg=seleccion["bg"])
        canvas.pack(side=tk.LEFT, padx=5)
        circle = canvas.create_oval(5, 5, 25, 25, fill=color, outline="black")
        canvas.tag_bind(circle, "<Button-1>", lambda event: set_segment_color(color))

    for color in ["red", "orange", "yellow", "green", "blue", "purple"]:
        crear_selector_color_segmento(color_segmento_frame, color)

    tk.Label(seleccion, text="3. Elige el espacio aéreo que quieres ver:").pack(pady=(10, 0))
    espacio_frame = tk.Frame(seleccion)
    espacio_frame.pack(pady=5)

    # Función para escoger espacio aéreo o gráfico nuevo
    def elegir(prefix):
        seleccion.destroy()
        main_interface(prefix)

    tk.Button(espacio_frame, text="Cataluña", command=lambda: elegir("Cat")).pack(side=tk.LEFT, padx=5)
    tk.Button(espacio_frame, text="España", command=lambda: elegir("Spain")).pack(side=tk.LEFT, padx=5)
    tk.Button(espacio_frame, text="Europa", command=lambda: elegir("ECAC")).pack(side=tk.LEFT, padx=5)
    tk.Button(espacio_frame, text="Crear gráfico", command=lambda: (seleccion.destroy(), crear_grafo_vacio())).pack(side=tk.LEFT, padx=5)

    seleccion.mainloop()

# Función para crear ruta manual escrita
def introducir_ruta_manual_por_nombres():
    global ruta_manual, grafo

    ventana = tk.Toplevel(root)
    ventana.title("Introducir nombres de navpoints")
    ventana.geometry("300x300")

    tk.Label(ventana, text="Introduce los nombres separados por comas:").pack(pady=10)
    entrada = tk.Entry(ventana, width=40)
    entrada.pack(pady=5)
    entrada.focus()

    # Función para confirmar que los puntos escritos existen
    def confirmar():
        nombres = entrada.get().split(',')
        nombres = [n.strip().upper() for n in nombres]

        navpoints_dict = {n.name.upper(): n for n in grafo.navPoint}
        ruta_manual.clear()

        for nombre in nombres:
            if nombre not in navpoints_dict:
                messagebox.showerror("Error", f"Navpoint '{nombre}' no encontrado.")
                return
            ruta_manual.append(navpoints_dict[nombre])

        ventana.destroy()
        mostrar_ruta_manual()

    tk.Button(ventana, text="Aceptar", command=confirmar).pack(pady=15)

# Función para crear ruta manual con clicks
def mostrar_ruta_manual():
    global ruta_manual

    if len(ruta_manual) < 2:
        messagebox.showerror("Error", "Debes introducir al menos dos navpoints.")
        return

    draw_nodes_only(grafo)

    for i in range(len(ruta_manual) - 1):
        n1 = ruta_manual[i]
        n2 = ruta_manual[i + 1]
        ax.plot([n1.longitude, n2.longitude], [n1.latitude, n2.latitude], color=segment_color, linewidth=2, zorder=9)
        ax.annotate('', xy=(n2.longitude, n2.latitude), xytext=(n1.longitude, n1.latitude),
                    arrowprops=dict(facecolor=segment_color, edgecolor=segment_color, arrowstyle='->', lw=2), zorder=10)

    for n in ruta_manual:
        ax.scatter(n.longitude, n.latitude, color=segment_color, s=40, zorder=11)
        ax.text(n.longitude, n.latitude, n.name, fontsize=9, color=segment_color, zorder=12)

    origen = ruta_manual[0]
    destino = ruta_manual[-1]
    flip = destino.longitude < origen.longitude

    añadir_icono(ax, "avion.png", origen.longitude, origen.latitude, zoom=0.06, flip=flip)

    pil_img = Image.open("avion.png").convert("RGBA").rotate(310, expand=True)
    if flip:
        pil_img = ImageOps.mirror(pil_img)
    img = np.array(pil_img)
    imagebox = OffsetImage(img, zoom=0.06)
    ab = AnnotationBbox(imagebox, (destino.longitude, destino.latitude), frameon=False, zorder=999)
    ax.add_artist(ab)

    canvas.draw()

    ruta = Path(ruta_manual[0])
    for punto in ruta_manual[1:]:
        ruta.AddNodeToPath(punto)

    export_path_to_kml(ruta, "ruta_manual.kml")
    messagebox.showinfo("KML generado", "Se ha actualizado 'ruta_manual.kml' con la ruta manual escrita.")

# Función para activar el modo añadir navpoint
def activar_modo_navpoint():
    global añadiendo_navpoint
    añadiendo_navpoint = True
    messagebox.showinfo("Modo activo", "Haz clic donde quieras añadir un nuevo NavPoint.")

# Función para activar el modo añadir segmento
def activar_modo_navsegment():
    global añadiendo_navsegment
    añadiendo_navsegment = 1
    messagebox.showinfo("Modo activo", "Haz clic en el origen del nuevo NavSegment.")

# Función para eliminar navpoint
def eliminar_navpoint():
    global esperando_eliminar_navpoint

    if grafo is None:
        messagebox.showwarning("Advertencia", "Primero carga un grafo.")
        return

    esperando_eliminar_navpoint = True
    messagebox.showinfo("Modo activo", "Haz clic en el NavPoint que quieres eliminar.")

# Función para añadir un segmento escrito
def navsegment_por_nombres():
    global grafo

    if grafo is None:
        messagebox.showwarning("Advertencia", "Primero debes cargar un espacio aéreo.")
        return

    navpoints_dict = {n.name.upper(): n for n in grafo.navPoint}

    top = tk.Toplevel(root)
    top.title("Crear segmento por nombre")
    top.geometry("300x180")
    top.transient(root)
    top.grab_set()

    tk.Label(top, text="Nombre del punto de origen:").pack(pady=(10, 0))
    entry_origen = tk.Entry(top)
    entry_origen.pack(pady=5)
    entry_origen.focus()

    tk.Label(top, text="Nombre del punto de destino:").pack(pady=(10, 0))
    entry_destino = tk.Entry(top)
    entry_destino.pack(pady=5)

    # Función para confirmar que los puntos existen
    def confirmar():
        origen = entry_origen.get().strip().upper()
        destino = entry_destino.get().strip().upper()

        if origen not in navpoints_dict or destino not in navpoints_dict:
            messagebox.showerror("Error", "Alguno de los nombres no existe.")
            return

        nodo_origen = navpoints_dict[origen]
        nodo_destino = navpoints_dict[destino]

        nuevo_segmento = NavSegment(nodo_origen.number, nodo_destino.number, Distance(nodo_origen, nodo_destino))
        grafo.navSegment.append(nuevo_segmento)

        ax.plot([nodo_origen.longitude, nodo_destino.longitude],
                [nodo_origen.latitude, nodo_destino.latitude],
                color=segment_color, linewidth=0.5)
        canvas.draw()

        export_navsegments_to_kml(grafo.navSegment, grafo.navPoint)
        messagebox.showinfo("Segmento creado", f"Segmento añadido entre {origen} y {destino}.")
        top.destroy()

    tk.Button(top, text="Aceptar", command=confirmar).pack(pady=10)

    top.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - top.winfo_width()) // 2
    y = root.winfo_y() + (root.winfo_height() - top.winfo_height()) // 2
    top.geometry(f"+{x}+{y}")

    top.wait_window()

# Función para guardar el gráfico actual
def guardar_txt():
    if grafo is None:
        messagebox.showwarning("Advertencia", "No hay grafo cargado.")
        return

    export_navpoints_to_txt(grafo.navPoint, "navpoint_new.txt")
    export_navsegments_to_txt(grafo.navSegment, "navsegment_new.txt")

    export_navpoints_to_kml(grafo.navPoint, "points.kml")
    export_navsegments_to_kml(grafo.navSegment, grafo.navPoint, "segments.kml")

    messagebox.showinfo("Guardado", "Se han guardado los archivos:\n- navpoint_new.txt\n- navsegment_new.txt\n- points.kml\n- segments.kml")

# Función para cargar un gráfico desde archivos
def cargar_grafo_desde_txt():
    global grafo

    navpoint_file = filedialog.askopenfilename(title="Selecciona archivo de NavPoints (.txt)", filetypes=[("Text files", "*.txt")])
    if not navpoint_file:
        return

    navsegment_file = filedialog.askopenfilename(title="Selecciona archivo de NavSegments (.txt)", filetypes=[("Text files", "*.txt")])
    if not navsegment_file:
        return

    nuevo_grafo = Graph()

    try:
        with open(navpoint_file, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 4:
                    raise ValueError("Formato incorrecto en navpoint.")
                number = int(parts[0])
                name = parts[1]
                latitude = float(parts[2])
                longitude = float(parts[3])
                nuevo_grafo.navPoint.append(NavPoint(number, name, latitude, longitude))

        with open(navsegment_file, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 3:
                    raise ValueError("Formato incorrecto en navsegment.")
                origin = int(parts[0])
                destination = int(parts[1])
                distance = float(parts[2])
                nuevo_grafo.navSegment.append(NavSegment(origin, destination, distance))

        grafo = nuevo_grafo
        draw_graph(grafo)
        messagebox.showinfo("Cargado", "Se ha cargado el grafo desde los archivos seleccionados.")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al cargar los archivos:\n{str(e)}")

# Función para crear un gráfico inicial vacío
def crear_grafo_vacio():
    global grafo
    grafo = Graph()
    main_interface(None)

# Interfaz interactiva
def main_interface(prefix):
    global root, plot_frame, grafo, airports
    if prefix is not None:
        grafo, airports_dict = load_airspace(prefix)
        airports = list(airports_dict.values())
    else:
        grafo = Graph()
        airports = []

    root = tk.Tk()
    root.title("Visualizador")
    root.geometry("900x700")

    # Función para acabar la ruta manual con ESC
    def finalizar_ruta_manual(event=None):
        global esperando_ruta_manual, ruta_manual
        if esperando_ruta_manual:
            esperando_ruta_manual = False

            if len(ruta_manual) >= 2:
                origen = ruta_manual[0]
                destino = ruta_manual[-1]
                flip = destino.longitude < origen.longitude

                # Añadir iconos de avión
                añadir_icono(ax, "avion.png", origen.longitude, origen.latitude, zoom=0.06, flip=flip)
                pil_img = Image.open("avion.png").convert("RGBA")
                pil_img = pil_img.rotate(310, expand=True)
                if flip:
                    pil_img = ImageOps.mirror(pil_img)
                img = np.array(pil_img)
                imagebox = OffsetImage(img, zoom=0.06)
                ab = AnnotationBbox(imagebox, (destino.longitude, destino.latitude), frameon=False, zorder=999)
                ax.add_artist(ab)

                # Convertir lista de puntos a objeto Path y exportar
                ruta = Path(ruta_manual[0])
                for punto in ruta_manual[1:]:
                    ruta.AddNodeToPath(punto)

                export_path_to_kml(ruta, "ruta_manual.kml")
                messagebox.showinfo("KML generado", "Se ha actualizado 'ruta_manual.kml' con la ruta manual seleccionada.")

            canvas.draw()
            messagebox.showinfo("Ruta finalizada", "Se ha terminado de definir la ruta manual.")

    root.bind("<Escape>", finalizar_ruta_manual)  # Ahora está después de root = tk.Tk()

    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)

    button_frame = tk.Frame(root)
    button_frame.pack(anchor='nw', pady=5, padx=5)

    tk.Button(button_frame, text="Vecinos", command=preparar_mostrar_vecinos).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Camino más corto (clicks)", command=preparar_camino_mas_corto).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Camino más corto (aeropuerto)", command=camino_mas_corto_por_aeropuerto).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Ruta manual", command=preparar_creacion_ruta_manual).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Gráfico completo", command=lambda: draw_graph(grafo)).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Añadir punto", command=activar_modo_navpoint).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Añadir segmento (clicks)", command=activar_modo_navsegment).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Añadir segmento (puntos)", command=navsegment_por_nombres).pack(side=tk.LEFT,padx=5)
    tk.Button(button_frame, text="Eliminar punto", command=eliminar_navpoint).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Guardar", command=guardar_txt).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Cargar", command=cargar_grafo_desde_txt).pack(side=tk.LEFT, padx=5)

    plot_frame = tk.Frame(root)
    plot_frame.pack(fill=tk.BOTH, expand=True)

    draw_graph(grafo)
    root.mainloop()

# Interfaz inicial
seleccionar_espacio_aereo_con_colores()
#