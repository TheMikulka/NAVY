class FractalGenerator:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.max_iter = 256
        self.zoom = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0

    def set_max_iter(self, value):
        self.max_iter = value

    def generate(self, x_min, x_max, y_min, y_max):
        raise NotImplementedError("This method should be implemented by subclasses.")