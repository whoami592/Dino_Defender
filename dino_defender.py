import pygame
import random
import asyncio
import platform

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DinoDefender - Coded by Pakistani Ethical Hacker Mr Sabaz Ali Khan")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player settings
player_width = 60
player_height = 60
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# Meteor settings
meteor_width = 40
meteor_height = 40
meteor_speed = 3
meteors = []

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 7
bullets = []

# Game variables
score = 0
game_over = False
font = pygame.font.SysFont("arial", 36)

# Stylish Banner
banner_font = pygame.font.SysFont("impact", 50)
banner_text = banner_font.render("DinoDefender - Coded by Pakistani Ethical Hacker Mr Sabaz Ali Khan", True, GREEN)
banner_rect = banner_text.get_rect(center=(WIDTH // 2, 50))

# Player class
class Player:
    def __init__(self):
        self.rect = pygame.Rect(player_x, player_y, player_width, player_height)

    def move(self, dx):
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)

# Meteor class
class Meteor:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - meteor_width), 0, meteor_width, meteor_height)
        self.speed = meteor_speed

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, bullet_width, bullet_height)

    def move(self):
        self.rect.y -= bullet_speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

# Game setup
player = Player()
clock = pygame.time.Clock()
FPS = 60

def spawn_meteor():
    if random.random() < 0.02:
        meteors.append(Meteor())

def check_collisions():
    global score, game_over
    for meteor in meteors[:]:
        for bullet in bullets[:]:
            if meteor.rect.colliderect(bullet.rect):
                meteors.remove(meteor)
                bullets.remove(bullet)
                score += 10
                break
        if meteor.rect.colliderect(player.rect):
            game_over = True

def draw_game():
    screen.fill(BLACK)
    screen.blit(banner_text, banner_rect)
    player.draw()
    for meteor in meteors:
        meteor.draw()
    for bullet in bullets:
        bullet.draw()
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, HEIGHT - 40))
    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

def setup():
    global score, game_over, meteors, bullets, player
    score = 0
    game_over = False
    meteors = []
    bullets = []
    player = Player()

async def main():
    setup()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and game_over and event.key == pygame.K_r:
                setup()

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move(-player_speed)
            if keys[pygame.K_RIGHT]:
                player.move(player_speed)
            if keys[pygame.K_SPACE]:
                if len(bullets) < 5:  # Limit bullets on screen
                    bullets.append(Bullet(player.rect.centerx - bullet_width // 2, player.rect.top))

            spawn_meteor()
            for meteor in meteors[:]:
                meteor.move()
                if meteor.rect.top > HEIGHT:
                    meteors.remove(meteor)
            for bullet in bullets[:]:
                bullet.move()
                if bullet.rect.bottom < 0:
                    bullets.remove(bullet)

            check_collisions()

        draw_game()
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())