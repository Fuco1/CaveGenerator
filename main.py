from cave import CaveFactory
from random import randint

def main():
    c = CaveFactory(50, 25, randint(0, 100000))
    cave = c.gen(0.5)
    print cave.tostring()
    #cave2 = c.gen(0.5, (cave, None, None, None))
    #cave3 = c.gen(0.5, (None, None, None, cave2))
    #cave4 = c.gen(0.5, (None, None, cave3, cave))

#    for row in range(cave.height):
#        r = ""
#        for col in range(cave.width):
#            r += cave.map[col][row] + ' '
#        for col in range(cave4.width):
#            r += cave4.map[col][row] + ' '
#        r += '\n'
#        print r,
#
#    for row in range(cave2.height):
#        r = ""
#        for col in range(cave2.width):
#            r += cave2.map[col][row] + ' '
#        for col in range(cave3.width):
#            r += cave3.map[col][row] + ' '
#        r += '\n'
#        print r,
    #print cave2.tostring()
    #print cave3.tostring()

if __name__ == "__main__":
    main()
