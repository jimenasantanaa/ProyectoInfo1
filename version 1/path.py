import math
from navPoint import *
from segment import *
from graph import *
from navPoint import Distance

class Path:
    def __init__(self, origin_navPoint):
        self.navPoints = [origin_navPoint]
        self.cost = 0

    # Añadir navPoint al camino
    def AddNodeToPath(self, navPoint):
        last_navPoint = self.navPoints[-1]
        distance = Distance(last_navPoint, navPoint)
        self.navPoints.append(navPoint)
        self.cost += distance

    # Verificar si navPoint está en el camino
    def ContainsNode(self, navPoint):
        return navPoint in self.navPoints

    # Distancia hasta un navPoint
    def CostToNode(self, navPoint):
        total_cost = 0
        found = False
        for i in range(len(self.navPoints) - 1):
            np1 = self.navPoints[i]
            np2 = self.navPoints[i + 1]
            total_cost += Distance(np1, np2)
            if navPoint == np2:
                found = True
                break
        return total_cost if found else -1

    # Dibujar camino
    def PlotPath(self, ax):
        for i in range(len(self.navPoints) - 1):
            np1 = self.navPoints[i]
            np2 = self.navPoints[i + 1]
            ax.plot([np1.longitude, np2.longitude], [np1.latitude, np2.latitude], 'r-')
            ax.annotate('', xy=(np2.longitude, np2.latitude), xytext=(np1.longitude, np1.latitude),
                        arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->'))

        for np in self.navPoints:
            ax.scatter(np.longitude, np.latitude, color='blue')
            ax.text(np.longitude, np.latitude, np.name, color='black', fontsize=10, ha='right')
