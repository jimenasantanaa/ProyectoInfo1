from graph import *

class NavPoint:
    def __init__(self, number: int, name: str, latitude: float, longitude: float):
        self.number = number
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

# Cargar puntos
def load_navpoints(filename):
    navpoints = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            num = float(parts[0])
            name = parts[1]
            lat = float(parts[2])
            lon = float(parts[3])
            navpoints.append(NavPoint(num,name,lat,lon))
    return navpoints

# Distancia
def Distance(n1, n2):
    return math.sqrt((n1.longitude - n2.longitude)**2 + (n1.latitude - n2.latitude)**2)