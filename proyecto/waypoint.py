import math

class Waypoint:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat =lat
        self.lon = lon

def ShowWaypoint(waypoint):
    print('Nombre:{0}, lat:{1}, lon:{2}'.format (waypoint.name, waypoint.lat, waypoint.lon ))

def Haversine(wp1,wp2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [wp1.lat, wp1.lon, wp2.lat, wp2.lon])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c