# step 1: comprobar
from waypoint import *
wp = Waypoint ('A', 41.56, 1.889)
ShowWaypoint(wp)

# step 2: distancia entre dos puntos
from waypoint import *
wp1 = Waypoint('Nou Camp', 41.381623923229995, 2.122853541678448)
wp2 = Waypoint('Santiago Bernabeu', 40.453030507454244, -3.6883551609249308)

ShowWaypoint(wp1)
ShowWaypoint(wp2)

distancia = Haversine(wp1, wp2)
print(f"Distancia entre {wp1.name} y {wp2.name}: {distancia:.2f} km")