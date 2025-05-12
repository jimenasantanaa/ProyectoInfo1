from NavAirport import *
from graph import *

airports = read_airport("Cat_aer.txt")

nombre = input("Introduce el nombre del aeropuerto: ")

print(f"sid aeropuerto {Airport.name}:")
for nav in Airport.sid:
    print(f"-{nav.name}: lat {nav.lat}, lon {nav.lon}")