from .world import Tile, World, Materials
from .source_material import SourceMaterial
from .harvested_material import HarvestedMaterial
from display_type import DisplayType

import enum

# Types of possible collecting tiles
# (used to control display)
class CollectorTiles(enum.Enum):
    CHOPPING_SITE = enum.auto()
    MINING_SITE = enum.auto()
    BOILER = enum.auto()
    STEAM_GEN = enum.auto()
    OIL_DRILL = enum.auto()
    POWER_LINE = enum.auto()
    DRILL = enum.auto()

# Main class
class CollectorTile(Tile):
    build_progress: dict[Materials, int]
    material: Materials
    output_material: Materials
    carrying_power: bool
    carrying_steam: bool

    requires_power: bool
    requires_water: bool
    requires_steam: bool
    
    def __init__(self, x: int, y: int, master: World, tile_type: CollectorTiles):
        Tile.__init__(self, x, y, master)

        self.carrying_power = False
        self.carrying_steam = False

        match tile_type: # FIXME: Double... TRIPLE check these stats are all good. 
            case CollectorTiles.CHOPPING_SITE:
                self.display = DisplayType("./assets/chopping_site.png")

                self.health = 2
                self.range = 1

                self.build_progress = {
                    Materials.WOOD: 1
                }
                self.material = Materials.WOOD
                self.output_material = Materials.WOOD

                self.requires_power = False
                self.requires_water = False
                self.requires_steam = False
            case CollectorTiles.MINING_SITE:
                self.display = DisplayType("./assets/mining_site.png")

                self.health = 2
                self.range = 1

                self.build_progress = {
                    Materials.WOOD: 2
                }
                self.material = Materials.STONE
                self.output_material = Materials.STONE

                self.requires_power = False
                self.requires_water = False
                self.requires_steam = False
            case CollectorTiles.DRILL:
                self.display = DisplayType("./assets/drill.png")

                self.health = 2
                self.range = 1

                self.build_progress = {
                    Materials.STONE: 1
                }
                self.material = Materials.METAL 
                self.output_material = Materials.METAL

                self.requires_power = True
                self.requires_water = False
                self.requires_steam = False
            case CollectorTiles.BOILER:
                self.display = DisplayType("./assets/boiler.png")

                self.health = 4
                self.range = 1

                self.build_progress = {
                    Materials.WOOD: 2,
                    Materials.STONE: 2
                }
                self.material = Materials.WATER
                self.output_material = lambda: self.set_carrying_steam(True)

                self.requires_power = False 
                self.requires_water = True 
                self.requires_steam = False
            case CollectorTiles.STEAM_GEN:
                self.display = DisplayType("./assets/generator.png")

                self.health = 4
                self.range = 2

                self.build_progress = {}
                self.material = None
                self.output_material = lambda: self.set_carrying_power(True)

                self.build_progress = {
                    Materials.WOOD: 2,
                    Materials.STONE: 2
                }
                self.material = None
                self.output_material = lambda: self.set_carrying_power(True)

                self.requires_power = False
                self.requires_water = False
                self.requires_steam = True 
            case CollectorTiles.OIL_DRILL:
                self.display = DisplayType("./assets/oil_drill.png")

                self.health = 4
                self.range = 1

                self.build_progress = {
                    Materials.STONE: 3,
                    Materials.METAL: 1
                }
                self.material = Materials.OIL
                self.output_material = Materials.OIL

                self.requires_power = True
                self.requires_water = False
                self.requires_steam = False
            case CollectorTiles.POWER_LINE:
                self.display = DisplayType("./assets/power_line.png")

                self.health = 1
                self.range = 2

                self.build_progress = {
                    Materials.WOOD: 1,
                    Materials.METAL: 1
                }
                self.material = None
                self.output_material = lambda: self.set_carrying_power(True)

                self.requires_power = True
                self.requires_water = False
                self.requires_steam = False

    def set_carrying_power(self, b: bool):
        self.carrying_power = b

    def set_carrying_steam(self, b: bool):
        self.carrying_steam = b

    def check_power(self) -> bool:
        # Getting set of tiles
        tile_set = self.get_tiles_in_range()

        # Checking that any tiles in range carry power
        for tile in tile_set:
            if type(tile) == CollectorTile and tile.carrying_power:
                return True
        return False

    def check_steam(self) -> bool:
        # Getting set of tiles
        tile_set = self.get_tiles_in_range()

        # Checking that any tiles in range carry power
        for tile in tile_set:
            if type(tile) == CollectorTile and tile.carrying_steam:
                return True
        return False
    
    def check_water(self) -> bool:
        # Getting set of tiles
        tile_set = self.get_tiles_in_range()

        # Checking that any tiles in range carry power
        for tile in tile_set:
            if type(tile) == SourceMaterial and tile.material == Materials.WATER:
                return True
        return False

    def check_collect(self, output_x: int, output_y: int):
        # Checking if power, water and steam requirements are met
        if self.requires_power and not self.check_power():
            return

        if self.requires_water and not self.check_water():
            return
    
        if self.requires_steam and not self.check_steam():
            return

        # Checking if the output tile is filled
        if self.master.world_map[output_y][output_x] != None:
            return
        
        # If all the conditions for collection have been met, then run one of two possible collection outcomes
        # outcome one: output_material is of type Materials, therefore it can be treated like damaging and spawning a tile
        # outcome two: output_material is another type (lambda function), so run the lambda function // this is used for flipping the boolean flags "carrying_`x`"
        # So check for outcome two first since it's the easiest to run
        self.carrying_power = False # Resetting params
        self.carrying_steam = False

        if type(self.output_material) != Materials:
            self.output_material()
            return
        
        # Otherwise, run outcome one
        # Getting tiles in range
        tile_set = self.get_tiles_in_range()

        # If all the conditions for collection has been met then run the collection process
        target_material: SourceMaterial = None
        
        for tile in tile_set:                   # Query for first tile that meets conditions
            if type(tile) == SourceMaterial:
                if tile.material == self.material:   
                    target_material = tile
                    break

        # Edge case if tile doesn't exist in range
        if target_material == None:
            return                  # IDE says this is unreachable, it is actually reachable

        # Consume resource
        target_material.health -= 1
        HarvestedMaterial(output_x, output_y, self.master, self.output_material) # Set output tile to harvested material

    def check_build(self):
        # Collect tiles in range
        tile_set = self.get_tiles_in_range()

        # Query for first tile that meets conditions
        first_tile: HarvestedMaterial = None

        for tile in tile_set:
            if type(tile) == HarvestedMaterial:
                if tile.material in self.build_progress.keys() and self.build_progress[tile.material] > 0:
                    first_tile = tile
                    break
        
        # Edge case if tile doesn't exist in range
        if first_tile == None:
            return

        # Consume resources and decrement build progress left counter
        first_tile.destroy()
        self.build_progress[first_tile.material] -= 1

    def get_free_output_location(self) -> tuple[int, int]: 
        x_offsets = [x for x in range(-self.range, self.range+1)]
        y_offsets = [y for y in range(-self.range, self.range+1)]

        for y in y_offsets:
            for x in x_offsets:
                # Checking if tile is out of bounds
                if (self.x + x >= len(self.master.world_map[0]) or self.x + x < 0 or 
                    self.y + y >= len(self.master.world_map)    or self.y + y < 0):
                    continue

                # Checking if tile exists at position (is not None)
                if self.master.world_map[self.y + y][self.x + x] is not None:
                    continue

                # If the above conditions are met (in bounds and not None), return
                return (self.x + x, self.y + y)

        return (self.x, self.y)

    def tick(self):
        # Checking the tile's health
        self.check_health()

        # Checking how many completed build values there are
        build_values = self.build_progress.values()             # TODO: maybe this code could flag a self.built variable for performance reasons, I don't really think doing this counting operation is too expensive but after the building has been built I don't think it should have to do this every tick 
        build_values_len = len(build_values)                    #        or move this to check_build, as a prerequisite for the function to run (early return execution flow)
        zero_count = list(build_values).count(0)

        # If the number of completed build values are equal to the number of build values,
        # then the building has been build, and can run the check collection process
        if build_values_len == zero_count:
            self.check_collect(*self.get_free_output_location())
            return
        
        # Otherwise, it should check what to build
        self.check_build()
