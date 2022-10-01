#I've included this as our beloved Kestutis is on linux
#!/usr/bin/env python3

# the library that we will use for the project
import tcod

# importing player movement
from engine import Engine
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler

def main() -> None:
    # this is the size of the terminal
    screen_width = 80
    screen_height = 50
    # this is the size of our game map
    map_width = 80
    map_height = 45

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    
    event_handler = EventHandler()

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 0))
    entities = {npc, player}

    game_map = GameMap(map_width, map_height)

    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="HEAVEN4",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
                engine.render(console=root_console, context=context)

                events = tcod.event.wait()

                engine.handle_events(events)
          

if __name__ =="__main__":
    main()