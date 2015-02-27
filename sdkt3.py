"""
Tactics and checks for Sudoku.

A tactic is a rule that can be used to determine and/or constrain the
possible choices for a Sudoku tile.

A check determines whether a given Sudoku board
(whether complete or incomplete) is legal.  A board is
legal if it contains only digits and open spaces, and
if all of the digits are unique in each row, column,
and 3x3 block.

Authors: austin gheen
"""
import sdkboard

# The following variables are private but global to the module
global groups
global progress

def prepare(board):
    """ 
    Prepare for checking and solving a sudoku board.
    Args:
       board:  An sdkboard.Board object
    Returns:
       nothing
    Effects:
       prepared for check(board) and solve(board)
    """
    global groups  # rows, columns, and blocks

    groups = [ ]

    # Rows  (we can reuse them from the board)
    for row in range(9):
        groups.append(board.tiles[row])

    for row in range(9):
        col_list = [ ]
        for col in range(9):
            col_list.append(board.tiles[col][row])
        groups.append([col])

    
    # Blocks  (we need new lists for these, too)
    for start_row in [0, 3, 6]:
        for start_col in [0, 3, 6]:
            sq_tiles = [ ] 
            for row in range(3):
                for col in range(3): 
                    t = board.tiles[start_row + row][start_col+col]
                    sq_tiles.append(t)
            groups.append(sq_tiles)

    # We need to know when we are making progress 
    for row in board.tiles:
        for tile in row:
            tile.register(progress_listener)

 
def progress_listener(tile, event):
    """
    An event listener, used to determine whether we have made
    some progress in solving a Sudoku puzzle.  This listener
    will be attached to Sudoku Tile objects, and informed when
    "determined" and "constrained" events occur.
    Args:
       tile:  The tile on which an event occurred
       event: What happened.  The events we listen for are "determined"
         and "constrained"
    Returns:  nothing
    Effects: module-global variable progress may be set to True
    """
    global progress 
    if event == "determined" or event == "constrained":
       progress = True
       # print("Notified of progress!")

def good_board(): 
        """Check that every group (row, column, and block)
        contains unique elements (no duplicate digits).
        Args:
           none  (implicit through prepare_board)
        Returns:
           Boolean True iff all groups contain unique elements
        Effects:
           Will announce "duplicate" event on tiles that are
           not unique in a group.
        Requires:
           prepare(board) must be called before good_board
        """
        #FIXME - detect duplicates
        #print(len(groups))
        given = [ ]
        vari = True

        for group in groups:
            copies = [ ]
            for i in group:
                if i.symbol != '.':
                    if i.symbol in copies:
                        vari = False
                        given.append(i.symbol)

                    else:
                        copies.append(i.symbol)
                
            for x in group:
                if x.symbol in given:
                    x.announce("duplicate")


        return vari

def solve():
    """
    Keep applying naked_single and hidden_single tactics to every
    group (row, column, and block) as long as there is progress.
    Args: 
        none
    Requires:
        prepare(board) must be called once before solve()
        use only if good_board() returns True
    Effects: 
        May modify tiles in the board passed to prepare(board), 
        setting symbols in open tiles, and reducing the possible
        sets in some tiles. 
    """
    global progress
    progress = True
    while(progress):
        # print("***Starting solution round***")
        progress = False
        # Note that naked_single and hidden_single may indirectly
        # set the progress flag by causing the progress listener to be
        # triggered.  
        for group in groups:
            naked_single(group)
            hidden_single(group)

def naked_single(group):
        """Constrain each tile to not contain any of the digits 
        that have already been used in the group.
        Args: 
            group: a list of 9 tiles in a row, column, or block
        Returns:
            nothing
        Effects:
            For each tile in the group, eliminates "possible" elements
            that match a digit used by another tile in the group.  If 
            this reduces it to one possibility, the selection will be 
            made (Tile.remove_choices does this), and progress may be 
            signaled.
        """  
        used = [ ]

        for i in group:
            if i.symbol != '.':
                used.append(i.symbol)

        for y in group:
            if y.symbol == '.':
                y.remove_choices(set(used))



def hidden_single(group):
        """Each digit has to go somewhere.  For each digit, 
        see if there is only one place that digit should 
        go.  If there is, put it there. 
        Args: 
           group:  a list of 9 tiles in a row, column, or block
        Returns: 
           nothing
        Effects: 
           For each tile, if it is the only tile that can accept a 
           particular digit (according to its "possible" set), 
           
        """

        valid = set(sdkboard.DIGITS)
        tile_counter = 0
        
        for i in group:
            if i.symbol != '.':
                valid.remove(i.symbol)

        for digit in valid:
            count = 0
            for tile in group:
                if digit in tile.valid:
                    saved_tile = tile
                    count += 1
            if count == 1:
                saved_tile.determine(digit)
