from typing import Callable, Any
import uw
from random import random

class BuildOrder:
    def __init__(self, proto: int, position_f: Callable[[], int], id: int = -1, deps: list[Any] = None) -> None:
        self.proto = proto
        self.position_f = position_f
        self.position = -1
        self.id = id
        self.deps = deps if deps is not None else []

    def build(self, game: uw.Game):
        if self.position != -1:
            if any(self._entity_is_this_shit(game, game.world.entity(id))
                    for id in game.map.entities(self.position)):
                return

        self.position = self.position_f()

        game.commands.command_place_construction(
            position=self.position,
            yaw=random(),
            proto=self.proto
        )

    def _entity_is_this_shit(self, game: uw.Game, entity: uw.Entity) -> bool:
        return entity.own() and game.prototypes.name(entity.Proto.proto) == game.prototypes.name(self.proto)

    def _entity_is_built(self, game: uw.Game, entity: uw.Entity) -> bool:
        return self._entity_is_this_shit(game, entity) and entity.has('Life')

    def is_built(self, game: uw.Game) -> bool:
        if self.position == -1:
            return False

        return any(self._entity_is_built(game, game.world.entity(id))
            for id in game.map.entities(self.position))
