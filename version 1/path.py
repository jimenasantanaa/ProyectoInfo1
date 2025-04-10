import math
from node import *
from segment import *
from graph import *

class Path:
    def __init__(self, origin_node):
        self.nodes = [origin_node]
        self.cost = 0

    def AddNodeToPath(self, node):
        last_node = self.nodes[-1]
        distance = Distance(last_node, node)
        self.nodes.append(node)
        self.cost = self.cost + distance

    def ContainsNode(self, node):
        for n in self.nodes:
            if n == node:
                return True
        return False

    def CostToNode(self, node):
        total_cost = 0
        found = False
        for i in range(len(self.nodes) -1):
            node1 = self.nodes[i]
            node2 = self.nodes[i + 1]
            total_cost = total_cost + Distance(node1, node2)
            if node == node2:
                found = True
                break
        return total_cost if found else -1

    def PlotPath(self, ax):
        for i in range(len(self.nodes) -1):
            node1 = self.nodes[i]
            node2 = self.nodes[i + 1]
            ax.plot([node1.coordinate_x, node2.coordinate_x], [node1.coordinate_y, node2.coordinate_y])
            ax.annotate('', xy = node2.coordinate_x, node2.coordinate_y), xytext = (node1.coordinate_x, node1.coordinate_y), arrowprops = dict(facecolor = 'red', edgecolor = 'red', arrowstyle = '->'))

        for node in self.nodes:
            ax.scatter(node.coordinate_x, node.coordinate_y, color = 'blue')
            ax.text(node.coordinate_x, node.coordinate_y, node.name, color = 'black', frontsize = 10, ha = 'right')
