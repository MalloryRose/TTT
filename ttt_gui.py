import pygame
from constants import *
from tictactoe import *

pygame.init()
pygame.display.set_caption("Tic Tac Toe")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
chip_font = pygame.font.Font(None, CHIP_FONT)  # 'X' or 'O' font
font = pygame.font.Font(None, GAME_OVER_FONT)

# initialize game state
board = initialize_board()
player = 1
chip = 'x'
winner = 0
game_over = False


def draw_grid():
    # draw horizontal lines
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (0, i * SQUARE_SIZE),
            (WIDTH, i * SQUARE_SIZE),
            LINE_WIDTH
        )

    # draw vertical lines
    for j in range(1, BOARD_COLS):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (j * SQUARE_SIZE, 0),
            (j * SQUARE_SIZE, HEIGHT),
            LINE_WIDTH
        )


def draw_chips():
    # draw a text, 1. define a surface, 2. define the location of the text
    chip_x_surf = chip_font.render('x', 0, CROSS_COLOR)
    chip_o_surf = chip_font.render('o', 0, CIRCLE_COLOR)

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'x':
                chip_x_rect = chip_x_surf.get_rect(center=(SQUARE_SIZE * col + SQUARE_SIZE // 2, SQUARE_SIZE * row + SQUARE_SIZE // 2))
                screen.blit(chip_x_surf, chip_x_rect)
            elif board[row][col] == 'o':
                chip_o_rect = chip_o_surf.get_rect(center=(SQUARE_SIZE * col + SQUARE_SIZE // 2, SQUARE_SIZE * row + SQUARE_SIZE // 2))
                screen.blit(chip_o_surf, chip_o_rect)


def draw_game_over(winner):
    screen.fill(BG_COLOR)
    if winner != 0:
        end_text = f"Player {winner} wins!"
    else:
        end_text = "No one wins!"
    end_surf = font.render(end_text, 0, LINE_COLOR)
    end_rect = end_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(end_surf, end_rect)

    restart_text = "Press r to play the game again..."
    restart_surf = font.render(restart_text, 0, LINE_COLOR)
    restart_rect = restart_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))
    screen.blit(restart_surf, restart_rect)


screen.fill(BG_COLOR)   # changes background color
draw_grid()


while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            row = y // SQUARE_SIZE
            col = x // SQUARE_SIZE
            if available_square(board, row, col):
                mark_square(board, row, col, chip)  # update the board state
                if check_if_winner(board, chip):
                    game_over = True
                    winner = player
                else:
                    if board_is_full(board):
                        game_over = True
                        winner = 0   # indicate a tie
                player = 2 if player == 1 else 1
                chip = 'o' if chip == 'x' else 'x'

                draw_chips()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # retart the game
                screen.fill(BG_COLOR)
                draw_grid()
                board = initialize_board()
                game_over = False
                player = 1
                chip = 'x'
                winner = 0

    if game_over:
        pygame.display.update()
        pygame.time.delay(1000)
        draw_game_over(winner)
    pygame.display.update()