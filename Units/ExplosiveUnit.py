from .RangedUnit import RangedUnit
from colorama import Fore
import time
import copy
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
        self.map_eng.flush()
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
