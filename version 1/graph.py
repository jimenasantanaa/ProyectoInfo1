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



def Plot(g):
    # Dibuja los segmentos (líneas entre navpoints)
    for segment in g.navSegment:
        # Buscamos los NavPoints origen y destino por número
        origin = next((n for n in g.navPoint if n.number == segment.origin_number), None)
        destination = next((n for n in g.navPoint if n.number == segment.destination_number), None)

        if origin is None or destination is None:
            continue  # Si no se encuentran los navpoints, saltar este segmento

        x_values = [origin.longitude, destination.longitude]
        y_values = [origin.latitude, destination.latitude]
        plt.plot(x_values, y_values, color='blue')

        # Flecha que indica dirección
        plt.annotate(
            '',
            xy=(destination.longitude, destination.latitude),
            xytext=(origin.longitude, origin.latitude),
            arrowprops=dict(facecolor='blue', edgecolor='blue', arrowstyle='->')
        )

        mid_x = (origin.longitude + destination.longitude) / 2
        mid_y = (origin.latitude + destination.latitude) / 2
        plt.text(mid_x, mid_y, f"{segment.cost:.2f}")

    # Dibuja los NavPoints
    for navpoint in g.navPoint:
        plt.scatter(navpoint.longitude, navpoint.latitude, label=navpoint.name, color='red')
        plt.text(navpoint.longitude, navpoint.latitude, navpoint.name, color='black', fontsize=8)

    plt.title("Gráfico con NavPoints y NavSegments")
    plt.grid(True)


def PlotNode(g, nameOrigin):
    # Buscar el NavPoint origen por nombre
    origin_node = next((n for n in g.navPoint if n.name == nameOrigin), None)
    if origin_node is None:
        return False

    # Obtener vecinos usando la función adaptada GetNavNeighbors
    vecinos = GetNavNeighbors(g, origin_node)

    # Dibujar todos los NavPoints con diferente color según su relación con el origen
    for navpoint in g.navPoint:
        if navpoint == origin_node:
            plt.scatter(navpoint.longitude, navpoint.latitude, color='blue')
            plt.text(navpoint.longitude, navpoint.latitude, navpoint.name, fontsize=8)
        elif navpoint in vecinos:
            plt.scatter(navpoint.longitude, navpoint.latitude, color='green')
            plt.text(navpoint.longitude, navpoint.latitude, navpoint.name, fontsize=8)
        else:
            plt.scatter(navpoint.longitude, navpoint.latitude, color='gray')
            plt.text(navpoint.longitude, navpoint.latitude, navpoint.name, fontsize=8)

    # Dibujar segmentos entre el origen y sus vecinos
    for vecino in vecinos:
        x_values = [origin_node.longitude, vecino.longitude]
        y_values = [origin_node.latitude, vecino.latitude]
        plt.plot(x_values, y_values, color='red')

        # Buscar costo del segmento correspondiente
        cost = None
        for segment in g.navSegment:
            if (segment.origin_number == origin_node.number and segment.destination_number == vecino.number) or \
               (segment.destination_number == origin_node.number and segment.origin_number == vecino.number):
                cost = segment.cost
                break

        if cost is not None:
            mid_x = (origin_node.longitude + vecino.longitude) / 2
            mid_y = (origin_node.latitude + vecino.latitude) / 2
            plt.text(mid_x, mid_y, f'{cost:.2f}')

    plt.title(f"Vecinos de {nameOrigin}")
    plt.grid(True)

    return True


def DeleteNavPoint(g, navpoint_number):
    navpoint_to_delete = None
    for navpoint in g.navPoint:
        if navpoint.number == navpoint_number:
            navpoint_to_delete = navpoint
            break

    if navpoint_to_delete is None:
        return False

    # Eliminar segmentos que tengan origen o destino en el navpoint a borrar
    g.navSegment = [
        seg for seg in g.navSegment
        if seg.origin_number != navpoint_to_delete.number and seg.destination_number != navpoint_to_delete.number
    ]
    g.navPoint.remove(navpoint_to_delete)
    return True

def SaveGraph(g, filename):
    with open(filename, 'w') as file:
        for navpoint in g.navPoint:
            file.write(f"N {navpoint.number} {navpoint.name} {navpoint.latitude} {navpoint.longitude}\n")
        for segment in g.navSegment:
            file.write(f"S {segment.name} {segment.origin_number} {segment.destination_number}\n")
