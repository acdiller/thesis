import math
import shapely

from algorithmic_art.techniques.base_technique import BaseTechnique
from algorithmic_art.techniques.params import radlines

class RadialLines(BaseTechnique):
    def __init__(self, rng, subdim, n_lines=None, line_length=None, base_r=None, shift=None, shiftstep=None):
        super().__init__(rng, subdim)

        if n_lines:
            self.n_lines = n_lines
        else:
            self.n_lines = radlines['randomizers']['n_lines'](self.rng, radlines['params']['n_lines'])

        if line_length:
            self.line_length = line_length
        else:
            self.line_length = radlines['randomizers']['line_length'](self.rng, radlines['params']['line_length'])

        if base_r:
            self.base_r = base_r
        else:
            self.base_r = radlines['randomizers']['base_r'](self.rng, radlines['params']['base_r'])

        if shift:
            self.shift = shift
        else:
            self.shift = radlines['randomizers']['shift'](self.rng, radlines['params']['shift'])

        if shiftstep:
            self.shiftstep = shiftstep
        else:
            self.shiftstep = radlines['randomizers']['shiftstep'](self.rng, radlines['params']['shiftstep'])

    
    def mutate(self):
        # randomly select mutatable parameter
        p = self.rng.choice([key for key in radlines['params']])
        # mutate parameter
        new_val = radlines['randomizers'][p](self.rng, radlines['params'][p])
        print("parameter '" + p + "' mutated from " + str(getattr(self, p)) + " to " + str(new_val))
        setattr(self, p, new_val)


    def draw(self):
        originx = self.width / 2
        originy = self.height / 2

        for i in range(self.n_lines):
            r = self.base_r + (i % self.shiftstep * self.shift)
            a = i * (math.tau / self.n_lines)

            x1 = r * math.cos(a) + originx
            y1 = r * math.sin(a) + originy
            x2 = x1 + self.line_length * math.cos(a)
            y2 = y1 + self.line_length * math.sin(a)

            self.geoms.append(shapely.LineString([(x1, y1), (x2, y2)]))
    

    def __str__(self):
        cls_name = type(self).__name__
        return f"{cls_name}(n_lines={self.n_lines}, line_length={self.line_length}, base_r={self.base_r}, shift={self.shift}, shiftstep={self.shiftstep})"

















