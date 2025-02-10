#https://www.gorillasun.de/blog/vera-molnar-homage-to-paul-klee/
import drawsvg
import math
from base_technique import BaseTechnique
from art_utils import p5map

GRID_COLOUR = '#2A2A72'

class MolnarHomage(BaseTechnique):
    def __init__(self, rng, palette, num_rows, num_cols, pad=0, show_grid=False):
        super().__init__("molnar-homage-klee", rng, palette)
        self.num_rows = num_rows
        self.num_cols = num_cols

        self.pad = pad
        self.show_grid = show_grid


    def molnar_rect(self, d, x, y, w, h):
        x1 = x
        x2 = x + w
        if self.rng.random() < 0.5:
            x1 = x + w
            x2 = x
        n_diagonals = round(10 * math.pow(self.rng.random(), 0.85))

        draw_lower = self.rng.random() < 0.96
        if draw_lower:
            colour = self.rng.choice(self.palette)
            for i in range(n_diagonals):
                px = p5map(i, 0, n_diagonals, x1, x2)
                py = y + h
                qx = x1
                qy = p5map(i, 0, n_diagonals, y+h, y)
                d.append(drawsvg.Line(px, py, qx, qy, stroke=colour, stroke_weight=1))
        draw_upper = self.rng.random() < 0.96
        if (not draw_lower) or draw_upper:
            colour = self.rng.choice(self.palette)
            for i in range(n_diagonals):
                px = p5map(i, 0, n_diagonals, x2, x1)
                py = y
                qx = x2
                qy = p5map(i, 0, n_diagonals, y, y+h)
                d.append(drawsvg.Line(px, py, qx, qy, stroke=colour, stroke_weight=1))
    

    def molnar_tri(self, d, x, y, w, h):
        x1 = x
        x2 = x + w
        if self.rng.random() < 0.5:
            x1 = x + w
            x2 = x
        n_diagonals = round(10 * math.pow(self.rng.random(), 0.6))

        if self.rng.random() < 0.5:
            colour = self.rng.choice(self.palette)
            for i in range(n_diagonals):
                px = p5map(i, 0, n_diagonals, x1, x2)
                py = y + h
                qx = x1
                qy = p5map(i, 0, n_diagonals, y+h, y)
                d.append(drawsvg.Line(px, py, qx, qy, stroke=colour, stroke_weight=1))
        else:
            colour = self.rng.choice(self.palette)
            for i in range(n_diagonals):
                px = p5map(i, 0, n_diagonals, x2, x1)
                py = y
                qx = x2
                qy = p5map(i, 0, n_diagonals, y, y+h)
                d.append(drawsvg.Line(px, py, qx, qy, stroke=colour, stroke_weight=1))
    

    def draw(self, d):
        cellw = (d.width - self.pad * 2) / self.num_cols
        cellh = (d.height - self.pad * 2) / self.num_rows

        # n rows or n cols???
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                x = i * cellw + self.pad
                y = j * cellh + self.pad
                #x = i * (cellw + pad)
                #y = j * (cellh + pad)

                # DRAW GRID LINES
                if self.show_grid:
                    d.append(drawsvg.Rectangle(x, y, cellw, cellh, fill='none', stroke=GRID_COLOUR, stroke_weight=0.5))
                
                cx = x + (cellw/2)
                cy = y + (cellh/2)

                # probability ladder
                pattern = self.rng.random()
                if pattern < 0.25:
                    # SPLIT CELL VERTICALLY
                    r = self.rng.random()
                    if r < 0.45:
                        self.molnar_rect(d, x, y, cellw/2, cellh)  # left half only
                    elif r < 0.9:
                        self.molnar_rect(d, cx, y, cellw/2, cellh)    # right half only
                    elif r < 0.99999:
                        self.molnar_rect(d, x, y, cellw/2, cellh) # both halves
                        self.molnar_rect(d, cx, y, cellw/2, cellh)
                elif pattern < 0.5:
                    # SPLIT CELL HORIZONTALLY
                    r = self.rng.random()
                    if r < 0.45:
                        self.molnar_rect(d, x, y, cellw, cellh/2) # top half only
                    elif r < 0.9:
                        self.molnar_rect(d, x, cy, cellw, cellh/2)  # bottom half only
                    elif r < 0.99999:
                        self.molnar_rect(d, x, y, cellw, cellh/2) # both
                        self.molnar_rect(d, x, cy, cellw, cellh/2)
                elif pattern < 0.9:
                    # ORTHOGONAL ("L" shaped)
                    if self.rng.random() < 0.5:
                        self.molnar_rect(d, x, y, cellw, cellh/2)   # top
                    else:
                        self.molnar_rect(d, x, cy, cellw, cellh/2)  # bottom
                    
                    if self.rng.random() < 0.5:
                        self.molnar_rect(d, x, y, cellw/2, cellh)   # left
                    else:
                        self.molnar_rect(d, cx, y, cellw/2, cellh)  # right
                else:
                    self.molnar_tri(d, x, y, cellw, cellh)

                    r = self.rng.random()
                    if r < 0.1:
                        self.molnar_rect(d, x, y, cellw, cellh/2)
                    elif r < 0.2:
                        self.molnar_rect(d, x, cy, cellw, cellh/2)
                    elif r < 0.3:
                        self.molnar_rect(d, x, y, cellw/2, cellh)
                    elif r < 0.4:
                        self.molnar_rect(d, cx, y, cellw/2, cellh)

