from algorithmic_art.techniques.base_technique import BaseTechnique
from algorithmic_art.techniques.params import eca
from algorithmic_art.tools.shapes import rect

class ElementaryCA(BaseTechnique):
    def __init__(self, rng, subdim, cellsize=None, rule=None, init_state=None, pad=2):
        super().__init__(rng, subdim)
        
        self.pad = pad  # minimum spacing between elements

        if cellsize:
            self.cellsize = cellsize
        else:
            self.cellsize = eca['randomizers']['cellsize'](self.rng, eca['params']['cellsize'])
        
        if rule:
            self.rule = rule
        else:
            self.rule = eca['randomizers']['rule'](self.rng, eca['params']['rule'])

        if init_state:
            self.init_state = init_state
        else:
            self.init_state = eca['randomizers']['init_state'](self.rng, eca['params']['init_state'])
        
        self.ruleset = [int(n) for n in format(self.rule, '08b')]

        self.history = []


    def reset(self):
        self.geoms.clear()
        self.history.clear()


    def mutate(self):
        # randomly select mutatable parameter
        p = self.rng.choice([key for key in eca['params']])
        # mutate parameter
        new_val = eca['randomizers'][p](self.rng, eca['params'][p])
        print("parameter '" + p + "' mutated from " + str(getattr(self, p)) + " to " + str(new_val))
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
    

    def draw(self):
        cells = []

        num_cells = int((self.width - self.pad * 2) // self.cellsize)
        cells = [0 for _ in range(num_cells)]

        if self.init_state == 'single':
            # starts with single cell in center with initial state of 1
            cells[len(cells) // 2] = 1
        else:
            # random initial cell states 
            for i in range(num_cells):
                cells[i] = 0 if self.rng.random() < 0.5 else 1
        
        num_gens = (self.height - self.pad * 2) // self.cellsize

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
                    
                    self.geoms.append(rect(x + self.pad, y + self.pad, self.cellsize - self.pad, self.cellsize - self.pad))
    

    def __str__(self):
        cls_name = type(self).__name__
        return f"{cls_name}(cellsize={self.cellsize}, rule={self.rule}, init_state={self.init_state})"