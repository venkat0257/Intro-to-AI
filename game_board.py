from main import WIN, WIDTH, HEIGHT
import pygame
import os

''' CREATE THE BOARD & PIECES:
    The board and game piece images are generated and utilized here.
    The game board slot positions are configured where the pieces can
    then be placed following a column selection from the player.
'''
# Image Assets
GAME_BOARD = pygame.image.load(os.path.join('assets', 'c4-board.png'))
RED_PIECE  = pygame.image.load(os.path.join('assets', 'c4-red-piece.png'))
YLW_PIECE  = pygame.image.load(os.path.join('assets', 'c4-yellow-piece.png'))

# Current game piece color.
CURRENT_COLOR = 'R'

# Update game piece color.
def update_current_color():
    global CURRENT_COLOR

    if CURRENT_COLOR == 'R':
        CURRENT_COLOR = 'Y'
    else:
        CURRENT_COLOR = 'R'

# Image Asset Dimensions / Constants
GAME_BOARD_WIDTH = 509
GAME_PIECE_DIMEN = 54 # GAME_PIECE WIDTH and HEIGHT are equal.
GAME_BOARD_ROWS  = 6
GAME_BOARD_COLS  = 7

# Game Board Position
GAME_BOARD_DEFAULT_POSITION = (WIDTH-GAME_BOARD_WIDTH)/2, 80

# Populate game board slot positions.
ROW_OFFSET_X = 1.25
ROW_OFFSET_Y = 7

# Column padding values to align the game pieces horizontally.
COL_PADDING = [0, 2, 0, 2, 2, 1.5, 1.25]

def populate_gameboard_slot_pos() -> list:
    TEMP_SLOT_POSITIONS = [(0,0)] * (GAME_BOARD_ROWS * GAME_BOARD_COLS)

    # -- Row 1
    TEMP_SLOT_POSITIONS[0] = (GAME_PIECE_DIMEN*4, (GAME_PIECE_DIMEN*2)-4)

    for i in range(1, 7):
        TEMP_SLOT_POSITIONS[i] = (TEMP_SLOT_POSITIONS[i-1][0] + \
                (GAME_PIECE_DIMEN*ROW_OFFSET_X) + COL_PADDING[i], TEMP_SLOT_POSITIONS[0][1])

    # -- Rows 2-6
    for i in range(7, 42):
        TEMP_SLOT_POSITIONS[i] = (TEMP_SLOT_POSITIONS[i-7][0],
                TEMP_SLOT_POSITIONS[i-7][1] + GAME_PIECE_DIMEN + ROW_OFFSET_Y)

    # Split 1D list into 2D list to separate each row.
    return [TEMP_SLOT_POSITIONS[i:i+GAME_BOARD_COLS] \
            for i in range(0, len(TEMP_SLOT_POSITIONS), GAME_BOARD_COLS)]

# List of all possible slot positions for game pieces.
GAME_BOARD_SLOT_POSITIONS = populate_gameboard_slot_pos()


''' HEADER COLUMN SELECTION SLOTS:
    These empty surface SLOTS are used when hovering above the board in
    order to indicate where the player would like to drop their game piece.
'''
COLUMN_SELECTION_SURFACES = [pygame.Surface((68, 80))] * 7

COLUMN_SELECTION_SURFACE_POS    = [(0, 0)] * 7
COLUMN_SELECTION_SURFACE_POS[0] = (208, 0)

for s in COLUMN_SELECTION_SURFACES:
    # Add transparent background color for BLACK.
    s.set_colorkey((0, 0, 0))

for i in range(1, len(COLUMN_SELECTION_SURFACE_POS)):
    # Configure all game board selection surface positions.
    COLUMN_SELECTION_SURFACE_POS[i] = (COLUMN_SELECTION_SURFACE_POS[i-1][0] + 69, 0)

def detect_selection_hover() -> int:
    selected_column = -1
    width, height = COLUMN_SELECTION_SURFACES[0].get_width(), \
                    COLUMN_SELECTION_SURFACES[0].get_height()
    x, y = pygame.mouse.get_pos()

    for i in range(len(COLUMN_SELECTION_SURFACES)):
        if x >= COLUMN_SELECTION_SURFACE_POS[i][0] and \
            x <= COLUMN_SELECTION_SURFACE_POS[i][0]+width and \
            y >= 0 and y <= height:
                selected_column = i
 
    return selected_column

