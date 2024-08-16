import uw
from .ProtoId import ConstructionUnit, Units, Recipes
from modules import EntityManager
from enum import Flag


class ForceStateFlags(Flag):
   NONE = 0
   Winner = 1 << 0
   Defeated = 1 << 1
   Disconnected = 1 << 2


class UnitComands:
    def __init__(
        self,
        game: uw.Game,
        entity_manager: EntityManager

    ) -> None:
        self.game: uw.Game = game
        self.entity_manager = entity_manager
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


    def twinfire_strategy(self, all_done = False):
        attack_unist: list[uw.Entity] = []
        enemy_units: list[uw.Entity] = []
        factory_units: list[uw.Entity] = []
        concrete_units: list[uw.Entity] = []
        forgepress_units: list[uw.Entity] = []
        arsenal_units: list[uw.Entity] = []
        vehicle_asembler_units: list[uw.Entity] = []

        for entity in self.game.world.entities().values():
            if entity.policy() == uw.Policy.Enemy and entity.has('Unit'):
                if entity.has('Owner'):
                    force_state_flags = ForceStateFlags(self.game.world.entity(entity.Owner.force).Force.state)
                    if ForceStateFlags.Defeated in force_state_flags or ForceStateFlags.Disconnected in force_state_flags:
                        # enemy is defeated, ignore them
                        continue

                enemy_units.append(entity)
                continue

            if not (entity.own() and entity.has('Proto')):
                continue

            ownEntity: uw.Entity = entity
            proto_id = int(ownEntity.Proto.proto)

            proto_type = self.game.prototypes.type(proto_id)

            if not proto_type == uw.Prototype.Unit:
                continue

            entity_unit = self.game.prototypes.unit(proto_id)

            if entity_unit is not None and entity_unit.get('dps', 0) > 0:
                if len(entity_unit.get('speeds', {})) > 0:
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

        enemy_whitelist_ids = {e.Id for e in enemy_units}
        attack_unist_ids = {e.Id for e in attack_unist}
        for unit in attack_unist:
            group_radius = 200
            if len(self.nearby_units(unit, enemy_whitelist_ids, 500)) > 0:
                group_radius = 75

            if self.group_size(unit, attack_unist_ids, group_radius) >= 15:
                self.attack_nearest_enemies(unit, enemy_units)
            elif len(self.nearby_units(unit, enemy_whitelist_ids, 300)) > 0:
                self.attack_nearest_enemies(unit, enemy_units)
            else:
                self.regroup(unit, attack_unist, group_radius)

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

    def group_size(self, unit: uw.Entity, whitelist: set[int], radius: float = 75) -> int:
        if len(whitelist) == 0:
            return 0

        return len(self.nearby_units(unit, whitelist, radius))

    def nearby_units(self, unit: uw.Entity, whitelist: set[int], radius: float = 75) -> list[uw.Entity]:
        if len(whitelist) == 0:
            return []

        area = self.game.map.area_extended(unit.Position.position, radius)
        result = []
        for position in area:
            for id in self.game.map.entities(position):
                if id in whitelist:
                    result.append(self.game.world.entity(id))

        return result

    def regroup(self, unit: uw.Entity, friendly_units: list[uw.Entity], radius: float = 75):
        target_id = self.entity_manager.main_building.Id

        friendly_ids = {e.Id for e in friendly_units}
        if len(friendly_units) > 0:
            ignore = {e.Id for e in self.nearby_units(unit, friendly_ids, radius)}
            targets = [e for e in sorted(
                friendly_units,
                key=lambda x: self.game.map.distance_estimate(
                    unit.Position.position, x.Position.position
                ),
            ) if e.Id not in ignore]

            if len(targets) > 0:
                target_id = targets[0].Id

        self.game.commands.order(unit.Id, self.game.commands.run_to_entity(target_id))


    def attack_nearest_enemies(self, unit: uw.Entity, enemy_units: list[uw.Entity]):
        if len(enemy_units) == 0:
            return

        _id = unit.Id
        pos = unit.Position.position

        moving_units: list[uw.Entity] = []

        for enemy in enemy_units:
            enemy_unit = self.game.prototypes.unit(enemy.Proto.proto)
            if enemy_unit is not None and len(enemy_unit.get('speeds', {})) > 0:
                moving_units.append(enemy)

        target_units = [e for e in moving_units if self.game.map.distance_estimate(
            unit.Position.position,
            e.Position.position,
        ) < 200]

        if len(target_units) == 0:
            target_units = enemy_units

        enemy = sorted(
            target_units,
            key=lambda x: self.game.map.distance_estimate(
                pos, x.Position.position
            ),
        )[0]

        # nearest_dist = self.game.map.distance_estimate(
        #     pos, enemy.Position.position
        # )

        # orders = self.game.commands.orders(_id)
        # order_dist = 0
        # for order in orders:
        #     if order.order_type == uw.OrderType.Fight and order.entity != uw.Commands.invalid:
        #         order_dist = self.game.map.distance_estimate(
        #             self.game.world.entity(order.entity).Position.position, enemy.Position.position
        #         )
        #         break

        # if nearest_dist < 200 or order_dist < 100:
        self.game.commands.order(
            _id, self.game.commands.fight_to_entity(enemy.Id)
        )
