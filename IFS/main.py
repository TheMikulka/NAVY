from IFSModel import IFSModel
from IFSUI import IFSUI
from models import *
class IFSMain:
    def __init__(self, model_data, iterations=10000):
        self.model = IFSModel(model_data)
        self.iterations = iterations
        self.history = []

    def generate(self):
        point = np.zeros(3)
        for _ in range(self.iterations):
            point = self.model.apply(point)
            self.history.append(point)

    def run(self, title="3D Fractal"):
        self.generate()
        IFSUI.plot_3d(np.array(self.history), title)

if __name__ == "__main__":
    print("Zobrazuji model 1...")
    model1 = IFSMain(MODELS[0], iterations=10000)
    model1.run("Fraktálový Model 1 (3D)")

    print("Zobrazuji model 2...")
    model2 = IFSMain(MODELS[1], iterations=1000)
    model2.run("Fraktálový Model 2 (3D)")