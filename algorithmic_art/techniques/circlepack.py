import math

from algorithmic_art.techniques.base_technique import BaseTechnique
from algorithmic_art.techniques.params import cp
from algorithmic_art.tools.art_utils import p5map
from algorithmic_art.tools.shapes import circle, circular_sinewave

class CirclePacking(BaseTechnique):
    def __init__(self, rng, subdim=None, n_spawn=None, max_failures=None, start_r=None, shape_type=None, pad=2):
        super().__init__(rng, subdim)
        
        self.pad = pad  # minimum spacing between elements
        
        if n_spawn:
            self.n_spawn = n_spawn
        else:
            self.n_spawn = cp['randomizers']['n_spawn'](self.rng, cp['params']['n_spawn'])

        if max_failures:
            self.max_failures = max_failures
        else:
            self.max_failures = cp['randomizers']['max_failures'](self.rng, cp['params']['max_failures'])
        
        if start_r:
            self.start_r = start_r  # starting radius of new circles
        else:
            self.start_r = cp['randomizers']['start_r'](self.rng, cp['params']['start_r'])
        
        if shape_type:
            self.shape_type = shape_type
        else:
            self.shape_type = cp['randomizers']['shape_type'](self.rng, cp['params']['shape_type'])
        
        self.max_r = 50

        self.circles = []
    

    def reset(self):
        self.geoms.clear()
        self.circles.clear()


    def mutate(self):
        # randomly select mutatable parameter
        p = self.rng.choice([key for key in cp['params']])
        # mutate parameter
        new_val = cp['randomizers'][p](self.rng, cp['params'][p])
        print("parameter '" + p + "' mutated from " + str(getattr(self, p)) + " to " + str(new_val))
        setattr(self, p, new_val)
    
    
    def spawn_circle(self):
        """
        Attempt to place new circle in a random, unoccupied location.
        """
        failures = 0
        spawned = False
        while (not spawned) and failures < self.max_failures:
            amp = 0
            if self.shape_type == "sinewave":
                amp = 2
            buffer = self.start_r + self.pad   # buffer distance from edge of canvas

            x = self.rng.randrange(buffer, int(self.width - buffer))
            y = self.rng.randrange(buffer, int(self.height - buffer))
            x += self.origin_x
            y += self.origin_y

            if self.collision({'x': x, 'y': y, 'r': self.start_r, 'amp': amp}):
                failures += 1
            else:
                # create new circle
                c = {
                    'x': x,
                    'y': y,
                    'r': self.start_r,
                    'amp': amp,
                    'growing': True
                }
                self.circles.append(c)
                spawned = True
        if failures >= self.max_failures:
            return False
        else:
            return True
    

    def spawn_sinewave(self):
        """
        Attempt to place a circular sine wave in a random, unoccupied location.
        """
        failures = 0
        spawned = False
        while (not spawned) and failures < self.max_failures:
            amp = 2     # new circles start at lowest possible amplitude value
            buffer = self.start_r + self.pad + amp   # buffer distance from edge of canvas
            
            x = self.rng.randrange(buffer, int(self.width - buffer))
            y = self.rng.randrange(buffer, int(self.height - buffer))
            x += self.origin_x
            y += self.origin_y

            if self.collision({'x': x, 'y': y, 'r': self.start_r, 'amp': 2}):
                failures += 1
            else:
                # create new circle
                csw = {
                    'x': x,
                    'y': y,
                    'r': self.start_r,
                    'amp': 2,
                    'growing': True
                }
                self.circles.append(csw)
                spawned = True
        if failures >= self.max_failures:
            return False
        else:
            return True


    def collision(self, c):
        """
        Check if a given circle collides with any other circle or canvas edge.

        Args:
            c (dict of str: int): the circle to check for collisions with
        """
        circle_collision = False
        
        for c2 in self.circles:
            if c != c2:    
                distance = math.dist((c['x'], c['y']), (c2['x'], c2['y']))
                if distance < c['r'] + c2['r'] + (self.pad * 2) + c['amp'] + c2['amp']:
                    circle_collision = True
        
        edge_collision = ((c['x'] - c['r'] - self.pad - c['amp'] <= self.origin_x) or
                          (c['x'] + c['r'] + self.pad + c['amp'] >= self.origin_x + self.width) or
                          (c['y'] - c['r'] - self.pad - c['amp'] <= self.origin_y) or
                          (c['y'] + c['r'] + self.pad + c['amp'] >= self.origin_y + self.height))
        return circle_collision or edge_collision
    

    def draw(self):
        terminated = False
        while not terminated:
            for _ in range(self.n_spawn):
                new_placed = self.spawn_circle()
                terminated = not new_placed
                if terminated:
                    break
            if not terminated:
                # grow circles that have not yet collided with other circles or canvas edge
                for c in self.circles:
                    if c['growing']:
                        if self.collision(c) or c['r'] >= self.max_r:
                            c['growing'] = False
                        else:
                            c['r'] += 1
                            if self.shape_type == 'sinewave':
                                c['amp'] = p5map(c['r'], self.start_r, self.max_r, 2, 8)
        else:
            for c in self.circles:
                if self.shape_type == 'circle':
                    self.geoms.append(circle(c['x'], c['y'], c['r']))
                elif self.shape_type == 'sinewave':
                    freq = self.rng.randint(5, 8)
                    self.geoms.append(circular_sinewave(c['x'], c['y'], c['r'], freq, c['amp']))
    

    def __str__(self):
        cls_name = type(self).__name__
        return (f"{cls_name}(n_spawn={self.n_spawn}, max_failures={self.max_failures}, " \
                f"start_r={self.start_r}, shape_type={self.shape_type})")