import uw
from .ProtoId import ConstructionUnit, Units, Recipes

def command_units(
        game: uw.Game,
        units_map: Units,
        construction_units_map: ConstructionUnit,
        recipes_map: Recipes,
    ):
    for entity in game.world.entities().values():
        if not (entity.own() and entity.has('Proto')):
            continue

        ownEntity: uw.Entity = entity
        proto_id = int(ownEntity.Proto.proto)

        proto_type = game.prototypes.type(proto_id)

        if not proto_type == uw.Prototype.Unit:
            continue

        if ownEntity.Proto.proto == construction_units_map.factory:
            game.commands.command_set_recipe(ownEntity.Id, recipes_map.kitsune)
        
        if ownEntity.Proto.proto == units_map.kitsune:
            ...