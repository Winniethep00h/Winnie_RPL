import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600  # Narrower width for tighter play area
FPS = 60

# Colors
COLOR_BACKGROUND_TOP = (34, 77, 34)
COLOR_BACKGROUND_BOTTOM = (22, 44, 22)
COLOR_PLAYER = (255, 200, 50)
COLOR_TEXT = (230, 230, 230)
COLOR_GAMEOVER_BG = (30, 30, 30)

# Fonts
FONT_NAME = pygame.font.match_font('freesansbold')
def get_font(size):
    return pygame.font.Font(FONT_NAME, size)

# Setup window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Winnie the Pooh - Hindari Barang Jatuh")

clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 60
        self.height = 80
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_pooh(self.image)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH // 2, HEIGHT - 30)
        self.speed = 7

    def draw_pooh(self, surface):
        body_color = (255, 204, 51)
        shirt_color = (204, 0, 0)
        pygame.draw.ellipse(surface, body_color, (10, 10, 40, 60))
        pygame.draw.rect(surface, shirt_color, (10, 40, 40, 30))
        pygame.draw.circle(surface, body_color, (30, 15), 15)
        eye_color = (30, 30, 30)
        pygame.draw.circle(surface, eye_color, (22, 12), 3)
        pygame.draw.circle(surface, eye_color, (38, 12), 3)
        pygame.draw.circle(surface, eye_color, (30, 22), 4)
        pygame.draw.arc(surface, eye_color, (20, 20, 20, 15), 3.14, 0, 2)

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class FallingObject(pygame.sprite.Sprite):
    def __init__(self, speed_multiplier):
        super().__init__()
        self.type = random.choice(['leaf', 'branch', 'rock'])
        self.size = random.randint(25, 45)
        self.image = pygame.Surface((self.size + 10, self.size + 10), pygame.SRCALPHA).convert_alpha()
        self.draw_object()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        base_speed = random.uniform(4.0, 8.0)
        self.speed = base_speed * speed_multiplier

    def draw_object(self):
        if self.type == 'leaf':
            self.draw_leaf()
        elif self.type == 'branch':
            self.draw_branch()
        elif self.type == 'rock':
            self.draw_rock()

    def draw_leaf(self):
        leaf_color = (34, 139, 34)
        stem_color = (85, 107, 47)
        w, h = self.image.get_size()
        pygame.draw.ellipse(self.image, leaf_color, (5, h//4, w-10, h//2))
        pygame.draw.rect(self.image, stem_color, (w//2 - 2, h//2 + 4, 4, h//3))

    def draw_branch(self):
        branch_color = (139, 69, 19)
        leaf_color = (50, 100, 30)
        w, h = self.image.get_size()
        pygame.draw.rect(self.image, branch_color, (0, h//2 - 5, w, 10), border_radius=4)
        pygame.draw.circle(self.image, leaf_color, (w//3, h//2 - 10), 7)
        pygame.draw.circle(self.image, leaf_color, (w//2, h//2 - 14), 6)
        pygame.draw.circle(self.image, leaf_color, (2*w//3, h//2 - 8), 7)

    def draw_rock(self):
        rock_base = (120, 120, 120)
        rock_shadow = (80, 80, 80)
        w, h = self.image.get_size()
        center = (w//2, h//2)
        radius = min(w, h)//2 - 3
        pygame.draw.circle(self.image, rock_base, center, radius)
        pygame.draw.arc(self.image, rock_shadow, (center[0]-radius, center[1]-radius, 2*radius, 2*radius), 3.5, 5.0, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

def draw_vertical_gradient(surface, color_top, color_bottom):
    height = surface.get_height()
    for y in range(height):
        ratio = y / height
        r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
        g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
        b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))

def draw_forest_silhouettes(surface):
    tree_color = (18, 43, 18)
    for x in range(0, WIDTH, 70):
        points = [
            (x, HEIGHT),
            (x + 35, HEIGHT),
            (x + 17, HEIGHT - 110),
        ]
        pygame.draw.polygon(surface, tree_color, points)

def draw_text(surface, text, size, x, y, center=False):
    font = get_font(size)
    text_surface = font.render(text, True, COLOR_TEXT)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def main():
    running = True
    game_over = False
    score = 0
    score_timer = 0
    spawn_interval = 800  # milliseconds
    spawn_decrease = 8  # decrease spawn_interval every increase_interval ms
    min_spawn_interval = 350
    increase_interval = 5000  # every 5 seconds increase difficulty
    last_increase_time = 0
    speed_multiplier = 1.0

    player = Player()
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    all_sprites.add(player)

    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, spawn_interval)

    start_ticks = pygame.time.get_ticks()  # to track elapsed time

    while running:
        dt = clock.tick(FPS) / 1000
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == spawn_event and not game_over:
                obj = FallingObject(speed_multiplier)
                all_sprites.add(obj)
                obstacles.add(obj)

            if game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    game_over = False
                    score = 0
                    score_timer = 0
                    spawn_interval = 800
                    speed_multiplier = 1.0
                    last_increase_time = current_time
                    pygame.time.set_timer(spawn_event, spawn_interval)
                    all_sprites.empty()
                    obstacles.empty()
                    player = Player()
                    all_sprites.add(player)

        if not game_over:
            player.update(keys)
            obstacles.update()

            if pygame.sprite.spritecollideany(player, obstacles):
                game_over = True

            score_timer += dt
            if score_timer >= 0.1:
                score += 1
                score_timer = 0

            # Increase difficulty every increase_interval milliseconds
            if current_time - last_increase_time > increase_interval:
                if spawn_interval > min_spawn_interval:
                    spawn_interval = max(min_spawn_interval, spawn_interval - spawn_decrease)
                    pygame.time.set_timer(spawn_event, spawn_interval)
                speed_multiplier += 0.1
                last_increase_time = current_time

        draw_vertical_gradient(screen, COLOR_BACKGROUND_TOP, COLOR_BACKGROUND_BOTTOM)
        draw_forest_silhouettes(screen)

        all_sprites.draw(screen)
        draw_text(screen, f"Skor: {score}", 28, 10, 10)

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(220)
            overlay.fill(COLOR_GAMEOVER_BG)
            screen.blit(overlay, (0, 0))
            draw_text(screen, "Game Over!", 64, WIDTH // 2, HEIGHT // 2 - 80, center=True)
            draw_text(screen, f"Skor Anda: {score}", 36, WIDTH // 2, HEIGHT // 2, center=True)
            draw_text(screen, "Tekan R untuk Mulai Ulang", 24, WIDTH // 2, HEIGHT // 2 + 50, center=True)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

