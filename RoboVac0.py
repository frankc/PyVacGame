'''
create robot vacuum that cleans all the floors of a grid.
main should provide:
- grid size
- loc of robovac
- list of x,y,w,h tuples or instance of Rect
goal: visit all tiles
exec will : create instance and in game loop call : nextMove()  ??
'''
import random
import numpy as np

class RoboVac:
    def __init__(self, config_list):
        self.room_width, self.room_height = config_list[0]
        self.pos = config_list[1]   # starting position of vacuum
        self.block_list = config_list[2]   # blocks list (x,y,width,ht)

        # fill in with your info
        self.name = "Zarkon Zeeblebrock"
        self.id = "66666666"


    def get_next_move(self, current_pos):  # called by PyGame code
        # random walk
        return random.choice([0,1,2,3])



