import math

import shapely

from algorithmic_art.techniques.base_technique import BaseTechnique
from algorithmic_art.techniques.params import phyllo
from algorithmic_art.tools.art_utils import constrain
from algorithmic_art.tools.curves import catrom_curve
from algorithmic_art.tools.shapes import circular_sinewave


class Phyllotaxis(BaseTechnique):
    def __init__(self, rng, subdim, start_n=None, c=None, mod=None, radius=None, freq=None, amp=None):
        super().__init__(rng, subdim)

        if start_n:
            self.start_n = start_n
        else:
            self.start_n = phyllo['randomizers']['start_n'](self.rng, phyllo['params']['start_n'])
        
        if c:
            self.c = c
        else:
            self.c = phyllo['randomizers']['c'](self.rng, phyllo['params']['c'])
        
        if mod:
            self.mod = mod
        else:
            self.mod = phyllo['randomizers']['mod'](self.rng, phyllo['params']['mod'])
        
        if radius:
            self.radius = radius
        else:
            self.radius = phyllo['randomizers']['radius'](self.rng, phyllo['params']['radius'])
        
        if freq:
            self.freq = freq
        else:
            self.freq = phyllo['randomizers']['freq'](self.rng, phyllo['params']['freq'])
        
        if amp:
            self.amp = amp
        else:
            self.amp = phyllo['randomizers']['amp'](self.rng, phyllo['params']['amp'])
    

    def reset(self):
        self.geoms.clear()

    
    def mutate(self): 
        # randomly select mutatable parameter
        p = self.rng.choice([key for key in phyllo['params']])
        # mutate parameter
        new_val = phyllo['randomizers'][p](self.rng, phyllo['params'][p])
        print("parameter '" + p + "' mutated from " + str(getattr(self, p)) + " to " + str(new_val))
        setattr(self, p, new_val)
    

    def draw(self):
        center_x = self.origin['x'] + (self.width / 2)
        center_y = self.origin['y'] + (self.height / 2)
        stop = int(min(self.width, self.height) * 0.8)
        for n in range(self.start_n, stop, self.mod):
            a = n * 137.5
            r = self.c * math.sqrt(n)

            a = math.radians(a)
            x = r * math.cos(a) + center_x
            y = r * math.sin(a) + center_y

            self.geoms.append(circular_sinewave(x, y, self.radius, self.freq, self.amp))
            
