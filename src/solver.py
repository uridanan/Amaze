from src.level import Level
import os

MAX_STEPS = 100
RIGHT, LEFT, UP, DOWN = 1,2,3,4
DIRECTIONS = [RIGHT,DOWN,LEFT,UP]

# class cursor:
#     # 0=white square 1=black square.
#     # The ball moves on black squares
#     # x is the index of the row, y the index of the column
#     # The method should return null if the level is non solveable
#     # 1 = right, 2= left, 3 = up, 4 = down
#     solution = []
#     level = None
#     x = 0
#     y = 0
#
#     def __init(self,l):
#         self.level = l
#         self.x = self.level.ballXStartLocation
#         self.y = self.level.ballYStartLocation
#
#     # Returns True if the puzzle is solved
#     def isDone(self):
#         if self.level.virgin(self.x, self.y):
#             self.level.beenThere(self.x, self.y)
#             return self.level.decreaseCount()
#         return False
#
#     # Returns True if the puzzle is solved
#     def goRight(self,depth):
#         self.solution.append(1)
#         while self.level.get(self.x,self.y) > 0 and self.y < self.level.getWidth():
#             if self.isDone():
#                 return True
#             self.y = self.y + 1
#
#
#     # Returns True if the puzzle is solved
#     def goLeft(self,depth):
#         self.solution.append(2)
#         while self.level.get(self.x,self.y) > 0 and self.y > -1 :
#             if self.isDone():
#                 return True
#             self.y = self.y - 1
#
#     # Returns True if the puzzle is solved
#     def goUp(self,depth):
#         self.solution.append(3)
#         while self.level.get(self.x,self.y) > 0 and self.x > -1:
#             if self.isDone():
#                 return True
#             self.x = self.x - 1
#
#     # Returns True if the puzzle is solved
#     def goDown(self,depth):
#         self.solution.append(4)
#         while self.level.get(self.x,self.y) > 0 and self.x < self.level.getHeight():
#             if self.isDone():
#                 return True
#             self.x = self.x + 1




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

    def isWall(self):
        return self.level.get(self.x, self.y) == 0

    def outOfBounds(self):
        return self.x == -1 or self.x == self.level.getHeight() or self.y == -1 or self.y == self.level.getWidth()

    def inPlay(self):
        return not self.isWall() and not self.outOfBounds()


def go(direction,x,y,solution,level):
    print("go", direction, x, y, solution)
    cur = cursor(level,x,y)
    while cur.inPlay():
        cur.step(direction)
    if not cur.used:
        return None

    solution.append(direction)

    if level.isDone():
        return solution
    else:
        return next(cur.x,cur.y,solution,level)


def noSolution(solution):
    return len(solution)+1 > MAX_STEPS

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
    solutions = {}
    for d in DIRECTIONS:
        solutions[d] = go(d,x,y,solution,level)

    # Return shortest solution or none
    rVal = None
    for d in DIRECTIONS:
        rVal = shorter(rVal,solutions[d])

    return rVal

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


def start(level):
    empty = []
    solution = next(level.ballXStartLocation,level.ballYStartLocation,empty,level)
    print(solution)

def debug():
    cwd = os.getcwd()
    level1 = Level('../levels/007.xml')
    start(level1)
    print('stop')

debug()