from .world import Tile, World, Materials
from .collector_tile import CollectorTile
from .harvested_material import HarvestedMaterial
from display_type import DisplayType

class HQ(CollectorTile):
    def __init__(self, x: int, y: int, master: World):
        Tile.__init__(self, x, y, master)

        self.display = DisplayType("./assets/HQ.png")
        self.health = 5

        # Checking if another HQ exists
        if not self.check_build():
            self.destroy()

    def check_collect(self):
        # Collect tiles in range
        tile_set = self.get_tiles_in_range()

        # Query for first tile that meets conditions
        first_tile: HarvestedMaterial = None

        for tile in tile_set:
            if type(tile) == HarvestedMaterial:
                first_tile = tile
                break
        
        # Edge case if tile doesn't exist in range
        if first_tile == None:
            return

        # Consume resources and add to games winning total
        first_tile.destroy()
        self.master.materials[ first_tile.material ] += 1
        self.master.materials[Materials.GOLD] += 1

    def check_build(self):
        # Unlike the other check build functions, this one just
        # limits the amount of HQs to 1 on the map
        for (_, row) in enumerate(self.master.world_map):
            for tile in row:
                if type(tile) == HQ:
                    if (tile.x != self.x) or (tile.y != self.y):
                        return False
            
        return True

    def tick(self):
        self.check_health()
        self.check_collect()
