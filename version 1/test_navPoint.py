import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from navPoint import load_navpoints

def load_and_draw():
    # Abrir el archivo de NavPoints
    file_path = filedialog.askopenfilename(
        title="Selecciona el archivo de NavPoints",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    if not file_path:
        return

    # Cargar los NavPoints
    grafo = load_navpoints(file_path)

    # Dibujar el gráfico con los puntos
    draw_graph(grafo)

def draw_graph(grafo):
    global canvas  # Necesario para poder destruir el canvas anterior
    if canvas:
        canvas.get_tk_widget().destroy()

    fig, ax = plt.subplots(figsize=(8, 6))

    # Usar navPoint en lugar de node
    lats = [n.latitude for n in grafo.navPoint]  # Cambiado de node a navPoint
    longs = [n.longitude for n in grafo.navPoint]  # Cambiado de node a navPoint
    names = [n.name for n in grafo.navPoint]  # Cambiado de node a navPoint

    ax.scatter(longs, lats, s=10, c='blue')
    for i, name in enumerate(names):
        ax.text(longs[i], lats[i], name, fontsize=6, alpha=0.6)

    ax.set_title("NavPoints en el grafo")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.grid(True)

    # Mostrar el gráfico en Tkinter
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# ----- Interfaz Tkinter principal -----
root = tk.Tk()
root.title("Visualizador de NavPoints")
root.geometry("900x700")

load_button = tk.Button(root, text="Cargar archivo Cat_nav.txt", command=load_and_draw)
load_button.pack(pady=10)

plot_frame = tk.Frame(root)
plot_frame.pack(fill=tk.BOTH, expand=True)

canvas = None  # Inicializamos el canvas como variable global

root.mainloop()
