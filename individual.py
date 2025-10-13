class Individual:
    def __init__(self, id, rng, dim, drawing, techniques):
        self.id = id
        self.rng = rng
        self.dim = dim
        self.drawing = drawing
        self.techniques = techniques

        self.num_elements = None

        self.isEvaluated = False
        self.fitness = 0.0
        self.plot_info = None