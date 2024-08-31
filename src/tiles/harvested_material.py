from .world import Tile, World, Materials
from display_type import DisplayType

class HarvestedMaterial(Tile):
    material: Materials

    def __init__(self, x: int, y: int, master: World, material: Materials):
        Tile.__init__(self, x, y, master)
        
        self.material = material

        match self.material:
            case Materials.WATER:
                self.display = DisplayType("./assets/h_water.png")
            case Materials.WOOD:
                self.display = DisplayType("./assets/h_tree.png")
            case Materials.STONE:
                self.display = DisplayType("./assets/h_stone.png")
            case Materials.METAL:
                self.display = DisplayType("./assets/h_metal.png")
            case Materials.OIL:
                self.display = DisplayType("./assets/h_oil.png")

    def tick(self):
        pass # TODO: maybe some functionality is required? Perhaps a checkhealth for enemy attacker tiles to destroy outputs? 