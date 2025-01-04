import pygame
import random
import sys


pygame.init()
pygame.mixer.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


clock = pygame.time.Clock()


player_width = 50
player_height = 50
player_speed = 5


bullet_width = 5
bullet_height = 10
bullet_speed = 7


alien_width = 50
alien_height = 50
alien_speed = 3
alien_rows = 5
alien_cols = 8


font = pygame.font.SysFont('arial', 30)


game_over = False


back = pygame.image.load('background.jpeg') 
background = pygame.transform.scale(back, (WIDTH, HEIGHT))  


shoot_sound = pygame.mixer.Sound('')  
alien_explosion_sound = pygame.mixer.Sound('')  
game_over_sound = pygame.mixer.Sound('')  

# Load background music
pygame.mixer.music.load('space-adventure.mp3')  
pygame.mixer.music.set_volume(0.2) 
pygame.mixer.music.play(-1)  


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
        shoot_sound.play()  


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


all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for row in range(alien_rows):
    for col in range(alien_cols):
        alien = Alien(col * (alien_width + 10) + 50, row * (alien_height + 10) + 50)
        all_sprites.add(alien)
        aliens.add(alien)


score = 0

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    
    all_sprites.update()

    
    for bullet in bullets:
        hit_aliens = pygame.sprite.spritecollide(bullet, aliens, True)
        for hit in hit_aliens:
            bullet.kill()
            alien_explosion_sound.play() 
            score += 1

    
    if pygame.sprite.spritecollide(player, aliens, True):
        game_over = True
        game_over_sound.play()  
    
    screen.blit(background, (0, 0))  
    all_sprites.draw(screen)

    
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    
    pygame.display.flip()

    
    clock.tick(60)


game_over_text = font.render("Game Over!", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(2000)


pygame.quit()
sys.exit()
