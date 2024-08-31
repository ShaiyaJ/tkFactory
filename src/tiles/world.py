from __future__ import annotations

from display_type import DisplayType

import enum
import time

TARGET_TICKRATE = 0.2

class Materials(enum.Enum):
    WATER = enum.auto()
    WOOD = enum.auto()
    STONE = enum.auto()
    METAL = enum.auto()
    GOLD = enum.auto()
    OIL = enum.auto()
    ENERGY = enum.auto()

class ActionTypes(enum.Enum):
    IDLE = enum.auto()      # action_metadata: [n/a]
    BUILD = enum.auto()     # action_metadata: [building: TileType, building_args*]
    DESTROY = enum.auto()   # action_metadata: [n/a]
    RESET = enum.auto()     # action_metadata: [n/a] 

class Action[T]:
    action_type: ActionTypes
    action_metadata: list[T]    # See ActionTypes for required metadata
    target_x: int
    target_y: int

    def __init__(self, action_type: ActionTypes, target_x: int, target_y: int):
        self.action_type = action_type
        self.target_x = target_x
        self.target_y = target_y

class Tile[TileTypes]:
        x: int
        y: int
        master: World
        display: DisplayType

        health: int     
        range: int 
    
        def __init__(self, x: int, y: int, master: World):
            self.x = x
            self.y = y
            self.master = master

            self.master.world_map[y][x] = self

            self.health = 0
            self.range = 1

        def tick(self):     # Since python doesn't have traits, I use NotImplementedError
            raise NotImplementedError()

        # def get_parent_tile(self, x: int, y: int):
        #     return self.master.world_map[y][x]

        def get_tiles_in_range(self) -> list[TileTypes]:
            result: list[TileTypes] = []

            # limit_x_coordinate = lambda x: 0 if x < 0 else x % len(self.master.world_map[0])
            # limit_y_coordinate = lambda x: 0 if x < 0 else x % len(self.master.world_map)
            limit_x_coordinate = lambda x: len(self.master.world_map[0]) if abs(x) >= len(self.master.world_map[0]) else (x if x > 0 else 0)
            limit_y_coordinate = lambda x: len(self.master.world_map) if abs(x) >= len(self.master.world_map) else (x if x > 0 else 0)

            start_x = limit_x_coordinate(self.x - self.range)
            start_y = limit_y_coordinate(self.y - self.range)
            end_x = limit_x_coordinate(self.x + self.range)
            end_y = limit_y_coordinate(self.y + self.range)

            rows = self.master.world_map[start_y:end_y+1]
            for row in rows: 
                cells = row[start_x:end_x+1]
                result.extend(cells)

            result.remove(self)     # Filtering out caller tile from results

            return result
            
        def check_health(self): 
            if self.health <= 0:
                self.destroy()

        def destroy(self):
            self.master.world_map[self.y][self.x] = None    # Blank tiles will be denoted with None since then we can make "if not" comparisons
            del self

class WinState(enum.Enum):
    WON = enum.auto()
    FAIL = enum.auto()
    IN_PROGRESS = enum.auto()

