from navPoint import NavPoint
from graph import *
import matplotlib.pyplot as plt
from path import *

# Crear nodos NavPoint
node_A = NavPoint("A", 1, 2.0, 1.0)
node_B = NavPoint("B", 2, 5.0, 5.0)
node_C = NavPoint("C", 3, 9.0, 2.0)
node_D = NavPoint("D", 4, 13.0, 7.0)

# Crear Path
path = Path(node_A)

path.AddNodeToPath(node_B)  # A -> B
path.AddNodeToPath(node_C)  # B -> C
path.AddNodeToPath(node_D)  # C -> D

print(path.ContainsNode(node_B))  # True
print(path.ContainsNode(node_A))  # True
print(path.ContainsNode(NavPoint("E", 5, 10.0, 10.0)))

print("Costo hasta C:", path.CostToNode(node_C))

fig, ax = plt.subplots(figsize=(6, 6))
for node in [node_A, node_B, node_C, node_D]:
    ax.scatter(node.longitude, node.latitude, color='green')
    ax.text(node.longitude, node.latitude, node.name, color='black')

path.PlotPath(ax)
plt.grid(True)
plt.show()
