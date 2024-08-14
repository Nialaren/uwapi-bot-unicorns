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

    def __init__(self, game: Game) -> None:
        self.resources: dict[str, list[Entity]] = {}
        self.recipes: dict[str, list[Entity]] = {}
        self.units: dict[str, list[Entity]] = {}
        self.deposits: dict[str, list[Entity]] = {
            'metal': [],
            'aether': [],
            'oil': [],
            'crystals': [],
        }
        self.constructions: dict[str, list[Entity]] = {}
        self.main_building: Entity = None
        self.enemy_mains: list[Entity] = []
        self.game = game
        self.loaded = False

    def processEntities(self):
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
                addToList(self.constructions, protoName, entity)

        # sort deposits by distance
        for depositType in DEPOSIT_TYPES:
            self.deposits[depositType] = sorted(self.deposits[depositType], key=lambda x: self.game.map.distance_estimate(
                self.main_building.Position.position, x.Position.position
            ))

        self.loaded = True
