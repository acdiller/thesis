#https://www.gorillasun.de/blog/an-object-oriented-approach-to-random-walkers/
import drawsvg
from base_technique import BaseTechnique

GRID_COLOUR = '#2a2a72'

class Pathways(BaseTechnique):
    def __init__(self, rng, palette, cellsize, show_grid=False):
        super().__init__("pathways", rng, palette)
        self.cellsize = cellsize
        self.show_grid = show_grid

        self.walkers = []
        self.grid = None
    

    def get_directions(self, w):
        dirs = []
        if w.x > 0:
            if not self.grid[w.y][w.x-1]:
                dirs.append((w.x-1, w.y))
        if w.x < len(self.grid[0]):
            if not self.grid[w.y][w.x+1]:
                dirs.append((w.x+1, w.y))
        if w.y > 0:
            if not self.grid[w.y-1][w.x]:
                dirs.append((w.x, w.y-1))
        if w.y < len(self.grid):
            if not self.grid[w.y+1][w.x]:
                dirs.append((w.x, w.y+1))
        return dirs


    def spawn_walker(self, x, y):
        pass


    def draw_grid(self, d, r, c):
        for i in range(r):
            for j in range(c):
                x = j * self.cellsize
                y = i * self.cellsize
                d.append(drawsvg.Rectangle(x, y, self.cellsize, self.cellsize, 
                                           fill='none', stroke=GRID_COLOUR, stroke_weight=0.5))
        return d
    

    def draw(self, d):
        n_rows = (d.height) // self.cellsize
        n_cols = (d.width) // self.cellsize

        self.grid = [[False for _ in range(n_cols)] for _ in range(n_rows)]

        # need to determine some termination criteria
        if self.show_grid:
            self.draw_grid(d, n_rows, n_cols)
        
        return d



class Walker:
    def __init__(self, x, y, life, colour):
        self.x = x
        self.y = y
        self.life = life
        self.colour = colour

        self.path = []