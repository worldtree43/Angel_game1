import pygame
import sys

screen_size = (800, 800)
game_size = (19, 19)
cube_height = screen_size[0] / game_size[0]
cube_width = screen_size[1] / game_size[1]

pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Angel v.s. Devil")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

board = [[0 for _ in range(game_size[0])] for _ in range(game_size[1])]

angel_pos = (game_size[0] // 2, game_size[1] // 2)
board[angel_pos[1]][angel_pos[0]] = 1  # initialize angel's position
devil_pos = None

def draw_board():
    for y in range(game_size[1]):
        for x in range(game_size[0]):
            rect = pygame.Rect(x*cube_width, y*cube_height, cube_width, cube_height)
            pygame.draw.rect(screen, WHITE, rect, 1)
            if (x, y) == angel_pos:
                pygame.draw.circle(screen, GREEN, (int(x*cube_width + cube_width/2), int(y*cube_height + cube_height/2)), int(cube_width/2))
            elif board[y][x] == 2:
                pygame.draw.circle(screen, RED, (int(x*cube_width + cube_width/2), int(y*cube_height + cube_height/2)), int(cube_width/2))

def highlight_moves():
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = angel_pos[0] + dx, angel_pos[1] + dy
            if is_valid_move(nx, ny):
                rect = pygame.Rect(nx*cube_width, ny*cube_height, cube_width, cube_height)
                pygame.draw.rect(screen, (0, 255, 0), rect, 3)  # 高亮显示可移动的方块

def is_valid_move(x, y):
    return 0 <= x < game_size[0] and 0 <= y < game_size[1] and board[y][x] == 0

def game_over():
    if angel_pos[0] in [0, game_size[0]-1] or angel_pos[1] in [0, game_size[1]-1]:
        return "angel"
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = angel_pos[0] + dx, angel_pos[1] + dy
            if is_valid_move(nx, ny):
                return None
    return "devil"


def show_winner(winner):
	font = pygame.font.Font(None, 74)
	text_message = "angel escapes" if winner == "angel" else "eaten by devil"
	text = font.render(text_message, True, WHITE)

	text_rect = text.get_rect(center=(screen_size[0] / 2, screen_size[1] / 2))
	background_rect = text_rect.inflate(20, 20)

	pygame.draw.rect(screen, BLACK, background_rect)
	screen.blit(text, text_rect)
	pygame.display.flip()
	pygame.time.wait(3000)

turn = "devil"
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            grid_x, grid_y = int(x // cube_width), int(y // cube_height)
            if turn == "devil" and is_valid_move(grid_x, grid_y):
                board[grid_y][grid_x] = 2
                turn = "angel"
            elif turn == "angel" and is_valid_move(grid_x, grid_y):
                angel_pos = (grid_x, grid_y)
                turn = "devil"

    screen.fill(BLACK)
    draw_board()
    if turn == "angel":
        highlight_moves()
    pygame.display.flip()

    winner = game_over()
    if winner:
        show_winner(winner)
        running = False

pygame.quit()
sys.exit()