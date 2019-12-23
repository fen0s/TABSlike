from colorama import Fore
import time
import copy


class Unit:
    
    def __init__(self, name, hp, damage, team, y, x, map_engine, cost):
        self.name = name
        self.hp = hp
        self.y = y
        self.x = x
        self.damage = damage
        self.map_eng = map_engine
        self.team = team
        self.cost = cost
        self.symbol = {'blue': Fore.LIGHTCYAN_EX + "{}".format(name[0].upper()) + Fore.RESET,
                       'red': Fore.LIGHTRED_EX + '{}'.format(name[0].upper()) + Fore.RESET}.get(self.team.lower())
        team_dict = {'blue': map_engine.alive_list[1],
                     'red': map_engine.alive_list[0]}
        self.team_dict = team_dict
        self.side = {'blue': 'left',
                     'red': 'right'}.get(team.lower())
        team_dict.get(self.team.lower()).append(self)
        map_engine.place_both(y, x, self, self.symbol)

    def check_inbounds(self, y, x):
        if y > self.map_eng.size_y - 1 or y < 0 or x > self.map_eng.size_x - 1 or x < 0:
            return False
        else:
            return True

    def move(self, side):
        if self.check_attackable():
            return
        sides = {'right': [0, 1],
                 'left': [0, -1],
                 'up': [-1, 0],
                 'down': [1, 0]}
        move_side = sides.get(side)
        if self.check_inbounds(self.y + move_side[0], self.x + move_side[1]) \
                and not self.map_eng.check_entity(self.y + move_side[0], self.x + move_side[1]):

            self.map_eng.make_empty(self.y, self.x)
            self.y += move_side[0]
            self.x += move_side[1]
            self.map_eng.place_both(self.y, self.x, tech_place=self, game_place=self.symbol)

# **** Attack an entity. Entity must be Unit class, don't forget it! ****
    def attack(self, entity):
        entity.hp -= self.damage
        entity_tile = copy.deepcopy(self.map_eng.gamemap)
        entity_tile[entity.y][entity.x] = Fore.LIGHTMAGENTA_EX + '/' + Fore.RESET
        print('\n' * 18)
        for y in entity_tile:
            print('  '.join(y))
        print('{} attacks {}! Damage: {},  HP of {} left: {}!'.format(
            self.name, entity.name, self.damage, entity.name, entity.hp))
        time.sleep(1)
        if entity.hp <= 0:
            entity.die()

# **** Deletes unit. On both map and whole program. ****
    def die(self):
        print('Oh no! {} dies!'.format(self.name))
        time.sleep(0.5)
        self.map_eng.make_empty(self.y, self.x)
        self.team_dict.get(self.team.lower()).remove(self)

# **** Check X and Y coordinates for presence of unit with another team. ****
    def check_enemies(self):
        for y in self.map_eng.techmap:
            for x in y:
                if hasattr(x, 'team') and x.team != self.team:
                    coords = [x.y, x.x]
                    self.move_on_enemy(coords[0], coords[1])
                    return

    def check_attackable(self):
        coord_list = [[self.y, self.x+1 if self.check_inbounds(self.y, self.x+1) else self.x],
                      [self.y, self.x-1 if self.check_inbounds(self.y, self.x-1) else self.x],
                      [self.y+1 if self.check_inbounds(self.y+1, self.x) else self.y, self.x],
                      [self.y-1 if self.check_inbounds(self.y-1, self.x) else self.y, self.x]]
        for coord in coord_list:
            if hasattr(self.map_eng.techmap[coord[0]][coord[1]], 'team') \
                    and self.map_eng.techmap[coord[0]][coord[1]].team != self.team:

                self.attack(self.map_eng.techmap[coord[0]][coord[1]])
                return True

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


