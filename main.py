import os
from engine import *
from colorama import init

if os.name == 'nt':
    init(convert=True)
else:
    init()


gmap = GameMap(10, 10)
menu = Menu(gmap)
