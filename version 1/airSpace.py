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
    with open(filename, "w") as f:
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

    with open(filename, "w") as f:
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

def export_neighbors_to_kml(node, neighbors, segments, filename="neighbors.kml"):
    with open(filename, "w") as f:
        f.write("<kml xmlns='http://www.opengis.net/kml/2.2'>\n")
        f.write("  <Document>\n")

        # Nodo central
        f.write("    <Placemark>\n")
        f.write(f"      <name>{node.name} (Central)</name>\n")
        f.write("      <Point>\n")
        f.write(f"        <coordinates>{node.longitude},{node.latitude},0</coordinates>\n")
        f.write("      </Point>\n")
        f.write("    </Placemark>\n")

        # Vecinos
        for neighbor in neighbors:
            f.write("    <Placemark>\n")
            f.write(f"      <name>{neighbor.name}</name>\n")
            f.write("      <Point>\n")
            f.write(f"        <coordinates>{neighbor.longitude},{neighbor.latitude},0</coordinates>\n")
            f.write("      </Point>\n")
            f.write("    </Placemark>\n")

        # Segmentos
        for seg in segments:
            if (seg.origin_number == node.number and any(n.number == seg.destination_number for n in neighbors)) or \
               (seg.destination_number == node.number and any(n.number == seg.origin_number for n in neighbors)):
                origin = node if seg.origin_number == node.number else next(n for n in neighbors if n.number == seg.origin_number)
                destination = next(n for n in neighbors if n.number == seg.destination_number) if seg.destination_number != node.number else node
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

def export_path_to_kml(path, filename="path.kml"):
    with open(filename, "w") as f:
        f.write("<kml xmlns='http://www.opengis.net/kml/2.2'>\n")
        f.write("  <Document>\n")

        # Escribimos la línea de la ruta
        f.write("    <Placemark>\n")
        f.write("      <name>Camino más corto</name>\n")
        f.write("      <LineString>\n")
        f.write("        <tessellate>1</tessellate>\n")
        f.write("        <coordinates>\n")

        for point in path.navPoints:
            f.write(f"          {point.longitude},{point.latitude},0\n")

        f.write("        </coordinates>\n")
        f.write("      </LineString>\n")
        f.write("    </Placemark>\n")

        # Escribimos cada punto de la ruta
        for point in path.navPoints:
            f.write("    <Placemark>\n")
            f.write(f"      <name>{point.name}</name>\n")
            f.write("      <Point>\n")
            f.write(f"        <coordinates>{point.longitude},{point.latitude},0</coordinates>\n")
            f.write("      </Point>\n")
            f.write("    </Placemark>\n")

        f.write("  </Document>\n")
        f.write("</kml>\n")


def export_navpoints_to_txt(navpoints, filename="navpoint_new.txt"):
    with open(filename, "w") as f:
        for p in navpoints:
            f.write(f"{p.number} {p.name} {p.latitude} {p.longitude}\n")

def export_navsegments_to_txt(navsegments, filename="navsegment_new.txt"):
    with open(filename, "w") as f:
        for s in navsegments:
            f.write(f"{s.origin_number} {s.destination_number} {s.distance}\n")
