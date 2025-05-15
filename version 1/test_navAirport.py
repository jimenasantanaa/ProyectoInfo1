from NavAirport import *
from navPoint import *
from graph import *


navpoints_list = load_navpoints("Cat_nav.txt")

graph = Graph()
graph.navPoint = navpoints_list

airports = read_airport("Cat_aer.txt")

nombre = input("Introduce el nombre del aeropuerto: ")

aeropuerto = airports.get(nombre)
if aeropuerto is None:
    print(f"Aeropuerto {nombre} no encontrado")
else:
    aeropuerto.relacionar(graph)

    print(f"sid aeropuerto {aeropuerto.name}:")
    for nav in aeropuerto.sid:
        print(f"- {nav.name}: lat {nav.latitude}, lon {nav.longitude}")

    print(f"star aeropuerto {aeropuerto.name}:")
    for nav in aeropuerto.star:
        print(f"- {nav.name}: lat {nav.latitude}, lon {nav.longitude}")