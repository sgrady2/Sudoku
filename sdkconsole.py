"""
A simple text display of duplicates as they are found. 
Can be used instead of the graphical sdkdisplay module, 
or can be used in addition to it.  Typically faster 
than the graphics updates.
"""

seen_duplicates = set()   # Global set to avoid re-reporting the same tile
def report_duplicate(tile, event):
    """Event listener: Respond to duplicate discovery event
    by printing a message on the standard output.
    
    Arguments: 
        tile:  The sdkboard.Tile object reporting an event
        event: What happened to the tile.  "duplicate" is the 
               one we care about here. 
    """
    global seen_duplicates  # So I don't re-report the same tile
    if tile in seen_duplicates:
        return
    if event == "duplicate":
        seen_duplicates.add(tile)
        print("Tile at ", tile.row, tile.col, " is a duplicate of ", tile.symbol)

def display(board): 
    """Register a listener to print reports of duplicate tiles.
    Arguments: 
        board:  An sdkboard.Board object that we wish to monitor. 
    """
    for row in board.tiles:
        for tile in row:
            tile.register(report_duplicate)
def standard_output(board):
    """Print the board tile symbols to the standard output.
    Arguments:
        board: An sdkboard.Board object that you would like 
            to view on the standard output.
    """
    i = 0
    for group in board.groups:
        if i < 9:
            line = ""
            for tile in group:
                line = line + tile.symbol
            print(line)
            i += 1
