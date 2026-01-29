import numpy as np

class Facility:
    def __init__(self, stations: dict):
        self.stations = stations

    def distance(self, a, b):
        return np.linalg.norm(
            np.array(self.stations[a]) -
            np.array(self.stations[b])
        )
