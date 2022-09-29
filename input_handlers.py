# although not necessary, using type hinting
from typing import Optional

# tcod.event will help us see what keys the player is pressing
import tcod.event

from actions import Action, EscapeAction, MovementAction

class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

# defining quit function, which is taken from EventDispatch: ev_quit
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
# this variable holds the key that was pressed
        key = event.sym

# defining movement keys
        if key == tcod.event.K_UP:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx=1, dy=0)

# defining quit key
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

# no valid key was pressed
        return action