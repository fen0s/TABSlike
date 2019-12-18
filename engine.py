from Units.units import Unit
import random
from colorama import init, Fore, Back, Style
import time


class GameMap:

    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.gamemap = self.generate_map()
        self.techmap = self.generate_map()
        self.alive_list = [[], []]

    def start_game(self):
        while self.alive_list[0] and self.alive_list[1]:
            for team in self.alive_list:
                for unit in team:
                    unit.check_enemies()
                self.display()
        if self.alive_list[0] and not self.alive_list[1]:
            print(Fore.LIGHTRED_EX + 'Red' + Fore.LIGHTYELLOW_EX + ' team wins!')
        else:
            print(Fore.LIGHTCYAN_EX + 'Blue' + Fore.LIGHTYELLOW_EX + ' team wins!')
        input('Press ENTER to quit...')

    def generate_blue(self, units_number):
        units_placed = 0
        while units_placed < units_number:
            b_coords = [random.randint(round(self.size_y / 2), self.size_y - 1),
                        random.randint(round(self.size_x / 2), self.size_x - 1)]
            if not self.check_entity(b_coords[0], b_coords[1]):
                unit_blue = Unit(name='Blue' + str(units_placed), hp=1, y=b_coords[0], x=b_coords[1],
                                 damage=1, map_engine=self, team='Blue')
                units_placed += 1
            else:
                continue

    def generate_red(self, units_number):
        units_placed = 0
        while units_placed < units_number:
            b_coords = [random.randint(0, round(self.size_y / 2)),
                        random.randint(0, round(self.size_x / 2))]
            if not self.check_entity(b_coords[0], b_coords[1]):
                unit_red = Unit(name='Red' + str(units_placed), hp=1, y=b_coords[0], x=b_coords[1],
                                damage=1, map_engine=self, team='Red')
                units_placed += 1
            else:
                continue

    def generate_map(self):
        gamemap = []
        for each_y in range(self.size_y):
            gamemap.append(['.' for _ in range(self.size_x)])
        return gamemap

    def display(self):
        """**** Display the map itself. ****"""
        print('\n' * 18)
        for x in self.gamemap:
            print('  '.join(x))
        time.sleep(1)

    def place(self, entity, y, x):
        """**** Place the symbol on frontend map. ****"""
        if -1 < x < self.size_x and -1 < y < self.size_y:
            self.gamemap[y][x] = entity
        else:
            print('Coordinates out of index.')

# **** Place the unit on techmap. ****
    def place_techmap(self, entity, y, x):
        if -1 < x < self.size_x and -1 < y < self.size_y:
            self.techmap[y][x] = entity
        else:
            print('Coordinates out of index.')

# **** Make the tile empty in both "dimensions" - techmap and frontmap.
    def make_empty(self, y, x):
        self.gamemap[y][x] = '.'
        self.techmap[y][x] = '.'

    def place_both(self, y, x, tech_place, game_place):
        self.place(game_place, y, x)
        self.place_techmap(tech_place, y, x)

# **** Check for presence of entity on tile in both gamemap and techmap.
    def check_entity(self, y, x):
        if self.techmap[y][x] == '.' and self.gamemap[y][x] == '.':
            return False
        else:
            return True


class Menu:
    def __init__(self, engine):
        self.engine = engine
        self.menu()

    def sandbox_mode(self):
        while True:
            user_place = input('Where to place red unit? Example: 5,8 where 5 is X and 8 is Y\n\nType "done" when all red units are placed: ')
            if user_place.lower() == 'done':
                break
            coords = user_place.split(',')
            print(user_place)
            unit = Unit(name='Red', hp=1, y=int(coords[1]), x=int(coords[0]), damage=1, map_engine=self.engine, team='Red')
            self.engine.display()
            print('Done!')
        while True:
            user_place = input('Where to place blue unit? Example: 5,8 where 5 is X and 8 is Y\n\nType "start" when all blue units are placed to start the game: ')
            if user_place.lower() == 'start':
                break
            coords = user_place.split(',')
            print(user_place)
            unit = Unit(name='Blue', hp=1, y=int(coords[1]), x=int(coords[0]), damage=1, map_engine=self.engine, team='Blue')
            self.engine.display()
            print('Done!')
        self.engine.start_game()

    def menu(self):
        print(Fore.LIGHTYELLOW_EX + '''Hello there, friend! Welcome to TABSlike 0.1! I hope you'll like this game :)\n
        Right now there's two modes - sandbox and random encounter. Which one would you like to see?\n
        1) Random encounter
        2) Sandbox mode''' + Fore.RESET)
        choice = input()
        if choice == '1':
            self.random_encounter()
        if choice == '2':
            self.sandbox_mode()
        else:
            print('Not an option.')
            self.menu()

    def random_encounter(self):
        self.engine.generate_blue(random.randint(5, 10))
        self.engine.display()
        print(Fore.LIGHTYELLOW_EX + "That's enemy army! Now, place your units...")
        while True:
            user_place = input('Where to place red unit? Example: 5,8 where 5 is X and 8 is Y\n\nType "start" to start when your army is ready: ')
            if user_place.lower() == 'start':
                break
            coords = user_place.split(',')
            print(user_place)
            unit = Unit(name='Red', hp=1, y=int(coords[1]), x=int(coords[0]), damage=1, map_engine=self.engine, team='Red')
            self.engine.display()
            print('Done!')
        self.engine.start_game()