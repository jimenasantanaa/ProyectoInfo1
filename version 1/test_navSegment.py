import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from matplotlib.backend_bases import NavigationToolbar2

from navPoint import load_navpoints
from navSegment import load_navsegment
from node import *
from segment import *
from graph import *

# Barra Zoom y Reset
class CustomToolbar(NavigationToolbar2Tk):
    toolitems = [t for t in NavigationToolbar2.toolitems if t[0] in ('Home', 'Zoom')]

# Cargar y dibujar
def load_and_draw():
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

# Dibujar gráfico
def draw_graph(grafo):
    global canvas, toolbar
    if canvas:
        canvas.get_tk_widget().destroy()
    if toolbar:
        toolbar.destroy()

    fig, ax = plt.subplots(figsize=(8, 6))

    # Dibujar puntos
    lats = [n.latitude for n in grafo.navPoint]
    longs = [n.longitude for n in grafo.navPoint]
    names = [n.name for n in grafo.navPoint]

    ax.scatter(longs, lats, s=10, c='blue')
    for i, name in enumerate(names):
        ax.text(longs[i], lats[i], name, fontsize=6, alpha=0.6)

    # Dibujar segmentos
    for seg in grafo.navSegment:
        origin = next((n for n in grafo.navPoint if n.number == seg.origin_number), None)
        destination = next((n for n in grafo.navPoint if n.number == seg.destination_number), None)
        if origin and destination:
            ax.plot([origin.longitude, destination.longitude],[origin.latitude, destination.latitude],'k-', linewidth=0.5)

    ax.set_title("Red de Navegación Aérea")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    toolbar = CustomToolbar(canvas, plot_frame)
    toolbar.update()
    toolbar.pack()

root = tk.Tk()
root.title("Visualizador de Rutas Aéreas")
root.geometry("900x700")

load_button = tk.Button(root, text="Cargar NavPoints y Segmentos", command=load_and_draw)
load_button.pack(pady=10)

plot_frame = tk.Frame(root)
plot_frame.pack(fill=tk.BOTH, expand=True)

canvas = None
toolbar = None

root.mainloop()
