import numpy as np
import random

class TerrainGenerator:
    def __init__(self, size=129):
        n = 0
        while (2**n + 1) < size:
            n += 1
        self.size = 2**n + 1
        self.terrain = np.zeros((self.size, self.size))
        
    def generate(self, roughness, seed=None):
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        size = self.size
        self.terrain = np.zeros((size, size))
        
        self.terrain[0, 0] = 0
        self.terrain[0, size-1] = 0
        self.terrain[size-1, 0] = 0
        self.terrain[size-1, size-1] = 0
        
        step = size - 1
        while step > 1:
            half = step // 2
            
            for x in range(0, size-1, step):
                for y in range(0, size-1, step):
                    a = self.terrain[x, y]
                    b = self.terrain[x+step, y]
                    c = self.terrain[x, y+step]
                    d = self.terrain[x+step, y+step]
                    
                    midpoint_value = (a + b + c + d) / 4 + random.uniform(-roughness, roughness)
                    self.terrain[x+half, y+half] = midpoint_value
            
            for x in range(0, size, half):
                for y in range((x + half) % step, size, step):
                    count = 0
                    total = 0
                    
                    # Top
                    if x - half >= 0:
                        total += self.terrain[x-half, y]
                        count += 1
                    
                    # Bottom
                    if x + half < size:
                        total += self.terrain[x+half, y]
                        count += 1
                    
                    # Left
                    if y - half >= 0:
                        total += self.terrain[x, y-half]
                        count += 1
                    
                    # Right
                    if y + half < size:
                        total += self.terrain[x, y+half]
                        count += 1
                    
                    self.terrain[x, y] = total / count + random.uniform(-roughness, roughness)
            roughness *= 0.5
            step = half
        return self.terrain
