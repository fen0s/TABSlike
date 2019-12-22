from Units.units import Unit, RangedUnit, ExplosiveUnit
import random
from colorama import Fore
import time


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
                                 damage=4, map_engine=self, team=team, cost=850, reload_time=2),
                     'Grenadier': lambda y, x, team: ExplosiveUnit(name='Grenadier' + '_' + team, hp=2, y=y, x=x,
                                 damage=3, map_engine=self, team=team, cost=700, reload_time=3)
                     }

    def start_game(self):
        while self.alive_list[0] and self.alive_list[1]:
            for team in self.alive_list:
                for unit in team:
                    unit.check_enemies()
                self.display()
        if self.alive_list[0] and not self.alive_list[1]:
            print("\n" + Fore.LIGHTRED_EX + 'Red' + Fore.LIGHTYELLOW_EX + ' team wins!')
        else:
            print("\n" + Fore.LIGHTCYAN_EX + 'Blue' + Fore.LIGHTYELLOW_EX + ' team wins!')
        input('Press ENTER to quit...')
        quit()

    def generate_blue(self, budget):
        unit_names = list(self.unitdict.keys())
        while budget > 199:
            b_coords = [random.randint(round(self.size_y / 2), self.size_y - 1),
                        random.randint(round(self.size_x / 2), self.size_x - 1)]
            if not self.check_entity(b_coords[0], b_coords[1]):
                unit = self.unitdict.get(random.choice(unit_names))(y=b_coords[0], x=b_coords[1], team='Blue')
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
            r_coords = [random.randint(0, round(self.size_y / 2)),
                        random.randint(0, round(self.size_x / 2))]
            if not self.check_entity(r_coords[0], r_coords[1]):
                unit = self.unitdict.get(random.choice(unit_names))(y=r_coords[0], x=r_coords[1], team='Red')
                if unit.cost > budget:
                    self.place_both(r_coords[0], r_coords[1], '.', '.')
                    self.alive_list[0].remove(unit)
                    continue
                budget -= unit.cost
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

    def choose_unit(self):
        user_unit = ['Warrior']
        while True:
            user_prompt = input(
                'This is choosing menu. Type "help" to see available units. '
                'To choose an unit, type its name here. To exit menu, type "exit": ')
            if user_prompt.lower() == 'exit':
                break
            if user_prompt.lower() == 'help':
                print("Available units:" + '\n' + '\n'.join(list(self.engine.unitdict.keys())))
                continue
            if user_prompt.title() in list(self.engine.unitdict.keys()):
                user_unit[0] = user_prompt.title()
                print('Current unit: ' + user_prompt.title())
        return user_unit

    def sandbox_mode(self):
        user_unit = ['Warrior']
        while True:
            user_place = input('Where to place red unit? Example: 5,8 where 5 is X and 8 is Y\n\n'
                               'Type "unit" to choose unit\n\n'
                               'Type "done" when all red units are placed: ')
            if user_place.lower() == 'done':
                break
            if user_place.lower() == 'unit':
                user_unit = self.choose_unit()
                continue
            coords = user_place.split(',')
            self.engine.unitdict.get(user_unit[0])(y=int(coords[1]), x=int(coords[0]), team='Red')
            self.engine.display()
            print('Done!')

        while True:
            user_place = input('Where to place blue unit? Example: 5,8 where 5 is X and 8 is Y'
                               '\n\n'
                               'Type "unit" to choose unit'
                               '\n\n'
                               'Type "start" when all blue units are placed to start the game: ')
            if user_place.lower() == 'start':
                break
            if user_place.lower() == 'unit':
                user_unit = self.choose_unit()
                continue
            coords = user_place.split(',')
            self.engine.unitdict.get(user_unit[0])(y=int(coords[1]), x=int(coords[0]), team='Blue')
            self.engine.display()
            print('Done!')
        self.engine.start_game()

    def menu(self):
        print(Fore.LIGHTYELLOW_EX + '''Hello there, friend! Welcome to TABSlike 0.1! I hope you'll like this game :)\n
        Right now there's two modes - sandbox and random encounter. Which one would you like to see?\n
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
        self.engine.generate_blue(random.randint(3000, 4000))
        self.engine.generate_red(random.randint(3000, 4000))
        self.engine.display()
        print("Here's your battle! Starting in 5 seconds...")
        time.sleep(5)
        self.engine.start_game()

    def random_encounter(self):
        blue_budget = random.randint(2000, 4000)
        self.engine.generate_blue(blue_budget)
        red_budget = round(blue_budget * 0.7)
        self.engine.display()
        print(Fore.LIGHTYELLOW_EX + "That's enemy army! Now, place your units..." + Fore.RESET)
        print('Your budget: {}'.format(red_budget))
        user_unit = ['Warrior']
        while True:
            user_place = input('Where to place red unit? Example: 5,8 where 5 is X and 8 is Y'
                               '\n\n'
                               'Type "unit" to select an unit'
                               '\n\n'
                               'Type "start" to start when your army is ready: ')
            if user_place.lower() == 'unit':
                user_unit = self.choose_unit()
                continue
            if user_place.lower() == 'start':
                self.engine.start_game()
            coords = user_place.split(',')
            try:
                if int(coords[0]) > self.engine.size_x / 2 or self.engine.check_entity(int(coords[0]), int(coords[1])):
                    print(Fore.RED + '\nPosition unavialable!\n' + Fore.RESET)
                    continue
                unit = self.engine.unitdict.get(user_unit[0])(y=int(coords[1]), x=int(coords[0]), team='Red')
                if unit.cost > red_budget:
                    self.engine.place_both(int(coords[1]), int(coords[0]), '.', '.')
                    self.engine.alive_list[0].remove(unit)
                    print(Fore.RED + "You can't afford this unit!" + Fore.RESET)
                    continue
                red_budget -= unit.cost
            except (ValueError, IndexError):
                print(Fore.RED + 'Position unavailable!' + Fore.RESET)
                continue
            self.engine.display()
            print(Fore.LIGHTYELLOW_EX + 'Done! Budget left: {}'.format(red_budget) + Fore.RESET)
