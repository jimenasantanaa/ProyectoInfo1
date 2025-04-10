from node import *
from segment import *

import matplotlib.pyplot as plt
import math

class Graph:
    def __init__(self):
        self.node = []
        self.segment = []

def AddNode(g, n):
    if n in g.node:
        return False
    g.node.append(n)
    return True

def AddSegment(g, name, nameOriginNode, nameDestinationNode):
    origin = None
    destination = None
    i = 0
    while i < len(g.node) and (origin is None or destination is None):
        if g.node[i].name == nameOriginNode:
            origin = g.node[i]
        elif g.node[i].name == nameDestinationNode:
            destination = g.node[i]
        i = i + 1
    if origin and destination:
        AddNeighbor(origin, destination)
        segment = Segment(name, origin, destination)
        g.segment.append(segment)
        return True
    return False

def GetClosest(g, x, y):
    if not g.node:
        return None
    closest = g.node[0]
    punto = Node('punto', x, y)
    minimo = Distance(g.node[0], punto)
    i = 1
    while i < len(g.node):
        node = g.node[i]
        d = Distance(node, punto)
        if d < minimo:
            minimo = d
            closest = node
        i = i + 1
    return closest

def Plot(g):
    for segment in g.segment:
        x_values = [segment.origin.coordinate_x, segment.destination.coordinate_x]
        y_values = [segment.origin.coordinate_y, segment.destination.coordinate_y]
        plt.plot(x_values, y_values, color = 'blue')

        plt.annotate('', xy=(segment.destination.coordinate_x, segment.destination.coordinate_y), xytext=(segment.origin.coordinate_x, segment.origin.coordinate_y), arrowprops=dict(facecolor='blue', edgecolor='blue', arrowstyle='->'))

        mid_x = (segment.origin.coordinate_x + segment.destination.coordinate_x) / 2
        mid_y = (segment.origin.coordinate_y + segment.destination.coordinate_y) / 2
        plt.text(mid_x, mid_y, f"{segment.cost:.2f}")

    for node in g.node:
        plt.scatter(node.coordinate_x, node.coordinate_y, label = node.name, color = 'red')
        plt.text(node.coordinate_x, node.coordinate_y, node.name, color = 'black')

    plt.title("Gráfico con nodos y segmentos")
    plt.grid(True)

def PlotNode(g, nameOrigin):
    origin_node = None
    for node in g.node:
        if node.name == nameOrigin:
            origin_node = node
            break
    if origin_node is None:
        return False
    for node in g.node:
        if node == origin_node:
            plt.scatter(node.coordinate_x, node.coordinate_y, color='blue')
            plt.text(node.coordinate_x, node.coordinate_y, node.name)
        elif node == origin_node.neighbors:
            plt.scatter(node.coordinate_x, node.coordinate_y, color='green')
            plt.text(node.coordinate_x, node.coordinate_y, node.name)
        else:
            plt.scatter(node.coordinate_x, node.coordinate_y, color='gray')
            plt.text(node.coordinate_x, node.coordinate_y, node.name)
    for neighbor in origin_node.neighbors:
        x_values = [origin_node.coordinate_x, neighbor.coordinate_x]
        y_values = [origin_node.coordinate_y, neighbor.coordinate_y]
        plt.plot(x_values, y_values, color='red')

    cost = None
    for segment in g.segment:
        if (segment.origin == origin_node and segment.destination == neighbor) or (segment.origin == neighbor and segment.destination == origin_node):
            cost = segment.cost
            break
        if cost is not None:
            mid_x = (origin_node.coordinate_x + neighbor.coordinate_x) / 2
            mid_y = (origin_node.coordinate_y + neighbor.coordinate_y) / 2
            plt.text(mid_x, mid_y, f'{cost:.2f}')
    return True

    plt.title("Gráfico con nodos y segmentos")
    plt.grid(True)

def Data(filename):
    import os
    g = Graph()
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split()
                if parts[0] == 'N':
                    name, x, y = parts[1], float(parts[2]), float(parts[3])
                    AddNode(g, Node(name, x, y))
                elif parts[0] == 'S':
                    name, origin, destination = parts[1], parts[2], parts[3]
                    AddSegment(g, name, origin, destination)
        return g
    else:
        print("El archivo no es correcto")

def DeleteNode(g, node_name):
    node_to_delete = None
    for node in g.node:
        if node.name == node_name:
            node_to_delete = node
            break

    if node_to_delete is None:
        return False

    g.segment = [segment for segment in g.segment if segment.origin != node_to_delete and segment.destination != node_to_delete]
    g.node.remove(node_to_delete)
    return True

def SaveGraph(g, filename):
    with open(filename, 'w') as file:
        for node in g.node:
            file.write(f"N {node.name} {node.coordinate_x} {node.coordinate_y}\n")
        for segment in g.segment:
            file.write(f"S {segment.name} {segment.origin.name} {segment.destination.name}\n")

