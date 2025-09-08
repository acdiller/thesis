from abc import ABC, abstractmethod

class BaseTechnique(ABC):
    def __init__(self, rng, subdim):
        self.rng = rng
        self.origin = (subdim[0], subdim[1])
        self.width = subdim[2]
        self.height = subdim[3]

        self.geoms = []
    
    @abstractmethod
    def draw(self, d):
        pass
