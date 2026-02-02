import math

import shapely
import numpy as np
from noise import pnoise2

from algorithmic_art.techniques.base_technique import BaseTechnique
from algorithmic_art.techniques.params import ltiles
from algorithmic_art.tools.art_utils import p5map

class LineTiles(BaseTechnique):
    def __init__(self, rng, subdim=None, tilesize=None, line_skip_chance=None, tile_repeat_chance=None, noise_based=None, noisescale=None):
        super().__init__(rng, subdim)

        if tilesize:
            self.tilesize = tilesize
        else:
            self.tilesize = ltiles['randomizers']['tilesize'](self.rng, ltiles['params']['tilesize'])
        
        if line_skip_chance:
            self.line_skip_chance = line_skip_chance
        else:
            self.line_skip_chance = ltiles['randomizers']['line_skip_chance'](self.rng, ltiles['params']['line_skip_chance'])
        
        if tile_repeat_chance:
            self.tile_repeat_chance = tile_repeat_chance
        else:
            self.tile_repeat_chance = ltiles['randomizers']['tile_repeat_chance'](self.rng, ltiles['params']['tile_repeat_chance'])
        
        if noise_based is not None:
            self.noise_based = noise_based
        else:
            self.noise_based = ltiles['randomizers']['noise_based'](self.rng, ltiles['params']['noise_based'])
        
        # only assign noisescale if noise_based is true
        if self.noise_based and noisescale:
            self.noisescale = noisescale
        elif self.noise_based:
            self.noisescale = ltiles['randomizers']['noisescale'](self.rng, ltiles['params']['noisescale'])
    

    def reset(self):
        self.geoms.clear()


    def mutate(self):
        # randomly select mutatable parameter
        p = self.rng.choice([key for key in ltiles['params'] if getattr(self, key) is not None])
        # mutate parameter
        new_val = ltiles['randomizers'][p](self.rng, ltiles['params'][p])
        #print("parameter '" + p + "' mutated from " + str(getattr(self, p)) + " to " + str(new_val))
        setattr(self, p, new_val)
    

    def draw(self):
        n_columns = self.width // self.tilesize
        n_rows = self.height // self.tilesize

        x_off = (self.width - (n_columns * self.tilesize)) / 2
        y_off = (self.height - (n_rows * self.tilesize)) / 2

        for j in range(n_rows):
            for i in range(n_columns):
                x = self.origin_x + (i * self.tilesize) + x_off
                y = self.origin_y + (j * self.tilesize) + y_off

                self.draw_tile(x, y)
                
                # small chance to draw second tile w/ new step and angle in same spot
                if self.rng.random() <= self.tile_repeat_chance:
                    self.draw_tile(x, y)


    def draw_tile(self, x, y):
        a = None
        if self.noise_based:
            noiseval = pnoise2(x / self.noisescale, y / self.noisescale)
            a = p5map(noiseval, 0.0, 1.0, 0.0, math.tau)
        else:
            a = self.rng.uniform(0.0, math.tau)
                
        step = self.rng.randint(4, 8)
        
        xstart = x + self.rng.uniform(0, self.tilesize)
        ystart = y + self.rng.uniform(0, self.tilesize)

        slope = math.tan(a)
        c = ystart - slope * xstart

        down_accept = True
        up_accept = True
        i = 0
        while down_accept or up_accept:
            x0 = x - self.tilesize / 2
            y0 = slope * x0 + c + i * step / math.cos(a)
            x1 = x + self.tilesize + self.tilesize / 2
            y1 = slope * x1 + c + i * step / math.cos(a)

            up_accept = self.line_clip(x0, y0, x1, y1, x, y)

            x0 = x - self.tilesize / 2
            y0 = slope * x0 + c - i * step / math.cos(a)
            x1 = x + self.tilesize + self.tilesize / 2
            y1 = slope * x1 + c - i * step / math.cos(a)

            down_accept = self.line_clip(x0, y0, x1, y1, x, y)

            i += 1
    

    def line_clip(self, x0, y0, x1, y1, clip_x, clip_y):
        # line endpoint encodings
        e0code = None
        e1code = None

        # min and max coordinates of clip window
        xmin = clip_x
        xmax = clip_x + self.tilesize
        ymin = clip_y
        ymax = clip_y + self.tilesize

        accept = False
        while True:
            # get encodings for where line endpoints fall
            e0code = self.encode_endpoint(x0, y0, clip_x, clip_y)
            e1code = self.encode_endpoint(x1, y1, clip_x, clip_y)

            if e0code == 0 and e1code == 0:
                # line is inside clip window - accept & break out
                accept = True
                break
            elif (e0code & e1code) != 0:
                # both points share an outside zone - reject
                break
            else:
                # pick an endpoint outside the clip window
                code = e0code if (e0code != 0) else e1code

                new_x = 0
                new_y = 0
                # find new endpoint to replace current one
                if (code & (1 << 3)) != 0:
                    # endpoint is to the left of clip window
                    new_x = xmin
                    new_y = ((y1 - y0) / (x1 - x0)) * (new_x - x0) + y0
                elif (code & (1 << 2)) != 0:
                    # endpoint is to the right of clip window
                    new_x = xmax
                    new_y = ((y1 - y0) / (x1 - x0)) * (new_x - x0) + y0
                elif (code & (1 << 1)) != 0:
                    # endpoint is above the clip window
                    new_y = ymax
                    new_x = ((x1 - x0) / (y1 - y0)) * (new_y - y0) + x0
                elif (code & (1 << 0)) != 0:
                    # endpoint is below the clip window
                    new_y = ymin
                    new_x = ((x1 - x0) / (y1 - y0)) * (new_y - y0) + x0
                
                # replace the old endpoint
                if code == e0code:
                    x0 = new_x
                    y0 = new_y
                else:
                    x1 = new_x
                    y1 = new_y
        
        d = math.dist([x0, y0], [x1, y1])   # cull very short line segments
        if accept and d > 5.0 and self.rng.random() > self.line_skip_chance:
            self.geoms.append(shapely.LineString([[x0, y0], [x1, y1]]))
        return accept
    

    def encode_endpoint(self, x, y, clip_x, clip_y):
        code = 0

        # min and max coordinates of clip window
        xmin = clip_x
        xmax = clip_x + self.tilesize
        ymin = clip_y
        ymax = clip_y + self.tilesize

        if x < xmin:
            code |= (1 << 3)    # left of clip window
        elif x > xmax:
            code |= (1 << 2)    # right of clip window
        
        if y < ymin:
            code |= (1 << 0)    # above clip window
        elif y > ymax:
            code |= (1 << 1)    # below clip window
        
        return code