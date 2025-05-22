from graph import Graph, AddNavPoint
from navPoint import *
from navSegment import *
from NavAirport import *

# Cargar espacio aéreo
def load_airspace(prefix):
    nav_filename = f"{prefix}_nav.txt"
    seg_filename = f"{prefix}_seg.txt"
    aer_filename = f"{prefix}_aer.txt"

    g = Graph()

    navpoints = load_navpoints(nav_filename)
    for nav in navpoints:
        AddNavPoint(g, nav)

    load_navsegment(seg_filename, g)
    airports = read_airport(aer_filename)

    for airport in airports.values():
        airport.relacionar(g)

    return g, airports


def export_navpoints_to_kml(navpoints, filename="points.kml"):
    with open(filename, "a") as f:
        f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        f.write("<kml xmlns='http://www.opengis.net/kml/2.2'>\n")
        f.write("  <Document>\n")

        for point in navpoints:
            f.write("    <Placemark>\n")
            f.write(f"      <name>{point.name}</name>\n")
            f.write("      <Point>\n")
            f.write(f"        <coordinates>{point.longitude},{point.latitude},0</coordinates>\n")
            f.write("      </Point>\n")
            f.write("    </Placemark>\n")

        f.write("  </Document>\n")
        f.write("</kml>\n")

def export_navsegments_to_kml(navsegments, navpoints, filename="segments.kml"):
    id_to_point = {p.number: p for p in navpoints}

    with open(filename, "a") as f:
        f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        f.write("<kml xmlns='http://www.opengis.net/kml/2.2'>\n")
        f.write("  <Document>\n")

        for seg in navsegments:
            origin = id_to_point.get(seg.origin_number)
            destination = id_to_point.get(seg.destination_number)
            if not origin or not destination:
                continue

            f.write("    <Placemark>\n")
            f.write("      <LineString>\n")
            f.write("        <tessellate>1</tessellate>\n")
            f.write("        <coordinates>\n")
            f.write(f"          {origin.longitude},{origin.latitude},0\n")
            f.write(f"          {destination.longitude},{destination.latitude},0\n")
            f.write("        </coordinates>\n")
            f.write("      </LineString>\n")
            f.write("    </Placemark>\n")

        f.write("  </Document>\n")
        f.write("</kml>\n")
