import xml.etree.ElementTree as ET
import os


class Level:
    # 0=white square 1=black square.
    # The ball moves on black squares
    # x is the index of the row, y the index of the column
    squares = None
    ballXStartLocation = 0
    ballYStartLocation = 0
    width = 0
    height = 0
    data = None
    count = 0

    def __init__(self,filename):
        self.load(filename)
        self.initSquares()
        self.iniStartLocation()

    def load(self,filename):
        root = ET.parse(filename)
        layer = root.findall('layer')[0]
        self.width = int(layer.get('width'))
        self.height = int(layer.get('height'))
        self.data = layer.findall('data')[0].text

    def initSquares(self):
        #  d = [ [ None for y in range( 2 ) ] for x in range( 2 ) ]
        squares = [[None for y in range(self.width)] for x in range(self.height)]
        values = self.data.split(',')
        i = 0
        for v in values:
            x = i // self.width
            y = i - x*self.width
            squares[x][y] = int(v)
            if squares[x][y] > 0:
                self.increaseCount()
            i=i+1
        self.squares = squares

    def iniStartLocation(self):
        for x in range(self.height):
            for y in range(self.width):
                if self.squares[x][y] > 0:
                    self.ballXStartLocation = x
                    self.ballYStartLocation = y
                    return

    def increaseCount(self):
        self.count = self.count + 1

    def decreaseCount(self):
        self.count = self.count - 1
        return self.count == 0

    def isDone(self):
        return self.count == 0

    def color(self,x,y):
        self.squares[x][y] = 3

    def colorMe(self,x,y):
        return self.squares[x][y] < 3 and self.squares[x][y] > 0

    def myWorkHereIsDone(self,x,y):
        if self.colorMe(x, y):
            self.color(x, y)
            self.decreaseCount()

    def get(self,x,y):
        return self.squares[x][y]

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def solve(self):
        path = []
        return path

    def id(self,x,y):
        return x*self.getWidth() + y

    def square(self,id):
        x = id // self.width
        y = id - x * self.width
        return [x,y]

    def isWall(self,x,y):
        return self.squares[x][y] == 0

    def outOfBounds(self,x,y):
        return x == -1 or x == self.getHeight() or y == -1 or y == self.getWidth()

    def inPlay(self,x,y):
        return not self.isWall(x,y) and not self.outOfBounds(x,y)

    def buildGraph(self):
        graph = dict()
        for x in range(self.height):
            for y in range(self.width):
                if self.squares[x][y] > 0:
                    n = Node(self.id(x, y), x, y)
                    for d in DIRECTIONS:
                        nx,ny = n.peek(d)
                        if self.inPlay(nx,ny):
                            n.neighbours.append({'node': self.id(nx, ny), 'dir': d})
                    graph[n.id] = n
        return graph


RIGHT, LEFT, UP, DOWN = 1,2,3,4
DIRECTIONS = [RIGHT,DOWN,LEFT,UP]


class Node:
    id = -1
    x = -1
    y =-1
    neighbours = []

    def __init__(self,id,x,y):
        self.id = id
        self.x = x
        self.y = y

    def peek(self,direction):
        switcher = {
            RIGHT: [self.x, self.y + 1],
            LEFT: [self.x, self.y - 1],
            UP: [self.x - 1, self.y],
            DOWN: [self.x + 1, self.y]
        }
        return switcher[direction]




def debug():
    cwd = os.getcwd()
    level1 = Level('../levels/007.xml')
    g = level1.buildGraph()
    print('stop')

debug()
