# dictionaries storing each technique's mutatable parameters, their associated ranges/sequences,
# and the methods use to randomize a given parameter
from math import pi

cp = {
    'params': {
        'n_spawn': (1, 10),
        'max_failures': (100, 200),
        'start_r': (1, 5)
    },
    'randomizers': {
        'n_spawn': (lambda rng, range: rng.randint(range[0], range[1])),
        'max_failures': (lambda rng, range: rng.randint(range[0], range[1])),
        'start_r': (lambda rng, range: rng.randint(range[0], range[1]))
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

linetiles = {
    'params': {
        'n_tiles': (3, 15),
        'step': (5, 10),
        'angle': (0, 2*pi)
    },
    'randomizers': {
        'n_tiles': (lambda rng, range: rng.randint(range[0], range[1])),
        'step': (lambda rng, range: rng.uniform(range[0], range[1])),
        'angle': (lambda rng, range: rng.uniform(range[0], range[1]))
    }
}