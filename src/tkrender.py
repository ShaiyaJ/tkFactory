from __future__ import annotations

import enum
import tkinter as tk
from os.path import abspath
import random

from display_type import DisplayType

from tiles.world import World, ActionTypes, Materials, WinState
import tiles
import save_manager


class UI_Button(tk.Button):
    def __init__(self, master, *args, **kwargs):
        tk.Button.__init__(self, master, *args, **kwargs)

        self.config(
            pady=5,
            borderwidth=5,
            bg="#AF6E42",
            fg="#FFE568",
            font=("Consolas", 12, "bold")
        )

class UI_ImageButton(tk.Button):
    def __init__(self, master, *args, **kwargs):
        # Avoiding asset garbage collection
        self.arg = args
        self.kwargs = kwargs

        # Making button
        tk.Button.__init__(self, master, *args, **kwargs)

        # Config
        self.config(
            pady=5,
            relief=tk.FLAT,
            bg="#9E5353"
        )

class UI_Canvas[TileTypes](tk.Canvas):
    ground_tile: DisplayType    # Needs their own display type to avoid garbage collection
    warn_triangle: DisplayType
    water_border: DisplayType
    harvested_gold: DisplayType
    harvested_wood: DisplayType
    harvested_stone: DisplayType
    harvested_metal: DisplayType
    harvested_oil: DisplayType
    harvested_water: DisplayType
    harvested_steam: DisplayType
    energy: DisplayType

    active_window: UI           # For communication with the currently running game- 
    scale: int

    def __init__(self, master, window: UI, scale: int=8, *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)

        # Setting attributes
        self.window = window
        self.scale = scale
        self.ground_tile = DisplayType("./assets/ground.png")
        self.warn_triangle = DisplayType("./assets/warn_triangle.png", scale=4)
        self.warn_bubble = DisplayType("./assets/warn_bubble.png", scale=4)
        self.water_border = DisplayType("./assets/water_border.png", scale=4)
        self.harvested_gold = DisplayType("./assets/gold.png", scale=4)
        self.harvested_wood = DisplayType("./assets/h_tree.png", scale=4)
        self.harvested_stone = DisplayType("./assets/h_stone.png", scale=4)
        self.harvested_metal = DisplayType("./assets/h_metal.png", scale=4)
        self.harvested_oil = DisplayType("./assets/h_oil.png", scale=4)
        self.harvested_water = DisplayType("./assets/h_water.png", scale=4)
        self.harvested_steam = DisplayType("./assets/h_steam.png", scale=4)
        self.energy = DisplayType("./assets/electricity.png", scale=4)

        # Setting controls
        self.bind("<Button-1>", self.on_click)

    def draw_frame(self, new_tiles: list[list[TileTypes]]): # Scales are used all throughout this class, and 
        # Clearing canvas
        self.delete(tk.ALL)

        # Drawing assets
        for (y, row) in enumerate(new_tiles):
            for (x, cell) in enumerate(row):
                # Ground texture
                self.create_image(x*(8*self.scale), y*(8*self.scale), anchor=tk.NE, image=self.ground_tile)

                # Tile texture
                if cell != None:
                    # Creating image
                    self.create_image(x*(8*self.scale),y*(8*self.scale), anchor=tk.NE, image=cell.display)

                # Overlays 
                if type(cell) == tiles.CollectorTile:  
                    # Drawing input requirements overlay
                    if cell.requires_power and not cell.check_power():
                        self.create_image(x*(8*self.scale),y*(8*self.scale)+16, anchor=tk.NE, image=self.warn_bubble)
                        self.create_image(x*(8*self.scale),y*(8*self.scale)+16, anchor=tk.NE, image=self.energy)
                        self.create_image(x*(8*self.scale)-32,y*(8*self.scale)+16, anchor=tk.NE, image=self.warn_triangle)

                    if cell.requires_water and not cell.check_water():
                        self.create_image(x*(8*self.scale),y*(8*self.scale)+16, anchor=tk.NE, image=self.warn_bubble)
                        self.create_image(x*(8*self.scale),y*(8*self.scale)+16, anchor=tk.NE, image=self.harvested_water)
                        self.create_image(x*(8*self.scale)-32,y*(8*self.scale)+16, anchor=tk.NE, image=self.warn_triangle)
                
                    if cell.requires_steam and not cell.check_steam():
                        self.create_image(x*(8*self.scale),y*(8*self.scale)+16, anchor=tk.NE, image=self.warn_bubble)
                        self.create_image(x*(8*self.scale),y*(8*self.scale)+16, anchor=tk.NE, image=self.harvested_steam)
                        self.create_image(x*(8*self.scale)-32,y*(8*self.scale)+16, anchor=tk.NE, image=self.warn_triangle)

                    # Drawing building requirements overlay
                    for key, value in cell.build_progress.items():
                        if value != 0:
                            self.create_image(x*(8*self.scale),y*(8*self.scale)+16, anchor=tk.NE, image=self.warn_bubble)

                            match key:
                                case Materials.WOOD:
                                    self.create_image(x*(8*self.scale),y*(8*self.scale)+16, anchor=tk.NE, image=self.harvested_wood)
                                case Materials.STONE:
                                    self.create_image(x*(8*self.scale),y*(8*self.scale)+16, anchor=tk.NE, image=self.harvested_stone)
                                case Materials.METAL:
                                    self.create_image(x*(8*self.scale),y*(8*self.scale)+16, anchor=tk.NE, image=self.harvested_metal)
                                case Materials.OIL:
                                    self.create_image(x*(8*self.scale),y*(8*self.scale)+16, anchor=tk.NE, image=self.harvested_oil)

                            self.create_image(x*(8*self.scale)-32,y*(8*self.scale)+16, anchor=tk.NE, image=self.warn_triangle)

                if type(cell) == tiles.Conveyor:
                    # Drawing carrying contents
                    if cell.carrying is not None:
                        self.create_image(x*(8*self.scale),y*(8*self.scale), anchor=tk.NE, image=cell.carrying.display)
                    
                    # Drawing power requirement
                    if not cell.check_power():
                        self.create_image(x*(8*self.scale),y*(8*self.scale)+16, anchor=tk.NE, image=self.warn_bubble)
                        self.create_image(x*(8*self.scale),y*(8*self.scale)+16, anchor=tk.NE, image=self.energy)
                        self.create_image(x*(8*self.scale)-32,y*(8*self.scale)+16, anchor=tk.NE, image=self.warn_triangle)

        # TODO: draw grid?

        # Resizing canvas
        bbox = self.bbox("all")
        if bbox:
            self.config(scrollregion=bbox)
            self.config(width=bbox[2] - bbox[0], height=bbox[3] - bbox[1])

    def on_click(self, event):
        # Getting tile coordinates and setting selection attributes
        selection_x = event.x // (8*self.scale)
        selection_y = event.y // (8*self.scale)

        # Queueing new action using the active window
        self.window.queue_action(selection_x, selection_y)



