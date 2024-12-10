puzzleInput = list(map((lambda line : line.strip()), open("./day10.txt", "r").readlines()))


class tile:
    def __init__(self, tileType, x, y):
        self.tile = tileType
        self.x = x
        self.y = y
        self.inside = False

    def __str__(self):
        return f'Tile Type: {self.tile} at Position: ({self.x}, {self.y})'

    def getNeighborTiles(self, grid):
        
        match self.tile:
            case "|":
                self.neighbors = [getPosition(grid, self.x, self.y-1), getPosition(grid, self.x, self.y+1)]

            case "-":
                self.neighbors = [getPosition(grid, self.x-1, self.y), getPosition(grid, self.x+1, self.y)]

            case "L":
                self.neighbors = [getPosition(grid, self.x, self.y-1), getPosition(grid, self.x+1, self.y)]

            case "J":
                self.neighbors = [getPosition(grid, self.x, self.y-1), getPosition(grid, self.x-1, self.y)]

            case "7":
                self.neighbors = [getPosition(grid, self.x, self.y+1), getPosition(grid, self.x-1, self.y)]

            case "F":
                self.neighbors = [getPosition(grid, self.x+1, self.y), getPosition(grid, self.x, self.y+1)]

            case ".":
                self.neighbors = []

    def get_S_type(self, grid):
        n = grid[self.y-1][self.x].tile
        e = grid[self.y][self.x+1].tile
        s = grid[self.y+1][self.x].tile
        w = grid[self.y][self.x-1].tile
        options = ["|", "-", "L", "J", "7", "F"]
        if n in ["|", "7", "F"]:
            options = [i for i in options if i not in ["-", "7", "F"]]
            #print(f'north value: {n}, options: {options}')

        if e in ["-", "J", "7"]:
            options = [i for i in options if i not in ["J", "7", "|"]]
            #print(f'east value: {e}, options: {options}')

        if s in ["|", "J", "L"]:
            options = [i for i in options if i not in ["-", "L", "J"]]
            #print(f'south value: {s}, options: {options}')

        if w in ["-", "L", "F"]:
            options = [i for i in options if i not in ["|", "L", "F"]]
            #print(f'west value: {w}, options: {options}')

        assert(len(options) == 1)
        self.tile = options[0]

def createGrid(puzzleInput):
    grid = []
    row = []
    x_count = 0
    y_count = 0
    for line in puzzleInput:
        for char in line:
            row.append(tile(char, x_count, y_count))
            x_count += 1
        x_count = 0
        grid.append(row)
        row = []
        y_count += 1

    return grid

def printGrid(grid):
    for row in grid:
        for item in row:
            print(item)

def getPosition(grid, x, y):
    #print(grid[y][x])
    return grid[y][x]

def findSPosition(grid):
    x_count = 0
    y_count = 0
    for row in grid:
        for item in row:
            if item.tile == "S":
                print(f'Found "S" at: ({x_count}, {y_count})')
                return item

            x_count += 1
        x_count = 0
        y_count += 1

def getNextTile(curr, prev):
    #neighbor_1 = curr.neighbors[0]
    #neighbor_2 = curr.neighbors[1]
    #print(f'Current:   {curr}')
    #print(f'Previous:  {prev}')
    #print(f'neigh 1:   {neighbor_1}')
    #print(f'neigh 2:   {neighbor_2}')
    #if neighbor_1 == prev:
    #    return neighbor_2
    #else:
    #    return neighbor_1
    try:
        for i in curr.neighbors:
            if i != prev:
                return i
    except:
        print("You done fucked up")
        print(f'Current:   {curr}')
        print(f'Previous:  {prev}')

def mapLoop(grid, start):
    
    currTile = start.neighbors[0]
    #print(currTile)

    prevTile = start
    startFound = 0
    count = 0
    while (not startFound):
        #print(currTile)
        temp = currTile 
        currTile = getNextTile(currTile, prevTile)
        #print(currTile)
        prevTile = temp
        #print(currTile)
        count += 1
        if currTile == start:
            print("Start Found")
            print(f'Previous Tile: {prevTile}')
            startFound = 1
    return count
    
