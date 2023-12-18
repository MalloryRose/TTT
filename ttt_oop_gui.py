from constants import *
import pygame


class Cell:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height

    def set_value(self, val):
        self.value = val

    def draw(self, screen):
        chip_font = pygame.font.Font(None, CHIP_FONT)  # 'X' or 'O' font
        chip_x_surf = chip_font.render('x', 0, CROSS_COLOR)
        chip_o_surf = chip_font.render('o', 0, CIRCLE_COLOR)

        if self.value == 'x':
            chip_x_rect = chip_x_surf.get_rect(
                center=(SQUARE_SIZE * self.col + SQUARE_SIZE // 2, SQUARE_SIZE * self.row + SQUARE_SIZE // 2))
            screen.blit(chip_x_surf, chip_x_rect)
        elif self.value == 'o':
            chip_o_rect = chip_o_surf.get_rect(
                center=(SQUARE_SIZE * self.col + SQUARE_SIZE // 2, SQUARE_SIZE * self.row + SQUARE_SIZE // 2))
            screen.blit(chip_o_surf, chip_o_rect)


class Board:
    def __init__(self, rows, cols, width, height, screen):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.screen = screen
        self.board = self.initialize_board()   # 2d list
        self.cells = [
            [Cell(self.board[i][j], i, j, SQUARE_SIZE, SQUARE_SIZE) for j in range(cols)]
            for i in range(rows)
        ]



    def draw(self):
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

        # draw cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(self.screen)


    def initialize_board(self):
        # 1st approach
        return [["-" for i in range(3)] for j in range(3)]

    def available_square(self, row, col):
        return self.board[row][col] == '-'

    def mark_square(self, row, col, chip_type):
        self.board[row][col] = chip_type
        self.update_cells()

    def update_cells(self):
        self.cells = [
            [Cell(self.board[i][j], i, j, SQUARE_SIZE, SQUARE_SIZE) for j in range(self.cols)]
            for i in range(self.rows)
        ]

    def board_is_full(self):
        for row in self.board:
            for chip in row:
                if chip == "-":
                    return False
        return True

    def check_if_winner(self, chip_type):
        # check all rows
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] == chip_type:
                return True

        # check all columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == chip_type:
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] == chip_type:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == chip_type:
            return True

        return False

    # row: row index, col: col index
    def is_valid(self, row, col):
        if 0 <= row <= 2 and 0 <= col <= 2 and self.board[row][col] == '-':
            return True
        return False

    def reset_board(self):
        self.board = self.initialize_board()
        self.update_cells()


def draw_game_over(winner):
    font = pygame.font.Font(None, GAME_OVER_FONT)
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


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic Tac Toe")
    screen.fill(BG_COLOR)

    # initialize game state
    player = 1
    chip = 'x'
    winner = 0
    game_over = False

    board = Board(BOARD_ROWS, BOARD_COLS, WIDTH, HEIGHT, screen)
    board.draw()

    while True:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                if board.available_square(row, col):
                    board.mark_square(row, col, chip)  # update the board state
                    if board.check_if_winner(chip):
                        game_over = True
                        winner = player
                    else:
                        if board.board_is_full():
                            game_over = True
                            winner = 0  # indicate a tie
                    player = 2 if player == 1 else 1
                    chip = 'o' if chip == 'x' else 'x'

                    board.draw()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # retart the game
                    screen.fill(BG_COLOR)
                    board.reset_board()
                    game_over = False
                    player = 1
                    chip = 'x'
                    winner = 0
                    board.draw()

        if game_over:
            pygame.display.update()
            pygame.time.delay(1000)
            draw_game_over(winner)
        pygame.display.update()
