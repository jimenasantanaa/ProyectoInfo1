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


