from .world import Tile, World, Materials
from display_type import DisplayType

class SourceMaterial(Tile):
    material: Materials
    
    def __init__(self, x: int, y: int, master: World, material: Materials):
        Tile.__init__(self, x, y, master)

        self.health = 3 
        self.material = material

        match self.material:
            case Materials.WATER:
                self.display = DisplayType("./assets/water.png")
            case Materials.WOOD:
                self.display = DisplayType("./assets/tree.png")
            case Materials.STONE:
                self.display = DisplayType("./assets/stone.png")
            case Materials.METAL:
                self.display = DisplayType("./assets/metal.png")
            case Materials.OIL:
                self.display = DisplayType("./assets/oil.png")
            case _:
                print(self.material)

    def tick(self):
        self.check_health()
