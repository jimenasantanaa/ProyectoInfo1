from navPoint import *
from navSegment import *
from NavAirport import *

class AirSpace:
    def __init__(self, navpoints, navsegments, navairports):
        self.navpoints = []
        self.navsegments = []
        self.navairports = {}

    def cargar_navpoints(self, filename):
        self.navpoints = load_navpoints(filename)

    def cargar_navsegments(self, filename, grafo):
        self.navsegments = []
        self.navsegments = load_navsegment(filename, grafo)

    def cargar_navairports(self, filename, grafo):
        self.navairports = read_airport(filename)
        for aeropuerto in self.navairports.values():
            aeropuerto.relacionar(grafo)

    def cargar_datos(self, prefijo, grafo):
        navpoints_file = f"{prefijo}_nav.txt"
        navsegments_file = f"{prefijo}_seg.txt"
        navairports_file = f"{prefijo}_aer.txt"

        self.cargar_navpoints(navpoints_file)
        grafo.navPoint = self.navpoints

        self.cargar_navsegments(navsegments_file, grafo)
        self.navsegments = grafo.navSegment

        self.cargar_navairports(navairports_file, grafo)