class RangedUnit(Unit):
    def __init__(self, name, hp, damage, team, y, x, map_engine, cost, reload_time):
        Unit.__init__(self, name, hp, damage, team, y, x, map_engine, cost)
        self.reload_time = reload_time
        self.reload = reload_time

    def check_enemies(self):
        coord_list = [self.map_eng.techmap[self.y],
                      self.map_eng.techmap[self.y+1] if self.check_inbounds(self.y+1, self.x) else [],
                      self.map_eng.techmap[self.y-1] if self.check_inbounds(self.y-1, self.x) else []]
        if self.reload < self.reload_time:
            self.reload += 1
            print(self.name + ' reloading....')
            time.sleep(0.5)
            return
        for y in coord_list:
            for x in y:
                if hasattr(x, 'team') and x.team != self.team and self.reload == self.reload_time:
                    self.attack(x)
                    self.reload = 0
                    return
        for y in self.map_eng.techmap:
            for x in y:
                if hasattr(x, 'team') and x.team != self.team:
                    self.move_on_enemy(x.y, x.x)
                    return

    def attack(self, entity):
        entity.hp -= self.damage
        Bullet(enemy_y=entity.y, enemy_x=entity.x, y=self.y, x=self.x, engine=self.map_eng)
        print('{} shoots {}! Damage: {},  HP of {} left: {}!'.format(
            self.name, entity.name, self.damage, entity.name, entity.hp))
        time.sleep(1)
        if entity.hp <= 0:
            entity.die()


class Bullet:
    def __init__(self, enemy_y, enemy_x, engine, y, x):
        self.enemy_y = enemy_y
        self.enemy_x = enemy_x
        self.map = copy.deepcopy(engine.gamemap)
        self.y = y
        self.x = x
        self.previous_position = copy.deepcopy(self.map[self.y][self.x])
        self.shoot()

    def shoot(self):
        while not self.check_attackable():
            self.move_on_enemy(self.enemy_y, self.enemy_x)
            print('\n' * 20)
            for y in self.map:
                print('  '.join(y))
            time.sleep(0.105)

    def check_attackable(self):
        if self.y == self.enemy_y and self.x == self.enemy_x:
            return True
        return False

    def move_on_enemy(self, enemy_y, enemy_x):
        if enemy_y < self.y:
            self.move('up')
        if enemy_y > self.y:
            self.move('down')
        if enemy_x < self.x:
            self.move('left')
        if enemy_x > self.x:
            self.move('right')

    def move(self, side):
        if self.check_attackable():
            return
        sides = {'right': [0, 1],
                 'left': [0, -1],
                 'up': [-1, 0],
                 'down': [1, 0]}
        move_side = sides.get(side)
        self.map[self.y][self.x] = self.previous_position
        self.y += move_side[0]
        self.x += move_side[1]
        self.previous_position = copy.deepcopy(self.map[self.y][self.x])
        self.map[self.y][self.x] = Fore.LIGHTYELLOW_EX + '*' + Fore.RESET


class ExplosiveUnit(RangedUnit):

    def attack(self, entity):
        coords_list = [[entity.y, entity.x],
                       [entity.y+1, entity.x],
                       [entity.y+1, entity.x+1],
                       [entity.y+1, entity.x-1],
                       [entity.y, entity.x+1],
                       [entity.y, entity.x-1],
                       [entity.y-1, entity.x],
                       [entity.y-1, entity.x-1],
                       [entity.y-1, entity.x+1]]
        close_quarters = [[self.x+1, self.y],
                          [self.x-1, self.y],
                          [self.x, self.y+1],
                          [self.x, self.y-1]]
        for coord in close_quarters:
            try:
                if hasattr(self.map_eng.techmap[coord[1]][coord[0]], 'team') and \
                  self.map_eng.techmap[coord[1]][coord[0]].team != self.team:

                    self.map_eng.techmap[coord[1]][coord[0]].hp -= 2
                    self.map_eng.display()
                    print(self.name + ' attacks ' + self.map_eng.techmap[coord[1]][coord[0]].name + '!' + ' Damage: 2')
                    time.sleep(1)
                    return
            except IndexError:
                continue
        map_copy = copy.deepcopy(self.map_eng.gamemap)
        for coord in coords_list:
            try:
                if self.check_inbounds(coord[0], coord[1]):
                    map_copy[coord[0]][coord[1]] = Fore.LIGHTYELLOW_EX + '*' + Fore.RESET
            except IndexError:
                continue
        print('\n' * 18)
        for y in map_copy:
            print('  '.join(y))
        for coord in coords_list:
            try:
                position = self.map_eng.techmap[coord[0]][coord[1]]
                if hasattr(position, 'hp') and self.check_inbounds(coord[0], coord[1]):
                    position.hp -= self.damage
                    print('{} explodes {}! Damage: {},  HP of {} left: {}!'.format(
                        self.name,
                        position.name,
                        self.damage,
                        position.name,
                        position.hp))

                    time.sleep(1)

                    if position.hp <= 0:
                        position.die()

            except IndexError:
                continue

        time.sleep(1)
