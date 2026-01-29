from shapely.geometry import box
from shapely.affinity import rotate


class Room:
    def __init__(self, name, width, height, buffer=1.0):
        self.name = name
        self.w = width
        self.h = height
        self.buffer = buffer

    def shape(self, x, y, rot=0):
        r = box(x, y, x + self.w, y + self.h)
        if rot:
            r = rotate(r, rot, origin="center")
        return r.buffer(self.buffer)


class FloorPlan:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def inside(self, geom):
        return geom.bounds[0] >= 0 and geom.bounds[1] >= 0 and \
               geom.bounds[2] <= self.width and geom.bounds[3] <= self.height

    def overlaps(self, geom, others):
        return any(geom.intersects(o) for o in others)

    def distance(self, g1, g2):
        return g1.centroid.distance(g2.centroid)
