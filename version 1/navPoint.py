from graph import *

class NavPoint:
    def __init__(self, number: int, name: str, latitude: float, longitude: float):
        self.number = number
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

# Cargar gráfico
def load_navpoints(filename):
    import os
    g = Graph()
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                parts = line.split()
                num, name, lat, long = float(parts[0]), parts[1], float(parts[2]), float(parts[3])
                AddNavPoint(g, NavPoint(num, name, lat, long))  # Añadir el punto al gráfico
        return g
    else:
        print("El archivo no es correcto")
