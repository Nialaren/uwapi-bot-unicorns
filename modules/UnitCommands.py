import uw
from .ProtoId import ConstructionUnit, Units, Recipes


class UnitComands:
    def __init__(
        self,
        game: uw.Game,
        
    ) -> None:
        self.game: uw.Game = game
        self._initialized = False
    
    def init(
        self,
        units_map: Units,
        construction_units_map: ConstructionUnit,
        recipes_map: Recipes,
    ):
        self.units_map: Units = units_map
        self.construction_units_map: ConstructionUnit = construction_units_map
        self.recipes_map: Recipes = recipes_map
        self._initialized = True

    def is_initialized(self):
        return self._initialized

    def command_units(self):
        attack_unist: list[uw.Entity] = []
        enemy_units: list[uw.Entity] = []
        for entity in self.game.world.entities().values():
            if entity.policy() == uw.Policy.Enemy and entity.has('Unit'):
                enemy_units.append(entity)
                continue

            if not (entity.own() and entity.has('Proto')):
                continue

            ownEntity: uw.Entity = entity
            proto_id = int(ownEntity.Proto.proto)

            proto_type = self.game.prototypes.type(proto_id)

            if not proto_type == uw.Prototype.Unit:
                continue

            if ownEntity.Proto.proto == self.construction_units_map.factory:
                self.game.commands.command_set_recipe(ownEntity.Id, self.recipes_map.kitsune)
            
            if self.game.prototypes.unit(proto_id).get('dps', 0) > 0:
                # fight unit
                attack_unist.append(ownEntity)
        
        if len(attack_unist) > 20:
            for unit in attack_unist:
                self.attack_nearest_enemies(unit, enemy_units)
                

    def attack_nearest_enemies(self, unit: uw.Entity, enemy_units: list[uw.Entity]):
        _id = unit.Id
        pos = unit.Position.position

        enemy_moving_units = filter(lambda e : len(self.game.prototypes.unit(e.Proto.proto).get('speeds', {})) > 0, enemy_units)
        if len(self.game.commands.orders(_id)) == 0:
            enemy = sorted(
                enemy_moving_units,
                key=lambda x: self.game.map.distance_estimate(
                    pos, x.Position.position
                ),
            )[0]
            self.game.commands.order(
                _id, self.game.commands.fight_to_entity(enemy.Id)
            )