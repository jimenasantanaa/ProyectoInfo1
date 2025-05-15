from airSpace import *
from navPoint import *

prefix = input("Introduce el prefijo del espacio aéreo (cat, esp, eu): ").strip().lower()

graph, airports = load_airspace(prefix)

nombre = input("Introduce el nombre del aeropuerto: ").strip().upper()

if nombre in airports:
    aeropuerto = airports[nombre]
    print(f"\nSID de {nombre}:")
    for sid in aeropuerto.sid:
        print(f"- {sid.name}: lat {sid.latitude}, lon {sid.longitude}")

    print(f"\nSTAR de {nombre}:")
    for star in aeropuerto.star:
        print(f"- {star.name}: lat {star.latitude}, lon {star.longitude}")
else:
    print("Aeropuerto no encontrado.")
