class Constructions:
    def __init__(self):
        self._protoDict: dict[str, int] = {}
        self.initialized = False
    
    def init(self, data: dict[str, int]):
        self._protoDict = data
        self.initialized = True

    def experimental_assembler(self):
        return self._protoDict['experimental_assembler']
    def brick(self):
        return self._protoDict['brick']
    def drill(self):
        return self._protoDict['drill']
    def talos(self):
        return self._protoDict['talos']
    def forgepress(self):
        return self._protoDict['forgepress']
    def pump(self):
        return self._protoDict['pump']
    def laboratory(self):
        return self._protoDict['laboratory']
    def vehicle_assembler(self):
        return self._protoDict['vehicle_assembler']
    def generator(self):
        return self._protoDict['generator']
    def factory(self):
        return self._protoDict['factory']
    def blender(self):
        return self._protoDict['blender']
    def heimdall(self):
        return self._protoDict['heimdall']
    def arsenal(self):
        return self._protoDict['arsenal']
    def smelter(self):
        return self._protoDict['smelter']
    def bot_assembler(self):
        return self._protoDict['bot_assembler']
    def concrete_plant(self):
        return self._protoDict['concrete_plant']
    def thor(self):
        return self._protoDict['thor']
    
    def is_initialized(self):
        return self.initialized

class Recipes:
    def __init__(self):
        self._protoDict: dict[str, int] = {}
        self.initialized = False
    
    def init(self, data: dict[str, int]):
        self._protoDict = data
        self.initialized = True

    def plasma_emitter(self):
        return self._protoDict['plasma_emitter']
    def mermaid(self):
        return self._protoDict['mermaid']
    def eagle(self):
        return self._protoDict['eagle']
    def ATV(self):
        return self._protoDict['ATV']
    def rail_gun(self):
        return self._protoDict['rail_gun']
    def aether(self):
        return self._protoDict['aether']
    def lurker(self):
        return self._protoDict['lurker']
    def armor_plates(self):
        return self._protoDict['armor_plates']
    def oil(self):
        return self._protoDict['oil']
    def kitsune(self):
        return self._protoDict['kitsune']
    def twinfire(self):
        return self._protoDict['twinfire']
    def atomic_forge(self):
        return self._protoDict['atomic_forge']
    def power_cell(self):
        return self._protoDict['power_cell']
    def reinforced_plates(self):
        return self._protoDict['reinforced_plates']
    def golem(self):
        return self._protoDict['golem']
    def paladin(self):
        return self._protoDict['paladin']
    def reinforced_concrete(self):
        return self._protoDict['reinforced_concrete']
    def alloys(self):
        return self._protoDict['alloys']
    def juggernaut(self):
        return self._protoDict['juggernaut']
    def quantum_ray(self):
        return self._protoDict['quantum_ray']
    def cyclops(self):
        return self._protoDict['cyclops']
    def shield_projector(self):
        return self._protoDict['shield_projector']
    def crystals(self):
        return self._protoDict['crystals']
    def arsenal(self):
        return self._protoDict['arsenal']
    def blaster(self):
        return self._protoDict['blaster']
    def colossus(self):
        return self._protoDict['colossus']
    def quark_foam(self):
        return self._protoDict['quark_foam']
    def metal(self):
        return self._protoDict['metal']
    
    def is_initialized(self):
        return self.initialized