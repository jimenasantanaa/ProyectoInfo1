from navPoint import NavPoint, load_navpoints
from NavSegment import NavSegment, load_navsegment
from NavAirport import Airport, read_airport

class AirSpace:
    def __init__(self, navpoints, navsegments, navairports):
        self.navpoints = navpoints      # Lista de NavPoint
        self.navsegments = navsegments  # Lista de NavSegment
        self.navairports = navairports  # Diccionario de Airport

    def cargar_navpoints(self, filename):
        self.navpoints = load_navpoints(filename)

    def cargar_navsegments(self, filename, grafo):
        self.navsegments = []
        # Se asume que grafo.navPoint ya contiene los NavPoints
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
        grafo.navPoint = self.navpoints  # Asignar los puntos al grafo

        self.cargar_navsegments(navsegments_file, grafo)
        self.navsegments = grafo.navSegment  # Actualizar desde el grafo

        self.cargar_navairports(navairports_file, grafo)
