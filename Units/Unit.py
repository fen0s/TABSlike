from colorama import Fore
import time
import copy
import itertools

class Unit:
    
    def __init__(self, name, hp, damage, team, y, x, map_engine, cost):
        self.name = name
        self.hp = hp
        self.y = y
        self.x = x
        self.damage = damage
        self.engine = map_engine
        self.team = team
        self.cost = cost
        self.symbol = {'blue': Fore.LIGHTCYAN_EX + "{}".format(name[0].upper()) + Fore.RESET,
                       'red': Fore.LIGHTRED_EX + '{}'.format(name[0].upper()) + Fore.RESET}.get(self.team.lower())
        self.team_dict = {'blue': map_engine.alive_list[1],
                          'red': map_engine.alive_list[0]}
        self.team_dict.get(self.team.lower()).append(self)
        map_engine.place_both(y, x, self, self.symbol)

    def move(self, side):
        if self.check_attackable():
            return
        sides = {'right': [0, 1],
                 'left': [0, -1],
                 'up': [-1, 0],
                 'down': [1, 0]}
        move_side = sides.get(side)
        if self.engine.check_inbounds(self.y + move_side[0], self.x + move_side[1]) \
                and not self.engine.check_entity(self.y + move_side[0], self.x + move_side[1]):

            self.engine.make_empty(self.y, self.x)
            self.y += move_side[0]
            self.x += move_side[1]
            self.engine.place_both(self.y, self.x, tech_place=self, game_place=self.symbol)

# **** Attack an entity. Entity must be Unit class, don't forget it! ****
    def attack(self, entity):
        entity.hp -= self.damage
        entity_copy = copy.deepcopy(self.engine.gamemap[entity.y][entity.x])
        self.engine.gamemap[entity.y][entity.x] = Fore.LIGHTMAGENTA_EX + '/' + Fore.RESET
        self.engine.display()
        print('{} attacks {}! Damage: {},  HP of {} left: {}!'.format(
            self.name, entity.name, self.damage, entity.name, entity.hp))
        time.sleep(0.5)
        self.engine.gamemap[entity.y][entity.x] = entity_copy
        if entity.hp <= 0:
            entity.die()

    def die(self):
        print('Oh no! {} dies!'.format(self.name))
        time.sleep(0.5)
        self.engine.make_empty(self.y, self.x)
        self.team_dict.get(self.team.lower()).remove(self)

# **** Check X and Y coordinates for presence of unit with another team. ****
    def check_enemies(self):
        for row in self.engine.techmap:
            for elem in row:
                if elem and elem.team != self.team:
                    coords = [elem.y, elem.x]
                    self.move_on_enemy(coords[0], coords[1])
                    return

    def check_attackable(self):
        coord_list = list(itertools.product([self.y - 1, self.y, self.y + 1], [self.x - 1, self.x, self.x + 1]))
        for coord in coord_list:
            try:
                if self.engine.techmap[coord[0]][coord[1]] and self.engine.techmap[coord[0]][coord[1]].team != self.team:
                    self.attack(self.engine.techmap[coord[0]][coord[1]])
                    return True
            except IndexError:
                continue
        return False

# **** Move to enemy unit. ****
    def move_on_enemy(self, enemy_y, enemy_x):
        if enemy_y < self.y:
            self.move('up')
        if enemy_y > self.y:
            self.move('down')
        if enemy_x < self.x:
            self.move('left')
        if enemy_x > self.x:
            self.move('right')
