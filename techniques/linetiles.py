import drawsvg
import shapely

from .base_technique import BaseTechnique
from .params import linetiles

class LineTiles(BaseTechnique):
    def __init__(self, rng, subdim, palette, n_tiles=None, step=None, angle=None):
        super().__init__(rng, subdim, palette)

        if n_tiles:
            self.n_tiles = n_tiles
        else:
            self.n_tiles = linetiles['randomizers']['n_tiles'](self.rng, linetiles['params']['n_tiles'])
        
        if step:
            self.step = step
        else:
            self.step = linetiles['randomizers']['step'](self.rng, linetiles['params']['step'])
        
        if angle:
            self.angle = angle
        else:
            self.angle = linetiles['randomizers']['angle'](self.rng, linetiles['params']['angle'])
    

    def mutate(self):
        # randomly select mutatable parameter
        p = self.rng.choice([key for key in linetiles['params']])
        # mutate parameter
        new_val = linetiles['randomizers'][p](self.rng, linetiles['params'][p])
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
            code |= (1<< 1)    # below clip window
        
        return code
    

    def line_clip(self, x0, y0, x1, y1, clipx, clipy, clipw, cliph):
        e0code, e1code = None

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
                newx, newy = 0

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
        
        return accept, x0, y0, x1, y1
    

    def draw(self, d):
        tilesize = min(self.width, self.height) / self.n_tiles

        for y in range(0, self.height, tilesize):
            for x in range(0, self.width, tilesize):
                