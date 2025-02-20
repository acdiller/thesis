import math
import random
import drawsvg
from base_technique import BaseTechnique

class CirclePacking(BaseTechnique):
    def __init__(self, rng, palette, num_to_spawn=2, max_fails=200, start_r=2, max_r=None, pad=2):
        super().__init__("circlepacking", rng, palette)
        self.num_to_spawn = num_to_spawn
        self.max_fails = max_fails

        self.start_r = start_r
        self.max_r = max_r
        self.pad = pad

        self.circles = []
    

    def spawn_circle(self, d):
        padding = self.start_r + self.pad
        x = self.rng.randrange(padding, d.width - padding)
        y = self.rng.randrange(padding, d.height - padding)

        if self.collision(c):
            return None
        else:
            # create new circle
            c = {
                'x': x,
                'y': y,
                'r': self.start_r,
                'colour': self.rng.choice(self.palette),
            }
            self.circles.append(c)
            return c


    # check if circle collides with other circles
    def collision(self, c1):
        for c2 in self.circles:
            distance = math.dist((c1.x, c1.y), (c2.x, c2.y))
            if distance < c1.r + c2.r + self.pad:
                return True
        return False
            

    def hit_edge(self, c, d):
        return ((c.x - c.r - self.pad <= 0) or
                (c.x + c.r + self.pad >= d.width) or
                (c.y - c.r - self.pad <= 0) or
                (c.y + c.r + self.pad >= d.height))


    def draw(self, d):
        growing = []
        done = False

        while not done:
            num_spawned = 0
            spawn_attempts = 0

            while num_spawned < self.num_to_spawn:
                c = self.spawn_circle(d)
                if c:
                    growing.append(c)
                    num_spawned += 1
                else:
                    spawn_attempts += 1


if __name__ == "__main__":
    r = random.Random()
    r.seed(22)
    pal = ['#75DDDD', '#09BC8A', '#004346', '#FFCFD2', '#FFAFC5']
    cp = CirclePacking(r, pal)

    if cp:
        print("yeet")