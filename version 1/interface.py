import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graph import *

def CreateGraph_1 ():
    G = Graph()
    AddNode(G, Node("A",1,20))
    AddNode(G, Node("B",8,17))
    AddNode(G, Node("C",15,20))
    AddNode(G, Node("D",18,15))
    AddNode(G, Node("E",2,4))
    AddNode(G, Node("F",6,5))
    AddNode(G, Node("G",12,12))
    AddNode(G, Node("H",10,3))
    AddNode(G, Node("I",19,1))
    AddNode(G, Node("J",13,5))
    AddNode(G, Node("K",3,15))
    AddNode(G, Node("L",4,10))
    AddSegment(G, "AB","A","B")
    AddSegment(G, "AE","A","E")
    AddSegment(G, "AK","A","K")
    AddSegment(G, "BA","B","A")
    AddSegment(G, "BC","B","C")
    AddSegment(G, "BF","B","F")
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

actual = None

def esconder():
    global actual
    if actual:
        actual.get_tk_widget().destroy()

def show_graph():
    global actual
    esconder()
    G = CreateGraph_1()
    fig, ax = plt.subplots(figsize=(5, 5))
    Plot(G)
    ax.set_title("Gráfico de Ejemplo")

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    actual = canvas

btn_show_graph = tk.Button(window, text="Gráfico Ejemplo", command=show_graph)
btn_show_graph.pack(pady=10)

def load_graph():
    global actual
    esconder()
    D = Data('datos.txt')
    fig, ax = plt.subplots(figsize=(5, 5))
    Plot(D)
    ax.set_title("Gráfico Inventado")

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    actual = canvas

btn_load_graph = tk.Button(window, text="Gráfico Inventado", command=load_graph)
btn_load_graph.pack(pady=10)

def file_graph():
    global actual
    esconder()
    filename = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    F = Data(filename)
    fig, ax = plt.subplots(figsize=(5, 5))
    Plot(F)
    ax.set_title("Gráfico Cargado")

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    actual = canvas

btn_file_graph = tk.Button(window, text="Gráfico cargado", command=file_graph)
btn_file_graph.pack(pady=10)

def update_node_dropdown():
    global actual
    if actual:
        node_names = [node.name for node in actual.node]  # Obtén los nombres de los nodos
        node_var.set("")  # Resetea la selección actual
        menu = node_dropdown['menu']
        menu.delete(0, 'end')  # Elimina las opciones anteriores
        for name in node_names:
            menu.add_command(label=name, command=tk._setit(node_var, name))

def show_neighbors():
    if not actual:
        messagebox.showwarning("Warning", "No hay un grafico")
        return

    node_name = node_var.get()
    if not node_name:
        messagebox.showwarning("Warning", "Selecciona un nodo")
        return

    selected_node = next((node for node in actual.node if node.name == node_name), None)
    if selected_node:
        neighbors = [n.name for n in selected_node.neighbors]
        neighbor_text = ", ".join(neighbors) if neighbors else "No tiene vecinos"
        messagebox.showinfo("Vecinos", f"Vecinos de {node_name}: {neighbor_text}")

node_label = tk.Label(window, text="Selecciona un nodo:")
node_label.pack(pady=5)
node_var = tk.StringVar(window)
node_dropdown = tk.OptionMenu(window, node_var, ())
node_dropdown.pack(pady=5)

btn_show_neighbors = tk.Button(window, text="Mostrar vecinos", command=show_neighbors)
btn_show_neighbors.pack(pady=10)

window.mainloop()


