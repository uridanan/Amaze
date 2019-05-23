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
import time
from copy import deepcopy



RIGHT, LEFT, UP, DOWN = 1,2,3,4
DIRECTIONS = [RIGHT,DOWN,LEFT,UP]
MAX_VISITS = 7

class Level:
    # 0=white square 1=black square.
    # The ball moves on black squares
    # x is the index of the row, y the index of the column
    squares = None
    visitableSquares = None
    width = 0
    height = 0
    data = None
    graph = None
    edges = None
    nodes = None

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
        self.visitableSquares = {}
        values = self.data.split(',')
        i = 0
        for v in values:
            x = i // self.width
            y = i - x*self.width
            squares[x][y] = int(v)
            if squares[x][y] > 0:
                self.visitableSquares[self.id(x,y)] = 0 # value is the number of edges that can visit the square
            i=i+1
        self.squares = squares

    def getSquares(self):
        # squares = {}
        # for x in range(self.height):
        #     for y in range(self.width):
        #         if self.squares[x][y] > 0:
        #             squares[self.id(x,y)] = 1
        return self.visitableSquares

    def id(self,x,y):
        return x*self.width + y

    def square(self,id):
        x = id // self.width
        y = id - x * self.width
        return [x,y]

    # Lookup the node, create new if not found
    def getNode(self,x,y):
        id = self.id(x, y)
        #n = self.nodes.get(id,None)
        n = self.graph.get(id,None)
        if n is None:
            n = Node(id,x,y)
            self.graph[n.id] = n
            #self.nodes[n.id] = n
        return n

    def openEdge(self,x,y,d):
        n = self.getNode(x,y)
        e = Edge(n,d)
        return e

    def closeEdge(self,x,y,e):
        if safeLen(e.squares) < 2:
            return None
        n = self.getNode(x, y)
        e.end = n
        e.start.edges[e.getId()] = e
        self.edges[e.getId()] = e

        #Mark squares and nodes to find lonely ones
        for s in e.squares:
            self.visitableSquares[s] = self.visitableSquares[s] + 1
        n.originCount = n.originCount + 1

        #print("Close Edge: %d,%d" % (e.start.id,e.end.id))
        return None

    # TODO: BUG 00,15,00,00,00,19,00, counts as edge with squares [15,19]
    def processSquare(self,x,y,d,e):
        if self.squares[x][y] == 0:
            if e is not None:
                # create a node for the previous square and close the edge
                ex,ey = Node(id,x,y).peek(opposite(d))
                e = self.closeEdge(ex, ey, e)
        else:
            if e is None:
                # create a new node and edge
                e = self.openEdge(x,y,d)
            e.squares.append(self.id(x,y))
        return e

    def buildGraph(self):
        self.graph = dict()
        #self.nodes = dict()
        self.edges = dict()

        # for i in range(10, -6, -2):
        # for i in reversed(range(5)):
        dimensions = {
            RIGHT: [0,self.height,1,0,self.width,1],
            LEFT: [0,self.height,1,self.width-1,-1,-1],
            DOWN: [0,self.width,1,0,self.height,1],
            UP: [0,self.width,1,self.height-1,-1,-1]
        }

        for d in DIRECTIONS:
            dim = dimensions[d]
            for x in range(dim[0],dim[1],dim[2]):
                e = None
                for y in range(dim[3],dim[4],dim[5]):
                    sx,sy = swap(x,y,d)
                    e = self.processSquare(sx,sy,d,e)

        self.findAllOrthogonalEdges()

        return self.graph

    def findAllOrthogonalEdges(self):
        #print("Search for orthogonal edges")
        for e in list(self.edges.values()):
            self.findOrthogonalEdges(e)

    # Some nodes can only be starting nodes because they close an edge
    def findOrthogonalEdges(self,e):
        if e is None or e.end is None:
            #print("ERROR ! Invalid open edge")
            return

        n = self.graph.get(e.end.id,None)
        if n is None:
            return

        orthogonalDirections = {
            RIGHT: [UP,DOWN],
            LEFT: [UP, DOWN],
            UP: [LEFT,RIGHT],
            DOWN: [LEFT, RIGHT]
        }

        dimensions = {
            RIGHT: [n.y,self.width,1],
            LEFT: [n.y,-1,-1],
            DOWN: [n.x,self.height,1],
            UP: [n.x,-1,-1]
        }

        for d in orthogonalDirections[e.dir]:
            # No point in trying blocked directions
            nx,ny = n.peek(d)
            if self.squares[nx][ny] == 0:
                continue

            dim = dimensions[d]
            orth = None
            for z in range(dim[0], dim[1], dim[2]):
                if d in [RIGHT,LEFT]:
                    x,y = n.x,z
                else:
                    x,y = z,n.y
                orth = self.processSquare(x, y, d, orth)



