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

def GetNavNeighbors(grafo, navpoint):
    vecinos = []
    for seg in grafo.navSegment:
        # Si el navpoint es el origen del segmento, añado el destino
        if seg.origin_number == navpoint.number:
            vecino = next((n for n in grafo.navPoint if n.number == seg.destination_number), None)
            if vecino and vecino not in vecinos:
                vecinos.append(vecino)
        # Si el navpoint es el destino del segmento, añado el origen
        elif seg.destination_number == navpoint.number:
            vecino = next((n for n in grafo.navPoint if n.number == seg.origin_number), None)
            if vecino and vecino not in vecinos:
                vecinos.append(vecino)
    return vecinos