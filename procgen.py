from __future__ import annotations
import random

from typing import TYPE_CHECKING, Tuple, Iterator
from entity import Entity
from typing import Iterator, Tuple, List, TYPE_CHECKING


import tcod

from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from entity import Entity

class RectangularRoom:
    def __init__(self, x: int, y: int, width:int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """return the inner area of this room as a 2D array index"""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    
    def intersects(self, other: RectangularRoom) -> bool:
        """Return true if one RectangularRoom overlaps with another"""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y

# def generate_dungeon(map_width, map_height) -> GameMap:
#     dungeon = GameMap(map_width, map_height)

#     room_1 = RectangularRoom(x=20, y=15, width=10, height=15)
#     room_2 = RectangularRoom(x=35, y=15, width=10, height=15)

#     dungeon.tiles[room_1.inner] = tile_types.floor
#     dungeon.tiles[room_2.inner] = tile_types.floor 

#     for x, y in tunnel_between(room_2.center, room_1.center):
#         dungeon.tiles[x, y] = tile_types.floor


#     return dungeon

def generate_dungeon(
    max_rooms: int,

    room_min_size: int,
    # picking a random size between this and room_min_size for both the width and the height of one room to carve out 
    room_max_size: int,
    map_width: int,
    map_height: int,
    # need to know this to know where to place the player
    player: Entity,
) -> GameMap:
    """Generate new dungeon map."""
    dungeon = GameMap(map_width, map_height)

    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue # this room intersects, so go to the next attempt
        # if there aren't any intersections the room is valid

        # Dig out this room's inner area.
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # the first room where the player starts
            player.x, player.y = new_room.center
        else: #All rooms after the first
            # Dig out a tunnel between this room and the previous one
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        rooms.append(new_room)

    return dungeon