def swap(x,y,d):
    if d == LEFT or d == RIGHT:
        return x,y
    else:
        return y,x


def opposite(direction):
    switcher = {
        RIGHT: LEFT,
        LEFT: RIGHT,
        UP: DOWN,
        DOWN: UP
    }
    return switcher.get(direction,0)
    

class Node:
    id = -1
    x = -1
    y =-1
    edges = None
    originCount = 0

    def __init__(self,id,x,y):
        self.id = id
        self.x = x
        self.y = y
        self.edges = dict()
        self.originCount = 0

    def peek(self,direction):
        switcher = {
            RIGHT: [self.x, self.y + 1],
            LEFT: [self.x, self.y - 1],
            UP: [self.x - 1, self.y],
            DOWN: [self.x + 1, self.y]
        }
        return switcher[direction]


class Edge:
    start = None  # a node
    end = None  # a node
    dir = None  # a direction
    squares = None  # a list of square Ids
    visited = 0

    def __init__(self,node,d):
        self.start = node
        self.dir = d
        self.end = None
        self.squares = []
        self.visited = 0

    def getId(self):
        s = e = -1
        if self.start is not None:
            s = self.start.id
        if self.end is not None:
            e = self.end.id
        return (s,e)


def getRoot(graph):
    if graph is None or len(graph.keys()) < 1:
        return None
    rootId = min(graph.keys())
    root = graph.get(rootId, None)
    return root



# Find unsolvable levels
# If the logs show that this never returns True remove it
def noSolution(level,graph):

    if level.edges is None or graph is None or len(graph.keys()) < 1:
        return True

    rootId = min(graph.keys())

    # Find squares that are not traversed by any edge
    for i,v in level.visitableSquares.items():
        if v == 0:
            print("Orphan Square")
            return True

    # Find orphan edges
    for i,e in level.edges.items():
        c = e.start.originCount
        if c == 0 and rootId < e.start.id:
            print("Orphan Edge")
            return True

    return False



# Traverse all nodes without going back just to see if I can cover all the squares
def isSolvable(root,squares,graph):
    #print(path)

    # If graph is empty, we are done
    if safeLen(squares) == 0:
        #print("Graph is empty")
        #print("Solved by: %s " % path)
        return True

    # No more nodes but we haven't covered all squares
    if graph is None or safeLen(graph.keys()) < 1:
        return False

    # If root is none: error, should not happen
    if root is None:
        print("ERROR ! Invalid root")
        return False

    # If node is no longer in graph we were already here
    n = graph.pop(root.id, None)
    if n is None:
        return False

    # Visit the neighbours
    success = False

    for e in root.edges.values():
        for s in e.squares:
            squares.pop(s, None)
        if isSolvable(e.end,squares,graph):
            return True

    return success


