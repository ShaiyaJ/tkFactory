from .world import Tile, World, Materials
from .harvested_material import HarvestedMaterial
from display_type import DisplayType

import enum
import math

# Types of possible attacking tiles
# (used to control display)
class AttackerTiles(enum.Enum):
    TURRET = enum.auto()
    LONG_RANGED_TURRET = enum.auto()
    BARBED_WIRE = enum.auto()
    ELECTRIC_FENCE = enum.auto()

    BEAR = enum.auto()
    GORILLA = enum.auto()
    SPIDER = enum.auto()

# Main class
class AttackerTile[TileTypes](Tile): # TODO: change display to include warning tiles based on power and shit
    build_progress: dict[Materials, int] 
    targets: list[TileTypes]

    max_cooldown: int
    cooldown: int

    def __init__(self, x: int, y: int, master: World, tile_type: AttackerTiles):
        Tile.__init__(self, x, y, master)

        match tile_type:
            case AttackerTiles.TURRET:
                self.display = DisplayType("./assets/turret.png")
            case AttackerTiles.LONG_RANGED_TURRET:
                self.display = DisplayType("./assets/long_ranged_turret.png")
            case AttackerTiles.BARBED_WIRE:
                self.display = DisplayType("./assets/barbed_wire.png")
            case AttackerTiles.ELECTRIC_FENCE:
                self.display = DisplayType("./assets/electric_fence.png")
                
            case AttackerTiles.BEAR:
                self.display = DisplayType("./assets/bear.png")
            case AttackerTiles.GORILLA:
                self.display = DisplayType("./assets/gorilla.png")
            case AttackerTiles.SPIDER:
                self.display = DisplayType("./assets/spider.png")

    def attack_tile(self, target: TileTypes):
        target.health -= 1
        self.cooldown = self.max_cooldown 

    def path_find(source_x: int, source_y: int, dest_x: int, dest_y: int) -> tuple[int, int]:
        pass    # TODO: implement function


    def tick(self):
        self.check_health()
        self.check_build()

        # Checking cooldown
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        
        # Get tiles in range
        tile_set = self.get_tiles_in_range()

        # Checking whether target tile exists in tile_set
        target_tile: TileTypes = None

        for tile in tile_set:
            if type(tile) in self.targets:
                target_tile = tile
                break

        # If valid target tile doesn't exist in range, pathfind 
        if target_tile == None:
            # Find closest attackable tile
            closest_target_tile: TileTypes
            closest_target_tile_dist: float = float("inf")

            for (y, row) in enumerate(self.master):
                for (x, tile) in enumerate(row):
                    dist = math.sqrt(x**2 + y**2)

                    if dist < closest_target_tile_dist:
                        closest_target_tile = tile
                        closest_target_tile_dist = dist
                        
            # Move towards it
            self.x, self.y = self.path_find(self.x, self.y, closest_target_tile.x, closest_target_tile.y)
        elif target_tile != None:
            self.attack_tile(target_tile)

    def check_build(self):
        # Collect tiles in range
        tile_set = self.get_tiles_in_range()

        # Query for first tile that meets conditions
        first_tile: HarvestedMaterial = None

        for tile in tile_set:
            if type(tile) == HarvestedMaterial:
                if tile.material in self.build_materials:
                    first_tile = tile
                    break
        
        # Edge case if tile doesn't exist in range
        if first_tile == None:
            return

        # Consume resources and decrement build progress left counter
        first_tile.destroy()
        self.build_progress[first_tile.material] -= 1