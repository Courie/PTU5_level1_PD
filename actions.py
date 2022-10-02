from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """perform this action with the objects needed to determine it's scope
        engine is the scope this action is being performed in 
        enntity is the object performing this action
        this method must be overriden by action subclasses"""

        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()

class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity):
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return # destination is out of bounds 

        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return #destiation is blocked by a tile

        entity.move(self.dx, self.dy)
