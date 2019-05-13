from src.level import Level


class Solver:
    # 0=white square 1=black square.
    # The ball moves on black squares
    # x is the index of the row, y the index of the column
    # The method should return null if the level is non solveable
    # 1 = right, 2= left, 3 = up, 4 = down
    solution = []
    level = None
    x = 0
    y = 0

    def __init(self,l):
        self.level = l
        self.x = self.level.ballXStartLocation
        self.y = self.level.ballYStartLocation

    # Returns True if the puzzle is solved
    def isDone(self):
        if self.level.virgin(self.x, self.y):
            self.level.beenThere(self.x, self.y)
            return self.level.decreaseCount()
        return False

    # Returns True if the puzzle is solved
    def goRight(self,depth):
        self.solution.append(1)
        while self.level.get(self.x,self.y) > 0 and self.y < self.level.getWidth():
            if self.isDone():
                return True
            self.y = self.y + 1


    # Returns True if the puzzle is solved
    def goLeft(self,depth):
        self.solution.append(2)
        while self.level.get(self.x,self.y) > 0 and self.y > -1 :
            if self.isDone():
                return True
            self.y = self.y - 1

    # Returns True if the puzzle is solved
    def goUp(self,depth):
        self.solution.append(3)
        while self.level.get(self.x,self.y) > 0 and self.x > -1:
            if self.isDone():
                return True
            self.x = self.x - 1

    # Returns True if the puzzle is solved
    def goDown(self,depth):
        self.solution.append(4)
        while self.level.get(self.x,self.y) > 0 and self.x < self.level.getHeight():
            if self.isDone():
                return True
            self.x = self.x + 1


def goRight(self,depth):
    self.solution.append(1)
    while self.level.get(self.x,self.y) > 0 and self.y < self.level.getWidth():
        if self.isDone():
            return True
        self.y = self.y + 1


# TODO : optimize by starting with the longest dimension
# Return none if no solution, int[] otherwise
# Solution length < 101
def next(depth,x,y,solution,level):
    if depth == 101: # solution exceeds 100 steps
        return None

    right = goRight(depth + 1)
    down = goDown(depth + 1)
    left = goLeft(depth + 1)
    up = goUp(depth + 1)

    # return shortest solution or none
    rVal = right
    # if right is not None and len(right) > 0:
    #     rVal = right
    if down is not None and len(down) < len(rVal):
        rVal = down
    if left is not None and len(left) < len(rVal):
        rVal = left
    if up is not None and len(up) < len(rVal):
        rVal = up

    return rVal


def start(level):
    solution = next(1,level.ballXStartLocation,level.ballYStartLocation,[None],level)