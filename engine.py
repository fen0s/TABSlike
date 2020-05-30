from Units.Unit import Unit
from Units.ExplosiveUnit import ExplosiveUnit
from Units.RangedUnit import RangedUnit
import random
from colorama import Fore
import time
import os
from Utils.marker import Marker


class GameMap:

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.gamemap = self.generate_map()
        self.techmap = self.generate_techmap()
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
        """Flush the terminal display."""
        if os.system('cls') == 127:
            os.system('clear')

    def generate_techmap(self):
        """Generate blank techmap."""
        gamemap = []
        for _ in range(self.size_y):
            gamemap.append([None for _ in range(self.size_x)])
        return gamemap

    def start_game(self):
        """Start the game. Goes on until one of teams dies."""
        while self.alive_list[0] and self.alive_list[1]:
            for team in self.alive_list:
                for unit in team:
                    unit.check_enemies()
                self.display()
        self.end_game()

    def end_game(self):
        """End the game and announce the winner."""
        if self.alive_list[0] and not self.alive_list[1]:
            print("\n" + Fore.LIGHTRED_EX + 'Red' + Fore.LIGHTYELLOW_EX + ' team wins!')
        else:
            print("\n" + Fore.LIGHTCYAN_EX + 'Blue' + Fore.LIGHTYELLOW_EX + ' team wins!')
        input('Press ENTER to quit...')
        quit()

    def check_inbounds(self, y, x):
        if y > self.size_y - 1 or y < 0 or x > self.size_x - 1 or x < 0:
            return False
        else:
            return True

    def spawn_unit(self, unit, y, x, team):
        """Spawn unit, returning their instance from unitdict."""
        return self.unitdict.get(unit)(y=y, x=x, team=team)

    def generate_blue(self, budget):
        """Generate blue team of the map. Generated on the right side."""
        unit_names = list(self.unitdict.keys())
        while budget > 199:  # while budget > min_unit_price
            b_coords = [random.randint(round(self.size_y / 2), self.size_y - 1),
                        random.randint(round(self.size_x / 2), self.size_x - 1)]
            if not self.check_entity(b_coords[0], b_coords[1]):
                unit = self.spawn_unit(unit=random.choice(unit_names), y=b_coords[0], x=b_coords[1], team='Blue')
                if unit.cost > budget:
                    self.place_both(b_coords[0], b_coords[1], None, '.')
                    self.alive_list[1].remove(unit)
                    continue
                budget -= unit.cost
            else:
                continue

    def generate_red(self, budget):
        """Generate red team of the map. Generated on the left side."""
        unit_names = list(self.unitdict.keys())
        while budget > 199:
            r_coords = [random.randint(0, round(self.size_y / 2) - 1),
                        random.randint(0, round(self.size_x / 2) - 1)]
            if not self.check_entity(r_coords[0], r_coords[1]):
                unit = self.spawn_unit(unit=random.choice(unit_names), y=r_coords[0], x=r_coords[1], team='Red')
                if unit.cost > budget:
                    self.place_both(r_coords[0], r_coords[1], None, '.')
                    self.alive_list[0].remove(unit)
                    continue
                budget -= unit.cost
            else:
                continue

    def generate_map(self):
        """Generate blank gamemap."""
        gamemap = []
        for _ in range(self.size_y):
            gamemap.append(['.' for _ in range(self.size_x)])
        return gamemap

    def display(self):
        """**** Display the map itself. ****"""
        self.flush()
        for row in self.gamemap:
            print('  '.join(row))
        time.sleep(1)

    def place(self, entity, y, x):
        """**** Place the symbol on frontend map. ****"""
        if self.check_inbounds(y, x):
            self.gamemap[y][x] = entity
        else:
            print('Coordinates out of index.')

    def place_techmap(self, entity, y, x):
        """**** Place the unit instance on techmap. ****"""
        if self.check_inbounds(y, x):
            self.techmap[y][x] = entity
        else:
            print('Coordinates out of index.')

    def make_empty(self, y, x):
        """**** Make the tile empty in both maps - techmap and frontmap. ****"""
        self.gamemap[y][x] = '.'
        self.techmap[y][x] = None

    def place_both(self, y, x, tech_place, game_place):
        """Place something on both techmap and gamemap."""
        self.place(game_place, y, x)
        self.place_techmap(tech_place, y, x)

    def check_entity(self, y, x):
        """Check if the tile is empty. If it is, returns False. If it is not, returns True."""
        if not self.techmap[y][x] and self.gamemap[y][x] == '.' or \
                self.gamemap[y][x] == Fore.LIGHTYELLOW_EX + 'X' + Fore.RESET and not self.techmap[y][x]:
            return False
        else:
            return True


