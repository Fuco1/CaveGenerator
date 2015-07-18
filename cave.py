import sys
from random import Random

class CaveFactory:
    def __init__(self, width, height, seed=1, ca_runs=2):
        self.r = Random()
        self.r.seed(seed)
        self.seed = seed
        self.ca_runs = ca_runs
        self.width = width
        self.height = height

    def gen(self, floor_chance=0.4, adjacent_maps=(None, None, None, None)):
        """Adjacent caves order: Top, Right, Bottom, Left"""
        map = []
        for col in range(self.width):
            r = []
            for row in range(self.height):
                if self.r.random() < floor_chance:
                    r.append('.')
                else:
                    r.append('#')
            map.append(r)

        self._copy_adjacent_maps(map, adjacent_maps)

        for i in range(self.ca_runs):
            map = self._run_ca(map)

        for col in range(1, self.width-1):
            top_adj = self._adjacent_walls(map, col, 0)
            bot_adj = self._adjacent_walls(map, col, self.height-1)
            if not top_adj:
                map[col][0] = '.'
            if not bot_adj:
                map[col][self.height-1] = '.'

        for row in range(1, self.height-1):
            left_adj = self._adjacent_walls(map, 0, row)
            right_adj = self._adjacent_walls(map, self.width-1, row)
            if not left_adj:
                map[0][row] = '.'
            if not right_adj:
                map[self.width-1][row] = '.'

        return Cave(self.width, self.height, map, self.seed)

    def _copy_adjacent_maps(self, map, adjacent_maps):
        (top, right, bottom, left) = adjacent_maps
        if top:
            for col in range(self.width):
                map[col][0] = top.map[col][self.height-1]
        if bottom:
            for col in range(self.width):
                map[col][self.height-1] = bottom.map[col][0]
        if left:
            map[0] = left.map[self.width-1]
        if right:
            map[self.width-1] = right.map[0]

    def _run_ca(self, map):
        map_re = [map[0]]
        for col in range(1, self.width-1):
            r = [map[col][0]]
            for row in range(1, self.height-1):
                adj = self._adjacent_walls(map, col, row)
                if adj < 4:
                    r.append('.')
                elif adj > 5:
                    r.append('#')
                else:
                    r.append(map[col][row])
            r.append(map[col][self.height-1])
            map_re.append(r)
            
        map_re.append(map[self.width-1])
        return map_re


    def _adjacent_walls(self, map, col, row):
        count = 0
        for c in (-1, 0, 1):
            for r in (-1, 0, 1):
                if (col + c >= 0 and col + c < self.width and
                    row + r >= 0 and row + r < self.height and
                    map[col + c][row + r] == '#' and
                    not (c == 0 and r == 0)):
                    count += 1
        return count


class Cave:
    def __init__(self, width, height, map, seed):
        self.seed = seed
        self.width = width
        self.height = height
        self.map = map
        self.cell_width = 8
        self.cell_height = 8        

        factor = 4
        hm_seed = (seed + 4515435) % sys.maxint
        r = Random()
        r.seed(hm_seed)
        heightmap = []

        # init the height map. erode in next steps
        for col in range(width * self.cell_width / factor):
            hmrow = []
            for row in range(height * self.cell_height / factor):
                hmrow.append(1.0 if r.random() > 0.5 else 0.0)
            heightmap.append(hmrow)    

        factor /= 2
        while factor != 0:
            w = width * self.cell_width / factor
            h = height * self.cell_height / factor
            tmp = []
            for r in heightmap: tmp.append([x for x in r for y in range(2)])
            heightmap = [x for x in tmp for y in range(2)]

#            for col in range(w):
#                for row in range(h):
#                    print heightmap[col][row],
#                print

            for col in range(w):
                for row in range(h):
                    v = self._average_adjacent_cells(heightmap, col, row, w, h)
                    heightmap[col][row] = v
        
#            print
#            for col in range(w):
#                for row in range(h):
#                    print heightmap[col][row],
#                print

            factor /= 2

            
    def _average_adjacent_cells(self, heightmap, col, row, width, height):
        h = 0
        count = 0
        for c in (-1, 0, 1):
            for r in (-1, 0, 1):
                if (col + c >= 0 and col + c < width and
                    row + r >= 0 and row + r < height):
                    h += heightmap[col + c][row + r]
                    count += 1
        return h / count
    

    def tostring(self):
        r = ""
        for row in range(self.height):
            for col in range(self.width):
                r += self.map[col][row] + ' '
            r += '\n'
        return r
