import math

import shapely
import numpy as np
from noise import pnoise2

from algorithmic_art.techniques.base_technique import BaseTechnique
from algorithmic_art.techniques.params import ltiles
from algorithmic_art.tools.art_utils import p5map

class LineTiles(BaseTechnique):
    def __init__(self, rng, subdim, tilesize=None, step=None, skip_chance=None, repeat_chance=None, noise_based=None, noisescale=None):
        super().__init__(rng, subdim)

        if tilesize:
            self.tilesize = tilesize
        else:
            self.tilesize = ltiles['randomizers']['tilesize'](self.rng, ltiles['params']['tilesize'])
        
        if step:
            self.step = step
        else:
            self.step = ltiles['randomizers']['step'](self.rng, ltiles['params']['step'])
        
        if skip_chance:
            self.skip_chance = skip_chance
        else:
            self.skip_chance = ltiles['randomizers']['skip_chance'](self.rng, ltiles['params']['skip_chance'])
        
        if repeat_chance:
            self.repeat_chance = repeat_chance
        else:
            self.repeat_chance = ltiles['randomizers']['repeat_chance'](self.rng, ltiles['params']['repeat_chance'])
        
        if noise_based:
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
    

    def encode_endpoint(self, x, y, clipx, clipy, clipw, cliph):
        code = 0

        # calculate min and max coordinates of clip window
        xmin = clipx
        xmax = clipx + clipw
        ymin = clipy
        ymax = clipy + cliph

        if x < xmin:
            code |= (1 << 3)    # left of clip window
        elif x > xmax:
            code |= (1 << 2)    # right of clip window
        
        if y < ymin:
            code |= (1 << 0)   # above clip window
        elif y > ymax:
            code |= (1 << 1)    # below clip window
        
        return code
    

    def line_clip(self, x0, y0, x1, y1, clipx, clipy):
        clipw = self.tilesize
        cliph = self.tilesize
        e0code = None
        e1code = None

        # calculate min and max coordinates of clip window
        xmin = clipx
        xmax = clipx + clipw
        ymin = clipy
        ymax = clipy + cliph

        # whether line should be drawn or not
        accept = False

        while True:
            # get encodings for line endpoints
            e0code = self.encode_endpoint(x0, y0, clipx, clipy, clipw, cliph)
            e1code = self.encode_endpoint(x1, y1, clipx, clipy, clipw, cliph)

            if (e0code == 0) and (e1code == 0):
                # if line is inside window, accept and break out of loop
                accept = True
                break
            elif (e0code & e1code) != 0:
                # if bitwise AND is not 0, both points share an outside zone - reject it and break out
                break
            else:
                # pick an endpoint outside clip window
                code = e0code if (e0code != 0) else e1code
                newx = 0
                newy = 0

                # find new endpoint to replace the current one
                if (code & (1 << 3)) != 0:
                    # endpoint is left of clip window
                    newx = xmin
                    newy = ((y1 - y0) / (x1 - x0)) * (newx - x0) + y0
                elif (code & (1 << 2)) != 0:
                    # endpoint is right of clip window
                    newx = xmax
                    newy = ((y1 - y0) / (x1 - x0)) * (newx - x0) + y0
                elif (code & (1 << 1)) != 0:
                    # endpoint is above clip window
                    newy = ymax
                    newx = ((x1 - x0) / (y1 - y0)) * (newy - y0) + x0
                elif (code & (1 << 0)) != 0:
                    # endpoint is below clip window
                    newy = ymin
                    newx = ((x1 - x0) / (y1 - y0)) * (newy - y0) + x0
                
                # replace the old endpoint
                if code == e0code:
                    x0 = newx
                    y0 = newy
                else:
                    x1 = newx
                    y1 = newy
        
        d = math.dist([x0, y0], [x1, y1])   # cull very short line segments
        if accept and d > 5.0:
            self.geoms.append(shapely.LineString([[x0, y0], [x1, y1]]))
        
        return accept
    

    def draw_tile(self, x, y, a):
        xstart = x + self.tilesize
        ystart = y + self.tilesize

        slope = math.tan(a)
        c = ystart - slope * xstart

        down_accept = True
        up_accept = True
        i = 0
        while (down_accept or up_accept):
            x0 = x - self.tilesize / 2
            y0 = slope * x0 + c + i * self.step / math.cos(a)
            x1 =  x + self.tilesize + self.tilesize / 2
            y1 = slope * x1 + c + i * self.step / math.cos(a)
            up_accept = self.line_clip(x0, y0, x1, y1, x, y)

            x0 = x - self.tilesize / 2
            y0 = slope * x0 + c - i * self.step / math.cos(a)
            x1 = x + self.tilesize + self.tilesize / 2
            y1 = slope * x1 + c - i * self.step / math.cos(a)
            down_accept = self.line_clip(x0, y0, x1, y1, x, y)

            i += 1

    

    def draw(self):
        for j in range(self.height // self.tilesize):
            for i in range(self.width // self.tilesize):
                a = None
                if self.noise_based:
                    noiseval = pnoise2(x / self.noisescale, y / self.noisescale)
                    a = p5map(noiseval, 0.0, 1.0, 0.0, math.tau)
                else:
                    a = self.rng.uniform(0.0, math.tau)
                
                x = i * self.tilesize
                y = j * self.tilesize

                self.draw_tile(x, y, a)

