from uw import Entity, Game, Prototype

def addToList(obj: dict[str, list[Entity]], key, value):
    if key in obj:
        obj[key].append(value)
    else:
        obj[key] = [value]

DEPOSIT_TYPES = [
    'metal',
    'aether',
    'oil',
    'crystals',
]

class EntityManager:
    def __init__(self, game: Game, bot) -> None:
        self.game = game
        self.bot = bot

        self.recipes: dict[str, list[Entity]] = {}
        self.deposits: dict[str, list[Entity]] = {
            'metal': [],
            'aether': [],
            'oil': [],
            'crystals': [],
        }
        self.constructions: dict[str, list[Entity]] = {}
        self.main_building: Entity = None

        self.BUILDING_PROTO_IDS = []

        # Changing entities
        self.resources: dict[str, list[Entity]] = {}
        self.units: dict[str, list[Entity]] = {}
        self.enemy_mains: list[Entity] = []
        self.own_buildings: list[Entity] = []
        self.own_constructions: list[Entity] = []

        self.loaded = False

    def processEntities(self):
        self.BUILDING_PROTO_IDS = [
            self.bot.construction_units.experimental_assembler,
            self.bot.construction_units.brick,
            self.bot.construction_units.drill,
            self.bot.construction_units.talos,
            self.bot.construction_units.forgepress,
            self.bot.construction_units.pump,
            self.bot.construction_units.laboratory,
            self.bot.construction_units.vehicle_assembler,
            self.bot.construction_units.generator,
            self.bot.construction_units.factory,
            self.bot.construction_units.blender,
            self.bot.construction_units.heimdall,
            self.bot.construction_units.arsenal,
            self.bot.construction_units.smelter,
            self.bot.construction_units.bot_assembler,
            self.bot.construction_units.concrete_plant,
            self.bot.construction_units.thor,
        ]

        for entity in self.game.world.entities().values():
            if not entity.has('Proto'):
                continue

            prototype_id = int(entity.Proto.proto)
            proto = self.game.prototypes.type(prototype_id)
            protoName = self.game.prototypes.name(prototype_id)

            if proto == Prototype.Resource:
                addToList(self.resources, protoName, entity)
            elif proto == Prototype.Recipe:
                addToList(self.recipes, protoName, entity)
            elif proto == Prototype.Unit:
                addToList(self.units, protoName, entity)
                if 'nucleus' in protoName:
                    if entity.own():
                        self.main_building = entity
                    else:
                        self.enemy_mains.append(entity)
                if 'deposit' in protoName:
                    addToList(self.deposits, protoName.replace(' deposit', ''), entity)
            elif proto == Prototype.Construction:
                if entity.own():
                    self.own_constructions.append(entity)
                addToList(self.constructions, protoName, entity)

        # sort deposits by distance
        for depositType in DEPOSIT_TYPES:
            self.deposits[depositType] = sorted(self.deposits[depositType], key=lambda x: self.game.map.distance_estimate(
                self.main_building.Position.position, x.Position.position
            ))

        self.loaded = True

    def update_entities(self):
        self.constructions = []
        self.enemy_mains = []
        self.resources = {}
        self.units = {}
        self.own_buildings = []
        self.own_constructions = []

        for entity in self.game.world.entities().values():
            if not entity.has('Proto'):
                continue

            prototype_id = int(entity.Proto.proto)
            proto_type = self.game.prototypes.type(prototype_id)
            protoName = self.game.prototypes.name(prototype_id)

            if proto_type == Prototype.Resource:
                addToList(self.resources, protoName, entity)
            elif proto_type == Prototype.Unit:
                addToList(self.units, protoName, entity)

                if entity.own():
                    if prototype_id in self.BUILDING_PROTO_IDS:
                        self.own_buildings.append(entity)

                else:
                    # ENEMY
                    if 'nucleus' in protoName:
                        self.enemy_mains.append(entity)
            elif proto_type == Prototype.Construction:
                if entity.own():
                    self.own_constructions.append(entity)