def draw_selection_hover():
    selected_column = detect_selection_hover()

    # Create the game piece above the board on hover.
    if selected_column >= 0:
        pygame.mouse.set_visible(False)
        x, y = COLUMN_SELECTION_SURFACE_POS[selected_column][0], \
                COLUMN_SELECTION_SURFACE_POS[selected_column][1]
        w, h = 68, 80

        PIECE = RED_PIECE if CURRENT_COLOR == 'R' else YLW_PIECE
        WIN.blit(PIECE, dest=(x+w-GAME_PIECE_DIMEN-((w-GAME_PIECE_DIMEN)/2)+1, \
                y+h-GAME_PIECE_DIMEN-10, w, h))
    elif pygame.mouse.get_visible() == False:
        pygame.mouse.set_visible(True)
 

''' GAME BOARD FILLED SLOTS:
    Keep track of all filled SLOTS within the game board.
    Add logic for dropping game pieces into the board.
'''
# Create a map for all filled SLOTS within the game board.
GAME_BOARD_FILLED_SLOTS = {}

def drop_game_piece(selected_column: int) -> tuple:
    first_available_slot = 0

    # If column is filled.
    if GAME_BOARD_FILLED_SLOTS.get((first_available_slot, selected_column)):
        print('This column is full. Try another column.')
        return (False, None)

    for row in range(GAME_BOARD_ROWS):
        if GAME_BOARD_FILLED_SLOTS.get((row, selected_column)) == None:
            first_available_slot = row
        else:
            break 

    # Add the game piece color to the filled SLOTS map.
    GAME_BOARD_FILLED_SLOTS[(first_available_slot, selected_column)] = CURRENT_COLOR
   
    # Return boolean and row to be used for confirming a winner.
    return (True, first_available_slot)

def detect_selection_click():
    selected_column = detect_selection_hover()
    col_width       = COLUMN_SELECTION_SURFACES[0].get_width()

    if selected_column >= 0:
        mouse_x = pygame.mouse.get_pos()[0]
        col_x   = COLUMN_SELECTION_SURFACE_POS[selected_column][0]
        if mouse_x > col_x and mouse_x < col_x + col_width:
            VALID_DROP = drop_game_piece(selected_column)
            if VALID_DROP[0]:
                WINNER = confirm_winner(VALID_DROP[1], selected_column)
                if WINNER[0]:
                    WINNER_COLOR = 'Red' if WINNER[1] == 'R' else 'Yellow'
                    print(f'{WINNER_COLOR} wins the game!')
                update_current_color()


''' CHECK FOR CONNECT 4:
    Confirm whether or not a player has connected
    four of their game pieces and won the game.
'''
def check_c4_vertical(r: int, c: int) -> tuple:
    SLOTS       = GAME_BOARD_FILLED_SLOTS
    piece_color = SLOTS.get((r, c))
    connect_4   = False
 
    # The height of the sliding window used
    # to check for a vertical connect 4.
    SLIDING_WINDOW_H = 4
 
    for row in range(GAME_BOARD_ROWS - SLIDING_WINDOW_H + 1):
        if SLOTS.get((row, c)) == piece_color and \
            SLOTS.get((row+1, c)) == piece_color and \
            SLOTS.get((row+2, c)) == piece_color and \
            SLOTS.get((row+3, c)) == piece_color:
                connect_4 = True

    return (connect_4, piece_color)

def check_c4_horizontal(r: int, c: int) -> tuple:
    SLOTS       = GAME_BOARD_FILLED_SLOTS
    piece_color = SLOTS.get((r, c))
    connect_4   = False
 
    # The width of the sliding window used
    # to check for a horizontal connect 4.
    SLIDING_WINDOW_W = 4
   
    for col in range(GAME_BOARD_COLS - SLIDING_WINDOW_W + 1):
        if SLOTS.get((r, col)) == piece_color and \
            SLOTS.get((r, col+1)) == piece_color and \
            SLOTS.get((r, col+2)) == piece_color and \
            SLOTS.get((r, col+3)) == piece_color:
                connect_4 = True

    return (connect_4, piece_color)

