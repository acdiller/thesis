from drawsvg import Drawing

class Individual:
    def __init__(self, id, dim, rng, technique):
        self.id = id
        self.dim = dim
        self.rng = rng
        self.technique = technique
        self.drawing = Drawing(dim[0], dim[1])
        self.isEvaluated = False
        self.fitness = 0.0
        self.plot_info = None
    
    def __str__(self):
        cls_name = type(self).__name__
        return f"{cls_name} {self.id}, fitness: {self.fitness}, technique={self.technique!s}"