class UIState(enum.Enum):
    MAIN_MENU = enum.auto()
    PAUSE = enum.auto()
    GAMEPLAY = enum.auto()
    WON = enum.auto()
    FAIL = enum.auto()

class UI[T](tk.Tk):
    state: UIState
    active_game: World

    # Main menu UI elements
    continue_game: UI_Button
    new_game: UI_Button

    # Pause UI elements
    unpause: UI_Button
    quit_main_menu: UI_Button
    quit_desktop: UI_Button

    # Gameplay UI elements
    tile_UI: UI_Canvas
    action_mode: ActionTypes
    action_metadata: list[T]

    tile_frame: tk.Frame
    control_frame: tk.Frame
    action_frame: tk.Frame
    build_frame: tk.Frame
    store_frame: tk.Frame
    info_frame: tk.Frame

    build_label: tk.Label

    build_chopping_site: UI_ImageButton
    build_mining_site: UI_ImageButton
    build_oil_drill: UI_ImageButton
    build_boiler: UI_ImageButton
    build_steam_gen: UI_ImageButton
    build_power_line: UI_ImageButton
    build_conveyor_left: UI_ImageButton
    build_conveyor_up: UI_ImageButton
    build_conveyor_right: UI_ImageButton
    build_conveyor_down: UI_ImageButton
    build_turret: UI_ImageButton
    build_long_turret: UI_ImageButton
    build_barbed_wire: UI_ImageButton
    build_electric_fence: UI_ImageButton
    build_HQ: UI_ImageButton
    build_drill: UI_ImageButton

    store_label: tk.Label

    build_source_wood: UI_ImageButton
    build_source_stone: UI_ImageButton
    build_source_metal: UI_ImageButton
    build_source_oil: UI_ImageButton

    action_label: tk.Label

    reset_command: UI_ImageButton   
    destroy_command: UI_ImageButton

    info_label: tk.Label
    info_img: tk.Label
    info_text: tk.Label    
    
    message_text: tk.Label

    # WON and FAIL UI elements
    time: tk.Label
    fail_label: tk.Label
    next_level: UI_Button
    reset_game: UI_Button

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Tinker Factory")
        self.iconbitmap(default=abspath("./assets/icon.ico"))
        self.geometry("1024x768")
        self.minsize(1024, 768)

        self.action_mode = ActionTypes.IDLE
        self.action_metadata = []

        self.bind("<Key>", self.handle_input)
        self.config(bg="#7A2E2E")

        self.__change_ui_state(UIState.MAIN_MENU)

    def generate_ui(self):
        # MAIN_MENU UI elements
        self.continue_game = UI_Button(self, text="Continue", command=self.continue_game_cmd)
        self.new_game = UI_Button(self, text="New Game", command=self.new_game_cmd)

        # PAUSE UI elements
        self.unpause = UI_Button(self, text="Unpause", command=self.unpause_cmd)
        self.quit_main_menu = UI_Button(self, text="Quit to main menu", command=self.quit_main_menu_cmd)
        self.quit_desktop = UI_Button(self, text="Quit to desktop", command=self.quit_desktop_cmd)

        # GAMEPLAY UI elements
        self.action_mode: ActionTypes = None
        
        self.tile_frame = tk.Frame(self, bg="#9E5353")
        self.tile_UI = UI_Canvas(self.tile_frame, self)

        self.control_frame = tk.Frame(self, bg="#7A2E2E")

        self.material_frame = tk.Frame(self.control_frame, bg="#9E5353")
        self.action_frame = tk.Frame(self.control_frame, bg="#9E5353")
        self.build_frame = tk.Frame(self.control_frame, bg="#9E5353")
        self.store_frame = tk.Frame(self.control_frame, bg="#9E5353")
        self.info_frame = tk.Frame(self.control_frame, bg="#9E5353")

        self.material_label = tk.Label(self.control_frame, text="Material", font=("Consolas", 12, "bold"), bg="#7A2E2E", fg="#FFE568")
        self.material_gold = tk.Label(self.material_frame, text="", font=("Consolas", 12, "bold"), bg="#9E5353", fg="#FFE568", image=self.tile_UI.harvested_gold, compound=tk.LEFT)
        self.material_wood = tk.Label(self.material_frame, text="", font=("Consolas", 12, "bold"), bg="#9E5353", fg="#FFE568", image=self.tile_UI.harvested_wood, compound=tk.LEFT)
        self.material_stone = tk.Label(self.material_frame, text="", font=("Consolas", 12, "bold"), bg="#9E5353", fg="#FFE568", image=self.tile_UI.harvested_stone, compound=tk.LEFT)
        self.material_metal = tk.Label(self.material_frame, text="", font=("Consolas", 12, "bold"), bg="#9E5353", fg="#FFE568", image=self.tile_UI.harvested_metal, compound=tk.LEFT)
        self.material_oil = tk.Label(self.material_frame, text="", font=("Consolas", 12, "bold"), bg="#9E5353", fg="#FFE568", image=self.tile_UI.harvested_oil, compound=tk.LEFT)

        self.action_label = tk.Label(self.control_frame, text="Actions", font=("Consolas", 12, "bold"), bg="#7A2E2E", fg="#FFE568")

        self.reset_command = UI_ImageButton(self.action_frame,
            command=lambda: self.set_gameplay_state_reset(),
            image=DisplayType("./assets/reset.png", scale=3)
        )
        self.destroy_command = UI_ImageButton(self.action_frame,
            command=lambda: self.set_gameplay_state_destroying(),
            image=DisplayType("./assets/destroy.png", scale=3)
        )

        self.build_label = tk.Label(self.control_frame, text="Buildings", font=("Consolas", 12, "bold"), bg="#7A2E2E", fg="#FFE568")

        self.build_chopping_site = UI_ImageButton(self.build_frame, 
            command=lambda: self.set_gameplay_state_building(tiles.CollectorTile, tiles.CollectorTiles.CHOPPING_SITE),
            image=DisplayType("./assets/chopping_site.png", scale=4)
        )
        self.build_mining_site = UI_ImageButton(self.build_frame, 
            command=lambda: self.set_gameplay_state_building(tiles.CollectorTile, tiles.CollectorTiles.MINING_SITE),
            image=DisplayType("./assets/mining_site.png", scale=4)
        )
        self.build_oil_drill = UI_ImageButton(self.build_frame, 
            command=lambda: self.set_gameplay_state_building(tiles.CollectorTile, tiles.CollectorTiles.OIL_DRILL),
            image=DisplayType("./assets/oil_drill.png", scale=4)
        )
        self.build_boiler = UI_ImageButton(self.build_frame, 
            command=lambda: self.set_gameplay_state_building(tiles.CollectorTile, tiles.CollectorTiles.BOILER),
            image=DisplayType("./assets/boiler.png", scale=4)
        )
        self.build_steam_gen = UI_ImageButton(self.build_frame, 
            command=lambda: self.set_gameplay_state_building(tiles.CollectorTile, tiles.CollectorTiles.STEAM_GEN),
            image=DisplayType("./assets/generator.png", scale=4)
        )
        self.build_power_line = UI_ImageButton(self.build_frame, 
            command=lambda: self.set_gameplay_state_building(tiles.CollectorTile, tiles.CollectorTiles.POWER_LINE),
            image=DisplayType("./assets/power_line.png", scale=4)
        )
        self.build_conveyor_left = UI_ImageButton(self.build_frame, 
            command=lambda: self.set_gameplay_state_building(tiles.Conveyor, (1,0)),
            image=DisplayType.rotate("./assets/conveyor.png", scale=4, deg=0)
        )
        self.build_conveyor_up= UI_ImageButton(self.build_frame, 
            command=lambda: self.set_gameplay_state_building(tiles.Conveyor, (0,-1)),
            image=DisplayType.rotate("./assets/conveyor.png", scale=4, deg=90)
        )
        self.build_conveyor_right = UI_ImageButton(self.build_frame, 
            command=lambda: self.set_gameplay_state_building(tiles.Conveyor, (-1,0)),
            image=DisplayType.rotate("./assets/conveyor.png", scale=4, deg=180)
        )
        self.build_conveyor_down = UI_ImageButton(self.build_frame, 
            command=lambda: self.set_gameplay_state_building(tiles.Conveyor, (0,1)),
            image=DisplayType.rotate("./assets/conveyor.png", scale=4, deg=270)
        )
        self.build_turret = UI_ImageButton(self.build_frame, 
            command=lambda: self.set_gameplay_state_building(tiles.AttackerTile, tiles.AttackerTiles.TURRET),
            image=DisplayType("./assets/turret.png", scale=4)
        )
        self.build_long_turret = UI_ImageButton(self.build_frame, 
            command=lambda: self.set_gameplay_state_building(tiles.AttackerTile, tiles.AttackerTiles.LONG_RANGED_TURRET),
            image=DisplayType("./assets/long_ranged_turret.png", scale=4)
        )
        self.build_barbed_wire = UI_ImageButton(self.build_frame, 
            command=lambda: self.set_gameplay_state_building(tiles.AttackerTile, tiles.AttackerTiles.BARBED_WIRE),
            image=DisplayType("./assets/barbed_wire.png", scale=4)
        )
        self.build_electric_fence = UI_ImageButton(self.build_frame, 
            command=lambda: self.set_gameplay_state_building(tiles.AttackerTile, tiles.AttackerTiles.ELECTRIC_FENCE),
            image=DisplayType("./assets/electric_fence.png", scale=4)
        )
        self.build_HQ = UI_ImageButton(self.build_frame, 
            command=lambda: self.set_gameplay_state_building(tiles.HQ),
            image=DisplayType("./assets/HQ.png", scale=4)
        )
        self.build_drill = UI_ImageButton(self.build_frame, 
            command=lambda: self.set_gameplay_state_building(tiles.CollectorTile, tiles.CollectorTiles.DRILL),
            image=DisplayType("./assets/drill.png", scale=4)
        )

        self.store_label = tk.Label(self.control_frame, text="Resource Shop", font=("Consolas", 12, "bold"), bg="#7A2E2E", fg="#FFE568")

        self.build_source_wood = UI_ImageButton(self.store_frame,
            command = lambda: self.set_gameplay_state_building(tiles.SourceMaterial, Materials.WOOD),
            image=DisplayType("./assets/h_tree.png", scale=4)
        )
        self.build_source_stone = UI_ImageButton(self.store_frame, 
            command = lambda: self.set_gameplay_state_building(tiles.SourceMaterial, Materials.STONE),
            image=DisplayType("./assets/h_stone.png", scale=4)
        )
        self.build_source_metal = UI_ImageButton(self.store_frame, 
            command = lambda: self.set_gameplay_state_building(tiles.SourceMaterial, Materials.METAL),
            image=DisplayType("./assets/h_metal.png", scale=4)
        )
        self.build_source_oil = UI_ImageButton(self.store_frame, 
            command = lambda: self.set_gameplay_state_building(tiles.SourceMaterial, Materials.OIL),
            image=DisplayType("./assets/h_oil.png", scale=4)
        )

        self.info_label = tk.Label(self.control_frame, text="INFO", font=("Consolas", 12, "bold"), bg="#7A2E2E", fg="#FFE568")
        self.elapsed_time = tk.Label(self.info_frame, font=("Consolas", 10, "bold"), bg="#9E5353", fg="#FFE568", justify=tk.LEFT)
        self.info_text = tk.Label(self.info_frame, text="", font=("Consolas", 10, "bold"), bg="#9E5353", fg="#FFE568", justify=tk.LEFT)

        self.message_text = tk.Label(self, text="Tinker Factory - Shaiya J.", font=("Consolas", 10, "bold"), bg="#7A2E2E", fg="#FFE568", justify=tk.LEFT)

        # WON and FAIL UI
        self.time = tk.Label(self, text="You completed the level in {}!", font=("Consolas", 12, "bold"), bg="#7A2E2E", fg="#FFE568")
        self.fail_label = tk.Label(self, text="You lost!", font=("Consolas", 12, "bold"), bg="#7A2E2E", fg="#FFE568")
        self.next_level = UI_Button(self, text="Next level...", command=self.next_level_cmd)
        self.reset_game = UI_Button(self, text="Retry", command=self.reset_cmd)

    # State management and rendering
    def __change_ui_state(self, state: UIState):
        # Clearing all widgets on screen
        for widget in self.winfo_children():
            widget.destroy()

        # Regenerating UI
        self.generate_ui() 

        # Updating UI state
        self.state = state

        # Rendering state
        match self.state:
            case UIState.MAIN_MENU:
                self.__render_main_menu()
            case UIState.PAUSE:
                self.__render_pause_menu()
            case UIState.GAMEPLAY:
                self.__render_gameplay()
                self.__render_gameplay_loop()
            case UIState.WON:
                self.__render_WON()
            case UIState.FAIL:
                self.__render_FAIL()

    def __render_main_menu(self):
        self.continue_game.pack(fill=tk.X, pady=5, padx=20)
        self.new_game.pack(fill=tk.X, pady=5, padx=20)
        self.quit_desktop.pack(fill=tk.X, pady=5, padx=20)

    def __render_pause_menu(self):
        self.unpause.pack(fill=tk.X, pady=5, padx=20)
        self.quit_main_menu.pack(fill=tk.X, pady=5, padx=20)
        self.quit_desktop.pack(fill=tk.X, pady=5, padx=20)

    def __render_gameplay(self):
        self.material_gold.grid(row=0, column=0)
        self.material_wood.grid(row=0, column=1)
        self.material_stone.grid(row=1, column=0)
        self.material_metal.grid(row=1, column=1)
        self.material_oil.grid(row=2, column=0)

        self.reset_command.grid(row=0, column=0)
        self.destroy_command.grid(row=0, column=1)


        self.build_chopping_site.grid(row=0, column=0)
        self.build_mining_site.grid(row=0, column=1)
        self.build_drill.grid(row=1, column=0)
        self.build_oil_drill.grid(row=1, column=1)
        self.build_boiler.grid(row=2, column=0)
        self.build_steam_gen.grid(row=2, column=1)
        self.build_power_line.grid(row=3, column=0)
        self.build_conveyor_left.grid(row=3, column=1)
        self.build_conveyor_up.grid(row=4, column=0)
        self.build_conveyor_right.grid(row=4, column=1)
        self.build_conveyor_down.grid(row=5, column=0)
        # self.build_turret.grid(row=5, column=0)
        # self.build_long_turret.grid(row=5, column=1)
        # self.build_barbed_wire.grid(row=6, column=0)
        # self.build_electric_fence.grid(row=6, column=1)
        self.build_HQ.grid(row=5, column=1)


        self.build_source_wood.grid(row=0, column=0)
        self.build_source_stone.grid(row=0, column=1)
        self.build_source_metal.grid(row=1, column=0)
        self.build_source_oil.grid(row=1, column=1)

        self.elapsed_time.pack(fill=tk.X, expand=tk.TRUE)
        self.info_text.pack(fill=tk.X, expand=tk.TRUE)

        if self.active_game.message != "":
            self.message_text.config(text=self.active_game.message)
        self.message_text.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.TRUE)


        # self.tile_UI.pack(fill=tk.BOTH, expand=tk.TRUE, side=tk.LEFT)
        self.tile_UI.pack_propagate(tk.FALSE)
        self.tile_UI.pack(anchor=tk.CENTER, expand=tk.TRUE, fill=tk.NONE)

        self.tile_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, expand=tk.FALSE, anchor=tk.N)

        self.action_label.pack()
        self.action_frame.pack()
        
        self.material_label.pack()
        self.material_frame.pack()

        self.build_label.pack()
        self.build_frame.pack()

        self.store_label.pack()
        self.store_frame.pack()

        self.info_label.pack()
        self.info_frame.pack(fill=tk.X, expand=tk.TRUE, padx=5)

    def __render_gameplay_loop(self):
        # Check win
        if self.active_game.win_state == WinState.WON:
            self.__change_ui_state(UIState.WON)
        if self.active_game.win_state == WinState.FAIL:
            self.__change_ui_state(UIState.FAIL)


        # Run tick 
        self.active_game.tick() # If not enough time has passed since the last tick, then this will return quickly

        # Update info UI elements
        self.material_gold.config(text=self.active_game.materials[Materials.GOLD])
        self.material_wood.config(text=self.active_game.materials[Materials.WOOD])
        self.material_stone.config(text=self.active_game.materials[Materials.STONE])
        self.material_metal.config(text=self.active_game.materials[Materials.METAL])
        self.material_oil.config(text=self.active_game.materials[Materials.OIL])

        lab = ""

        match self.action_mode:
            case ActionTypes.DESTROY:
                lab = ">Destroy mode\n  READY!"
            case ActionTypes.BUILD:
                lab = ">Build mode\n"
                match self.action_metadata[0].__name__:
                    case "CollectorTile":
                        lab += "  " + self.action_metadata[1].name.replace("_", " ")
                    case "SourceMaterial":
                        lab += "  " + self.action_metadata[1].name.replace("_", " ")
                    case "Conveyor":
                        lab += "  " + "CONVEYOR"
                    case "HQ":
                        lab += "  " + "HQ"
            case _:
                lab = ">Idle mode\n  Waiting..."


        self.info_text.config(text=lab)
        self.elapsed_time.config(text=f"{int(self.active_game.elapsed_time//60)}m {int(round(self.active_game.elapsed_time%60, ndigits=0))}s")

        # Push the mainloop back onto the event loop 
        if self.state == UIState.GAMEPLAY:
            self.tile_UI.draw_frame(self.active_game.world_map)
            self.after(1, self.__render_gameplay_loop)

    def __render_WON(self):
        self.time.config(text=f"You completed the level in {int(self.active_game.elapsed_time//60)}m {round(self.active_game.elapsed_time%60, ndigits=1)}s!")
        self.time.pack(fill=tk.X, pady=5, padx=20)
        self.next_level.pack(fill=tk.X, pady=5, padx=20)
        self.reset_game.pack(fill=tk.X, pady=5, padx=20)
        self.quit_main_menu.pack(fill=tk.X, pady=5, padx=20) 
        self.quit_desktop.pack(fill=tk.X, pady=5, padx=20)

    def __render_FAIL(self):
        self.fail_label.pack(fill=tk.X, pady=5, padx=20)
        self.reset_game.pack(fill=tk.X, pady=5, padx=20)
        self.quit_main_menu.pack(fill=tk.X, pady=5, padx=20)
        self.quit_desktop.pack(fill=tk.X, pady=5, padx=20)


    # Main menu functionality
    def continue_game_cmd(self):
        level = save_manager.load_game()
        self.active_game = save_manager.load_level(level)
        self.__change_ui_state(UIState.GAMEPLAY)

    def new_game_cmd(self):
        save_manager.save_game(0)
        self.continue_game_cmd()

    # Pause menu functionality
    def unpause_cmd(self):
        self.kbhit_esc()

    def quit_main_menu_cmd(self):
        if self.state == UIState.WON:
            level = save_manager.load_game()
            save_manager.progress_game(level)

        self.__change_ui_state(UIState.MAIN_MENU)

    def quit_desktop_cmd(self):
        if self.state == UIState.WON:
            level = save_manager.load_game()
            save_manager.progress_game(level)

        self.destroy()
        exit()

    # Gameplay functionality
    def set_gameplay_state_building[TileTypes](self, building: TileTypes, *args):
        self.action_mode = ActionTypes.BUILD
        self.action_metadata = [building, *args]

    def set_gameplay_state_destroying(self):
        self.action_mode = ActionTypes.DESTROY
        self.action_metadata = []

    def set_gameplay_state_reset(self):
        level = save_manager.load_game()
        self.active_game = save_manager.load_level(level)

        self.action_mode = ActionTypes.IDLE

    def queue_action(self, x: int, y: int):
        self.active_game.queue_new_action(self.action_mode, x, y, *self.action_metadata)

    # WON and FAIL functionality
    def reset_cmd(self):
        self.set_gameplay_state_reset()
        self.__change_ui_state(UIState.GAMEPLAY)

    def next_level_cmd(self):
        level = save_manager.load_game()
        save_manager.progress_game(level)

        new_level = save_manager.load_game()
        self.active_game = save_manager.load_level(new_level)

        self.__change_ui_state(UIState.GAMEPLAY)


    # Keybind functionality
    def handle_input(self, event):
        key = event.keysym.lower()

        match key:
            case "escape":
                self.kbhit_esc()
            
            case "d":
                self.kbhit_d()

            case "r":
                self.kbhit_r()

            case _:
                self.kbhit_other(key)

    def kbhit_esc(self):                    # Gameplay pause menu
        if self.state == UIState.GAMEPLAY:
            self.__change_ui_state(UIState.PAUSE)
        elif self.state == UIState.PAUSE:
            self.__change_ui_state(UIState.GAMEPLAY)

    def kbhit_d(self):                      # Destroy hotkey
        if self.state == UIState.GAMEPLAY:
            self.set_gameplay_state_destroying()

    def kbhit_r(self):                      # Reset hotkey
        if self.state == UIState.GAMEPLAY:
            self.set_gameplay_state_reset()

    def kbhit_other(self, char: str):       # Hitting buttons and selecting buildings
        match self.state:
            case UIState.MAIN_MENU:
                match char:
                    case "1":
                        self.continue_game.invoke()
                    case "2":
                        self.new_game.invoke()
                    case "3":
                        self.quit_desktop.invoke()

            case UIState.PAUSE:
                match char:
                    case "1":
                        self.unpause.invoke()
                    case "2":
                        self.quit_main_menu.invoke()
                    case "3":
                        self.quit_desktop.invoke()

            case UIState.GAMEPLAY:
                match char:
                    case "6":
                        self.build_chopping_site.invoke()
                    case "7":
                        self.build_mining_site.invoke()
                    case "8":
                        self.build_drill.invoke()
                    case "9":
                        self.build_oil_drill.invoke()
                    case "y":
                        self.build_boiler.invoke()
                    case "u":
                        self.build_steam_gen.invoke()
                    case "i":
                        self.build_power_line.invoke()
                    case "o":
                        self.build_conveyor_left.invoke()
                    case "h":
                        self.build_conveyor_up.invoke()
                    case "j":
                        self.build_conveyor_right.invoke()
                    case "k":
                        self.build_conveyor_down.invoke()
                    case "l":
                        self.build_HQ.invoke()
                    case "n":
                        self.build_source_wood.invoke()
                    case "m":
                        self.build_source_stone.invoke()
                    case "comma":
                        self.build_source_metal.invoke()
                    case "period":
                        self.build_source_oil.invoke()
