from engine import *
from colorama import init

if os.name == 'nt':
    init(convert=True)
else:
    init()
gmap = GameMap(20, 20)
menu = Menu(gmap)
