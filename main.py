import os
import random
import uw
from modules import EntityManager, Constructions, Recipes, BuildOrder, ConstructionUnit, Units, UnitComands


class Bot:
    def __init__(self):
        self.game = uw.Game()
        self.step = 0

        # register update callback
        self.game.add_connection_state_callback(self.connection_state_callback_closure())
        self.game.add_game_state_callback(self.game_state_callback_closure())
        self.game.add_map_state_callback(self.map_state_callback_closure())
        self.game.add_update_callback(self.update_callback_closure())
        self.game.add_shooting_callback(self.shooting_callback_closure())
        self.entityManager = EntityManager(self.game, self)
        self.constructions = Constructions()
        self.recipes = Recipes()
        self.units = Units()
        self.construction_units = ConstructionUnit()

        self.command_center = UnitComands(self.game, self.entityManager)

        self.build_order = []
        self.previous_orders = {}

    def start(self):
        self.game.log_info("starting")
        self.game.set_player_name("unicron")
        self.game.set_player_color(0.95, 0.375, 0.75)
        if not self.game.try_reconnect():
            self.game.set_start_gui(True)
            lobby = os.environ.get("UNNATURAL_CONNECT_LOBBY", "")
            addr = os.environ.get("UNNATURAL_CONNECT_ADDR", "")
            port = os.environ.get("UNNATURAL_CONNECT_PORT", "")
            if lobby != "":
                self.game.connect_lobby_id(lobby)
            elif addr != "" and port != "":
                self.game.connect_direct(addr, int(port))
            else:
                self.game.connect_new_server()
        self.game.log_info("done")



    def assign_random_recipes(self):
        for e in self.game.world.entities().values():
            if not (e.own() and hasattr(e, "Unit")):
                continue
            recipes = self.game.prototypes.unit(e.Proto.proto)
            if not recipes:
                continue
            recipes = recipes["recipes"]
            if len(recipes) > 0:
                self.game.commands.command_set_recipe(e.Id, random.choice(recipes))

    def connection_state_callback_closure(self):
        def connection_state_callback(state: uw.ConnectionState):
            ...

        return connection_state_callback

    def game_state_callback_closure(self):
        def game_state_callback(state: uw.GameState):
            ...

        return game_state_callback

    def map_state_callback_closure(self):
        def map_state_callback(state: uw.MapState):
            ...

        return map_state_callback
    
    def basic_build_order(self):
        return [
            [
                BuildOrder(self.constructions.drill, lambda: self.entityManager.deposits['metal'][0].Position.position,
                            id=10,
                            deps=[
                                BuildOrder(self.constructions.concrete_plant, lambda: self.game.map.find_construction_placement(
                                    self.constructions.concrete_plant,
                                    self.previous_orders[10].position,
                                )),
                            ]),

                BuildOrder(self.constructions.drill, lambda: self.entityManager.deposits['metal'][1].Position.position,
                            id=11,
                            deps=[
                                BuildOrder(self.constructions.forgepress, lambda: self.game.map.find_construction_placement(
                                    self.constructions.forgepress,
                                    self.previous_orders[11].position,
                                ), deps=[
                                    BuildOrder(self.constructions.vehicle_assembler, lambda: self.game.map.find_construction_placement(
                                        self.constructions.vehicle_assembler,
                                        self.previous_orders[11].position,
                                    ))
                                ]),
                            ]),

                BuildOrder(self.constructions.drill, lambda: self.entityManager.deposits['metal'][2].Position.position,
                            id=12,
                            deps=[
                                BuildOrder(self.constructions.arsenal, lambda: self.game.map.find_construction_placement(
                                    self.constructions.arsenal,
                                    self.previous_orders[12].position,
                                )),
                            ]),
            ],
        ]

    def expansion_build_order(self):
        return [
                    [
                        BuildOrder(self.constructions.drill, lambda: self.entityManager.deposits['metal'][0].Position.position,
                                   id=10,
                                   deps=[
                                        BuildOrder(self.constructions.concrete_plant, lambda: self.game.map.find_construction_placement(
                                            self.constructions.concrete_plant,
                                            self.previous_orders[10].position,
                                        )),
                                   ]),

                        BuildOrder(self.constructions.drill, lambda: self.entityManager.deposits['metal'][1].Position.position,
                                   id=11,
                                   deps=[
                                        BuildOrder(self.constructions.forgepress, lambda: self.game.map.find_construction_placement(
                                            self.constructions.forgepress,
                                            self.previous_orders[11].position,
                                        ), deps=[
                                            BuildOrder(self.constructions.vehicle_assembler, lambda: self.game.map.find_construction_placement(
                                                self.constructions.vehicle_assembler,
                                                self.previous_orders[11].position,
                                            )),
                                            BuildOrder(self.constructions.drill, lambda: self.entityManager.deposits['metal'][3].Position.position,
                                                id=31,
                                                deps=[
                                                    BuildOrder(self.constructions.concrete_plant, lambda: self.game.map.find_construction_placement(
                                                        self.constructions.concrete_plant,
                                                        self.previous_orders[31].position,
                                                    ),
                                                    deps=[
                                                        BuildOrder(self.constructions.drill, lambda: self.entityManager.deposits['metal'][4].Position.position,
                                                            id=41,
                                                            deps=[
                                                                BuildOrder(self.constructions.forgepress, lambda: self.game.map.find_construction_placement(
                                                                    self.constructions.forgepress,
                                                                    self.previous_orders[41].position,
                                                                )),
                                                            ]
                                                        ),
                                                        BuildOrder(self.constructions.drill, lambda: self.entityManager.deposits['metal'][5].Position.position,
                                                            id=42,
                                                            deps=[
                                                                BuildOrder(self.constructions.arsenal, lambda: self.game.map.find_construction_placement(
                                                                    self.constructions.arsenal,
                                                                    self.previous_orders[42].position,
                                                                ), id=51, deps=[
                                                                    BuildOrder(self.constructions.vehicle_assembler, lambda: self.game.map.find_construction_placement(
                                                                        self.constructions.vehicle_assembler,
                                                                        self.previous_orders[51].position,
                                                                    )),
                                                                ]),
                                                                
                                                            ]
                                                        ),
                                                    ]),
                                                ]
                                            ),
                                        ]),
                                   ]),

                        BuildOrder(self.constructions.drill, lambda: self.entityManager.deposits['metal'][2].Position.position,
                                   id=12,
                                   deps=[
                                        BuildOrder(self.constructions.arsenal, lambda: self.game.map.find_construction_placement(
                                            self.constructions.arsenal,
                                            self.previous_orders[12].position,
                                        )),
                                   ]),
                    ],
                ]

    def update_callback_closure(self):
        def update_callback(stepping):
            if not stepping:
                return
            self.step += 1  # save some cpu cycles by splitting work over multiple steps

            # Prepare prototype dict
            if not self.constructions.is_initialized():
                proto_dict = {}
                unit_dict = {}
                for protoId in self.game.prototypes.all():
                    protoType = self.game.prototypes.type(protoId)
                    if protoType == uw.Prototype.Construction:
                        protoName = self.game.prototypes.name(protoId).replace(' ', '_')
                        proto_dict[protoName] = protoId
                    elif protoType == uw.Prototype.Recipe:
                        protoName = self.game.prototypes.name(protoId).replace(' ', '_')
                        proto_dict[protoName] = protoId
                    elif protoType == uw.Prototype.Unit:
                        protoName = self.game.prototypes.name(protoId).replace(' ', '_')
                        unit_dict[protoName] = protoId

                self.constructions.init(proto_dict)
                self.recipes.init(proto_dict)
                self.units.init(unit_dict)
                self.construction_units.init(unit_dict)

            if not self.entityManager.loaded:
                self.entityManager.processEntities()
                # Kitsune rush
                # Pridanim dalsich tovaren muzem mit produkci az dvojnasobnou. tzn v dobe kdy mel darik 1x juggernauta, my uz mohli mit cca 35 kitsune
                # self.build_order = [
                #     [
                #         BuildOrder(self.constructions.drill, lambda: self.entityManager.deposits['metal'][0].Position.position,
                #                    id=10,
                #                    deps=[
                #                         BuildOrder(self.constructions.concrete_plant, lambda: self.game.map.find_construction_placement(
                #                             self.constructions.concrete_plant,
                #                             self.previous_orders[10].position,
                #                         ), deps=[
                #                             BuildOrder(self.constructions.factory, lambda: self.game.map.find_construction_placement(
                #                                 self.constructions.factory,
                #                                 self.previous_orders[10].position,
                #                             )),
                #                         ]),
                #                    ]),

                #         BuildOrder(self.constructions.drill, lambda: self.entityManager.deposits['metal'][1].Position.position,
                #                    id=11,
                #                    deps=[
                #                         BuildOrder(self.constructions.factory, lambda: self.game.map.find_construction_placement(
                #                             self.constructions.factory,
                #                             self.previous_orders[11].position,
                #                         )),
                #                    ]),

                #         BuildOrder(self.constructions.drill, lambda: self.entityManager.deposits['metal'][2].Position.position,
                #                    id=12,
                #                    deps=[
                #                         BuildOrder(self.constructions.factory, lambda: self.game.map.find_construction_placement(
                #                             self.constructions.factory,
                #                             self.previous_orders[12].position,
                #                         )),
                #                    ]),
                #     ],
                # ]

                # Twinfire rush
                # potencial in 2:22 - 4 twinfires. Darik ma prvniho juggernauta az 3:45 - moznost rushe
                # Ted je nastaveno na 4 jednotky
                # TODO build order spíš nahradit něčím chytřejším, co se bude dívat, kde co má postavené, aby líp fungoval reconnect
                # self.build_order = self.expansion_build_order()
                self.build_order =  [
                    [
                        BuildOrder(self.constructions.vehicle_assembler, lambda:  self.game.map.find_construction_placement(
                                    self.constructions.vehicle_assembler,
                                    self.entityManager.deposits['metal'][0].Position.position,
                        )),
                    ]
                ]
            # elif self.step % 40:
                # self.entityManager.update_entities()

            # COMMAND CENTER
            if not self.command_center.is_initialized():
                self.command_center.init(
                    self.units,
                    self.construction_units,
                    self.recipes,
                )

            build_order_len = len(self.build_order)
            if build_order_len > 0:
                done = []
                add = []

                for i, order in enumerate(self.build_order[0]):
                    if order.is_built(self.game):
                        done.append(i)
                        if len(order.deps) > 0:
                            add.extend(order.deps)
                    else:
                        order.build(self.game)
                        self.previous_orders[order.id] = order

                for i in reversed(done):
                    self.build_order[0].pop(i)
                self.build_order[0].extend(add)

                if len(self.build_order[0]) == 0:
                    self.build_order = self.build_order[1:]

            if self.step % 50 == 1:
                self.command_center.twinfire_strategy(build_order_len == 0)

            # if self.step % 10 == 5:
            #     self.assign_random_recipes()

        return update_callback

    def shooting_callback_closure(self):
        def shooting_callback(state: list[uw.ShootingData]):
            ...

        return shooting_callback


if __name__ == "__main__":
    bot = Bot()
    bot.start()
