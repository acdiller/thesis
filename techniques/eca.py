import drawsvg
import shapely

from .base_technique import BaseTechnique
from .params import eca_params, eca_randomizers

class ElementaryCA(BaseTechnique):
    def __init__(self, rng, subdim, palette, cellsize=None, rule=None, init_state=None):
        super().__init__(rng, subdim, palette)
        
        if cellsize:
            self.cellsize = cellsize
        else:
            self.cellsize = eca_randomizers['cellsize'](self.rng, eca_params['cellsize'])
        
        if rule:
            self.rule = rule
        else:
            self.rule = eca_randomizers['rule'](self.rng, eca_params['rule'])

        if init_state:
            self.init_state = init_state
        else:
            self.init_state = eca_randomizers['init_state'](self.rng, eca_params['init_state'])
        
        self.ruleset = [int(n) for n in format(self.rule, '08b')]

        self.history = []


    def mutate(self):
        # randomly select mutatable parameter
        p = self.rng.choice([key for key in eca_params])
        # mutate parameter
        new_val = eca_randomizers[p](self.rng, eca_params[p])
        setattr(self, p, new_val)


    def generate(self, cells):
        """Compute the next generation of the ECA based on the current generation."""
        nextgen = [0 for _ in range(len(cells))]
        # LEFTMOST EDGE CELL
        nextgen[0] = self.check_rule(cells[len(cells)-1], cells[0], cells[1])
        # RIGHTMOST EDGE CELL
        nextgen[len(cells)-1] = cells[0]
        # EVERYTHING ELSE
        for i in range(1, len(cells) - 1):
            left = cells[i-1]
            mid = cells[i]
            right = cells[i+1]
            nextgen[i] = self.check_rule(left, mid, right)
        return nextgen
    

    def check_rule(self, a, b, c):
        s = str(a) + str(b) + str(c)
        index = int(s, 2)
        return self.ruleset[7 - index]
    

    def draw(self, d):
        cells = []

        num_cells = int((self.width - 2) // self.cellsize)
        cells = [0 for _ in range(num_cells)]

        if self.init_state == 'single':
            # starts with single cell in center with initial state of 1
            cells[len(cells) // 2] = 1
        else:
            # random initial cell states 
            for i in range(num_cells):
                cells[i] = 0 if self.rng.random() < 0.5 else 1
        
        num_gens = (self.height - 2) // self.cellsize

        self.history.append(cells)
        gen = 1
        while gen < num_gens:
            cells = self.generate(cells)
            self.history.append(cells)
            gen += 1
        
        # draw out full history
        for g, generation in enumerate(self.history):
            for i in range(len(generation)):
                if generation[i] == 1:
                    x = self.origin['x'] + (i * self.cellsize)
                    y = self.origin['y'] + (g * self.cellsize)

                    colour = self.rng.choice(self.palette)
                    pad = 2   # offset so lines don't overlap
                    d.append(drawsvg.Rectangle(x + pad, y + pad , self.cellsize - pad, self.cellsize - pad,
                                       fill='none', stroke=colour, stroke_weight=1))
                    
                    self.geoms.append(shapely.box(x + pad, y + pad, (x + self.cellsize - pad), (y + self.cellsize - pad)).boundary)
        return d