class World[TileTypes]:
    world_map: list[list[TileTypes]] 
    win_condition: str
    win_state: WinState 
    elapsed_time: float 
    message: str
    materials: dict
    next_action: list[Action]

    target_tickrate: float
    last_tick_complete: int

    def __init__(self):
        # Setting all collected materials to 0
        self.materials = {}

        for material in Materials:
            self.materials[material] = 0

        # Setting default variables
        self.world_map = []
        self.win_condition = "no_source"
        self.win_state = WinState.IN_PROGRESS
        self.elapsed_time = 0.0
        self.message = ""
        self.next_action = []

        # Setting tickrate information
        self.target_tickrate = TARGET_TICKRATE
        self.last_tick_complete = time.time() 

    def queue_new_action(self, action_type: ActionTypes, x: int, y: int, *args):
        action = Action(action_type, x, y)
        action.action_metadata = list(args)

        self.next_action.append(action)

    def set_world_size(self, size_x: int, size_y: int):
        # Clearing map
        self.world_map = []

        # Generating blank tiles
        self.world_map = [
            [None for x in range(size_x)] for y in range(size_y)
        ]


    def tick(self):
        current_time = time.time()
        # print(current_time - self.last_tick_complete) # Uncomment line to perform performance checks

        # Checking if enough time has passed
        if not current_time - self.last_tick_complete > self.target_tickrate:
            return
        
        # Checking if won or lost
        if self.win_state != WinState.IN_PROGRESS:
            return

        # If the conditions for a tick are met, run each tile's tick
        for (_, row) in enumerate(self.world_map):
            for tile in row:
                if tile != None:
                    tile.tick()

        # Check if the win condition is true
        match self.win_condition:
            case "no_source":
                win = True

                for y, row in enumerate(self.world_map):
                    for tile in row:
                        if tile.__class__.__name__ == "SourceMaterial" and tile.material != Materials.WATER:
                            win = False
                
                if win:
                    self.win_state = WinState.WON

            case "all_hq":
                HQ = False
                win = True

                for y, row in enumerate(self.world_map):
                    for tile in row:
                        if tile.__class__.__name__ == "HQ":             # A HQ must be on the map
                            HQ = True

                        if (tile.__class__.__name__ == "SourceMaterial" and tile.material != Materials.WATER) or tile.__class__.__name__ == "HarvestedMaterial":
                            win = False
                
                if HQ and win:
                    self.win_state = WinState.WON

            case _:
                max_time = int(self.win_condition)

                if self.elapsed_time > max_time:
                    self.win_state = WinState.FAIL

                # no_source check
                win = True

                for y, row in enumerate(self.world_map):
                    for tile in row:
                        if tile.__class__.__name__ == "SourceMaterial" and tile.material != Materials.WATER:
                            win = False
                
                if win:
                    self.win_state = WinState.WON


        # Lastly, run the next queued action if it exists
        if len(self.next_action) > 0:
            # Getting the next action by dequeueing it
            action = self.next_action[0]     
            del self.next_action[0]

            # Running logic based on action type
            match action.action_type:
                case ActionTypes.IDLE:
                    pass

                case ActionTypes.BUILD:
                    # Dequeueing first action_metadata to get building type
                    building_type = action.action_metadata[0]
                    del action.action_metadata[0]

                    # Checking if tile is in range
                    if (
                        action.target_x >= len(self.world_map[0]) or action.target_x < 0 or
                        action.target_y >= len(self.world_map) or action.target_y < 0 
                    ):
                        return

                    # Checking if the tile is free
                    if self.world_map[action.target_y][action.target_x] == None: 

                        # Checking if this is a source materials (they get charged gold to place)
                        if building_type.__name__ == "SourceMaterial":
                            if self.materials[Materials.GOLD] < 2:
                                return
                        
                            self.materials[Materials.GOLD] -= 2

                        # After all checks, place the building
                        building_type(action.target_x, action.target_y, self, *action.action_metadata)   # Setting tile to the building type with all provided metadata


                case ActionTypes.DESTROY:
                    tile = self.world_map[action.target_y][action.target_x]
                    if tile is not None:
                        if tile.__class__.__name__ == "CollectorTile" or tile.__class__.__name__ == "Conveyor":
                            if self.materials[Materials.GOLD] >= 2:
                                self.materials[Materials.GOLD] -= 2
                                tile.destroy()
                        
                        if tile.__class__.__name__ == "HQ":             # Extra penalty for destroying (and replacing) HQ
                            if self.materials[Materials.GOLD] >= 4:
                                self.materials[Materials.GOLD] -= 4
                                tile.destroy()


                # case ActionTypes.RESET:   # Both handled in UI code
                #     pass

        # Add to elapsed time
        time_diff = current_time - self.last_tick_complete
        self.elapsed_time += time_diff

        # Update last tick
        self.last_tick_complete = time.time()