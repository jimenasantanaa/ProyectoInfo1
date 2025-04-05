from waypoint import Waypoint, ShowWaypoint, Haversine

class FlightPlan:
    def __init__(self, name):
        self.name = name
        self.list = []

    def ShowFlightPlan(self):
        print(f"Flight plan: {self.name}")
        print("list: ")
        for wp in self.list:
            ShowWaypoint(wp)

    def AddWaypoint(self, waypoint):
        self.list.append(waypoint)

    def FindWaypoint(fp, name):
        for wp in fp.list:
            if wp.name == name:
                return wp
        return None
    def RemoveWaypoint(self, name):
        for wp in self.list:
            if wp.name == name:
                self.list.remove(wp)

    def FlightPlanLenght(self):
        distancia = 0
        i = 0
        while i < len(self.list) -1:
            distancia = distancia + Haversine(self.list[i], self.list[i+1])
            i = i + 1
        return distancia

import math
import matplotlib.pyplot as plt
def PlotFlightPlan (fp):
    for wp in fp.list:
        plt.plot(wp.lon,wp.lat, 'o', color='red', markersize=5)
        plt.text(wp.lon + 0.5, wp.lat + 0.5, wp.name, color='green', weight='bold', fontsize=6)
    for i in range(len(fp.list) - 1):
        wp1 = fp.list[i]
        wp2 = fp.list[i + 1]

        plt.annotate("", xy=(wp2.lon, wp2.lat), xytext=(wp1.lon, wp1.lat), arrowprops=dict(arrowstyle="->", color='blue', lw=1.5))

        mid_lon = (wp1.lon + wp2.lon) / 2
        mid_lat = (wp1.lat + wp2.lat) / 2

        distance = Haversine(wp1, wp2)

        plt.text(mid_lon, mid_lat, f"{distance:.1f} km", color='blue', fontsize=7, weight='bold')
    # Coordenadas de un punto en el extremo Noroeste de la penñinsula ibérica
    latNW = 43.62481631158062
    lonNW = -8.902207838560653
    # Coordenadas de un punto en el extremo Sureste de la península ibérica
    latSE = 35.98754955400314
    lonSE = 3.8847514743561953

    plt.axis([lonNW, lonSE, latSE, latNW])
    plt.grid(color='red', linestyle='dashed', linewidth=0.5)
    plt.title('Tu plan de vuelo: '+ fp.name)
    plt.show()

def LoadFlightPlan(fileName):
    with open(fileName, 'r') as file:
        lines = file.readlines()

    flight_plan = FlightPlan(lines[0].strip())

    for line in lines[1:]:
        name, lat, lon = line.strip().split(',')
        flight_plan.AddWaypoint(Waypoint(name, float(lat), float(lon)))

    return flight_plan

def SaveFlightPlan(fp, fileName):
    with open(fileName, 'w') as file:
        file.write(fp.name + '\n')
        for wp in fp.list:
            file.write(f"{wp.name},{wp.lat},{wp.lon}\n")

