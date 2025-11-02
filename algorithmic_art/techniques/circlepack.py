import math
import shapely

from algorithmic_art.techniques.base_technique import BaseTechnique
from algorithmic_art.techniques.params import cp

class CirclePacking(BaseTechnique):
    def __init__(self, rng, subdim, n_spawn=None, max_failures=None, start_r=None, pad=2):
        super().__init__(rng, subdim)
        
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

        self.pad = pad  # minimum spacing between circles

        self.circles = []
    
    
    def mutate(self):
        # randomly select mutatable parameter
        p = self.rng.choice([key for key in cp['params']])
        # mutate parameter
        new_val = cp['randomizers'][p](self.rng, cp['params'][p])
        #print("parameter '" + p + "' mutated from " + str(getattr(self, p)) + " to " + str(new_val))
        setattr(self, p, new_val)
    
    
    def spawn_circle(self):
        """
        Attempt to place new circle in a random, unoccupied location.
        """
        buffer = self.start_r + self.pad   # buffer distance from edge of canvas
        failures = 0
        spawned = False
        while (not spawned) and failures < self.max_failures:
            x = self.rng.randrange(buffer, int(self.width - buffer))
            y = self.rng.randrange(buffer, int(self.height - buffer))
            x += self.origin['x']
            y += self.origin['y']
            #print(str(x) + ", " + str(y))

            if self.collision({'x': x, 'y': y, 'r': self.start_r}):
                failures += 1
            else:
                # create new circle
                c = {
                    'x': x,
                    'y': y,
                    'r': self.start_r,
                    'growing': True,
                    'colour': self.rng.choice(self.palette)
                }
                self.circles.append(c)
                spawned = True
        if failures >= self.max_failures:
            return False
        else:
            return True
    

    def collision(self, c):
        """
        Check if a given circle collides with any other circle or canvas edge.
        """
        circle_collision = False
        
        for c2 in self.circles:
            if c != c2:    
                distance = math.dist((c['x'], c['y']), (c2['x'], c2['y']))
                if distance < c['r'] + c2['r'] + (self.pad * 2):
                    circle_collision = True
        
        edge_collision = ((c['x'] - c['r'] - self.pad <= self.origin['x']) or
                          (c['x'] + c['r'] + self.pad >= self.origin['x'] + self.width) or
                          (c['y'] - c['r'] - self.pad <= self.origin['y']) or
                          (c['y'] + c['r'] + self.pad >= self.origin['y'] + self.height))
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
                        if self.collision(c):
                            c['growing'] = False
                        else:
                            c['r'] += 1
        else:
            for c in self.circles:
                cx = c['x']
                cy = c['y']
                r = c['r']
                colour = c['colour']
                # approximate circles as point buffers 
                self.geoms.append(shapely.Point(cx, cy).buffer(r).boundary)
    

    def __str__(self):
        cls_name = type(self).__name__
        return (f"{cls_name}(n_spawn={self.n_spawn}, max_failures={self.max_failures}, " \
                f"start_r={self.start_r}, pad={self.pad})")