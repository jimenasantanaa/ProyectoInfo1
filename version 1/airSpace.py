from navPoint import *
from navSegment import *
from NavAirport import *
from graph import *

class AirSpace:
    def __init__(self):
        self.navpoints = []
        self.navsegments = []
        self.navairports = []

    def cargar_navpoints(self,filename):
        self.navpoints = load_navpoints(filename)

    def cargar_navsegments(self, filename):

        grafo_temp = Graph()
        grafo_temp.navPoint = self.navpoints
        load_navsegment(filename, grafo_temp)
        self.navsegments = grafo_temp.navSegment

    def cargar_airports(self, filename):
        self.navairports = read_airport(filename)
