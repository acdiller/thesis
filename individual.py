class Individual:
    def __init__(self, id, rng, dim, pentype):
        self.id = id
        self.rng = rng

        self.dim = dim
        self.pentype = pentype
        
        self.techniques = []

        self.features = None

        self.fitness = 0.0