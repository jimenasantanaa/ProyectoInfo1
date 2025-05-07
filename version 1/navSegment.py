from graph import *

class NavSegment:
    def __init__(self, origin_number, destination_number, distance):
        self.origin_number = origin_number
        self.destination_number = destination_number
        self.distance = distance

# Cargar gráfico
def load_navsegment(filename):
    import os
    g = Graph()
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                parts = line.split()
                origin_num, destination_num, distance = float(parts[0]), parts[1], float(parts[2])
                AddNavSegment(g, NavSegment(origin_num, destination_num, distance))
        return g
    else:
        print("El archivo no es correcto")