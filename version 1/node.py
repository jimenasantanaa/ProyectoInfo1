import math

class Node:
    def __init__(self, name: str, coordinate_x: float, coordinate_y: float):
        self.name = str(name)
        self.coordinate_x = float(coordinate_x)
        self.coordinate_y = float(coordinate_y)
        self.neighbors = []

def AddNeighbor(n1, n2):
    if n2 not in n1.neighbors:
        n1.neighbors.append(n2)
        return True
    return False

def Distance(n1, n2):
    return math.sqrt((n1.coordinate_x - n2.coordinate_x)**2 + (n1.coordinate_y - n2.coordinate_y)**2)
