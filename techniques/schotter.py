#https://generativeartistry.com/tutorials/cubic-disarray/
import drawsvg
import math
from base_technique import BaseTechnique
from art_utils import *

class Schotter(BaseTechnique):
    def __init__(self, rng, palette, size, displacement=15, rotate_mult=20):
        super().__init__("schotter-homage", rng, palette)
        self.size = size
        self.displacement = displacement
        self.rotate_mult = rotate_mult
    

    def draw(self, d):
        num_cols, x_offset = divmod(d.width - self.size, self.size)
        num_rows, y_offset = divmod(d.height - self.size, self.size)

        for i in range(num_cols):
            for j in range(num_rows):
                sign = -1 if self.rng.random() < 0.5 else 1
                rotate_amt = round(math.degrees((j * self.size) / d.height * math.pi / 180 * sign * self.rng.random() * self.rotate_mult), 4)

                sign = -1 if self.rng.random() < 0.5 else 1
                translate_amt = round((j * self.size) / d.height * sign * self.rng.random() * self.displacement, 4)

                x = (i * self.size) + (self.size + x_offset) / 2
                y = (j * self.size) + (self.size + y_offset) / 2

                # center of rotation
                rx = x + translate_amt + (self.size / 2)
                ry = y + translate_amt + (self.size / 2)

                trans = translate_str(tx=translate_amt) + " " + rotate_str(rotate_amt, rx, ry)

                d.append(drawsvg.Rectangle(x, y, self.size, self.size, fill='none', stroke='#50514f', transform=trans))
        
        return d