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

    def kitsune_strategy(self):
        attack_unist: list[uw.Entity] = []
        enemy_units: list[uw.Entity] = []
        factory_units: list[uw.Entity] = []
        concrete_units: list[uw.Entity] = []

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
                factory_units.append(ownEntity)

            if ownEntity.Proto.proto == self.construction_units_map.concrete_plant:
                concrete_units.append(ownEntity)
            
            if self.game.prototypes.unit(proto_id).get('dps', 0) > 0:
                # fight unit
                attack_unist.append(ownEntity)
        
        if len(attack_unist) > 20:
            for unit in attack_unist:
                self.attack_nearest_enemies(unit, enemy_units)

        if len(factory_units) >= 3:
            for concrete_factory in concrete_units:
                self.game.commands.command_set_priority(concrete_factory.Id, 0) 
                

    def twinfire_strategy(self):
        attack_unist: list[uw.Entity] = []
        enemy_units: list[uw.Entity] = []
        factory_units: list[uw.Entity] = []
        concrete_units: list[uw.Entity] = []
        forgepress_units: list[uw.Entity] = []
        arsenal_units: list[uw.Entity] = []
        vehicle_asembler_units: list[uw.Entity] = []

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

            
            if self.game.prototypes.unit(proto_id).get('dps', 0) > 0:
                # fight unit
                attack_unist.append(ownEntity)
            elif ownEntity.Proto.proto == self.construction_units_map.factory:
                self.game.commands.command_set_recipe(ownEntity.Id, self.recipes_map.kitsune)
                factory_units.append(ownEntity)
            elif ownEntity.Proto.proto == self.construction_units_map.concrete_plant:
                concrete_units.append(ownEntity)
            elif ownEntity.Proto.proto == self.construction_units_map.arsenal:
                arsenal_units.append(ownEntity)
            elif ownEntity.Proto.proto == self.construction_units_map.forgepress:
                forgepress_units.append(ownEntity)
            elif ownEntity.Proto.proto == self.construction_units_map.vehicle_assembler:
                vehicle_asembler_units.append(ownEntity)
        
        if len(attack_unist) > 5:
            for unit in attack_unist:
                self.attack_nearest_enemies(unit, enemy_units)

        if len(forgepress_units) >= 0 and len(arsenal_units) > 0 and len(vehicle_asembler_units) > 0:
            for concrete_factory in concrete_units:
                self.game.commands.command_set_priority(concrete_factory.Id, 0)

        if len(forgepress_units) > 0:
            for forgepress in forgepress_units:
                self.game.commands.command_set_recipe(forgepress.Id, self.recipes_map.armor_plates)

        if len(arsenal_units) > 0:
            for arsenal in arsenal_units:
                self.game.commands.command_set_recipe(arsenal.Id, self.recipes_map.rail_gun)
        
        if len(vehicle_asembler_units) > 0:
            for asembler in vehicle_asembler_units:
                self.game.commands.command_set_recipe(asembler.Id, self.recipes_map.twinfire)

    def attack_nearest_enemies(self, unit: uw.Entity, enemy_units: list[uw.Entity]):
        _id = unit.Id
        pos = unit.Position.position

        moving_units: list[uw.Entity] = []

        for enemy in enemy_units:
            enemy_unit = self.game.prototypes.unit(enemy.Proto.proto)
            if enemy_unit is not None and len(enemy_unit.get('speeds', {})) > 0:
                moving_units.append(enemy)

        target_units = moving_units

        if len(target_units) == 0:
            target_units = enemy_units
        
        if len(self.game.commands.orders(_id)) == 0:
            enemy = sorted(
                target_units,
                key=lambda x: self.game.map.distance_estimate(
                    pos, x.Position.position
                ),
            )[0]
            self.game.commands.order(
                _id, self.game.commands.fight_to_entity(enemy.Id)
            )