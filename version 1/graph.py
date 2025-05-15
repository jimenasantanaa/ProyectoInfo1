from node import *
from segment import *
import matplotlib.pyplot as plt
import math
from navPoint import *

class Graph:
    def __init__(self):
        self.navPoint = []
        self.navSegment = []

# Añadir navpoint
def AddNavPoint(g, n):
    if n in g.navPoint:
        return False
    g.navPoint.append(n)
    return True

# Añadir segmento
def AddNavSegment(grafo, segmento):
    origin = None
    destination = None

    for nav_point in grafo.navPoint:
        if nav_point.number == segmento.origin_number:
            origin = nav_point
        elif nav_point.number == segmento.destination_number:
            destination = nav_point

    if origin and destination:
        grafo.navSegment.append(segmento)
        return True
    return False

# Obtener más cercano
def GetClosest(g, latitude, longitude):
    if not g.navPoint:
        return None

    punto = NavPoint(-1, "temp", latitude, longitude)
    closest = g.navPoint[0]
    minimo = Distance(g.navPoint[0], punto)

    for navpoint in g.navPoint[1:]:
        d = Distance(navpoint, punto)
        if d < minimo:
            minimo = d
            closest = navpoint

    return closest

# Obtener vecinos
def GetNavNeighbors(grafo, navpoint):
    vecinos = []
    for seg in grafo.navSegment:
        if seg.origin_number == navpoint.number:
            vecino = next((n for n in grafo.navPoint if n.number == seg.destination_number), None)
            if vecino and vecino not in vecinos:
                vecinos.append(vecino)
        elif seg.destination_number == navpoint.number:
            vecino = next((n for n in grafo.navPoint if n.number == seg.origin_number), None)
            if vecino and vecino not in vecinos:
                vecinos.append(vecino)
    return vecinos

def Plot(g):
    fig, ax = plt.subplots()
    for np in g.navPoint:
        ax.scatter(np.latitude, np.longitude, color='blue')
        ax.text(np.latitude, np.longitude, np.name)

    for seg in g.navSegment:
        origin = next((n for n in g.navPoint if n.number == seg.origin_number), None)
        dest = next((n for n in g.navPoint if n.number == seg.destination_number), None)
        if origin and dest:
            ax.plot([origin.latitude, dest.latitude], [origin.longitude, dest.longitude], 'r-')

    plt.grid(True)
    plt.show()
