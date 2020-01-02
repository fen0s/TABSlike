# import module
from . import Unit
# import class from module
from .Unit import Unit
from colorama import Fore
import time
import copy
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