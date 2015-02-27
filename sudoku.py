"""
Sudoku Solver

Reads in a Sudoku board from a text file, attempts 
to solve the Sudoku board and either prints the solution
to the standard output or displays it if the '--display'
option has been used.

Author: Thomas Rowland and Michael McGirr, 3 March 2013 for CIS 210
"""
import sdkboard         # The Sudoku board  (model component)
import sdkdisplay       # Display of Sudoku board (view component)
import sdkconsole       # Simple textual output (alternative view component)
import argparse         # Interpret command line

# Command line processing - the Pythonic way

parser = argparse.ArgumentParser(description="""
   Check a Sudoku board (complete or incomplete) to
   report whether it is correct or whether, on the
   contrary, there are duplicate digits in a row,
   a column, or a subsquare.""")

parser.add_argument('board', metavar="filename",
                    type=argparse.FileType('r'), 
                    help="file containing board description")
                    
parser.add_argument('--display', action="store_true", 
                    help="Display Sudoku board graphically")

args = parser.parse_args()

# Main program logic
board = sdkboard.Board.from_file(args.board)  # Makes a board object called board

# Display code
if args.display:
    sdkdisplay.display(board)

def update_possibilities():
    """This function modifies the possible values the open tiles in the 
    group can be according to the rules of Sudoku ensuring that if a symbol
    is already present in the group of tile objects, it is not listed as a
    possiblity for an open tile.

    Arguments:
        None: Uses the global board object

    Returns:
        None: Modifies the global board object
    """
    for group in board.groups:
        symbol_list = []
        for tile in group:  # Creating a list of existing symbols in the group
            if tile.symbol != sdkboard.OPEN:
                symbol_list.append(tile.symbol)
        for tile in group:  # Removing from each tile's list of possibilities
                            # the symbols which are already present in the group
            if tile.symbol == sdkboard.OPEN:
                for sym in symbol_list:
                    if sym in tile.possible:
                        tile.possible.remove(sym)
def naked_single():
    """Attempts to correctly place a number in a group of 9 tile 
    object according to the rules of Sudoku.
    
    This function attempts to place a number in an open tile out of 
    a group of 9 tile objects. The function does this by looking at
    each open tile, if that open tile only has one possiblility then
    the tile symbol is set equal to that possibility and the tile is 
    no longer empty.

    Arguments:
        None: performs operations on the global board object

    Returns: 
        None: modifies the existing global board object 
    """
    update_possibilities()
    for group in board.groups:
        for tile in group:
            if tile.symbol == sdkboard.OPEN and len(tile.possible) == 1:
                tile.symbol = tile.possible.pop()
                tile.announce("filled")
                naked_single()

def hidden_single():
    """Attempt to correctly place a number in a group of 9 tile 
    objects according to the rules of Sudoku.

    This function attempts to place a number in an open tile out
    of a group of 9 tile objects. The function does this by looking
    at all open tiles in the group and recording what their possible 
    values are, then if the tile in question has a particular value 
    which no other tile can be it makes that value the tile symbol
    and the tile is no longer empty.

    Arguments:
        None: performs operations on the global board object

    Returns: 
        None: modifies the existing global board object
    """
    update_possibilities()
    for group in board.groups:
        possibilities = []
        for tile in group:
            if tile.symbol == sdkboard.OPEN:
                for option in tile.possible:
                    possibilities.append(option)
        for tile in group:
            if tile.symbol == sdkboard.OPEN:
                for option in tile.possible:
                    if possibilities.count(option) == 1: 
                        tile.symbol = option
                        tile.possible = tile.symbol
                        tile.announce("filled")
                        naked_single()
                        hidden_single()  
        
def main():
    naked_single()
    hidden_single()

if __name__ == "__main__":
    main()

# Output to command line if the --display option is not used
if not args.display: 
    sdkconsole.display(board)
    sdkconsole.standard_output(board)

# Leave graphic display until user presses Enter
if args.display: 
    input("Press enter to close")
