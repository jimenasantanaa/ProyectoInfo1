import math
from node import *
from segment import *
from graph import *

class Path:
    def __init__(self, origin_node):
        self.nodes = [origin_node]
        self.cost = 0

    def AddNodeToPath(self, node, cost):
        self.nodes.append(node)
        self.cost = self.cost + cost

    def ContainsNode(self, node):
        for n in self.nodes:
            if n == node:
                return True
        return False

    def CostToNode(self, node):
        if node in self.nodes:
            return self.cost
        return -1

    def PlotPath(self, graph):
        for i in range(len(self.nodes) -1):
            node1 = self.nodes[i]
            node2 = self.nodes[i + 1]
            x_values = [node1.coordinate_x, node2.coordinate_x]
            y_values = [node1.coordinate_y, node2.coordinate_y]
            plt.plot(x_values, y_values, color ='purple')

