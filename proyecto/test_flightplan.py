#step 3: flight plan
from flightplan import *
from waypoint import *

fp = FlightPlan("Flight plan")

wp1 = Waypoint('Nou Camp', 41.381623923229995, 2.122853541678448)
wp2 = Waypoint('Santiago Bernabeu', 40.453030507454244, -3.6883551609249308)
wp3 = Waypoint('Balaidos', 42.211904178262195, -8.739772189675971)
wp4 = Waypoint('Sanchez Pizjuan', 37.38276157689335, -5.971691936532935)

AddWaypoint(fp, wp1)
AddWaypoint(fp, wp2)
AddWaypoint(fp, wp3)
AddWaypoint(fp, wp4)

ShowFlightPlan(fp)

# Waypoint encontrado
wp_found = FindWaypoint(fp, "Nou Camp")
if wp_found:
    print(f"Waipoint encontrado {wp_found.name}, {wp_found.lat}, {wp_found.lon}")
else:
    print("No encontrado")

# Eliminar waypoint
RemoveWaypoint(fp, "Nou Camp")
ShowFlightPlan(fp)

# Distancia total
distancia = FlightPlanLenght(fp)
print(f"Distancia total: {distancia:.2f} km")

PlotFlightPlan(fp)
plt.show()

SaveFlightPlan(fp, "plan_vuelo.txt")
fp_cargado = LoadFlightPlan("plan_vuelo.txt")
for wp in fp_cargado.list:
    print(f"📍 {wp.name}: ({wp.lat}, {wp.lon})")


