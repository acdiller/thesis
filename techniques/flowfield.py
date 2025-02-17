import math
import drawsvg
from perlin_noise import PerlinNoise
from techniques.art_utils import p5map
from techniques.base_technique import BaseTechnique

#TODO: add styles

class FlowField(BaseTechnique):
    def __init__(self, rng, palette, resolution=4, noisescale=500, octaves=4):
        super().__init__(rng, palette)
        self.resolution = resolution
        self.noisescale = noisescale
        self.octaves = octaves
        #self.style = style

        self.particles = []


    def add_particles(self, w, h):
        for x in range(0, w, self.resolution):
            r = self.rng.random()
            if r < 0.5:
                p = {'x': x, 'y': 0, 'colour': self.rng.choice(self.palette)}
                self.particles.append(p)
            else:
                p = {'x': x, 'y': h, 'colour': self.rng.choice(self.palette)}
                self.particles.append(p)
            #x += self.resolution

        for y in range(0, h, self.resolution):
            r = self.rng.random()
            if r < 0.5:
                p = {'x': 0, 'y': y, 'colour': self.rng.choice(self.palette)}
                self.particles.append(p)
            else:
                p = {'x': w, 'y': y, 'colour': self.rng.choice(self.palette)}
                self.particles.append(p)
            #y += self.resolution


    def draw(self, d):
        self.add_particles(d.width, d.height)

        #noise = PerlinNoise(seed=self.rng.randint(0, 100000))
        noise = PerlinNoise()
        
        for p in self.particles:
            path = drawsvg.Path(stroke=p['colour'], fill='none')
            path.M(p['x'], p['y'])

            while (p['x'] >= 0) and (p['x'] < d.width) and (p['y'] >= 0) and (p['y'] < d.height):
                noiseval = noise([p['x'] / self.noisescale, p['y'] / self.noisescale])

                angle = p5map(noiseval, 0.0, 1.0, 0.0, math.pi * 2.0)

                p['x'] += math.cos(angle)
                p['y'] += math.sin(angle)

                path.L(p['x'], p['y'])

            #append path to drawing
            d.append(path)
        return d
    
    def __str__(self):
        cls_name = type(self).__name__
        return f"{cls_name}(resolution={self.resolution}, noisescale={self.noisescale}, octaves={self.octaves})"