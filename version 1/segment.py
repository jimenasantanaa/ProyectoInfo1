from node import *

class Segment:
    def __init__(self, name, origin: Node, destination: Node):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = Distance(origin, destination)
