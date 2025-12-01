class Individual:
    def __init__(self, id, rng, dim, pentype, techniques=None):
        self.id = id
        self.rng = rng

        self.dim = dim
        self.pentype = pentype
        
        if techniques:
            self.techniques = techniques
        else:
            self.techniques = []

        self.features = None

        self.fitness = 0.0
    

    def __str__(self):
        #cls_name = type(self).__name__
        return (f"{self.id} \t {self.fitness} \t {', '.join(str(t) for t in self.techniques)}")