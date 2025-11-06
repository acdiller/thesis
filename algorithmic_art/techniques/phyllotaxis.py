import math

import shapely

from algorithmic_art.techniques.base_technique import BaseTechnique
#from algorithmic_art.techniques.params import phyllo
from algorithmic_art.tools.curves import catrom_curve
from algorithmic_art.tools.shapes import circular_sinewave


class Phyllotaxis(BaseTechnique):
    def __init__(self, rng, subdim, start_n=None, c=None, mod=None, radius=None, freq=None, amp=None):
        super().__init__(rng, subdim)

        if start_n:
            self.start_n = start_n
        
        if c:
            self.c = c
        
        if mod:
            self.mod = mod
        
        if radius:
            self.radius = radius
        
        if freq:
            self.freq = freq
        
        if amp:
            self.amp = amp
    
    def mutate(self): 
        pass
    

    def draw(self):
        stop = int(min(self.width, self.height) * 0.8)
        for n in range(self.start_n, stop, self.mod):
            a = n * 137.5
            r = self.c * math.sqrt(n)

            a = math.radians(a)
            x = r * math.cos(a) + self.width / 2
            y = r * math.sin(a) + self.height / 2

            self.geoms.append(circular_sinewave(x, y, self.radius, self.freq, self.amp))
            
