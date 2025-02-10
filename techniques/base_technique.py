class BaseTechnique:
    def __init__(self, name, rng, palette, monocolour=False):
        self.name = name
        self.rng = rng
        if palette:
            self.palette = palette
        else:
            self.palette = self.get_palette
        self.monocolour = monocolour


    def draw(self, d):
        """Draw algorithmic technique on vector drawing object and return it."""
        pass

    def get_palette(self, n):
        pass