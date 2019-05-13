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

    def beenThere(self,x,y):
        self.squares[x][y] = 3

    def virgin(self,x,y):
        self.squares[x][y] < 3

    def get(self,x,y):
        return self.squares[x][y]

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def solve(self):
        path = []
        return path


def debug():
    cwd = os.getcwd()
    level1 = Level('../levels/007.xml')
    print('stop')

debug()
