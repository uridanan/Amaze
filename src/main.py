#
#
# * This is the main method that receives a Level and returns
#
# * a solution with the minimal number of steps to this level
#
# * in the form of array of movements.
#
# * The method should return null if the level is non solveable
#
# * 1 = right, 2= left, 3 = up, 4 = down
#
# */
#
# static int[] shortestSolution(Level level){
#
#     //Do your magic here
#
# }


import xml.etree.ElementTree as ET
import os


RIGHT, LEFT, UP, DOWN = 1,2,3,4
DIRECTIONS = [RIGHT,DOWN,LEFT,UP]
MAX_STEPS = 10

class Level:
    # 0=white square 1=black square.
    # The ball moves on black squares
    # x is the index of the row, y the index of the column
    squares = None
    width = 0
    height = 0
    data = None
    graph = dict()

    def __init__(self,filename):
        self.load(filename)
        self.initSquares()

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
            i=i+1
        self.squares = squares

    def id(self,x,y):
        return x*self.width + y

    def square(self,id):
        x = id // self.width
        y = id - x * self.width
        return [x,y]

    def isWall(self,x,y):
        return self.squares[x][y] == 0

    def outOfBounds(self,x,y):
        return x == -1 or x == self.height or y == -1 or y == self.width

    def inPlay(self,x,y):
        return not self.isWall(x,y) and not self.outOfBounds(x,y)

    def isNode(self,x,y,d):
        pass


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


    # When building the graph, also build a graph where for every node we store the direction coming into it from other nodes
    # When adding a neighbor to a node, make sure that the node actually has an entry point
    # i.e. if n1 has an entry point going RIGHT into it, it can have a neighbor on the RIGHT, but not UP
    def buildGraphNFlow(self):
        graph = dict()
        flow = dict()
        for x in range(self.height):
            for y in range(self.width):
                if self.squares[x][y] > 0:  # node is not a wall
                    n = Node(self.id(x, y), x, y)

                    # If node next to a wall, add flow
                    # Each node in graph should have neighbours only for allowed directions
                    # If node not next to a wall, the only direction is the same that entered the node
                    for d in DIRECTIONS:
                        nx,ny = n.peek(d)
                        if self.isWall(nx,ny):
                            n.flow[opposite(d)]


                    for d in DIRECTIONS:
                        nx,ny = n.peek(d)
                        if self.inPlay(nx,ny):
                            nId = self.id(nx, ny)
                            n.neighbours.append({'node': nId, 'dir': d})

                            nb = Node(nId, nx, ny)
                            nb.neighbours.append({'node': nId, 'dir': opposite(d)})
                            flow[nId] = nb
                    graph[n.id] = n
        return graph

def opposite(direction):
    switcher = {
        RIGHT: LEFT,
        LEFT: RIGHT,
        UP: DOWN,
        DOWN: UP
    }
    return switcher[direction]

class Node:
    id = -1
    x = -1
    y =-1
    neighbours = []

    #Flow returns an array of the directions available from the node when entering from a given direction
    flow = {
        RIGHT: [],
        LEFT: [],
        UP: [],
        DOWN: []
    }

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


def start(graph):
    if graph is None or len(graph.keys()) < 1:
        return None
    path = []
    visited = dict()
    rootId = min(graph.keys())
    root = graph.get(rootId, None)
    path = traverse(root,graph,visited,path)
    print("Done")


def traverse(root,graph,visited,path):

    # If graph is empty, we are done
    if root is None:
        print("Graph is empty")
        return path, visited

    # If path exceeds limit, there is no solution here
    if safeLen(path) > MAX_STEPS:
        print("Path exceeds limit")
        return None, visited

    # Mark our visit here
    visited[root.id] = root
    graph.pop(root.id, None)

    # Visit the neighbours
    paths = {}
    for nb in root.neighbours:
        if safeLen(path) < 1 or nb['dir'] != path[-1]:
            path.append(nb['dir'])
        node = graph.get(nb['node'],None)
        paths[nb['dir']] = traverse(node,graph,visited,path)

    path = None
    for p in paths.values():
        path = shorter(path, p)

    return path


def shorter(l1,l2):
    if l1 is None and l2 is None:
        return None
    if l1 is None:
        return l2
    if l2 is None:
        return l1
    if len(l2) < len(l1):
        return l2
    else:
        return l1


def safeLen(list):
    if list is None:
        return -1
    return len(list)

# TODO: make sure not to include nodes / neigbours in the graph when you can't stop on them
# TODO: use MAX_STEPS as a parameter to find the solution faster
# TODO: identify loops on the fly?
# TODO: is visited useless?
def debug():
    cwd = os.getcwd()
    level1 = Level('../levels/007.xml')
    g = level1.buildGraph()
    start(g)
    print('stop')

debug()
