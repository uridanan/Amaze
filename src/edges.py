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
MAX_STEPS = 5

class Level:
    # 0=white square 1=black square.
    # The ball moves on black squares
    # x is the index of the row, y the index of the column
    squares = None
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
        n = self.getNode(x, y)
        e.end = n
        e.start.edges[e.getId()] = e
        self.edges[e.getId()] = e
        print("Close Edge: %d,%d" % (e.start.id,e.end.id))
        return None

    def processSquare(self,x,y,d,e):
        if self.squares[x][y] == 0:
            if e is not None:
                # create a node for the previous square and close the edge
                ex,ey = Node(id,x,y).peek(opposite(d))
                if safeLen(e.squares) > 1:
                    e = self.closeEdge(ex,ey,e)
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

    # TODO: Circular infinite loop: iterate edges while adding edges
    def findAllOrthogonalEdges(self):
        print("Search for orthogonal edges")
        for e in list(self.edges.values()):
            self.findOrthogonalEdges(e)

    # Some nodes can only be starting nodes because they close an edge
    def findOrthogonalEdges(self,e):
        if e is None or e.end is None:
            print("ERROR ! Invalid open edge")
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

    def getSquares(self):
        squares = {}
        for x in range(self.height):
            for y in range(self.width):
                if self.squares[x][y] > 0:
                    squares[self.id(x,y)] = 1
        return squares




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
    return switcher[direction]
    

class Node:
    id = -1
    x = -1
    y =-1
    edges = None


    def __init__(self,id,x,y):
        self.id = id
        self.x = x
        self.y = y
        self.edges = dict()

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

    def __init__(self,node,d):
        self.start = node
        self.dir = d
        self.end = None
        self.squares = []

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


def startBFS(graph):
    r = getRoot(graph)
    path = []
    solution = bfs(graph,[r],path)


def bfs(graph,nodes,path):
    next = []
    for n in nodes:
        for e in n.edges:
            next.append(e.end)
    return path



def start(graph,level):
    path = []
    squares = level.getSquares()
    root = getRoot(graph)
    path = traverse(root,squares,path,graph)
    print("Solution: %s" % path)
    print("Done")


# Pop squares traversed by edges, not Nodes
# Iterate edges, not neighbours
# TODO: Try BFS against DFS
# TODO: Why won't it try [1,4,2,4,1,3,2,1,2,3,1] ?
# TODO: why won't stop at MAX_STEPS? why won't try 1,4,2,4?
# TODO: how do I handle path is None on return?
def traverse(root,squares,path,graph):
    print(path)

    # If graph is empty, we are done
    if safeLen(squares) == 0:
        print("Graph is empty")
        return path

    # If path exceeds limit, there is no solution here
    if safeLen(path) > MAX_STEPS:
        print("Path exceeds limit")
        return None

    # If root is none: error, should not happen
    if root is None:
        print("ERROR ! Invalid root")
        return None

    # Mark our visit here
    found = squares.pop(root.id,None)

    # We're stuck in a loop, no solution here
    if found is None and isStuckInLoop(path):
        print("ERROR ! Stuck in loop")
        return None

    # Visit the neighbours
    paths = {}
    reverse = None
    for e in root.edges.values():
        if safeLen(path) > 1 and e.dir == opposite(path[-1]):
            # leave the return path for last
            reverse = e
        else:
            for s in e.squares:
                squares.pop(s, None)
            # don't append on same instance otherwise it is shared between all siblings. i.e. siblings are queued instead of replacing each other
            paths[e.dir] = traverse(e.end,squares,list(path).append(e.dir),graph)
    # Process the return edge
    if reverse is not None:
        e = reverse
        paths[e.dir] = traverse(e.end, squares, list(path).append(e.dir), graph)

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


# TODO: make sure not to include nodes / neigbours in the graph when you can't stop on them
# TODO: use MAX_STEPS as a parameter to find the solution faster
# TODO: identify loops on the fly?
# TODO: is visited useless?
def debug():
    cwd = os.getcwd()
    level1 = Level('../levels/007.xml')
    root = level1.buildGraph()
    start(root,level1)
    print('stop')

debug()
