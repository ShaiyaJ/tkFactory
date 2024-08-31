from .world import Tile, World
from .harvested_material import HarvestedMaterial
from .collector_tile import CollectorTile
from display_type import DisplayType

class Conveyor(Tile):
    rotation: tuple[int, int]       # Measured in an offset to add to the Conveyor's coordinates - describes the OUTPUT tile of the conveyor
    carrying: HarvestedMaterial
    updated_last_tick: bool         # This stops conveyors in the right direction automatically zipping their contents to the end of the screen in 1 tick

    def __init__(self, x: int, y: int, master: World, rotation: tuple[int, int]):
        Tile.__init__(self, x, y, master)


        self.rotation = rotation
        self.carrying = None
        self.updated_last_tick = False

        # Setting display type
        match self.rotation: # TODO: change conveyor to grabber to make behavior more understandable
            case (1,0):     # Right
                self.display = DisplayType.rotate("./assets/conveyor.png", scale=8, deg=0)
            case (-1,0):    # Left
                self.display = DisplayType.rotate("./assets/conveyor.png", scale=8, deg=180)
            case (0,-1):    # Up
                self.display = DisplayType.rotate("./assets/conveyor.png", scale=8, deg=90)
            case (0,1):     # Down
                self.display = DisplayType.rotate("./assets/conveyor.png", scale=8, deg=270)
    
    def check_power(self) -> bool:
        self.range = 2

            # Getting set of tiles
        tile_set = self.get_tiles_in_range()

        self.range = 1

        # Checking that any tiles in range carry power
        for tile in tile_set:
            if type(tile) == CollectorTile and tile.carrying_power:
                return True
        return False
    
    def destroy(self):
        if self.carrying != None:
            self.master.world_map[self.y][self.x] = self.carrying
            del self
        else:
            super().destroy()

    def tick(self):
        # Resetting update flag
        self.updated_last_tick = False

        # Checking power condition
        if not self.check_power():
            print("AAAAA")
            return

        input_posx = self.x - self.rotation[0]
        input_posy = self.y - self.rotation[1]
        output_posx = self.x + self.rotation[0]
        output_posy = self.y + self.rotation[1]

        # Checking if output is out of bounds
        if (output_posx < 0 or output_posy < 0 or                                                           # Checking if below zero
            output_posx >= len(self.master.world_map[0]) or output_posy >= len(self.master.world_map)):     # Checking if above map limit
            print("AA")
            return

        # Fetching input output tiles
        if (                                                                                            # If input is out of range, set to None so normal logic can continue
            input_posx < 0 or input_posy < 0 or                                                         # Checking if below zero
            input_posx >= len(self.master.world_map) or input_posy >= len(self.master.world_map[0])):   # Checking if above map limit
            input_tile = None
            print("BB")
        else:
            input_tile = self.master.world_map[input_posy][input_posx]
        output_tile = self.master.world_map[output_posy][output_posx]

        # Checking if input has been updated last tick
        # (if so, delay execution by one tick)
        if type(input_tile) == Conveyor and input_tile.updated_last_tick:
            return

        # If carrying something
        if self.carrying != None:
            if type(output_tile) == Conveyor:           # Push it to the next conveyor's carrying attribute
                if output_tile.carrying == None:
                    output_tile.carrying = self.carrying
                    self.carrying = None
                    self.updated_last_tick = True
            elif output_tile is None:             # Else, if there is no conveyor then push it to the world_map if the tile is empty
                # Putting the carried object on the main world and then setting carrying to None
                self.carrying.x = output_posx
                self.carrying.y = output_posy
                self.master.world_map[output_posy][output_posx] = self.carrying
                self.carrying = None
                # self.updated_last_tick = True

        # Checking if target_tile is a harvested material and picking it up if it is 
        # we don't have to worry about picking up things from conveyors since conveyors should "push" things onto us
        elif self.carrying == None:
            if type(input_tile) == HarvestedMaterial:
                self.carrying = input_tile
                self.master.world_map[input_posy][input_posx] = None
                self.updated_last_tick = True
            elif type(input_tile) == Conveyor:          # Edge case for vertical vertical conveyors picking up from horizontal ones
                if input_tile.carrying is not None and self.carrying is None:
                    self.carrying = input_tile.carrying
                    input_tile.carrying = None
                    self.updated_last_tick = True