from node import *
from graph import *
import matplotlib.pyplot as plt

node_A = Node("A", 1, 2)
node_B = Node("B", 5, 5)
node_C = Node("C", 9, 2)
node_D = Node("D", 13, 7)

path = Path(node_A)

path.AddNodeToPath(node_B)  # A -> B
path.AddNodeToPath(node_C)  # B -> C
path.AddNodeToPath(node_D)  # C -> D

print(path.ContainsNode(node_B))
print(path.ContainsNode(node_A))
print(path.ContainsNode(Node("E", 10, 10)))

print("Costo hasta C:", path.CostToNode(node_C))

fig, ax = plt.subplots(figsize=(6, 6))
for node in [node_A, node_B, node_C, node_D]:
    ax.scatter(node.coordinate_x, node.coordinate_y, color='green')
    ax.text(node.coordinate_x, node.coordinate_y, node.name, color='black')

path.PlotPath(ax)
plt.grid(True)
plt.show()
