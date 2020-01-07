from Units.Unit import Unit
from Units.ExplosiveUnit import ExplosiveUnit
from Units.RangedUnit import RangedUnit
import random
from colorama import Fore
import time
from pynput import keyboard
import copy
import os

class GameMap:

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.gamemap = self.generate_map()
        self.techmap = self.generate_map()
        self.alive_list = [[], []]
        self.unitdict = {'Warrior': lambda y, x, team: Unit(name='Warrior' + '_' + team, hp=2, y=y, x=x,
                                 damage=2, map_engine=self, team=team, cost=200),
                         'Swordsman': lambda y, x, team: Unit(name='Swordsmen' + '_' + team, hp=4, y=y, x=x,
                                 damage=2, map_engine=self, team=team, cost=500),
                         'Bowman': lambda y, x, team: RangedUnit(name='Bowman' + '_' + team, hp=2, y=y, x=x,
                                 damage=1.5, map_engine=self, team=team, cost=400, reload_time=1),
                         'Musketeer': lambda y, x, team: RangedUnit(name='Musketeer' + '_' + team, hp=4, y=y, x=x,
                                 damage=3.5, map_engine=self, team=team, cost=850, reload_time=2),
                         'Grenadier': lambda y, x, team: ExplosiveUnit(name='Grenadier' + '_' + team, hp=2, y=y, x=x,
                                 damage=3, map_engine=self, team=team, cost=700, reload_time=3)}

    def flush(self):
        if os.system('cls') == 127:
            os.system('clear')

    def start_game(self):
        while self.alive_list[0] and self.alive_list[1]:
            for team in self.alive_list:
                for unit in team:
                    unit.check_enemies()
                self.display()
        self.end_game()

    def end_game(self):
        if self.alive_list[0] and not self.alive_list[1]:
            print("\n" + Fore.LIGHTRED_EX + 'Red' + Fore.LIGHTYELLOW_EX + ' team wins!')
        else:
            print("\n" + Fore.LIGHTCYAN_EX + 'Blue' + Fore.LIGHTYELLOW_EX + ' team wins!')
        input('Press ENTER to quit...')
        quit()

    def spawn_unit(self, unit, y, x, team):
        return self.unitdict.get(unit)(y=y, x=x, team=team)

    def generate_blue(self, budget):
        unit_names = list(self.unitdict.keys())
        while budget > 199:  # while budget < min_unit_price
            b_coords = [random.randint(round(self.size_y / 2), self.size_y - 1),
                        random.randint(round(self.size_x / 2), self.size_x - 1)]
            if not self.check_entity(b_coords[0], b_coords[1]):
                unit = self.spawn_unit(unit=random.choice(unit_names), y=b_coords[0], x=b_coords[1], team='Blue')
                if unit.cost > budget:
                    self.place_both(b_coords[0], b_coords[1], '.', '.')
                    self.alive_list[1].remove(unit)
                    continue
                budget -= unit.cost
            else:
                continue

    def generate_red(self, budget):
        unit_names = list(self.unitdict.keys())
        while budget > 199:
            r_coords = [random.randint(0, round(self.size_y / 2) - 1),
                        random.randint(0, round(self.size_x / 2) - 1)]
            if not self.check_entity(r_coords[0], r_coords[1]):
                unit = self.spawn_unit(unit=random.choice(unit_names), y=r_coords[0], x=r_coords[1], team='Red')
                if unit.cost > budget:
                    self.place_both(r_coords[0], r_coords[1], '.', '.')
                    self.alive_list[0].remove(unit)
                    continue
                budget -= unit.cost
            else:
                continue

    def generate_map(self):
        gamemap = []
        for _ in range(self.size_y):
            gamemap.append(['.' for _ in range(self.size_x)])
        return gamemap

    def display(self):
        """**** Display the map itself. ****"""
        self.flush()
        for x in self.gamemap:
            print('  '.join(x))
        time.sleep(1)

    def place(self, entity, y, x):
        """**** Place the symbol on frontend map. ****"""
        if -1 < x < self.size_x and -1 < y < self.size_y:
            self.gamemap[y][x] = entity
        else:
            print('Coordinates out of index.')

    def place_techmap(self, entity, y, x):
        """**** Place the unit on techmap. ****"""
        if -1 < x < self.size_x and -1 < y < self.size_y:
            self.techmap[y][x] = entity
        else:
            print('Coordinates out of index.')

    def make_empty(self, y, x):
        """**** Make the tile empty in both "dimensions" - techmap and frontmap. ****"""
        self.gamemap[y][x] = '.'
        self.techmap[y][x] = '.'

    def place_both(self, y, x, tech_place, game_place):
        self.place(game_place, y, x)
        self.place_techmap(tech_place, y, x)

# **** Check for presence of entity on tile in both gamemap and techmap.
    def check_entity(self, y, x):
        if self.techmap[y][x] == '.' and self.gamemap[y][x] == '.' or \
                self.gamemap[y][x] == Fore.LIGHTYELLOW_EX + 'X' + Fore.RESET and self.techmap[y][x] == '.':
            return False
        else:
            return True


