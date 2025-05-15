import math
from node import *
from segment import *
from graph import *
from navPoint import Distance  # Importar Distance aquí

class Path:
    def __init__(self, origin_node):
        self.nodes = [origin_node]
        self.cost = 0

    # Añadir nodo al camino
    def AddNodeToPath(self, node):
        last_node = self.nodes[-1]
        distance = Distance(last_node, node)
        self.nodes.append(node)
        self.cost += distance

    # Verificar si nodo está en el camino
    def ContainsNode(self, node):
        return node in self.nodes

    # Distancia hasta un nodo
    def CostToNode(self, node):
        total_cost = 0
        found = False
        for i in range(len(self.nodes) - 1):
            node1 = self.nodes[i]
            node2 = self.nodes[i + 1]
            total_cost += Distance(node1, node2)
            if node == node2:
                found = True
                break
        return total_cost if found else -1

    # Dibujar camino
    def PlotPath(self, ax):
        for i in range(len(self.nodes) - 1):
            node1 = self.nodes[i]
            node2 = self.nodes[i + 1]
            # Usar longitude y latitude para las coordenadas
            ax.plot([node1.longitude, node2.longitude], [node1.latitude, node2.latitude], 'r-')
            ax.annotate(
                '',
                xy=(node2.longitude, node2.latitude),
                xytext=(node1.longitude, node1.latitude),
                arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->')
            )

        for node in self.nodes:
            ax.scatter(node.longitude, node.latitude, color='blue')
            ax.text(node.longitude, node.latitude, node.name, color='black', fontsize=10, ha='right')
