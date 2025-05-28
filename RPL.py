import pygame
import sys

# --- Konstanta ---
TILE_SIZE = 100
GRID_SIZE = 6
SCREEN_SIZE = TILE_SIZE * GRID_SIZE
FPS = 60

# Warna
WHITE = (240, 240, 240)
BLACK = (10, 10, 10)
WOOD_COLOR = (205, 125, 50)
BLUE = (60, 80, 200)
RED = (200, 50, 50)
GREEN = (0, 200, 0)

# Inisialisasi pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE + 100, SCREEN_SIZE))
pygame.display.set_caption("Sliding Puzzle")
clock = pygame.time.Clock()

# Load gambar
arrow_img = pygame.image.load("2.jpg")
arrow_img = pygame.transform.scale(arrow_img, (50, 50))

wood_texture = pygame.image.load("1.jpg")
wood_texture = pygame.transform.scale(wood_texture, (TILE_SIZE, TILE_SIZE))

# --- Level ---
# Format blok: [x, y, w, h, color]
levels = [
    [  # Level 0
        [0, 2, 2, 1, BLUE],  # block target
        [2, 0, 1, 3, WOOD_COLOR],
        [3, 0, 1, 2, WOOD_COLOR],
        [4, 1, 1, 3, WOOD_COLOR],
        [2, 3, 2, 1, WOOD_COLOR],
        [0, 4, 2, 1, WOOD_COLOR],
        [3, 4, 2, 1, WOOD_COLOR],
    ],
    [  # Level 1
        [1, 2, 2, 1, BLUE],
        [0, 0, 1, 3, WOOD_COLOR],
        [3, 0, 1, 2, WOOD_COLOR],
        [4, 2, 2, 1, WOOD_COLOR],
        [3, 3, 1, 2, WOOD_COLOR],
        [1, 4, 2, 1, WOOD_COLOR],
        [0, 5, 3, 1, WOOD_COLOR],
    ],
    [  # Level 2
        [2, 2, 2, 1, BLUE],
        [0, 0, 2, 1, WOOD_COLOR],
        [0, 1, 1, 3, WOOD_COLOR],
        [3, 0, 1, 3, WOOD_COLOR],
        [4, 1, 2, 1, WOOD_COLOR],
        [3, 4, 1, 2, WOOD_COLOR],
        [0, 4, 2, 1, WOOD_COLOR],
    ],
    [  # Level 3
        [2, 2, 2, 1, BLUE],
        [0, 0, 1, 2, WOOD_COLOR],
        [1, 0, 2, 1, WOOD_COLOR],
        [3, 1, 1, 3, WOOD_COLOR],
        [0, 3, 2, 1, WOOD_COLOR],
        [1, 4, 2, 1, WOOD_COLOR],
        [4, 3, 1, 2, WOOD_COLOR],
    ],
    [  # Level 4
        [2, 2, 2, 1, BLUE],
        [0, 0, 2, 1, WOOD_COLOR],
        [0, 1, 1, 2, WOOD_COLOR],
        [3, 0, 1, 2, WOOD_COLOR],
        [4, 1, 2, 1, WOOD_COLOR],
        [3, 3, 1, 2, WOOD_COLOR],
        [1, 4, 2, 1, WOOD_COLOR],
    ]
]

current_level = 0
blocks = []

# --- Fungsi ---
def load_level(level):
    global blocks
    blocks = [b[:] for b in levels[level]]

def draw_background_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (200, 180, 150), rect, 1)

def draw_blocks():
    for b in blocks:
        rect = pygame.Rect(b[0]*TILE_SIZE, b[1]*TILE_SIZE, b[2]*TILE_SIZE, b[3]*TILE_SIZE)
        if b[4] == BLUE:
            pygame.draw.rect(screen, b[4], rect)
        else:
            for i in range(b[2]):
                for j in range(b[3]):
                    r = pygame.Rect((b[0]+i)*TILE_SIZE, (b[1]+j)*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    screen.blit(wood_texture, r)
            pygame.draw.rect(screen, BLACK, rect, 2)

def check_win():
    for b in blocks:
        if b[4] == BLUE:
            if b[0] + b[2] == GRID_SIZE:
                return True
    return False

def get_block_at(x, y):
    for b in blocks:
        bx, by, bw, bh = b[:4]
        if bx <= x < bx + bw and by <= y < by + bh:
            return b
    return None

def can_move(block, dx, dy):
    new_rect = pygame.Rect((block[0]+dx)*TILE_SIZE, (block[1]+dy)*TILE_SIZE, block[2]*TILE_SIZE, block[3]*TILE_SIZE)
    if not (0 <= block[0] + dx <= GRID_SIZE - block[2] and 0 <= block[1] + dy <= GRID_SIZE - block[3]):
        return False
    for b in blocks:
        if b == block:
            continue
        b_rect = pygame.Rect(b[0]*TILE_SIZE, b[1]*TILE_SIZE, b[2]*TILE_SIZE, b[3]*TILE_SIZE)
        if new_rect.colliderect(b_rect):
            return False
    return True

# --- Main Loop ---
selected_block = None
start_pos = None
blink_timer = 0

def main():
    global current_level, blink_timer, selected_block, start_pos
    load_level(current_level)

    while True:
        screen.fill(WHITE)
        draw_background_grid()
        draw_blocks()

        if check_win():
            blink_timer += 1
            if blink_timer % 30 < 15:
                font = pygame.font.SysFont(None, 60)
                text = font.render("MENANG! Tekan N", True, GREEN)
                screen.blit(text, (50, 30))
            screen.blit(arrow_img, (SCREEN_SIZE + 20, SCREEN_SIZE//2 - 25))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n and check_win():
                    current_level += 1
                    if current_level >= len(levels):
                        pygame.quit()
                        sys.exit()
                    load_level(current_level)
                    blink_timer = 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                grid_x, grid_y = mx // TILE_SIZE, my // TILE_SIZE
                if grid_x < GRID_SIZE and grid_y < GRID_SIZE:
                    selected_block = get_block_at(grid_x, grid_y)
                    start_pos = (grid_x, grid_y)

            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_block and start_pos:
                    mx, my = pygame.mouse.get_pos()
                    end_x, end_y = mx // TILE_SIZE, my // TILE_SIZE
                    dx = end_x - start_pos[0]
                    dy = end_y - start_pos[1]

                    if abs(dx) > abs(dy):
                        step = 1 if dx > 0 else -1
                        while can_move(selected_block, step, 0):
                            selected_block[0] += step
                            break
                    elif abs(dy) > 0:
                        step = 1 if dy > 0 else -1
                        while can_move(selected_block, 0, step):
                            selected_block[1] += step
                            break

                selected_block = None
                start_pos = None

        pygame.display.flip()
        clock.tick(FPS)

main()