class Menu:
    def __init__(self, engine):
        self.engine = engine
        self.menu()

    def choose_unit(self):
        """Executes CLI interface of choosing an unit."""
        user_unit = 'Warrior'
        while True:
            self.engine.flush()
            user_prompt = input(
                'This is choosing menu. Type "help" to see available units. '
                'To choose an unit, type its name here. To exit menu, type "exit": '
                'Current unit: {}'.format(user_unit))
            if user_prompt.lower() == 'exit':
                break
            if user_prompt.lower() == 'help':
                print("Available units:" + '\n' + '\n'.join(list(self.engine.unitdict.keys())))
                input('\n Press ENTER to continue...')
            if user_prompt.title() in list(self.engine.unitdict.keys()):
                user_unit = user_prompt.title()
            else:
                print("\n" + Fore.RED + "No unit with such name!" + Fore.RESET)
                time.sleep(2)
            continue
        return user_unit

    def sandbox_mode(self):
        self.engine.display()
        import math
        marker_red = Marker(budget=math.inf, y=0, x=0,
                            inbound_x=self.engine.size_x - 1, engine=self.engine, team='Red')
        self.call_choosing_menu(marker_red)
        print(Fore.LIGHTRED_EX + "\nRed" + Fore.RESET + " team placed! Proceeding to Blue team...")
        time.sleep(3)
        marker_blue = Marker(budget=math.inf, y=0, x=self.engine.size_x - 1,
                             inbound_x=self.engine.size_x - 1, engine=self.engine, team='Blue')
        self.call_choosing_menu(marker_blue)
        self.engine.start_game()

    def menu(self):
        print(Fore.LIGHTYELLOW_EX + '''Hello there, friend! Welcome to TABSlike 0.4! I hope you'll like this game :)\n
        Right now there's three modes. Which one would you like to see?\n
        1) Random encounter
        2) Sandbox mode
        3) Random battle''' + Fore.RESET)
        choice = input()
        choices = {'1': self.random_encounter,
                  '2': self.sandbox_mode,
                  '3': self.random_battle}
        if choices[choice]:
            choices[choice]()
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

    def call_choosing_menu(self, marker):
        while True:
            self.engine.flush()
            user_place = input('Type "place" to start placing the units. Current unit: {}'.format(marker.unit) +
                               '\n\n'
                               'Type "unit" to select an unit'
                               '\n\n'
                               'Type "done" to start when your army is ready: ')
            if user_place.lower() == 'unit':
                marker.unit = self.choose_unit()
            if user_place.lower() == 'done':
                marker.die()
                break
            if user_place.lower() == 'place':
                time.sleep(0.3)
                marker.enable()
                self.engine.display()
                print("To place an unit, press ENTER. To stop placement, press ESC.")
                while not marker.disabled:
                    time.sleep(0.5)
                time.sleep(0.3)

    def random_encounter(self):
        blue_budget = random.randint(self.engine.size_x * 200, self.engine.size_y * 400)
        self.engine.generate_blue(blue_budget)
        self.engine.display()
        print(Fore.LIGHTYELLOW_EX + "That's enemy army! Now, place your units..." + Fore.RESET)
        print('Your budget: {}'.format(round(blue_budget * 0.7)))
        time.sleep(5)
        marker = Marker(budget=blue_budget * 0.7, y=0, x=0,
                        inbound_x=round(self.engine.size_x / 2) - 1, engine=self.engine, team='Red')
        self.call_choosing_menu(marker)
        self.engine.start_game()
