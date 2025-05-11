import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation

class ForestFireSimulation:
    EMPTY = 0
    TREE = 1
    FIRE = 2
    BURNT = 3
    
    def __init__(self, size=100, p=0.05, f=0.001, forest_density=0.5, neighborhood="moore"):
        self.size = size
        self.p = p 
        self.f = f  
        self.forest_density = forest_density 
        self.neighborhood = neighborhood
        self.forest = self._initialize_forest()
        
        self.fig, self.ax = plt.subplots()
        cmap = colors.ListedColormap(['brown', 'green', 'orange', 'black'])
        bounds = [self.EMPTY, self.TREE, self.FIRE, self.BURNT, self.BURNT + 1]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        self.img = self.ax.imshow(self.forest, cmap=cmap, norm=norm)
        
    def _initialize_forest(self):
        forest = np.zeros((self.size, self.size)) 
        
        for i in range(self.size):
            for j in range(self.size):
                if np.random.random() < self.forest_density:
                    forest[i, j] = self.TREE
        
        forest[0, :] = self.BURNT
        forest[self.size-1, :] = self.BURNT
        forest[:, 0] = self.BURNT
        forest[:, self.size-1] = self.BURNT
        
        return forest
    
    def _update_forest(self):
        new_forest = np.copy(self.forest)
        
        for i in range(1, self.size-1):
            for j in range(1, self.size-1):
                if self.forest[i, j] == self.TREE:
                    if self.neighborhood == "moore":
                        neighbors_on_fire = np.any(self.forest[i-1:i+2, j-1:j+2] == self.FIRE)
                    else: 
                        neighbors = [self.forest[i-1, j], self.forest[i+1, j], 
                                    self.forest[i, j-1], self.forest[i, j+1]]
                        neighbors_on_fire = np.any([n == self.FIRE for n in neighbors])
                    
                    if neighbors_on_fire:
                        new_forest[i, j] = self.FIRE 
                    elif np.random.random() < self.f:
                        new_forest[i, j] = self.FIRE 
                        
                elif self.forest[i, j] == self.FIRE:
                    new_forest[i, j] = self.BURNT 
                    
                elif (self.forest[i, j] == self.BURNT and 0.5 > np.random.random()) or self.forest[i, j] == self.EMPTY:
                    if np.random.random() < self.p:
                        new_forest[i, j] = self.TREE  
                    else:
                        new_forest[i, j] = self.EMPTY
        
        self.forest = new_forest
        return self.forest
    
    def _update_frame(self, frameNum):
        self._update_forest()
        self.img.set_data(self.forest)
        return [self.img]
    
    def run(self, interval=50, title=None):
        self.ani = animation.FuncAnimation(
            self.fig, self._update_frame, interval=interval, blit=True
        )
        plt.title(f"Forest Fire Simulation {title}")
        plt.show()