class Menu:
    def __init__(self, engine):
        self.engine = engine
        self.menu()

    def choose_unit(self):
        user_unit = 'Warrior'
        while True:
            self.engine.flush()
            user_prompt = input(
                'This is choosing menu. Type "help" to see available units. '
                'To choose an unit, type its name here. To exit menu, type "exit": ')
            if user_prompt.lower() == 'exit':
                break
            if user_prompt.lower() == 'help':
                print("Available units:" + '\n' + '\n'.join(list(self.engine.unitdict.keys())))
                time.sleep(5)
                continue
            if user_prompt.title() in list(self.engine.unitdict.keys()):
                user_unit = user_prompt.title()
                print('Current unit: ' + user_prompt.title())
                time.sleep(3)
                continue
            else:
                print("\n" + Fore.RED + "No unit with such name!" + Fore.RESET)
                time.sleep(3)
                continue
        return user_unit

    def sandbox_mode(self):
        self.engine.display()
        import math
        marker_red = Marker(budget=math.inf, y=0, x=0,
                            inbound_x=self.engine.size_x - 1, engine=self.engine, team='Red')
        while True:
            self.engine.flush()
            user_place = input('Type "place" to start unit placement. Current unit: {}'.format(marker_red.unit) +
                               '\n\n'
                               'Type "unit" to select an unit'
                               '\n\n'
                               'Type "done" when your army is ready: ')
            if user_place.lower() == 'unit':
                marker_red.unit = self.choose_unit()
                continue
            if user_place.lower() == 'done':
                self.engine.flush()
                print(Fore.LIGHTRED_EX + "Red " + Fore.RESET + "team placed! Proceeding to "
                      + Fore.LIGHTCYAN_EX + "Blue " + Fore.RESET + "team!")
                time.sleep(3)
                print('\n' * 40)
                self.engine.flush()
                break
            if user_place.lower() == 'place':
                time.sleep(0.20)
                marker_red.enable()
                self.engine.display()
                print("To place an unit, press ENTER. To stop placement, press ESC.")
                while not marker_red.disabled:
                    time.sleep(0.01)
                continue
        marker_blue = Marker(budget=math.inf, y=0, x=self.engine.size_x - 1,
                             inbound_x=self.engine.size_x - 1, engine=self.engine, team='Blue')
        while True:
            self.engine.flush()
            user_place = input('Type "place" to start unit placement. Current unit: {}'.format(marker_blue.unit) +
                               '\n\n'
                               'Type "unit" to select an unit'
                               '\n\n'
                               'Type "start" when your army is ready to start the game: ')
            if user_place.lower() == 'unit':
                marker_blue.unit = self.choose_unit()
                continue
            if user_place.lower() == 'start':
                marker_blue.die()
                break
            if user_place.lower() == 'place':
                time.sleep(0.20)
                marker_blue.enable()
                self.engine.display()
                print("To place an unit, press ENTER. To stop placement, press ESC.")
                while not marker_blue.disabled:
                    time.sleep(0.01)
                continue
        self.engine.start_game()

    def menu(self):
        print(Fore.LIGHTYELLOW_EX + '''Hello there, friend! Welcome to TABSlike 0.4! I hope you'll like this game :)\n
        Right now there's three modes. Which one would you like to see?\n
        1) Random encounter
        2) Sandbox mode
        3) Random battle''' + Fore.RESET)
        choice = input()
        if choice == '1':
            self.random_encounter()
        if choice == '2':
            self.sandbox_mode()
        if choice == '3':
            self.random_battle()
        else:
            print('Not an option.')
            self.menu()

    def random_battle(self):
        self.engine.generate_blue(random.randint(self.engine.size_x * 300, self.engine.size_y * 400))
        self.engine.generate_red(random.randint(self.engine.size_x * 300, self.engine.size_y * 400))
        self.engine.display()
        print("Here's your battle! Starting in 5 seconds...")
        time.sleep(5)
        self.engine.start_game()

    def random_encounter(self):
        blue_budget = random.randint(self.engine.size_x * 200, self.engine.size_y * 400)
        self.engine.generate_blue(blue_budget)
        self.engine.display()
        print(Fore.LIGHTYELLOW_EX + "That's enemy army! Now, place your units..." + Fore.RESET)
        print('Your budget: {}'.format(round(blue_budget * 0.7)))
        time.sleep(5)
        marker = Marker(budget=blue_budget * 0.7, y=0, x=0,
                        inbound_x=round(self.engine.size_x / 2) - 1, engine=self.engine, team='Red')
        while True:
            self.engine.flush()
            user_place = input('Type "place" to start placing the units. Current unit: {}'.format(marker.unit) +
                               '\n\n'
                               'Type "unit" to select an unit'
                               '\n\n'
                               'Type "start" to start when your army is ready: ')
            if user_place.lower() == 'unit':
                marker.unit = self.choose_unit()
            if user_place.lower() == 'start':
                marker.die()
                self.engine.start_game()
                return
            if user_place.lower() == 'place':
                time.sleep(0.3)
                marker.enable()
                self.engine.display()
                print("To place an unit, press ENTER. To stop placement, press ESC.")
                while not marker.disabled:
                    time.sleep(0.5)


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

    def check_inbounds(self, y, x):
        if y > self.engine.size_y - 1 or y < 0 or x > self.engine.size_x - 1 or x < 0 or x > self.inbound_x:
            return False
        else:
            return True

    def move(self, side):
        move_side = self.sides.get(side)
        if self.check_inbounds(self.y + move_side[0], self.x + move_side[1]):
            self.engine.gamemap[self.y][self.x] = self.previous_position
            self.y += move_side[0]
            self.x += move_side[1]
            self.previous_position = copy.deepcopy(self.engine.gamemap[self.y][self.x])
            self.engine.gamemap[self.y][self.x] = Fore.LIGHTYELLOW_EX + 'X' + Fore.RESET
            self.engine.flush()
            for y in self.engine.gamemap:
                print('  '.join(y))
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
                unit = self.engine.spawn_unit(y=self.y, x=self.x, team=self.team)
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
        self.engine.techmap[self.y][self.x] = '.'
        unit.team_dict.get(unit.team.lower()).remove(unit)

    def die(self):
        self.engine.gamemap[self.y][self.x] = self.previous_position
        self.listener.stop()

    def disable(self):
        self.disabled = True

    def enable(self):
        self.disabled = False
