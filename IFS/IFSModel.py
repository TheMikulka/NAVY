import random

class IFSModel:
    def __init__(self, transformations):
        self.transformations = transformations

    def apply(self, point):
        t = random.choice(self.transformations)
        return t[0]@point + t[1]