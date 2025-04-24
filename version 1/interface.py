import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graph import *
from path import *

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

# Crear el marco para los botones
button_container = tk.Frame(window)
button_container.grid(row=0, column=0, pady=10, padx=10, sticky="w")

# Crear el marco para el gráfico
graph_frame = tk.Frame(window)
graph_frame.grid(row=1, column=0, sticky="nsew")

window.grid_rowconfigure(1, weight=1)  # Asegura que la segunda fila, donde está el gráfico, se expanda
window.grid_columnconfigure(0, weight=1)

selected_node = None
origin_node = None
destination_node = None
actual = None
segment_mode = False  # Variable para controlar el modo de creación de segmentos

def esconder():
    for widget in graph_frame.winfo_children():
        widget.destroy()

# Variables de control
shortest_path_mode = False  # Modo de Camino Más Corto
origin_node = None
destination_node = None
segment_mode = False  # Modo de Segmento

def on_click(event, g):
    global selected_node, origin_node, destination_node, segment_mode, shortest_path_mode
    x, y = event.xdata, event.ydata
    if x is None or y is None:
        return

    # Obtener el nodo más cercano al clic
    closest_node = GetClosest(g, x, y)
    if closest_node:
        if segment_mode:
            # Modo Segmento: Selección de origen y destino para crear un segmento
            if origin_node is None:
                origin_node = closest_node
                messagebox.showinfo("Nodo Origen Seleccionado", f"Has seleccionado el nodo de origen: {origin_node.name}")
            elif destination_node is None:
                destination_node = closest_node
                messagebox.showinfo("Nodo Destino Seleccionado", f"Has seleccionado el nodo de destino: {destination_node.name}")
                # Añadir el segmento
                segment_name = f"{origin_node.name}{destination_node.name}"
                if origin_node != destination_node:
                    AddSegment(g, segment_name, origin_node.name, destination_node.name)
                    messagebox.showinfo("Segmento Agregado", f"Se ha agregado un segmento entre {origin_node.name} y {destination_node.name}.")
                origin_node = None
                destination_node = None
                segment_mode = False
                show_graph()  # Mostrar el gráfico con el nuevo segmento
        elif shortest_path_mode:
            # Modo Camino Más Corto: Selección de nodos de origen y destino
            if origin_node is None:
                origin_node = closest_node
                messagebox.showinfo("Nodo Origen Seleccionado", f"Has seleccionado el nodo de origen: {origin_node.name}")
            elif destination_node is None:
                destination_node = closest_node
                messagebox.showinfo("Nodo Destino Seleccionado", f"Has seleccionado el nodo de destino: {destination_node.name}")
                # Calcular el camino más corto
                show_shortest_path()  # Llamamos a la función para calcular y mostrar el camino más corto
                shortest_path_mode = False  # Desactivamos el modo de camino más corto
                origin_node = None
                destination_node = None  # Actualizamos el gráfico para reflejar el camino más corto
        else:
            # Si no estamos en modo de segmento ni camino más corto, seleccionamos un nodo normal
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

def show_neighbors():
    global actual, selected_node
    if actual is None:
        messagebox.showwarning("Gráfico no cargado", "Primero carga o crea un gráfico.")
        return

    if selected_node is None:
        messagebox.showwarning("Nodo no seleccionado", "Selecciona un nodo primero.")
        return

    filtered_graph = Graph()
    AddNode(filtered_graph, selected_node)
    for neighbor in selected_node.neighbors:
        AddNode(filtered_graph, neighbor)

    for segment in actual.segment:
        if (segment.origin == selected_node and segment.destination in selected_node.neighbors) or \
           (segment.destination == selected_node and segment.origin in selected_node.neighbors):
            AddSegment(filtered_graph, segment.name, segment.origin.name, segment.destination.name)

    esconder()

    fig, ax = plt.subplots(figsize=(5, 5))
    Plot(filtered_graph)
    ax.set_title(f"Vecinos de {selected_node.name}")

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()

# Variable para controlar el modo de selección de Camino Más Corto
shortest_path_mode = False

def set_shortest_path_mode():
    global shortest_path_mode
    shortest_path_mode = True
    messagebox.showinfo("Modo Camino Más Corto", "Haz clic en un nodo para seleccionar el nodo de origen y luego en otro nodo para seleccionar el destino.")

