try:
    from game_board import *

    import alpha_beta
    import pygame
except ImportError as E:
    print(f'main.py => {E}')


''' Name:    Connect 4 [Reinforcement Learning]
    Class:   Intro to AI - CSCI 6660-01
    School:  University of New Haven, 2021 (c)
    Authors: Marcus Novoa, Jawahar Kandra
'''

# Window Dimensions
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Alpha-Beta Object
ab = alpha_beta.AlphaBeta()

# Title Bar Caption
pygame.display.set_caption('[AI-F21] Connect 4 - University of New Haven')

# Color Constants
LIGHT_BLUE = (52, 180, 235)
YELLOW     = (255, 255, 0)
WHITE      = (255, 255, 255)
RED        = (255, 0, 0)

FPS = 60 # Frame Rate

# Boolean for indicating end of game.
game_over = False

# Set the default game font.
pygame.font.init()

def create_font_text(size: int) -> pygame.font.SysFont:
    return pygame.font.SysFont('Monoscape', size)

def set_game_over():
    global game_over
    game_over = True
    pygame.mouse.set_visible(True)

# Create and update display window.
def draw_window():
    global game_over

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

    # Create text for title and author names.
    title_font = create_font_text(32)
    WIN.blit(title_font.render('Connect 4', 1, (WHITE)),
        (12, HEIGHT - 64))
    WIN.blit(title_font.render('Intro to AI', 1, (WHITE)),
        (12, HEIGHT - 36))
    WIN.blit(title_font.render('Marcus Novoa', 1, (WHITE)),
        (WIDTH - 164, HEIGHT - 64))
    WIN.blit(title_font.render('Jawahar Kandra', 1, (WHITE)),
        (WIDTH - 184, HEIGHT - 36))

    # Draw game piece when hovering above the game board.
    if not game_over:
        draw_selection_hover()

    if game_over:
        # Create alpha-black overlay.
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        WIN.blit(s, (0, 0))

        end_screen_font = create_font_text(75)
        WIN.blit(end_screen_font.render('Game Over!', 1, (WHITE)),
            ((WIDTH / 2) - 146, 20))

    pygame.display.update()

def main():
    global game_over

    # Fill gameboard slot positions.
    populate_gameboard_slot_pos()

    clock = pygame.time.Clock()
    run   = True

    while run:
        clock.tick(FPS) # Run at 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if not game_over:
                if event.type == pygame.MOUSEBUTTONUP:
                    if detect_selection_click():
                        draw_window()
                        pygame.time.wait(700)
                        ab.ai_move(GAME_BOARD_ALL_SLOTS)
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_w:
                #         set_game_over()

        draw_window()

    pygame.quit()

if __name__ == '__main__':
    main()
