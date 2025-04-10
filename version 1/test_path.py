# Crear algunos nodos de ejemplo
node_A = Node("A", 1, 2)
node_B = Node("B", 5, 5)
node_C = Node("C", 9, 2)
node_D = Node("D", 13, 7)

# Crear un camino desde A
path = Path(node_A)

# Agregar nodos al camino
path.AddNodeToPath(node_B)  # A -> B
path.AddNodeToPath(node_C)  # B -> C
path.AddNodeToPath(node_D)  # C -> D

# Verificar si un nodo está en el camino
print(path.ContainsNode(node_B))  # Debería devolver True
print(path.ContainsNode(node_A))  # Debería devolver True
print(path.ContainsNode(Node("E", 10, 10)))  # Debería devolver False

# Calcular el costo hasta el nodo C
print("Costo hasta C:", path.CostToNode(node_C))  # Debería devolver la distancia entre A, B y C

# Graficar el camino
fig, ax = plt.subplots(figsize=(6, 6))
for node in [node_A, node_B, node_C, node_D]:
    ax.scatter(node.coordinate_x, node.coordinate_y, color='green')
    ax.text(node.coordinate_x, node.coordinate_y, node.name, color='black')

path.PlotPath(ax)  # Dibuja el camino en el gráfico
plt.grid(True)
plt.show()
