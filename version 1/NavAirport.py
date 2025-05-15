from graph import *
from navPoint import *

class Airport:
    def __init__(self, name: str):
        self.name = str(name)
        self.sid = []
        self.star = []

    def relacionar(self, graph:Graph):
        self.sid = list(set(name.strip().upper() for name in self.sid))
        self.star = list(set(name.strip().upper() for name in self.star))

        sid_nuevo = []
        for name in self.sid:
            for nav in graph.navPoint:
                if nav.name.strip().upper() == name:
                    sid_nuevo.append(nav)
                    break

        self.sid = sid_nuevo

        star_nuevo = []
        for name in self.star:
            for nav in graph.navPoint:
                if nav.name.strip().upper() == name:
                    star_nuevo.append(nav)
                    break
        self.star = star_nuevo

# Cargar aeropuertos
def read_airport(filename):
    airports = {}
    current_airport = None
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if not line.endswith(".D") and not line.endswith(".A"):
                current_airport = Airport(line)
                airports[line.upper()] = current_airport
            elif line.endswith(".D"):
                if current_airport:
                    current_airport.sid.append(line.upper())
            elif line.endswith(".A"):
                if current_airport:
                    current_airport.star.append(line)
    return airports

