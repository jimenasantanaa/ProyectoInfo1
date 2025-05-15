from graph import Graph, AddNavPoint
from navPoint import *
from navSegment import *
from NavAirport import *

# Cargar espacio aéreo
def load_airspace(prefix):
    nav_filename = f"{prefix}_nav.txt"
    seg_filename = f"{prefix}_seg.txt"
    aer_filename = f"{prefix}_aer.txt"

    g = Graph()

    navpoints = load_navpoints(nav_filename)
    for nav in navpoints:
        AddNavPoint(g, nav)

    load_navsegment(seg_filename, g)
    airports = read_airport(aer_filename)

    for airport in airports.values():
        airport.relacionar(g)

    return g, airports