def show_shortest_path():
    global actual, origin_node, destination_node

    if origin_node is None or destination_node is None:
        messagebox.showwarning("Nodos no seleccionados", "Por favor, selecciona tanto el nodo de origen como el nodo de destino.")
        return

    # Llamar a la función FindShortestPath para obtener el camino más corto
    shortest_path = FindShortestPath(actual, origin_node, destination_node)

    if shortest_path:
        esconder()
        plot_shortest_path(actual, shortest_path)
    else:
        messagebox.showinfo("Resultado", "No se encontró un camino entre los nodos seleccionados.")

    # Reiniciar nodos para permitir nuevas selecciones
    origin_node = None
    destination_node = None


def add_shortest_path_button():
    global shortest_path_mode, origin_node, destination_node

    # 👇 Esto reinicia la vista limpia
    show_graph()

    shortest_path_mode = True
    origin_node = None
    destination_node = None
    messagebox.showinfo("Modo Camino Más Corto Activado", "Haz clic en un nodo para seleccionar el origen y luego en otro nodo para seleccionar el destino.")


def plot_shortest_path(graph, shortest_path):
    global actual

    # 👇 Esta línea es clave para borrar el gráfico anterior (incluyendo cualquier camino dibujado)
    esconder()

    fig, ax = plt.subplots(figsize=(5, 5))

    # Dibujar el gráfico completo
    Plot(graph)

    # Dibujar el camino más corto
    for i in range(len(shortest_path) - 1):
        node1 = shortest_path[i]
        node2 = shortest_path[i + 1]
        ax.plot([node1.coordinate_x, node2.coordinate_x], [node1.coordinate_y, node2.coordinate_y], color='red', linewidth=2)
        ax.annotate('', xy=(node2.coordinate_x, node2.coordinate_y), xytext=(node1.coordinate_x, node1.coordinate_y),
                    arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->'))

    ax.set_title("Camino más corto entre los nodos seleccionados")

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()

# Grupo de botones de Gráficos
label_graph = tk.Label(button_container, text="Gráficos", font=("Helvetica", 12, "bold"))
label_graph.grid(row=0, column=0, pady=5, padx=10, sticky="w")

btn_show_graph = tk.Button(button_container, text="Gráfico Ejemplo", command=new_example_graph)
btn_show_graph.grid(row=1, column=0, padx=5, sticky="w")

btn_load_graph = tk.Button(button_container, text="Gráfico Inventado", command=load_graph)
btn_load_graph.grid(row=1, column=1, padx=5, sticky="w")

btn_file_graph = tk.Button(button_container, text="Gráfico Cargado", command=file_graph)
btn_file_graph.grid(row=1, column=2, padx=5, sticky="w")

# Grupo de botones de Funciones
label_functions = tk.Label(button_container, text="Funciones", font=("Helvetica", 12, "bold"))
label_functions.grid(row=2, column=0, pady=5, padx=10, sticky="w")

btn_add_node = tk.Button(button_container, text="Agregar Nodo", command=add_node)
btn_add_node.grid(row=3, column=0, padx=5, sticky="w")

btn_add_segment = tk.Button(button_container, text="Modo Segmento", command=add_segment_button)
btn_add_segment.grid(row=3, column=1, padx=5, sticky="w")

btn_remove_node = tk.Button(button_container, text="Eliminar Nodo", command=remove_selected_node)
btn_remove_node.grid(row=3, column=2, padx=5, sticky="w")

btn_show_neighbors = tk.Button(button_container, text="Mostrar Vecinos", command=show_neighbors)
btn_show_neighbors.grid(row=4, column=0, padx=5, pady=5, sticky="w")

btn_save_current_graph = tk.Button(button_container, text="Guardar Gráfico", command=save_current_graph)
btn_save_current_graph.grid(row=4, column=1, padx=5, pady=5, sticky="w")

btn_add_shortest_path = tk.Button(button_container, text="Modo Camino Más Corto", command=add_shortest_path_button)
btn_add_shortest_path.grid(row=3, column=2, padx=5, sticky="w")

window.mainloop()