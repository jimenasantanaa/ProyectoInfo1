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
        ("AB", 1, 2), ("AE", 1, 5), ("AK", 1, 11),
        ("BA", 2, 1), ("BC", 2, 3), ("BF", 2, 6), ("BK", 2, 11), ("BG", 2, 7),
        ("CD", 3, 4), ("CG", 3, 7),
        ("DG", 4, 7), ("DH", 4, 8), ("DI", 4, 9),
        ("EF", 5, 6), ("FL", 6, 12),
        ("GB", 7, 2), ("GF", 7, 6), ("GH", 7, 8),
        ("ID", 9, 4), ("IJ", 9, 10), ("JI", 10, 9),
        ("KA", 11, 1), ("KL", 11, 12), ("LK", 12, 11), ("LF", 12, 6)
    ]

    for name, origin, dest in segmentos:
        AddNavSegment(G, NavSegment(name, origin, dest))

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
