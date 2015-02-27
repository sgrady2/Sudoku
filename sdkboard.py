"""
Sudoku Board. Assignment for week 8, CIS 210
Author: Thomas Rowland and Michael McGirr
Date: February 2013 for Winter, CIS 210

This functions as a Sudoku board checker. This program will check for
violations of the Sudoku solution rules.
"""
# Global Constants
DIGITS = frozenset('123456789')
OPEN = '.'
SYMBOLS = frozenset('.123456789')

class Tile:
    """One tile on a Sudoku board.
    Public data atributes: 
        row: integer 0..8  (position on board, read only after creating)
        col: integer 0..8  (position on board, read only after creating)
        symbol: String 1-9 or '.'  (read-write in solver)
        possible: set of possible symbols that could be here (read-write in solver)
    """
    def __init__(self, row, col, sym):
        self.row = row
        self.col = col
        self.symbol = sym
        self.listeners = [] 
        if sym == OPEN:
            self.possible = set(DIGITS)
        else:
            self.possible = {self.symbol}
            
    def __str__(self):
        return self.symbol
              
    def announce(self, event):
        """Announce an event (string) to each registered listener.
        Arguments:
            event: A string describing this event. Currently the
                only possible value is "duplicate", to indicate that
                this tile has been marked as a duplicate.
        """
        for func in self.listeners:
            func(self, event)
            
    def register(self, listener):
        """Register a listener callback function.
        Arguments:
            listener(tile,event): Function that reacts to a
                an event (identified by a string) on this tile.
        """
        self.listeners.append(listener)
    
class Board:
    """9 x 9 grid of Sudoku tiles.
    Public Attributes: 
        tiles:  a list of lists of Tile objects, organized by row
        groups: a list of lists of Tile objects.
             Each group is a row, a column, or a block (sub-square).
             Note that each Tile object will belong to three different
             groups, but in Sudoku the groups are treated exactly the 
             same.  
    """
    def __init__(self, symbols):
        """Constructor from a sequence of 9 sequences of 9 symbols."""
        rowcount = 0
        self.tiles = [ ] 
        for row in symbols:
            colcount = 0
            cols = [ ]
            for col in row:
                if not (col in SYMBOLS):
                    raise ValueError("Invalid sudoku symbol: " + col )
                cols.append(Tile(rowcount, colcount, col))
                colcount += 1
            if colcount != 9: 
                raise ValueError("Length of row is wrong: '" + row + "'")
            self.tiles.append(cols)
            rowcount += 1
        if rowcount != 9:
            raise ValueError("Wrong number of rows")
        
        # Master list, everything gets appended to it
        self.groups = [ ]
        # Row groups
        for row in self.tiles:
            self.groups.append(row)
        # Column groups
        for col in range(9):
            columns = [ ]
            for r in self.tiles:
                tile = r[col]
                columns.append(tile)
            self.groups.append(columns)
        # Block groups
        for start_row in [0, 3, 6]:
            for start_col in [0, 3, 6]:
                sq_tiles = [ ] 
                for row in range(3):
                    for col in range(3):
                        t = self.tiles[start_row + row][start_col+col]
                        sq_tiles.append(t)
                self.groups.append(sq_tiles)

    @classmethod
    def from_file(cls, f):
        """Factory method: Read a Sudoku board from a file.
        Arguments: 
            f: file to read the Sudoku board from
        Returns: a Board object with tiles from the file
        """
        lines = [ ] 
        for line in f: 
            lines.append( line.strip() )
        return Board(lines)
        
    def unique_choices(self, group):
        """Check a list of 9 tiles for unique symbols.
        Arguments: 
             group: list of 9 tiles
             
        Returns: boolean "True" if each tile symbol is unique in the list, 
                otherwise "False"
        Effect:  If a tile symbol is duplicated, a "duplicate" event
                will be announced through the tile. 
        """
        ok = True
        dict_announce = { }
        for tile in group:
            sym = tile.symbol
            if sym != OPEN:  
                if sym in dict_announce:
                    dict_announce[sym] += 1
                else:
                    dict_announce[sym] = 1
        for tile in group:
            sym = tile.symbol
            if sym in dict_announce:
                if dict_announce[sym] > 1:
                    ok = False
                    tile.announce("duplicate")
        return ok

    def good_board(self): 
        """Check all rows, columns, blocks"""
        ok = True
        for group in self.groups:
            ok = self.unique_choices(group) and ok
        return ok

    def __str__(self): 
        rep = ""
        for row in self.tiles:
            for col in row:
                rep += str(col)
            rep += "\n"
        return rep
        
if __name__ == "__main__":
    brd_txt = ["435269781", "682571493", "197834562",
               "826195347", "374682915", "951743628",
               "519326874", "248957136", "763418295"]
    brd = Board(brd_txt)
    print(brd)
    ok = brd.good_board()
    print(ok)
