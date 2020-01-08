from pynput import keyboard
from colorama import Fore
import copy
import time


class Marker:
    def __init__(self, y, x, engine, inbound_x, team, budget):
        self.inbound_x = inbound_x
        self.y = y
        self.x = x
        self.engine = engine
        self.previous_position = self.engine.gamemap[y][x]
        self.engine.gamemap[y][x] = Fore.LIGHTYELLOW_EX + 'X' + Fore.RESET
        self.disabled = True
        self.unit = "Warrior"
        self.budget = budget
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.team = team
        self.sides = {'right': [0, 1],
                      'left': [0, -1],
                      'up': [-1, 0],
                      'down': [1, 0]}
        self.listener.start()

    def move(self, side):
        move_side = self.sides.get(side)
        if self.engine.check_inbounds(self.y + move_side[0], self.x + move_side[1]):
            self.engine.gamemap[self.y][self.x] = self.previous_position
            self.y += move_side[0]
            self.x += move_side[1]
            self.previous_position = copy.deepcopy(self.engine.gamemap[self.y][self.x])
            self.engine.gamemap[self.y][self.x] = Fore.LIGHTYELLOW_EX + 'X' + Fore.RESET
            self.engine.flush()
            for x in self.engine.gamemap:
                print('  '.join(x))
            try:
                print("To place an unit, press ENTER. To stop placement, press ESC. Budget: {}".format(round(self.budget)))
            except OverflowError:
                print("To place an unit, press ENTER. To stop placement, press ESC.")

    def on_press(self, key):
        keys_list = {keyboard.Key.up: 'up',
                     keyboard.Key.down: 'down',
                     keyboard.Key.left: 'left',
                     keyboard.Key.right: 'right'}
        if key in keys_list.keys() and not self.disabled:
            self.move(keys_list.get(key))

    def on_release(self, key):
        if self.disabled:
            return
        if key == keyboard.Key.esc:
            time.sleep(0.1)
            self.disable()
            time.sleep(0.1)
        elif key == keyboard.Key.enter:
            if not self.engine.check_entity(self.y, self.x):
                unit = self.engine.spawn_unit(y=self.y, x=self.x, team=self.team, unit=self.unit)
                if unit.cost > self.budget:
                    self.remove_unit(unit)
                    print(Fore.RED + "Unit too expensive!" + Fore.RESET)
                    return
                self.budget -= unit.cost
                try:
                    print("Unit {} placed! Budget left: {}".format(unit.name, round(self.budget)))
                except OverflowError:
                    print("Unit {} placed!".format(unit.name))
                self.previous_position = copy.deepcopy(self.engine.gamemap[self.y][self.x])
                return
            else:
                print(Fore.RED + "Unit already exists here!" + Fore.RESET)

    def remove_unit(self, unit):
        self.engine.gamemap[self.y][self.x] = Fore.LIGHTYELLOW_EX + 'X' + Fore.RESET
        self.engine.techmap[self.y][self.x] = None
        unit.team_dict.get(unit.team.lower()).remove(unit)

    def die(self):
        self.engine.gamemap[self.y][self.x] = self.previous_position
        self.listener.stop()

    def disable(self):
        self.disabled = True

    def enable(self):
        self.disabled = False
