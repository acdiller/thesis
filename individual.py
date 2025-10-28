class Individual:
    def __init__(self, id, rng, dim, penwidth, techniques):
        self.id = id
        self.rng = rng
        self.dim = dim
        self.penwidth = penwidth
        
        self.techniques = techniques

        self.features = None

        self.isEvaluated = False
        self.fitness = 0.0
        self.plot_info = None