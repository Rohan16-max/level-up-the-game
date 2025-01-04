import pygame
import random
import sys

# Initialize pygame and mixer for sounds
pygame.init()
pygame.mixer.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game clock
clock = pygame.time.Clock()

# Player settings
player_width = 50
player_height = 50
player_speed = 5

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 7

# Alien settings
alien_width = 50
alien_height = 50
alien_speed = 3
alien_rows = 5
alien_cols = 8

# Font
font = pygame.font.SysFont('arial', 30)

# Game over flag
game_over = False

# Load background image
back = pygame.image.load('background.jpeg')  # Replace with your background file
background = pygame.transform.scale(back, (WIDTH, HEIGHT))  # Scale to fit the screen

# Load sound effects
shoot_sound = pygame.mixer.Sound('shoot.wav')  # Replace with your shoot sound file
alien_explosion_sound = pygame.mixer.Sound('alien_explosion.wav')  # Replace with alien explosion sound
game_over_sound = pygame.mixer.Sound('game_over.wav')  # Replace with game over sound

# Load background music
pygame.mixer.music.load('space-adventure.mp3')  # Replace with your music file
pygame.mixer.music.set_volume(0.2)  # Set background music volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play the music indefinitely (-1)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= player_speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += player_speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()  # Play the shoot sound when firing

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((bullet_width, bullet_height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= bullet_speed
        if self.rect.bottom < 0:
            self.kill()

# Alien class
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((alien_width, alien_height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += alien_speed
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.rect.x = random.randint(0, WIDTH - alien_width)

# Initialize all sprites groups
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player object
player = Player()
all_sprites.add(player)

# Create alien objects
for row in range(alien_rows):
    for col in range(alien_cols):
        alien = Alien(col * (alien_width + 10) + 50, row * (alien_height + 10) + 50)
        all_sprites.add(alien)
        aliens.add(alien)

# Score
score = 0

# Main game loop
while not game_over:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # Check for collisions between bullets and aliens
    for bullet in bullets:
        hit_aliens = pygame.sprite.spritecollide(bullet, aliens, True)
        for hit in hit_aliens:
            bullet.kill()
            alien_explosion_sound.play()  # Play explosion sound when alien is destroyed
            score += 1

    # Check for collisions between aliens and player
    if pygame.sprite.spritecollide(player, aliens, True):
        game_over = True
        game_over_sound.play()  # Play game over sound when player is hit

    # Draw everything
    screen.blit(background, (0, 0))  # Draw the background
    all_sprites.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Refresh the display
    pygame.display.flip()

    # Frame rate
    clock.tick(60)

# Game over
game_over_text = font.render("Game Over!", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(2000)

# Quit the game
pygame.quit()
sys.exit()
