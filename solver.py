import time
from subprocess import *
import sys, io

class HyperSudoku:
    
    
    def forwardChecking(grid, i, j):
        """
        Given a 2d-list grid and index of a single entry, return a list of 
        all possible values for the entry.
        """
        possibilities = {}
        domain = []
        degree = 3
        
        # Assume all possiblities valid by default
        for num in range(1,10):
            possibilities[num] = True
        
        # ____Check row to determine possible values____
        for x in range (9):
            # Eliminate option if vlaue exists in row
            if grid[x][j] != 0:
                possibilities[grid[x][j]] = False
        
        # ____Check column to determine possible values____
        for y in range (9):
            # Eliminate option if value exists in column
            if grid[i][y] != 0:
                possibilities[grid[i][y]] = False
        
        # ___Check 3x3 normal block for possible values____
        
        # Define range of corresponding 3x3 normal block
        starti = i - (i % 3)
        endi = i + (2 - (i % 3)) +1
        
        startj = j - (j % 3)
        endj = j + (2 - (j % 3)) +1
        
        # Check possibitlies within normal block
        for x in range(starti, endi):
            for y in range(startj, endj):
                # eliminate possiblity if value exists in regular block
                if grid[x][y] != 0:
                    possibilities[grid[x][y]] = False
        
        # ____Check 3x3 hyper block for possible values____
        
        # If entry exists inside a hyper block
        if str(i) in "123567" and str(j) in "123567":
            # Increase degree by 1
            degree += 1
            
            # Define range of corresponding 3x3 hyper block
            if i <= 3:
                starti = 1
                endi = 4
            elif i <= 7:
                starti = 5
                endi = 8
            
            if j <= 3:
                startj = 1
                endj = 4
            elif j <= 7:
                startj = 5
                endj = 8
                
            # Check possibitlies within hyper block
            for x in range(starti, endi):
                for y in range(startj, endj):
                    if grid[x][y] != 0:
                        possibilities[grid[x][y]] = False

        # Create domain list in an increasing order
        for num in possibilities:
            if possibilities[num]:
                domain.append(num)
         
        return domain, degree
        
    def isSolved(grid):
        '''
        Return true if a Sudoku grid is fully solved
        '''
        check = True
        # Check for 0 within grid
        # If at least one 0 exists, return false
        for i in range(len(grid[0])):
            blankFound = False
            for j in range(len(grid)):
                if grid[i][j] == 0:
                    check = False
                    blankFound = True
                    break
            if blankFound:
                break
            
        return check
                
    def selectVariable(grid):
        '''
        Select unassigned value using minimum remaining value heuristic
        and then degree heuristic
        '''
        minDomain = 0
        # Each item in these lists is a list containing 2 values [x,y]
        # representing the coordinate
        min_lst = []
        deg_lst = []
        
        # Minimum remaining value heuristic
        for m in range(9):
            for n in range(9):
                if grid[m][n] == 0:
                    domain = HyperSudoku.forwardChecking(grid,m,n)[0]
                    if 0 < len(domain) < minDomain or minDomain == 0:
                        minDomain = len(domain)
                        min_lst = [[m,n]]
                    elif len(domain) == minDomain:
                        min_lst.append([m,n])
        if len(min_lst) == 1:
            return min_lst[0][0], min_lst[0][1]
        # Degree heuristic
        else:
            max_degree = 3
            for coordinate in min_lst:
                degree = HyperSudoku.forwardChecking(grid,coordinate[0],coordinate[1])[1]
                if degree > max_degree:
                    deg_lst.append(coordinate)
            # If after applying both heuristics, there are more than one candidates,
            # just select the first one in the list
            if len(deg_lst) >= 1:
                return deg_lst[0][0], deg_lst[0][1]
            else:
                return min_lst[0][0], min_lst[0][1]

    def solver_function(grid):
        """
        Provides solutions for a given Sudoku grid, returns as list of lists,
        values are strings.
        
        Called by solve() 
        """
        if not HyperSudoku.isSolved(grid):
            
            # find indexes of next "0" entry
            i,j = HyperSudoku.selectVariable(grid)
            
            # check all possibilities at entry
            domain = HyperSudoku.forwardChecking(grid, i, j)[0]
            
            for num in domain:
                grid[i][j] = num
                grid = HyperSudoku.solver_function(grid)
            
            # A violation/error occurs at this point
            # Backtrack to explore other possiblities
            grid[i][j] = 0
        
        # Fully solved
        else:
            print(grid)
        
        return grid        
        
    
    def solve(grid):
        """
        Solve the given grid. Change 0 into suitable number.
        If no solution, return None
        """
        # Create new list to store solution
        solution = []
        for i in range(9):
            solution.append([])
        
        stdout = sys.stdout
        sys.stdout = io.StringIO()
       
        # Call solver function
        HyperSudoku.solver_function(grid)
        
        # Capture stdout as string
        output = sys.stdout.getvalue()
        sys.stdout = stdout

        nums_visited = 0
        row= 0
        # Manually store each integer value from grid string to list
        for char in output:
            if char in "0123456789":
                solution[row].append(int(char))
                nums_visited += 1
                if nums_visited % 9 == 0:
                    row += 1
            
        # If list is empty, ie unsolvable grid
        if len(solution[0]) == 0:
            solution = None
                      
        return solution
      
    def printGrid(grid):
        """
        Prints out the grid 
        """
        print("-"*25)
        for i in range(9):
            print("|", end=" ")
            for j in range(9):
                print(grid[i][j], end =" ")
                if (j % 3 == 2): 
                    print("|", end=" ")
            print()
            if (i % 3 == 2):
                print("-"*25)

""" Get initial grid from input file and solve """
filename = input("Enter input file: ")
myFile = open(filename, 'r')
grid = []
Lines = myFile.readlines()
numLine = 0
for line in Lines:
    numLine += 1
    if numLine < 10:
        line = line.strip().split(' ')
        line = [int(i) for i in line]
        grid.append(line)
sol = HyperSudoku.solve(grid)
myFile.close()
if sol is not None:
    HyperSudoku.printGrid(sol)

""" Create and write output file """
outName = input("Enter output file name: ")
outFile = open(outName,'w')
if sol is None:
    outFile.write("No Solution\n")
else:
    for line in sol:
        for num in line:
            outFile.write("%d " % num)
        outFile.write("\n")
outFile.close()
