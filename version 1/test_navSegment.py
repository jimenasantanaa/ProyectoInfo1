import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from navPoint import load_navpoints  # Importa la función load_navpoints
from navSegment import load_navsegment  # Importa la función load_navsegment
from graph import Graph  # Asegúrate de tener la clase Graph definida correctamente

# Crear la ventana de Tkinter
root = tk.Tk()
root.title("Visualizador de Rutas Aéreas")
root.geometry("800x600")

# Crear la figura para el gráfico
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

global_graph = None

# Función para dibujar el gráfico
def draw_graph(g):
    ax.clear()  # Limpia el gráfico previo
    for node in g.navPoint:
        ax.plot(node.longitude, node.latitude, 'bo')  # Dibuja puntos (Lon, Lat)
        ax.text(node.longitude + 0.01, node.latitude + 0.01, node.name, fontsize=6)
    for segment in g.navSegment:
        origin = next((np for np in g.navPoint if np.number == segment.origin_number), None)
        destination = next((np for np in g.navPoint if np.number == segment.destination_number), None)
        if origin and destination:
            ax.plot([origin.longitude, destination.longitude], [origin.latitude, destination.latitude], 'k-', linewidth=0.5)
    ax.set_title("Red de Navegación Aérea")
    canvas.draw()

# Función para cargar los archivos de puntos y segmentos
def load_files():
    global global_graph
    nav_file = filedialog.askopenfilename(title="Selecciona el archivo de puntos de navegación (Cat_nav.txt)")
    global_graph = load_navpoints(nav_file)  # Usar la función de carga de NavPoint
    seg_file = filedialog.askopenfilename(title="Selecciona el archivo de segmentos de navegación (Cat_seg.txt)")
    load_navsegment(seg_file, global_graph)  # Usar la función de carga de NavSegment
    draw_graph(global_graph)

# Botón para cargar los archivos y generar el gráfico
button = tk.Button(root, text="Cargar Rutas de Catalunya", command=load_files)
button.pack(pady=10)

# Ejecutar la ventana de Tkinter
root.mainloop()
