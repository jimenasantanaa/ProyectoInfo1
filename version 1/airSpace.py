from graph import Graph, AddNavPoint
from navPoint import *
from navSegment import *
from NavAirport import *

def load_airspace(prefix):
    nav_filename = f"{prefix}_nav.txt"
    seg_filename = f"{prefix}_seg.txt"
    aer_filename = f"{prefix}_aer.txt"

    g = Graph()

    # Cargar NavPoints
    navpoints = load_navpoints(nav_filename)
    for nav in navpoints:
        AddNavPoint(g, nav)

    # Cargar NavSegments
    load_navsegment(seg_filename, g)

    # Cargar Aeropuertos
    airports = read_airport(aer_filename)

    # Relacionar SID y STAR
    for airport in airports.values():
        airport.relacionar(g)

    return g, airports
