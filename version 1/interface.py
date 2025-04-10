import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graph import *

def CreateGraph_1():
    G = Graph()
    AddNode(G, Node("A", 1, 20))
    AddNode(G, Node("B", 8, 17))
    AddNode(G, Node("C", 15, 20))
    AddNode(G, Node("D", 18, 15))
    AddNode(G, Node("E", 2, 4))
    AddNode(G, Node("F", 6, 5))
    AddNode(G, Node("G", 12, 12))
    AddNode(G, Node("H", 10, 3))
    AddNode(G, Node("I", 19, 1))
    AddNode(G, Node("J", 13, 5))
    AddNode(G, Node("K", 3, 15))
    AddNode(G, Node("L", 4, 10))
    AddSegment(G, "AB", "A", "B")
    AddSegment(G, "AE", "A", "E")
    AddSegment(G, "AK", "A", "K")
    AddSegment(G, "BA", "B", "A")
    AddSegment(G, "BC", "B", "C")
    AddSegment(G, "BF", "B", "F")
    AddSegment(G, "BK", "B", "K")
    AddSegment(G, "BG", "B", "G")
    AddSegment(G, "CD", "C", "D")
    AddSegment(G, "CG", "C", "G")
    AddSegment(G, "DG", "D", "G")
    AddSegment(G, "DH", "D", "H")
    AddSegment(G, "DI", "D", "I")
    AddSegment(G, "EF", "E", "F")
    AddSegment(G, "FL", "F", "L")
    AddSegment(G, "GB", "G", "B")
    AddSegment(G, "GF", "G", "F")
    AddSegment(G, "GH", "G", "H")
    AddSegment(G, "ID", "I", "D")
    AddSegment(G, "IJ", "I", "J")
    AddSegment(G, "JI", "J", "I")
    AddSegment(G, "KA", "K", "A")
    AddSegment(G, "KL", "K", "L")
    AddSegment(G, "LK", "L", "K")
    AddSegment(G, "LF", "L", "F")
    return G

window = tk.Tk()
window.title("Graph Viewer")

button_frame = tk.Frame(window)
button_frame.pack(side="top", fill="x", pady=10)

graph_frame = tk.Frame(window)
graph_frame.pack(side="top", fill="both", expand=True)

selected_node = None
origin_node = None
destination_node = None
actual = None
segment_mode = False  # Variable para controlar el modo de creación de segmentos

def esconder():
    for widget in graph_frame.winfo_children():
        widget.destroy()

def on_click(event, g):
    global selected_node, origin_node, destination_node, segment_mode
    x, y = event.xdata, event.ydata
    if x is None or y is None:
        return

    closest_node = GetClosest(g, x, y)
    if closest_node:
        if segment_mode:
            if origin_node is None:
                origin_node = closest_node
                messagebox.showinfo("Nodo Origen Seleccionado", f"Has seleccionado el nodo de origen: {origin_node.name}")
            elif destination_node is None:
                destination_node = closest_node
                messagebox.showinfo("Nodo Destino Seleccionado", f"Has seleccionado el nodo de destino: {destination_node.name}")
                # Añadir el segmento al gráfico actual
                segment_name = f"{origin_node.name}{destination_node.name}"
                if origin_node != destination_node:
                    AddSegment(g, segment_name, origin_node.name, destination_node.name)
                    messagebox.showinfo("Segmento Agregado", f"Se ha agregado un segmento entre {origin_node.name} y {destination_node.name}.")
                origin_node = None
                destination_node = None
                segment_mode = False
                show_graph(segment_mode)  # Mostrar el gráfico con el nuevo segmento
        else:
            selected_node = closest_node
            messagebox.showinfo("Nodo Seleccionado", f"Has seleccionado el nodo: {selected_node.name}")


def show_graph():
    global actual
    esconder()

    if actual is None:
        actual = CreateGraph_1()

    fig, ax = plt.subplots(figsize=(5, 5))
    Plot(actual)  # Asumiendo que Plot dibuja el gráfico
    ax.set_title("Gráfico Actual")

    fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, actual))

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()

def new_example_graph():
    global actual
    actual = CreateGraph_1()
    show_graph()

