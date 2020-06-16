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
                       'red': Fore.LIGHTRED_EX + '{}'.format(name[0].upper()) + Fore.RESET}[self.team.lower()]
        self.team_dict = {'blue': map_engine.alive_list[1],
                          'red': map_engine.alive_list[0]}

    def move(self, side):
        if self.check_attackable(): #check for attackable entities, and don't move if you've preformed an attack
            return
        sides = {'right': [0, 1],
                 'left': [0, -1],
                 'up': [-1, 0],
                 'down': [1, 0]}
        move_side = sides.get(side)
        move_coords = [self.y + move_side[0], self.x + move_side[1]] #current coordinates + move side coordinates
        if self.engine.check_inbounds(move_coords[0], move_coords[1]) \
                and not self.engine.check_entity(move_coords[0], move_coords[1]): #if tile not occupied and coords are inbounds...

            self.engine.make_empty(self.y, self.x)
            self.y = move_coords[0]
            self.x = move_coords[1]
            self.engine.place_both(self.y, self.x, tech_place=self, game_place=self.symbol)

    def attack(self, entity):
        entity.hp -= self.damage
        
        self.engine.gamemap[entity.y][entity.x] = Fore.LIGHTMAGENTA_EX + '/' + Fore.RESET
        self.engine.display()
        print(f'{self.name} attacks {entity.name}! Damage: {self.damage},  HP of {entity.name} left: {entity.hp}')
        time.sleep(0.5)
        
        self.engine.gamemap[entity.y][entity.x] = entity.symbol
        if entity.hp <= 0:
            entity.die()

    def die(self):
        print(f'Oh no! {self.name} died!')
        time.sleep(0.5)
        self.engine.make_empty(self.y, self.x)
        self.team_dict.get( self.team.lower() ).remove(self)

    def check_enemies(self): #check whole map for enemies and move to the first found enemy
        for row in self.engine.techmap:
            for entity in row:
                if entity and entity.team != self.team:
                    self.move_on_enemy(entity.y, entity.x)
                    return

    def check_attackable(self):
        entities = self.check_surroundings(self.y, self.x)
        for entity in entities:
            self.attack(entity)
            return True
        return False
    
    def check_surroundings(self, y_coord, x_coord):
        y_coord -= 1 #to check y level above unit
        enemies = []
        for _ in range(3): #for 3 rows of the map...
                if self.engine.check_inbounds(y_coord, x_coord-1) and self.engine.check_inbounds(y_coord, x_coord+1):
                    for entity in self.engine.techmap[y_coord][x_coord-1:x_coord+1]: #check the slice of the map for entities...
                        if entity and entity.team != self.team:
                            enemies.append(entity)
                y_coord+=1 #move onto the next row
        return enemies

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
        #not using elseifs here so diagonal movement is kinda allowed. will fix in the future i guess?
    
    def place(self):
        self.team_dict.get(self.team.lower()).append(self) #append unit to the corresponding team
        self.engine.place_both(self.y, self.x, self, self.symbol) #and place unit instance on the map
