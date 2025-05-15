from graph import *
from navPoint import *
import matplotlib.pyplot as plt
from navSegment import *

def CreateGraphNav():
    G = Graph()
    AddNavPoint(G, NavPoint(1, "A", 1, 20))
    AddNavPoint(G, NavPoint(2, "B", 8, 17))
    AddNavPoint(G, NavPoint(3, "C", 15, 20))
    AddNavPoint(G, NavPoint(4, "D", 18, 15))
    AddNavPoint(G, NavPoint(5, "E", 2, 4))
    AddNavPoint(G, NavPoint(6, "F", 6, 5))
    AddNavPoint(G, NavPoint(7, "G", 12, 12))
    AddNavPoint(G, NavPoint(8, "H", 10, 3))
    AddNavPoint(G, NavPoint(9, "I", 19, 1))
    AddNavPoint(G, NavPoint(10, "J", 13, 5))
    AddNavPoint(G, NavPoint(11, "K", 3, 15))
    AddNavPoint(G, NavPoint(12, "L", 4, 10))

    segmentos = [
        (1, 2, 5), (1, 5, 17), (1, 11, 14),
        (2, 1, 5), (2, 3, 7), (2, 6, 13), (2, 11, 8), (2, 7, 9),
        (3, 4, 6), (3, 7, 10),
        (4, 7, 8), (4, 8, 7), (4, 9, 9),
        (5, 6, 6), (6, 12, 9),
        (7, 2, 9), (7, 6, 4), (7, 8, 6),
        (9, 4, 9), (9, 10, 8), (10, 9, 8),
        (11, 1, 14), (11, 12, 6), (12, 11, 6), (12, 6, 10)]

    for origin, dest, dist in segmentos:
        AddNavSegment(G, NavSegment(origin, dest, dist))

    return G

print("Probando el grafo...")
G = CreateGraphNav()

plt.figure()
Plot(G)

origin = GetClosest(G, 15, 5)
print(origin.name)  # Debería ser J

origin = GetClosest(G, 8, 19)
print(origin.name)  # Debería ser B

plt.show()
