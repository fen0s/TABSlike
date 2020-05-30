from .RangedUnit import RangedUnit
from colorama import Fore
import time
import copy
import itertools


class ExplosiveUnit(RangedUnit):

    def attack(self, entity):
        if self.check_attackable():
            return
        coords_list = list(itertools.product([entity.y - 1, entity.y, entity.y + 1], [entity.x - 1, entity.x, entity.x + 1]))
        map_copy = copy.deepcopy(self.engine.gamemap)
        for coord in coords_list:
            try:
                if self.engine.check_inbounds(coord[0], coord[1]):
                    map_copy[coord[0]][coord[1]] = Fore.LIGHTYELLOW_EX + '*' + Fore.RESET
            except IndexError:
                continue
        self.engine.flush()
        for row in map_copy:
            print('  '.join(row))
        for coord in coords_list:
            try:
                position = self.engine.techmap[coord[0]][coord[1]]
                if position and self.engine.check_inbounds(coord[0], coord[1]):
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
