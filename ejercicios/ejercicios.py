from graph import *

class NavPoint:
    def __init__(self, number: int, name: str, latitude: float, longitude: float):
        self.number = number
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

# Cargar gráfico
def load_navpoints(filename):
    import os
    g = Graph()
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                parts = line.split()
                num, name, lat, long = float(parts[0]), parts[1], float(parts[2]), float(parts[3])
                AddNavPoint(g, NavPoint(num, name, lat, long))
        return g
    else:
        print("El archivo no es correcto")


import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from navPoint import load_navpoints

# Cargar y dibujar
def load_and_draw():
    file_path = filedialog.askopenfilename(
        title="Selecciona el archivo de NavPoints",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if not file_path:
        return

    grafo = load_navpoints(file_path)
    draw_graph(grafo)

# Dibujar gráfico
def draw_graph(grafo):
    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()

    fig, ax = plt.subplots(figsize=(8, 6))

    lats = [n.latitude for n in grafo.node]
    longs = [n.longitude for n in grafo.node]
    names = [n.name for n in grafo.node]

    ax.scatter(longs, lats, s=10, c='blue')
    for i, name in enumerate(names):
        ax.text(longs[i], lats[i], name, fontsize=6, alpha=0.6)

    ax.set_title("NavPoints en el grafo")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root = tk.Tk()
root.title("Visualizador de NavPoints")
root.geometry("900x700")

#load_button = tk.Button(root, text="Cargar archivo", command=load_and_draw)
load_button.pack(pady=10)

plot_frame = tk.Frame(root)
plot_frame.pack(fill=tk.BOTH, expand=True)

canvas = None

root.mainloop()



# Añadir navpoint
def AddNavPoint(g, n):
    if n in g.node:
        return False
    g.node.append(n)
    return True

# Añadir segmento
def AddNavSegment(g, name, nameOriginNode, nameDestinationNode):
    origin = None
    destination = None
    i = 0
    while i < len(g.node) and (origin is None or destination is None):
        if g.node[i].name == nameOriginNode:
            origin = g.node[i]
        elif g.node[i].name == nameDestinationNode:
            destination = g.node[i]
        i = i + 1
    if origin and destination:
        AddNeighbor(origin, destination)
        segment = Segment(name, origin, destination)
        g.segment.append(segment)
        return True
    return False


from graph import *

class NavSegment:
    def __init__(self, origin_number, destination_number, distance):
        self.origin_number = origin_number
        self.destination_number = destination_number
        self.distance = distance

# Cargar gráfico
def load_navsegment(filename):
    import os
    g = Graph()
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                parts = line.split()
                origin_num, destination_num, distance = float(parts[0]), parts[1], float(parts[2])
                AddNavSegment(g, NavSegment(origin_num, destination_num, distance))
        return g
    else:
        print("El archivo no es correcto")