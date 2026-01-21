from abc import ABC, abstractmethod

class BaseTechnique(ABC):
    def __init__(self, rng, subdim=None):
        self.rng = rng
        if subdim:
            self.origin_x = int(subdim[0])
            self.origin_y = int(subdim[1])
            self.width = int(subdim[2] - subdim[0])
            self.height = int(subdim[3] - subdim[1])
        else:
            self.origin_x = 0
            self.origin_y = 0
            self.width = 1054
            self.height = 816
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