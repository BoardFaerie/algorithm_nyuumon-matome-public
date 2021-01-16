class World:
    """3D world for placing polygons and lights"""

    def __init__(self, name="Default World"):
        self.name = name
        self.objects = []
        self.lights = []
