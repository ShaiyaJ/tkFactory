import json
import random
import copy
import time

from tiles.world import World, Materials
from tiles.source_material import SourceMaterial
from tiles.harvested_material import HarvestedMaterial
from tiles.HQ import HQ

def __open_level_json() -> list[dict]:
    with open("./levels/levels.json") as file:
        raw = file.read()
        file.close()

    return json.loads(raw)

def save_game(level: int):
    with open("./save.txt", "w") as file:
        file.write(str(level))
        file.close()
    
def progress_game(level: int):
    level_json = __open_level_json()

    # If there isn't a next level
    if level+1 >= len(level_json):
        save_game(level)
        return

    # Otherwise increment the level counter
    with open("./save.txt", "w") as file:
        file.write(str(level+1))
        file.close()

def load_game() -> int:
    with open("./save.txt", "r") as file:
        raw = file.read()
        file.close()

    return int(raw)

def load_level(level: int) -> World:
    return_world = World()

    # Getting raw level data
    level_json = __open_level_json()
    level_data = level_json[level]

    # Assuming maps are square, generate blank tiles
    size_y = len(level_data["tiles"])
    size_x = len(level_data["tiles"][0])
    return_world.set_world_size(size_x, size_y)

    # Translating it into a level
    for (y, row) in enumerate(level_data["tiles"]):
        for (x, cell) in enumerate(row):
            match cell: 
                case "~":
                    SourceMaterial(x, y, return_world, Materials.WATER)
                case "W":
                    SourceMaterial(x, y, return_world, Materials.WOOD)
                case "w":
                    HarvestedMaterial(x, y, return_world, Materials.WOOD)
                case "S":
                    SourceMaterial(x, y, return_world, Materials.STONE)
                case "s":
                    HarvestedMaterial(x, y, return_world, Materials.STONE)
                case "M":
                    SourceMaterial(x, y, return_world, Materials.METAL)
                case "m":
                    HarvestedMaterial(x, y, return_world, Materials.METAL)
                case "O":
                    SourceMaterial(x, y, return_world, Materials.OIL)
                case "o":
                    HarvestedMaterial(x, y, return_world, Materials.OIL)
                case "H":
                    HQ(x, y, return_world)
                case _:
                    return_world.world_map[y][x] = None

    # Setting win condition and message
    return_world.win_condition = level_data["win"]
    return_world.message = level_data["message"]
    return_world.materials[Materials.GOLD] = level_data["starting_gold"]

    return return_world