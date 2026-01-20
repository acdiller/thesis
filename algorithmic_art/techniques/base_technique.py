from abc import ABC, abstractmethod

class BaseTechnique(ABC):
    def __init__(self, rng, subdim):
        self.rng = rng
        self.origin = {'x': int(subdim[0]), 'y': int(subdim[1])}
        self.width = int(subdim[2] - subdim[0])
        self.height = int(subdim[3] - subdim[1])
        #self.palette = palette

        self.geoms = []
    
    
    @abstractmethod
    def reset(self):
        pass


    @abstractmethod
    def mutate(self):
        pass


    @abstractmethod
    def draw(self):
        pass