def check_c4_diagonal_left(r: int, c: int) -> tuple:
    SLOTS       = GAME_BOARD_FILLED_SLOTS
    piece_color = SLOTS.get((r, c))
    connect_4   = False
 
    ''' Top-Left -> Bottom-Right Diagonal:
    [X - - - -]
    [- X - - -]
    [- - C - -]
    [- - - X -]
    [- - - - X]
    '''
    DIAGONAL_PIECES = [piece_color]

    # Create two pointers to keep track of pieces
    # moving outwards (up-left and down-right.)
    ptr_u = [r-1, c-1]
    ptr_d = [r+1, c+1]

    run_loop = True
    while run_loop:
        # If pointers can no longer move outwards.
        if (ptr_u[0] < 0 or ptr_u[1] < 0) and \
            (ptr_d[0] > GAME_BOARD_ROWS-1 or \
             ptr_d[1] > GAME_BOARD_COLS-1):
                run_loop = False
                break

        # Add piece colors to front and back of pieces list.
        DIAGONAL_PIECES.insert(0, SLOTS.get((ptr_u[0], ptr_u[1])))
        DIAGONAL_PIECES.append(SLOTS.get((ptr_d[0], ptr_d[1])))

        # Search for 4 game pieces in a row diagonally.
        # Return if a winner is found.
        in_a_row = 0
        for color in DIAGONAL_PIECES:
            if color == piece_color:
                in_a_row += 1
            else:
                in_a_row = 0

            if in_a_row == 4:
                connect_4 = True
                return (connect_4, piece_color)

        # Update pointers as necessary.
        if ptr_u[0] >= 0: ptr_u[0] -= 1
        if ptr_u[1] >= 0: ptr_u[1] -= 1
        if ptr_d[0] <= GAME_BOARD_ROWS-1: ptr_d[0] += 1
        if ptr_d[1] <= GAME_BOARD_COLS-1: ptr_d[1] += 1

    return (connect_4, piece_color)

def check_c4_diagonal_right(r: int, c: int) -> tuple:
    SLOTS       = GAME_BOARD_FILLED_SLOTS
    piece_color = SLOTS.get((r, c))
    connect_4   = False
 
    ''' Bottom-Left -> Top-Right Diagonal:
    [- - - - X]
    [- - - X -]
    [- - C - -]
    [- X - - -]
    [X - - - -]
    '''
    DIAGONAL_PIECES = [piece_color]

    # Create two pointers to keep track of pieces
    # moving outwards (down-left and up-right.)
    ptr_u = [r-1, c+1]
    ptr_d = [r+1, c-1]

    run_loop = True
    while run_loop:
        # If pointers can no longer move outwards.
        if (ptr_d[0] > GAME_BOARD_ROWS-1 or ptr_d[1] < 0) and \
            (ptr_u[0] < 0 or ptr_u[1] > GAME_BOARD_COLS-1):
                run_loop = False
                break

        # Add piece colors to front and back of pieces list.
        DIAGONAL_PIECES.insert(0, SLOTS.get((ptr_d[0], ptr_d[1])))
        DIAGONAL_PIECES.append(SLOTS.get((ptr_u[0], ptr_u[1])))

        # Search for 4 game pieces in a row diagonally.
        # Return if a winner is found.
        in_a_row = 0
        for color in DIAGONAL_PIECES:
            if color == piece_color:
                in_a_row += 1
            else:
                in_a_row = 0

            if in_a_row == 4:
                connect_4 = True
                return (connect_4, piece_color)

        # Update pointers as necessary.
        if ptr_u[0] >= 0: ptr_u[0] -= 1 
        if ptr_u[1] <= GAME_BOARD_COLS-1: ptr_u[1] += 1
        if ptr_d[0] <= GAME_BOARD_ROWS-1: ptr_d[0] += 1 
        if ptr_d[1] >= 0: ptr_d[1] -= 1

    return (connect_4, piece_color)

def check_c4_diagonal(r: int, c: int) -> tuple:
    DIAGONAL_L = check_c4_diagonal_left(r, c)
    DIAGONAL_R = check_c4_diagonal_right(r, c)

    if DIAGONAL_L[0]: return DIAGONAL_L
    elif DIAGONAL_R[0]: return DIAGONAL_R

    return (False, None)

def confirm_winner(row: int, col: int) -> bool:
    WINNER_VERTICAL = check_c4_vertical(row, col)
    WINNER_HORIZONT = check_c4_horizontal(row, col)
    WINNER_DIAGONAL = check_c4_diagonal(row, col)

    if (WINNER_VERTICAL[0] is not None and WINNER_VERTICAL[0]) or \
        (WINNER_HORIZONT[0] is not None and WINNER_HORIZONT[0]) or \
        (WINNER_DIAGONAL[0] is not None and WINNER_DIAGONAL[0]):
            if WINNER_VERTICAL[1]: WINNER_COLOR = WINNER_VERTICAL[1]
            elif WINNER_HORIZONT[1]: WINNER_COLOR = WINNER_HORIZONT[1]
            elif WINNER_DIAGONAL[1]: WINNER_COLOR = WINNER_DIAGONAL[1]
            return (True, WINNER_COLOR)

    return (False, None)

