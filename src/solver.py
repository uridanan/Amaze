from src.level import Level
import os

MAX_STEPS = 100
RIGHT, LEFT, UP, DOWN = 1,2,3,4
DIRECTIONS = [RIGHT,DOWN,LEFT,UP]

class cursor:
    level = None
    x = 0
    y = 0
    used = False

    def __init__(self,level,x,y):
        self.x = x
        self.y = y
        self.level = level
        self.level.myWorkHereIsDone(self.x,self.y)  #color the starting point

    def right(self):
        self.y = self.y + 1

    def left(self):
        self.y = self.y - 1

    def up(self):
        self.x = self.x-1

    def down(self):
        self.x = self.x + 1

    def step(self,direction):
        if direction == RIGHT:
            self.right()
        elif direction == LEFT:
            self.left()
        elif direction == UP:
            self.up()
        else:  # direction == DOWN:
            self.down()
        self.used = True
        self.level.myWorkHereIsDone(self.x, self.y)

    def peek(self,direction):
        switcher = {
            RIGHT: [self.x, self.y + 1],
            LEFT: [self.x, self.y - 1],
            UP: [self.x - 1, self.y],
            DOWN: [self.x + 1, self.y]
        }
        return switcher[direction]

    def isWall(self,direction):
        x, y = self.peek(direction)
        return self.level.get(x, y) == 0

    def outOfBounds(self,direction):
        x, y = self.peek(direction)
        return x == -1 or x == self.level.getHeight() or y == -1 or y == self.level.getWidth()

    def inPlay(self,direction):
        return not self.isWall(direction) and not self.outOfBounds(direction)


def go(direction,x,y,solution,level):
    print("go", direction, x, y, solution)
    cur = cursor(level,x,y)
    while cur.inPlay(direction):
        cur.step(direction)
    if not cur.used:
        return None

    solution.append(direction)

    if level.isDone():
        return solution
    else:
        return next(cur.x,cur.y,solution,level)


def noSolution(solution):
    return safeLen(solution)+1 > MAX_STEPS

# TODO: prevent long loops, why are repeats still happening?
# TODO: optimize by starting with the longest dimension
# TODO: optimize with multithreading one thread per file
# TODO: move methods into level or create a cursor class
# Return none if no solution, int[] otherwise
# Solution length < 101
def next(x,y,solution,level):
    print("Next",x,y,solution)
    if noSolution(solution):
        return None

    #Compute next step
    usefulDirections = DirectionsFilter(solution).filter()

    solutions = {}
    for d in usefulDirections:
        solutions[d] = go(d,x,y,solution,level)

    # Return shortest solution or none
    rVal = None
    for d in usefulDirections:
        rVal = shorter(rVal,solutions[d])

    return rVal


class DirectionsFilter:
    directions = None
    solution = None

    def __init__(self,solution):
        self.solution = solution
        self.directions = DIRECTIONS.copy()

    def rotate(self):
        first = self.directions[0]
        del self.directions[0]
        self.directions.append(first)

    # No point in doing the same direction that just hit a wall
    def preventRepeats(self):
        if self.solution is None or len(self.solution) == 0:
            return
        self.directions.remove(self.solution[-1])

    def preventLoops(self, d1, d2):
        if self.solution is None or len(self.solution) < 3:
            return
        if self.solution[-1] == d1 and self.solution[-2] == d2 and self.solution[-3] == d1:
            self.directions.remove(d2)

    def filter(self):
        self.rotate()
        self.preventRepeats()
        self.preventLoops(RIGHT,LEFT)
        self.preventLoops(LEFT, RIGHT)
        self.preventLoops(UP, DOWN)
        self.preventLoops(DOWN, UP)
        return self.directions


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


def start(level):
    empty = []
    solution = next(level.ballXStartLocation,level.ballYStartLocation,empty,level)
    print("Solution:")
    print(solution)

def debug():
    cwd = os.getcwd()
    level1 = Level('../levels/007.xml')
    start(level1)
    print('stop')

debug()