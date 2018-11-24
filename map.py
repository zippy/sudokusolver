class OffBoardException(Exception):
    pass

class Board:
    def __init__(self, filename):
        self.filename = filename
        self.tiles = [["\0" for x in range(9)] for y in range(9)]

    def loadBoard(self):
        try:
            file = open(self.filename)
            y = 0      # y is different than lineno as some lines may be comments
            for line in file:
                if (y >= 9):
                    parts = line.split()

                else:
                    if (len(line) < 10):
                        print(f"Line {y} of map is malformed")
                        exit(1)
                    for x in range(9):
                        self.tiles[y][x] = line[x]#, x, y
                y += 1
            file.close()
        except:
            print(f"Could not load map file {self.filename}")
            exit(1)

    # gets tile
    def getTile(self, x, y): return self.tiles[y][x]

    # sets a tile
    def setTile(self, x, y, value): self.tiles[y][x] = value

    # returns a list of all items in a given row, 0 through 8
    # starting from the top
    def getRow(self, row):
        if row > 8:
            raise OffBoardException
        return self.tiles[row]

    # returns a list of all items in a given column, 0 through 8
    # starting from the left
    def getColumn(self, x):
        if x > 8:
            raise OffBoardException
        out = []
        for y in self.tiles:
            out += [y[x]]
        return out

    # Gets a list of all the items in a given box. Boxes like so:
    # 0 | 1 | 2
    #---+---+---
    # 3 | 4 | 5
    #---+---+---
    # 6 | 7 | 8
    def getBox(self,boxID):
        # check if boxID is valid
        if boxID > 8:
            raise OffBoardException
        out = []
        xStart = x = boxID%3*3
        y = int(boxID/3)*3
        yEnd = y + 3
        xEnd = x + 3
        while y < yEnd:
            while x < xEnd:
                out += [self.getTile(x,y)]
                x += 1
            y+= 1
            x = xStart
        return out

    def prepare(self):
        for y in self.tiles:
            x = 0
            while x < 9:
                if y[x] == ".": y[x] = "123456789"
                x += 1

    # returns whether the tile is "sure" (the tile has only one value)
    def isSure(self,tile):
        return len(tile)==1

    def calculateBoxID(self, x,y):
        return int(y/3)*3 + int(x/3)

    # If the tile isn't sure, removes numbers from the tile
    # which we see as sure in the current tile's column, row, or
    # box. Returns number of numbers removed.
    def removeImpossibles(self, x, y):
        tile = self.getTile(x,y)
        originalLength = len(tile)
        # don't do anything and return 0 if tile is sure
        if self.isSure(tile):
            return 0
        # add numbers we see to a big list
        c = self.getColumn(x)
        r = self.getRow(y)
        b = self.getBox(self.calculateBoxID(x,y))
        l = c + r + b
        # strip unsure tiles from the list
        l = [possib for possib in l if len(possib) == 1]
        # walk through the list and remove numbers we find from
        # current tile
        for possib in l:
            tile = tile.replace(possib,"")
        self.setTile(x,y, tile)
        return originalLength - len(tile)

    def removeAll(self):
        done = False
        while not done:
            c = 0
            for y in range(9):
                for x in range(9):
                    c += self.removeImpossibles(x,y)
            if c == 0: done = True

    # print out a map pretty
    def __str__(self):
        out = "\n"
        h = 1 # horizontal lines
        for x in self.tiles:
            v = 1 # vertical lines
            for y in x:
                if len(y) != 1: out += "."
                else: out += f"{y}"
                if v%3 == 0 and v <= 8:
                    out += " | "
                v += 1
            if h%3 == 0 and h <= 8:
                out += "\n----+-----+----"
            h += 1
            out += "\n"
        return out
