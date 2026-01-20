from algorithmic_art.techniques import (
    CirclePacking,
    ElementaryCA,
    FlowField,
    Phyllotaxis,
    RadialLines
)
# cmd-line arguments
n_iterations = None
pop_size = None
mutation_rate = None

# other values set in main.py
rng = None
pentype = None

# constants that should only be touched in this file
DIM = (1054, 816)   # US letter paper at 96 DPI
ALL_TECHNIQUES = (CirclePacking, ElementaryCA, FlowField, Phyllotaxis, RadialLines)
MAX_T = 8   # maximum number of technique instances per individual
MAX_ELEM = 6000 # maximum number of elements in plot, for feature dimension bins
ELEM_STEP = 500 # step size for generating number of elements feature dimension bins