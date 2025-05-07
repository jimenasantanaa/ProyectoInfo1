from graph import AddNavSegment

class NavSegment:
    def __init__(self, origin_number, destination_number, distance):
        self.origin_number = origin_number
        self.destination_number = destination_number
        self.distance = distance

# Cargar segmentos
def load_navsegment(filename, grafo):
    import os
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                parts = line.split()
                origin_num = int(parts[0])
                destination_num = int(parts[1])
                distance = float(parts[2])

                nav_segment = NavSegment(origin_num, destination_num, distance)
                AddNavSegment(grafo, nav_segment)
        return grafo
    else:
        print("El archivo no es correcto")
        return grafo