# Pop squares traversed by edges, not Nodes
# Iterate edges, not neighbours
def traverse(root,squares,path,graph,max):
    #print(path)

    # If graph is empty, we are done
    if safeLen(squares) == 0:
        #print("Graph is empty")
        print("Solved by: %s " % path)
        return path

    if path is None:
        #print("ERROR! Path is None")
        return None

    # If path exceeds limit or current solution, there is no solution here
    if safeLen(path) > max:
        #print("Path exceeds limit")
        return None

    # If root is none: error, should not happen
    if root is None:
        #print("ERROR ! Invalid root")
        return None

    # We're stuck in a loop, no solution here
    if isStuckInLoop(path):
        #print("ERROR ! Stuck in loop")
        return None

    # Visit the neighbours
    paths = {}
    reverse = None
    for e in root.edges.values():
        if e.visited > MAX_VISITS: # if we've visited this edge too many times already we must be in a loop
            continue
        elif safeLen(path) > 1 and e.dir == opposite(path[-1]):
            # leave the return path for last
            reverse = e
        else:
            # don't append on same instance otherwise it is shared between all siblings. i.e. siblings are queued instead of replacing each other
            copyOfPath = list(path)
            copyOfPath.append(e.dir)
            copyOfSquares = deepcopy(squares)
            for s in e.squares:
                copyOfSquares.pop(s, None)
            e.visited = e.visited + 1
            paths[e.dir] = traverse(e.end,copyOfSquares,copyOfPath,graph,max)
            if paths[e.dir] is not None and len(paths[e.dir]) < max:
                max = len(paths[e.dir])

    # Process the return edge
    if reverse is not None:
        e = reverse
        copyOfPath = list(path)
        copyOfPath.append(e.dir)
        copyOfSquares = deepcopy(squares)
        e.visited = e.visited + 1
        paths[e.dir] = traverse(e.end, copyOfSquares, copyOfPath, graph, max)
        if paths[e.dir] is not None and len(paths[e.dir]) < max:
            max = len(paths[e.dir])

    newpath = None
    for p in paths.values():
        newpath = shorter(newpath, p)

    return newpath



def isStuckInLoop(path):
    if path is None or len(path) < 3:
        return False
    if path[-1] == path[-3] and path[-2] == opposite(path[-1]):
        return True
    else:
        return False


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


def start(filename):
    MAX_STEPS = 50
    started = time.process_time()
    path = []
    level = Level(filename)
    graph = level.buildGraph()
    squares = level.getSquares()
    root = getRoot(graph)
    # if noSolution(level,graph):
    # if isSolvable(root,deepcopy(squares),deepcopy(graph)) is False:
    #     path = None
    # else:
    #     path = traverse(root,squares,path,graph,MAX_STEPS)
    path = traverse(root, squares, path, graph, MAX_STEPS)
    elapsedTime = time.process_time() - started
    print("%s: %s, %s" % (filename, elapsedTime, path))
    #print("Done")



def debug():
    #cwd = os.getcwd()
    fileNames = [
        # '../levels/001.xml',
        '../levels/002.xml'
        # '../levels/003.xml',
        # '../levels/004.xml',
        # '../levels/005.xml',
        # '../levels/006.xml',
        # '../levels/007.xml',
        # '../levels/008.xml',
        # '../levels/009.xml',
        # '../levels/010.xml',
        # '../levels/011.xml',
        # '../levels/012.xml',
        # '../levels/013.xml',
        # '../levels/014.xml',
        # '../levels/015.xml',
        # '../levels/016.xml',
        # '../levels/017.xml',
        # '../levels/018.xml',
        # '../levels/019.xml',
        # '../levels/020.xml',
        # '../levels/021.xml',
        # '../levels/022.xml',
        # '../levels/023.xml',
        # '../levels/024.xml',
        # '../levels/025.xml',
        # '../levels/026.xml',
        # '../levels/027.xml',
        # '../levels/028.xml',
        # '../levels/029.xml'
    ]
    for f in fileNames:
        start(f)


def doAllFiles():
    folderName = '../levels/'
    for entry in os.scandir(folderName):
        if entry.is_file():
            start(entry.path)



def isImpossible(filename):
    started = time.process_time()
    level = Level(filename)
    graph = level.buildGraph()
    squares = level.getSquares()
    root = getRoot(graph)

    msg = ''
    if isSolvable(root,deepcopy(squares),deepcopy(graph)):
        msg = 'LEVEL CAN BE SOLVED'
    else:
        msg = 'IMPOSSIBLE LEVEL'
    elapsedTime = time.process_time() - started
    print("%s: %s, %s" % (filename, elapsedTime, msg))


# TODO: all the levels really all possible ?
# TODO: why do I need 7 visits for some levels? Should not be more than 4
# TODO: why do I not return the shortest solution when I increase MAX_STEPS? Debug using 002.xml
# TODO: Use isSolved as basis to build path?
def findAllPossibleLevels():
    folderName = '../levels/'
    for entry in os.scandir(folderName):
        if entry.is_file():
            isImpossible(entry.path)


debug()
#findAllPossibleLevels()
#doAllFiles()
