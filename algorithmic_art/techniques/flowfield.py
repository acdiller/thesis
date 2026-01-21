import math
import shapely

from noise import pnoise2, snoise2

from algorithmic_art.techniques.base_technique import BaseTechnique
from algorithmic_art.techniques.params import ff
from algorithmic_art.tools.art_utils import p5map, constrain


class Particle():
    def __init__(self, x, y, life=None):
        self.x = x
        self.y = y
        self.life = life


class FlowField(BaseTechnique):
    def __init__(self, rng, subdim=None, style=None, resolution=None, noisescale=None, octaves=None, persistence=None, lacunarity=None):
        super().__init__(rng, subdim)
        
        if style:
            self.style = style
        else:
            self.style = ff['randomizers']['style'](self.rng, ff['params']['style'])
        
        if resolution:
            self.resolution = resolution
        else:
            self.resolution = ff['randomizers']['resolution'](self.rng, ff['params']['resolution'])
        
        if noisescale:
            self.noisescale = noisescale
        else:
            self.noisescale = ff['randomizers']['noisescale'](self.rng, ff['params']['noisescale'])
        
        if octaves:
            self.octaves = octaves
        else:
            self.octaves = ff['randomizers']['octaves'](self.rng, ff['params']['octaves'])
        
        if persistence:
            self.persistence = persistence
        else:
            self.persistence = ff['randomizers']['persistence'](self.rng, ff['params']['persistence'])
        
        if lacunarity:
            self.lacunarity = lacunarity
        else:
            self.lacunarity = ff['randomizers']['lacunarity'](self.rng, ff['params']['lacunarity'])

        self.particles = []
    

    def reset(self):
        self.geoms.clear()
        self.particles.clear()


    def mutate(self):
        # randomly select mutatable parameter
        p = self.rng.choice([key for key in ff['params']])
        # mutate parameter
        new_val = ff['randomizers'][p](self.rng, ff['params'][p])
        print("parameter '" + p + "' mutated from " + str(getattr(self, p)) + " to " + str(new_val))
        setattr(self, p, new_val)


    def edge_particles(self):
        """
        Place particles randomly along the edges of the drawing area.
        """
        for x in range(self.origin_x, self.width, self.resolution):
            y = 0 if self.rng.random() < 0.5 else self.height
            self.particles.append(Particle(x, y))
        
        for y in range(self.origin_y, self.height, self.resolution):
            x = 0 if self.rng.random() < 0.5 else self.width
            self.particles.append(Particle(x, y))


    def random_particles(self):
        """
        Place particles in random locations within the drawing area.
        """
        n = (self.width//self.resolution) + (self.height//self.resolution)
        for _ in range(n):
            x = self.rng.randrange(self.origin_x, self.origin_x + self.width)
            y = self.rng.randrange(self.origin_y, self.origin_y + self.height)
            self.particles.append(Particle(x, y, 200))


    def in_bounds(self, p):
        """
        Check if a particle is within the drawing area.
        """
        return (p.x >= self.origin_x) and (p.x < self.origin_x + self.width) and (p.y >= self.origin_y) and (p.y < self.origin_y + self.height)


    def draw(self):
        #self.edge_particles()
        self.random_particles()

        for p in self.particles:
            points = []
            points.append((p.x, p.y))

            while self.in_bounds(p) and (p.life > 0 if p.life is not None else True):
                noiseval = pnoise2(p.x / self.noisescale, p.y / self.noisescale, self.octaves, self.persistence, self.lacunarity)
                
                angle = None
                if self.style == 'flowy':
                    angle = p5map(noiseval, 0.0, 1.0, 0.0, math.pi * 2.0)
                elif self.style == 'edgy':
                    angle = math.ceil((p5map(noiseval, 0.0, 1.0, 0.0, math.pi * 2.0) * (math.pi/4)) / (math.pi/4))

                p.x += math.cos(angle)
                p.y += math.sin(angle)

                #points.append((p.x, p.y))
                points.append((constrain(p.x, self.origin_x, self.origin_x + self.width), constrain(p.y, self.origin_y, self.origin_y + self.height)))

                if p.life is not None:
                    p.life -= 1

            if len(points) > 20:
                self.geoms.append(shapely.LineString(points))
            
        # simplify geometries to reduce number of line segments
        self.geoms = shapely.simplify(self.geoms, tolerance=0.1).tolist()
    

    def __str__(self):
        cls_name = type(self).__name__
        return (f"{cls_name}(style={self.style}, resolution={self.resolution}, noisescale={self.noisescale}, "\
                f"octaves={self.octaves}, persistence={self.persistence}, lacunarity={self.lacunarity})")