import random
import time
from colorama import init, Fore, Back, Style
import os
from engine import *
from Units.units import *


if os.name == 'nt':
    init(convert=True)
else:
    init()


gmap = GameMap(10, 10)
gmap.generate_blue(random.randint(5, 10))
gmap.generate_red(random.randint(5, 10))
menu = Menu(gmap)