def mapNeighbors(grid):
    for row in grid:
        for item in row:
            #print(item)
            item.getNeighborTiles(grid)

def padInput(puzzleInput):
    paddedInput = []
    padRow = list((len(puzzleInput[0])+2) * ".")
    paddedInput.append(padRow)
    padCol = len(puzzleInput)
    for row in puzzleInput:
        paddedRow = ["."]
        paddedRow.extend(row)
        paddedRow.extend(".")
        paddedInput.append(paddedRow)

    paddedInput.append(padRow)
    return paddedInput

def doPart1():

    # create the grid
    print("Creating the grid with padded input")
    grid = createGrid(padInput(puzzleInput))
    #for line in padInput(puzzleInput):
    #    print(line)
    # get the starting tile and convert it
    print("Getting starting tile")
    S_tile = findSPosition(grid)
    S_tile.get_S_type(grid)
    S_tile.getNeighborTiles(grid)
    print(S_tile)
    print("Getting S_tile nieghbors")
    for item in S_tile.neighbors:
        print(item)
    # give everyone in the grid neighbors 
    print("Getting all neighbors")
    mapNeighbors(grid)
    # map the loop
    print("Going through the loop")
    length = mapLoop(grid, S_tile)
    print(f'Total Loop Length: {length+1}')
    print(f'Part 1 Result: {(length+1)/2}')


doPart1()

def mapLoopPart2(grid, start):
    
    currTile = start.neighbors[0]
    #print(currTile)

    prevTile = start
    startFound = 0
    count = 0
    loop = [start]
    while (not startFound):
        temp = currTile 
        currTile = getNextTile(currTile, prevTile)
        prevTile = temp
        count += 1
        if currTile == start:
            #print("Start Found")
            #print(f'Previous Tile: {prevTile}')
            startFound = 1
        loop.append(currTile)
    return loop



def checkInsideLoop(grid, loop):
    outside = set()
    for y_count, row in enumerate(grid):
        within = False
        up = None
        for x_count, itemTile in enumerate(row):
            item = itemTile.tile

            if item == "|":
                assert up is None
                within = not within
 
            elif item == "-":
               assert up is not None

            elif item in "LF":
                #print(f'Fails: {itemTile}')
                assert up is None
                up = item == "L"

            elif item in "7J":
                assert up is not None
                if item != ("J" if up else "7"):
                    within = not within
                up = None

            elif item == ".":
                pass

            else:
                raise RuntimeError(f"unexpected character (horizontal): {item}")

            if not within:
                outside.add((x_count, y_count))

    loopCoords = []
    for item in loop:
        loopCoords.append((item.x, item.y))

    loopSet = set(loopCoords)
    # change length because of the padding I did
    len_col = len(grid)
    print("len_col: {}".format(len_col))

    len_row = len(grid[0])
    print("len_row:  {}".format(len_row))

    len_grid = len_col * len_row
    print("len_grid: {}".format(len_grid))

    len_out = len(outside)
    print("len_out: {}".format(len_out))

    len_loop = len(loopSet)
    print("len_loop: {}".format(len_loop))

    len_out_loop = len(outside | loopSet)
    print("len_out_loop: {}".format(len_out_loop))

    inside_total = (len_grid) - len_out_loop
    print(f'Part 2 Result: {inside_total}')

def convertOutsideLoop(grid, loop):
    for row in grid:
        for item in row:
            if item not in loop:
                item.tile = "."


def doPart2():

    # create the grid
    print("Creating the grid with padded input")
    grid = createGrid(padInput(puzzleInput))
    
    print("Getting starting tile")
    S_tile = findSPosition(grid)
    S_tile.get_S_type(grid)
    S_tile.getNeighborTiles(grid)
    
    print("Getting all neighbors")
    mapNeighbors(grid)
    
    print("Going through the loop")
    loop = mapLoopPart2(grid, S_tile)
    print(len(loop)/2)

    print("Checking if constrained by Loop")
    convertOutsideLoop(grid, loop)
    checkInsideLoop(grid, loop)


doPart2()
