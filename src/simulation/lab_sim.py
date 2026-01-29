import simpy
import random
import numpy as np


class ClinicalLabSimulation:
    def __init__(self, env, facility, flows, staff, machines):
        self.env = env
        self.facility = facility
        self.flows = flows

        # Resources
        self.accession_staff = simpy.Resource(env, capacity=staff["accessioning"])
        self.tech_staff = simpy.Resource(env, capacity=staff["techs"])

        self.centrifuges = simpy.Resource(env, capacity=machines["centrifuge"])
        self.analyzers = simpy.Resource(env, capacity=machines["analyzer"])

        self.results = {
            "tat": [],
            "distance": []
        }

    def transport(self, a, b):
        d = self.facility.distance(a, b)
        walking_speed = 1.4  # m/s
        yield self.env.timeout(d / walking_speed)
        return d

    def process_sample(self, name):
        start = self.env.now
        dist = 0

        # Courier -> Accessioning
        d = yield self.env.process(self.transport("Courier Dock", "Accessioning"))
        dist += d

        with self.accession_staff.request() as req:
            yield req
            yield self.env.timeout(random.uniform(1, 3))

        # Accessioning -> Centrifuge
        d = yield self.env.process(self.transport("Accessioning", "Centrifuge"))
        dist += d

        with self.centrifuges.request() as req:
            yield req
            yield self.env.timeout(random.uniform(5, 8))

        # Branching
        branch = random.choice(["Chemistry", "Hematology"])

        d = yield self.env.process(self.transport("Centrifuge", branch))
        dist += d

        with self.analyzers.request() as req:
            yield req
            yield self.env.timeout(random.uniform(8, 15))

        # To storage
        d = yield self.env.process(self.transport(branch, "Cold Storage"))
        dist += d

        self.results["tat"].append(self.env.now - start)
        self.results["distance"].append(dist)

    def arrivals(self, rate):
        i = 0
        while True:
            yield self.env.timeout(random.expovariate(rate))
            i += 1
            self.env.process(self.process_sample(f"S{i}"))
