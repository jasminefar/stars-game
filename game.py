import pygame
import random

pygame.init()

# screen fitting
screen_width = 800
screen_height = 600

# colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
purple = (128, 0, 128)
colors = [red, green, blue, yellow, purple]

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Catch the Falling Objects Game")

# fonts
font = pygame.font.SysFont(None, 36)

# classes
class Basket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 100
        self.height = 20
        self.color = white
        self.rect = pygame.Rect(screen_width // 2 - self.width // 2, screen_height - 50, self.width, self.height)
        self.speed = 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class FallingObject(pygame.sprite.Sprite):
    def __init__(self, color, width, height, speed):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        self.rect = pygame.Rect(random.randint(0, screen_width - self.width), random.randint(-100, -40), self.width, self.height)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, screen_width - self.width)
            self.speed = random.randint(2, 6)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, width, height, speed):
        super().__init__()
        self.color = white
        self.width = width
        self.height = height
        self.rect = pygame.Rect(random.randint(0, screen_width - self.width), random.randint(-100, -40), self.width, self.height)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, screen_width - self.width)
            self.speed = random.randint(2, 4)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class Score:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.font = pygame.font.SysFont(None, 36)

    def draw(self):
        text = self.font.render(f"Score: {self.score}  High Score: {self.high_score}  Level: {self.level}", True, white)
        screen.blit(text, (10, 10))

    def increase_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score

    def reset_score(self):
        self.score = 0
        self.level = 1

    def next_level(self):
        self.level += 1

# Initialize game objects
all_sprites = pygame.sprite.Group()
falling_objects = pygame.sprite.Group()
powerups = pygame.sprite.Group()

basket = Basket()
all_sprites.add(basket)

for _ in range(10):
    falling_object = FallingObject(random.choice(colors), 20, 20, random.randint(2, 6))
    falling_objects.add(falling_object)
    all_sprites.add(falling_object)

for _ in range(3):
    powerup = PowerUp(15, 15, random.randint(2, 4))
    powerups.add(powerup)
    all_sprites.add(powerup)

score = Score()

# Game loop
running = True
clock = pygame.time.Clock()
spawn_time = pygame.time.get_ticks()
spawn_delay = 3000  # milliseconds

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update objects
    all_sprites.update()

    # Collision detection aka basket and falling objects
    hits = pygame.sprite.spritecollide(basket, falling_objects, True)
    for hit in hits:
        score.increase_score(10)
        new_falling_object = FallingObject(random.choice(colors), 20, 20, random.randint(2, 6))
        falling_objects.add(new_falling_object)
        all_sprites.add(new_falling_object)

    # Collision detection - basket and power-ups
    hits = pygame.sprite.spritecollide(basket, powerups, True)
    for hit in hits:
        score.increase_score(50)
        new_powerup = PowerUp(15, 15, random.randint(2, 4))
        powerups.add(new_powerup)
        all_sprites.add(new_powerup)

    # Spawn new falling objects
    current_time = pygame.time.get_ticks()
    if current_time - spawn_time > spawn_delay:
        falling_object = FallingObject(random.choice(colors), 20, 20, random.randint(2, 6))
        falling_objects.add(falling_object)
        all_sprites.add(falling_object)
        spawn_time = current_time

    # Level up conditions
    if score.score >= score.level * 100:
        score.next_level()
        for _ in range(score.level * 5):
            falling_object = FallingObject(random.choice(colors), 20, 20, random.randint(2, 6))
            falling_objects.add(falling_object)
            all_sprites.add(falling_object)

    # Draw everything
    screen.fill(black)
    all_sprites.draw(screen)
    score.draw()

    # Refresh screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
