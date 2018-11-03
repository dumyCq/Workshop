# -*- coding:utf-8 –*-
# npuzzle.py
# let python print chinese
from importlib import reload
import search
import util
import time
import sys

reload(sys)
type = sys.getfilesystemencoding()

# Module Classes
global size

class NPuzzleState:
    def __init__(self, numbers):

        global size
        self.cells = []
        number = numbers[:]
        number.reverse()

        for row in range(size):
            self.cells.append([])
            for col in range(size):
                if len(number) != 0:
                    self.cells[row].append(number.pop())
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col

    def isGoal( self ):
        """
          Checks to see if the puzzle is in its goal state.

        """
        global size
        other = NPuzzleState(goal)
        for row in range( size ):
            for col in range( size ):
                if self.cells[row][col] != other.cells[row][col]:
                    return False
        return True


    def dis_Goal(self):
        global size
        dis = 0
        other = NPuzzleState(goal)

        # use manhattanDistance as heuristic
        for row in range(size):
            for col in range(size):
                if self.cells[row][col] == 0:
                    continue
                for r in range(size):
                    for c in range(size):
                        if self.cells[row][col] == other.cells[r][c]:
                            dis = dis + util.manhattanDistance((row, col), (r, c))
        return dis

    def euc_Goal(self):
        global size
        euc = 0
        other = NPuzzleState(goal)

        # use euclidDistance as heuristic
        for row in range(size):
            for col in range(size):
                if self.cells[row][col] == 0:
                    continue
                for r in range(size):
                    for c in range(size):
                        if self.cells[row][col] == other.cells[r][c]:
                            euc = euc + util.euclidDistance((row, col), (r, c))
        return euc

    def tri_Goal(self):
        global size
        tri = 0
        other = NPuzzleState(goal)

        # use triangleDistance as heuristic
        for row in range(size):
            for col in range(size):
                if self.cells[row][col] == 0:
                    continue
                for r in range(size):
                    for c in range(size):
                        if self.cells[row][col] == other.cells[r][c]:
                            tri = tri + util.triangleDistance((row, col), (r, c))
        return tri


    def heuristic(self):
        """return the heuristic function u choose"""
        # use euclidDistance as heuristic
        # return self.euc_Goal()

        # use triangleDistance as heuristic
        # return self.tri_Goal()

        # use manhattanDistance as heuristic
        return self.dis_Goal()


    def legalMoves( self ):

        global size
        moves = []
        row, col = self.blankLocation
        if(row != 0):
            moves.append('up')
        if(row != (size-1)):
            moves.append('down')
        if(col != 0):
            moves.append('left')
        if(col != (size-1)):
            moves.append('right')
        return moves

    def result(self, move):
        row, col = self.blankLocation
        if(move == 'up'):
            newrow = row - 1
            newcol = col
        elif(move == 'down'):
            newrow = row + 1
            newcol = col
        elif(move == 'left'):
            newrow = row
            newcol = col - 1
        elif(move == 'right'):
            newrow = row
            newcol = col + 1
        else:
            raise "Illegal Move"

        # Create a copy of the current NPuzzle
        global size
        l = [0] * size * size
        # print l
        newPuzzle = NPuzzleState(l)
        newPuzzle.cells = [values[:] for values in self.cells]
        # And update it to reflect the move
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

    # Utilities for comparison and display
    def __eq__(self, other):

        global size
        for row in range( size ):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __str__(self):
        lines = ''
        for row in self.cells:
            for col in row:
                lines = lines + str(col) + ' '
            lines = lines + '\n'
        return lines

class NPuzzleSearchProblem(search.SearchProblem):

    def __init__(self,puzzle):

        self.puzzle = puzzle

    def getStartState(self):
        return puzzle

    def isGoalState(self,state):
        return state.isGoal()

    def getSuccessors(self, state):

        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):

        return len(actions)

    def getHeuristic(self, state):
        return state.heuristic()

def createNPuzzle(start, goal):
    # initial npuzzle
    global size
    # python read path with Chinese name
    path = 'C:\\Npuzzle_in.txt'
    path = unicode(path, "utf8")
    f = open(path)
    size = int(f.readline())
    for i in range(size):
        # read the initial state
        start += map(int, f.readline().split(' '))
    for j in range(size):
        # read the goal state
        goal += map(int, f.readline().split(' '))

    puzzle = NPuzzleState(start)
    return puzzle

def judge(start, goal):
    # judge whether problem has solution
    puzzle_s = NPuzzleState(start)
    puzzle_g = NPuzzleState(goal)
    diff = puzzle_s.blankLocation[0] - puzzle_g.blankLocation[0]
    num_s = 0
    num_g = 0
    for i in range(len(start)):
        for j in range(len(start)-i-1):
            if (start[i] > start[i+j+1]) and start[i] != 0 and start[i+j+1] != 0:
                num_s += 1
                # print start[i], start[i+j+1]

    for i in range(len(goal)):
        for j in range(len(goal)-i-1):
            if goal[i] > goal[i+j+1] and goal[i] != 0 and goal[i+j+1] != 0:
                num_g += 1
                # print goal[i], goal[i+j+1]
    # print num_s, num_g
    if (size % 2) != 0:
        if (num_s % 2) == (num_g % 2):
            return True
    else:
        if ((diff % 2 == 0) and (num_s % 2) == (num_g % 2)) or ((diff % 2 != 0) and (num_s % 2) != (num_g % 2)):
            return True
    return False

if __name__ == '__main__':
    starttime = time.time()
    # programm running

    global size
    start = []
    goal = []
    puzzle = createNPuzzle(start, goal)

    if judge(start, goal):
        problem = NPuzzleSearchProblem(puzzle)
        path = search.aStarSearch(problem)
        sc = open('C:\\Npuzzle_out.txt','w+')
        sc.write("共" + str(len(path)) + "步"+"\n")
        sc.write("初始状态"+"\n" )
        print>> sc,puzzle
        curr = puzzle
        i = 1
        for a in path:
            curr = curr.result(a)
            if i == len(path):
                sc.write( "目标状态"+"\n")
                print>>sc,curr
                break
            sc.write("第" + str(i) + "步"+"\n")
            print>> sc, curr
            i += 1
    else:
        sc = open('D:\\Npuzzle_out.txt', 'w+')
        sc.write("无解")

    # print running time
    endtime = time.time()
    print("running time：" + str(endtime - starttime))



