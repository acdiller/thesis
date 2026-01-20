# dictionaries storing each technique's mutatable parameters, their associated ranges/sequences,
# and the methods use to randomize a given parameter
from math import pi

cp = {
    'params': {
        'n_spawn': (1, 10),
        'max_failures': (100, 250),
        'start_r': (5, 10),
        'shape_type': ['circle', 'sinewave']
    },
    'randomizers': {
        'n_spawn': (lambda rng, range: rng.randint(range[0], range[1])),
        'max_failures': (lambda rng, range: rng.randint(range[0], range[1])),
        'start_r': (lambda rng, range: rng.randint(range[0], range[1])),
        'shape_type': (lambda rng, sequence: rng.choice(sequence))
    }
}

eca = {
    'params': {
        'cellsize': (10, 40),
        'rule': [18, 22, 26, 30, 41, 45, 54, 57, 60, 62, 67, 73, 75, 86, 89, 90, 
             101, 105, 106, 107, 109, 110, 118, 121, 122, 126, 146, 150, 154],
        'init_state': ['random', 'single']
    },
    'randomizers': {
        'cellsize': (lambda rng, range: rng.randint(range[0], range[1])),
        'rule': (lambda rng, sequence: rng.choice(sequence)),
        'init_state': (lambda rng, sequence: rng.choice(sequence))
    }
}

ff = {
    'params': {
        'style': ['flowy', 'edgy'],
        'resolution': (3, 6),
        'noisescale': (300, 800),
        'octaves': (2, 8),
        'persistence': (0.25, 0.75),
        'lacunarity': (1.5, 2.5)
    },
    'randomizers': {
        'style': (lambda rng, sequence: rng.choice(sequence)),
        'resolution': (lambda rng, range: rng.randint(range[0], range[1])),
        'noisescale': (lambda rng, range: rng.randint(range[0], range[1])),
        'octaves': (lambda rng, range: rng.randint(range[0], range[1])),
        'persistence': (lambda rng, range: round(rng.uniform(range[0], range[1]), 2)),
        'lacunarity': (lambda rng, range: round(rng.uniform(range[0], range[1]), 2))
    }
}

ltiles = {
    'params': {
        'tilesize': (30, 80),
        'step': (4.0, 8.0),
        'skip_chance': (0.0, 0.60),
        'repeat_chance': (0.0, 0.40),
        'noise_based': [True, False],
        'noisescale': (300, 800)
    },
    'randomizers': {
        'tilesize': (lambda rng, range: rng.randint(range[0], range[1])),
        'step': (lambda rng, range: round(rng.uniform(range[0], range[1]), 1)),
        'skip_chance': (lambda rng, range: round(rng.uniform(range[0], range[1]), 2)),
        'repeat_chance': (lambda rng, range: round(rng.uniform(range[0], range[1]), 2)),
        'noise_based': (lambda rng, sequence: rng.choice(sequence)),
        'noisescale': (lambda rng, range: rng.randint(range[0], range[1]))
    }
}

phyllo = {
    'params': {
        'start_n': (50, 100),
        'c': (8, 12),
        'mod': (5, 10),
        'radius': (30, 60),
        'freq': (5, 15),
        'amp': (2, 8)
    },
    'randomizers': {
        'start_n': (lambda rng, range: rng.randint(range[0], range[1])),
        'c': (lambda rng, range: rng.randint(range[0], range[1])),
        'mod': (lambda rng, range: rng.randint(range[0], range[1])),
        'radius': (lambda rng, range: rng.randint(range[0], range[1])),
        'freq': (lambda rng, range: rng.randint(range[0], range[1])),
        'amp': (lambda rng, range: rng.randint(range[0], range[1]))
    }
}

radlines = {
    # 'params': {
    #     'n_lines': (50, 100),
    #     'line_length': (50, 200),
    #     'base_r': (10, 50),
    #     'shift': (5, 20),
    #     'shiftstep': (5, 10)
    # },
        'params': {
        'n_lines': (50, 100),
        'line_length': (20, 80),
        'base_r': (5, 30),
        'shift': (5, 15),
        'shiftstep': (5, 10)
    },
    'randomizers': {
        'n_lines': (lambda rng, range: rng.randint(range[0], range[1])),
        'line_length': (lambda rng, range: rng.randint(range[0], range[1])),
        'base_r': (lambda rng, range: rng.randint(range[0], range[1])),
        'shift': (lambda rng, range: rng.randint(range[0], range[1])),
        'shiftstep': (lambda rng, range: rng.randint(range[0], range[1]))
    }
}