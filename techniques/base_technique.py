from abc import ABC, abstractmethod

class BaseTechnique(ABC):
    def __init__(self, rng, subdim, palette):
        self.rng = rng
        self.origin = {'x': subdim[0], 'y': subdim[1]}
        self.width = subdim[2]
        self.height = subdim[3]
        self.palette = palette

        self.geoms = []
    
    @abstractmethod
    def draw(self, d):
        pass

    @abstractmethod
    def randomize_parameters(self):
        pass

    @abstractmethod
    def mutate(self):
        pass