def add_segment_button():
    global segment_mode
    segment_mode = True
    messagebox.showinfo("Modo Segmento Activado", "Haz clic en un nodo para seleccionar el origen y luego en otro nodo para seleccionar el destino.")

def load_graph():
    global actual
    esconder()
    D = Data('datos.txt')
    actual = D
    fig, ax = plt.subplots(figsize=(5, 5))
    Plot(D)
    ax.set_title("Gráfico Inventado")

    fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, D))

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()


def file_graph():
    global actual
    esconder()
    filename = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    F = Data(filename)
    actual = F
    fig, ax = plt.subplots(figsize=(5, 5))
    Plot(F)
    ax.set_title("Gráfico Cargado")

    fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, F))

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()


def add_node():
    global actual
    if actual is None:
        messagebox.showwarning("Seleccionar gráfico", "Por favor, selecciona un gráfico antes de agregar un nodo.")
        return

    node_input = simpledialog.askstring("Agregar Nodo", "Introduce el nodo en el formato 'P, 2, 3' (sin comillas):")

    if node_input:
        parts = node_input.split(',')

        if len(parts) != 3:
            messagebox.showwarning("Formato incorrecto", "El formato debe ser: 'Nombre, X, Y' con comas.")
            return

        try:
            name = parts[0].strip()
            x = float(parts[1].strip())
            y = float(parts[2].strip())

            for node in actual.node:
                if node.name == name:
                    messagebox.showwarning("Nodo Existente", f"Ya existe un nodo con el nombre '{name}'.")
                    return

            node = Node(name, x, y)

            AddNode(actual, node)
            messagebox.showinfo("Nodo Agregado", f"Se ha agregado el nodo {name} en ({x}, {y}).")

            show_graph()

        except ValueError:
            messagebox.showwarning("Datos incorrectos", "Las coordenadas X y Y deben ser números.")
    else:
        messagebox.showwarning("Entrada vacía", "Por favor, introduce los datos del nodo.")

def remove_selected_node():
    global actual, selected_node
    if actual is None:
        messagebox.showwarning("Seleccionar gráfico", "Por favor, selecciona un gráfico antes de eliminar un nodo.")
        return

    if selected_node is None:
        messagebox.showwarning("Seleccionar Nodo", "Por favor, selecciona un nodo para eliminar.")
        return

    confirm = messagebox.askyesno("Confirmación", f"¿Seguro que deseas eliminar el nodo {selected_node.name} y sus segmentos?")

    if confirm:
        success = DeleteNode(actual, selected_node.name)

        if not success:
            messagebox.showwarning("Nodo no encontrado", f"No se encontró un nodo con el nombre '{selected_node.name}'.")
        else:
            messagebox.showinfo("Nodo Eliminado", f"Se ha eliminado el nodo {selected_node.name} y sus segmentos asociados.")
            selected_node = None
            show_graph()

def save_current_graph():
    global actual
    if actual is None:
        messagebox.showwarning("Seleccionar gráfico", "Por favor, selecciona un gráfico antes de guardar.")
        return

    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])

    if filename:
        SaveGraph(actual, filename)
        messagebox.showinfo("Guardar gráfico", f"El gráfico se ha guardado correctamente en {filename}")

btn_show_graph = tk.Button(button_frame, text="Gráfico Ejemplo", command=new_example_graph)
btn_show_graph.pack(side="left", padx=5)

btn_load_graph = tk.Button(button_frame, text="Gráfico Inventado", command=load_graph)
btn_load_graph.pack(side="left", padx=5)

btn_file_graph = tk.Button(button_frame, text="Gráfico Cargado", command=file_graph)
btn_file_graph.pack(side="left", padx=5)

btn_add_node = tk.Button(window, text="Agregar Nodo", command=add_node)
btn_add_node.pack(pady=10)

btn_add_segment = tk.Button(window, text="Modo Segmento", command=add_segment_button)
btn_add_segment.pack(pady=10)

btn_remove_node = tk.Button(window, text="Eliminar nodo", command=remove_selected_node)
btn_remove_node.pack(pady=10)

btn_save_graph = tk.Button(window, text="Guardar gráfico", command=save_current_graph)
btn_save_graph.pack(pady=10)

window.mainloop()

#algo