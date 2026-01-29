import random

from src.models.floorplan import FloorPlan, Room


ROOM_SPECS = {
    "Accessioning": (8, 6),
    "Chemistry": (12, 8),
    "Microbiology": (10, 8),
    "Pathology": (10, 8),
    "Cold Storage": (6, 6),
    "Waste": (6, 6),
}


class LayoutSampler:
    def __init__(self, floor: FloorPlan):
        self.floor = floor
        self.rooms = {
            k: Room(k, *v)
            for k, v in ROOM_SPECS.items()
        }

    def random_layout(self, max_tries=500):
        placed = {}
        geoms = []

        for name, room in self.rooms.items():
            ok = False
            for _ in range(max_tries):
                x = random.uniform(0, self.floor.width - room.w)
                y = random.uniform(0, self.floor.height - room.h)
                rot = random.choice([0, 90])

                g = room.shape(x, y, rot)

                if not self.floor.inside(g):
                    continue
                if self.floor.overlaps(g, geoms):
                    continue

                placed[name] = (x, y, rot, g)
                geoms.append(g)
                ok = True
                break

            if not ok:
                return None

        return placed
