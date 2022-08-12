'''
create robot vacuum that cleans all the floors of a grid.
main should provide:
- grid size
- loc of robovac
- list of x,y,w,h tuples or instance of Rect
goal: visit all floors
exec will : create instance and in game loop call : nextMove()  ??
'''
import random
import numpy as np

def gen_cells_between(path):
    # path has 3 points: origin, intermediary, destination
    p1x, p1y = path[0]
    p2x, p2y = path[1]
    p3x, p3y = path[2]

    tile_set = set()
    tile_set.add( (p2x, p2y))   # always add intermediate point

    set1 = fill_between_points(p1x, p1y, p2x, p2y)
    set2 = fill_between_points(p2x, p2y, p3x, p3y)
    tile_set = tile_set.union(set1)
    tile_set = tile_set.union(set2)

    return (tile_set)


def fill_between_points(p1x, p1y, p2x, p2y):
    between_set = set()
    if p1x != p2x:
        if p1x < p2x:
            between = range(p1x, p2x)
        else:
            between = range(p1x, p2x, -1)  # go backward
        for x in between:
            between_set.add((x, p2y))

    else:  # must be y that varies
        if p1y < p2y:
            between = range(p1y, p2y)
        else:
            between = range(p1y, p2y, -1)  # go backward
        for y in between:
            between_set.add((p1x, y))

    return between_set

def manhattan_dist(p1, p2, blocks_set):
    x1,y1 = p1
    x2,y2 = p2
    path1 = [(x1,y1), (x1,y2), (x2,y2)]
    path2 = [(x1,y1), (x2,y1), (x2,y2)]

    set1 = gen_cells_between(path1)
    set2 = gen_cells_between(path2)

    if len(set1.intersection(blocks_set)) == 0:
        #print (f"blcks_set: {blocks_set}  set1={set1}")
        return len(set1) +1
    elif len(set2.intersection(blocks_set)) == 0:
        #print (f"blocks-set; {blocks_set}  set2: {set2}")
        return len(set2)  +1
    else:
        return 10000

# for tracking recent pos - gettng stuck
def push_pop(v, recent_pos_list):
    recent_pos_list.append(v)
    return recent_pos_list[1:]

class RoboVac:
    def __init__(self, config_list):
        self.room_width, self.room_height = config_list[0]
        self.pos = config_list[1]   # starting position of vacuum
        self.block_list = config_list[2]   #blocks list (x,y,width,ht)

        # fill in with your info
        self.name = "Zarkon Zeeblebrock"
        self.id = "66666666"

        # fc implementation
        self.max_x = self.room_width  -1
        self.max_y = self.room_height -1

        self.visited_set = set()
        self.recent_pos_list = [1,2,3,4,5,6]   # shift in each new pos

        # set up sets..
        # create set with all tiles
        self.free_tiles_set = set()
        for x in range(self.room_width):
            for y in range(self.room_height):
                self.free_tiles_set.add((x, y))


        # create set with block tiles
        self.block_tiles_set = set()
        for b in self.block_list:
            for x in range(b[0], b[0] + b[2]):
                for y in range(b[1], b[1] + b[3]):
                    self.block_tiles_set.add((x, y))

        self.free_tiles_set = self.free_tiles_set - self.block_tiles_set


        self.unvisited_tiles_set = self.free_tiles_set - \
                                   self.visited_set

    def gen_next_list(self, origin):
        x, y = origin
        return [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]

    def does_pos_intersect_blocks(self, pos):
        #  check all blocks
        for rect in self.block_list:
            if self.rect_intersect(pos, rect):
                return True
        return False

    def get_dir_for_closest_unvisited_point(self, origin, unvisited_np):
        ''' 'works! 8/7/22 : when no unvisited surrounding spot  (origin)
           go direction that gets us closest to nearest unvisited pt
           returns dir
        '''
        import numpy as np

        def distance(p1, p2):
            return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

        next_list = self.gen_next_list(origin)

        shortest_dist_to_unvisited = [0, 0, 0, 0]  # track by direction


        for idx in range(4):
            # for each idx (dir) get distance to closest unvisited pt
            # then pick point with closest unvisited neighbor

            # is the next point part of a block. if yes, set dist high
            if  self.does_pos_intersect_blocks(next_list[idx]):
                shortest_dist_to_unvisited[idx] = 10000
            else:
                #  manhattan called
                dist_arr = np.array([manhattan_dist(pt, next_list[
                    idx], self.block_tiles_set) for pt in
                                     unvisited_np])
                # for our possible pt, get distance to closest unvisited
                shortest_dist_to_unvisited[idx] = np.min(dist_arr)


        # each next pt dist (0,1,2,3) has own shortest dist; pick best
        # the argmin will be the direction
        return np.argmin(shortest_dist_to_unvisited)

    def does_pos_intersect_blocks(self, pos):
        #  check all blocks
        for rect in self.block_list:
            if self.rect_intersect(pos, rect):
                return True
        return False

    def rect_intersect(self, pos, rect):
        rx, ry, width, height = rect
        x,y = pos
        is_intersect =   x >= rx and x < (rx + width) and \
           y >= ry and y < (ry + height)
        return is_intersect

    def get_next_move(self, current_pos):  # called by UI or main
        # track most recent positions; trap stuck situations
        self.recent_pos_list = push_pop(current_pos,
                                       self.recent_pos_list)

        # determine a direction to move -- needs logic
        if not current_pos in self.visited_set:    # not needed if set
            self.visited_set.add(current_pos)

        x,y = current_pos
        next_options = [(x,y-1), (x+1,y), (x, y+1), (x-1,y)]

        for idx in range(4):    # each idx is a direction (0..3)
            next_pos = next_options[idx]
            x1,y1 = next_pos           

            if not self.does_pos_intersect_blocks(next_pos) and \
                not next_options[idx] in self.visited_set and \
                    x1 >=0 and y1 >=0 and x1 <= self.max_x and \
                    y1 <= self.max_y:
                return idx

        # blocked everywhere ...move to square with closeset
        # open tile.. unless we are stuck
        pos = self.recent_pos_list[-1]
        if self.recent_pos_list.count(pos) > len(
                self.recent_pos_list)-3:
                dir = random.choice([0,1,2,3])
                return dir
        else:
            self.unvisited_tiles_set = self.free_tiles_set - self.visited_set
            unvisited_np = np.array(list(self.unvisited_tiles_set))
            return  self.get_dir_for_closest_unvisited_point(current_pos, unvisited_np)
        



