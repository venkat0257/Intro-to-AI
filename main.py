from game_board import *
import pygame

''' Name:    Connect 4 [Reinforcement Learning]
    Class:   Intro to AI - CSCI 6660-01
    School:  University of New Haven, 2021 (c)
    Authors: Marcus Novoa, Jawahar Kandra
'''

# Window Dimensions
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Title Bar Caption
pygame.display.set_caption('[AI-F21] Connect 4 - University of New Haven')

# Color Constants
LIGHT_BLUE = (52, 180, 235)

FPS = 60 # Frame Rate

# Create and update display window.
def draw_window():
    # Add Background Color
    WIN.fill(LIGHT_BLUE) 
    # Draw Game Board Image
    WIN.blit(GAME_BOARD, (GAME_BOARD_DEFAULT_POSITION))

    # Create column selection surfaces above the game board.
    for i in range(len(COLUMN_SELECTION_SURFACES)):
        WIN.blit(COLUMN_SELECTION_SURFACES[i], COLUMN_SELECTION_SURFACE_POS[i])

    # Draw game pieces in the filled game board slots.
    for (row, col) in GAME_BOARD_FILLED_SLOTS:
        if GAME_BOARD_FILLED_SLOTS[(row, col)] == 'R':
            WIN.blit(RED_PIECE, GAME_BOARD_SLOT_POSITIONS[row][col])
        elif GAME_BOARD_FILLED_SLOTS[(row, col)] == 'Y':
            WIN.blit(YLW_PIECE, GAME_BOARD_SLOT_POSITIONS[row][col])

    # Draw game piece when hovering above the game board.
    draw_selection_hover()

    pygame.display.update()

def main():
    populate_gameboard_slot_pos() # Fill gameboard slot positions.
    clock = pygame.time.Clock()
    run = True
 
    while run:
        clock.tick(FPS) # Run at 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            if event.type == pygame.MOUSEBUTTONUP:
                detect_selection_click()
        draw_window()

    pygame.quit()

if __name__ == '__main__':
    main()

