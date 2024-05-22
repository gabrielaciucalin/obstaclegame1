import pygame
import random

# Initialize Pygame
pygame.init()

# Set window dimensions
WIDTH = 800
HEIGHT = 600

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Obstacle Dodge & Shoot")

# Define the Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.vel = 5
        self.bullets = []

    def draw(self):
        pygame.draw.rect(win, WHITE, (self.x, self.y, self.width, self.height))

    def move_left(self):
        self.x -= self.vel

    def move_right(self):
        self.x += self.vel

    def move_up(self):
        self.y -= self.vel

    def move_down(self):
        self.y += self.vel

    def shoot(self):
        x = self.x + self.width // 2
        y = self.y
        bullet = Bullet(x, y)
        self.bullets.append(bullet)

# Define the Obstacle class
class Obstacle:
    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel

    def draw(self):
        pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += self.vel

# Define the Bonus class
class Bonus:
    def __init__(self, x, y, radius, vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = vel

    def draw(self):
        pygame.draw.circle(win, BLUE, (self.x, self.y), self.radius)

    def move(self):
        self.y += self.vel

# Define the Bullet class
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.vel = 10

    def draw(self):
        pygame.draw.circle(win, GREEN, (self.x, self.y), self.radius)

    def move(self):
        self.y -= self.vel

# Define the Game class
class Game:
    def __init__(self):
        self.player = Player(WIDTH // 2 - 25, HEIGHT - 70)
        self.obstacles = []
        self.bonuses = []
        self.score = 0
        self.lives = 3
        self.font = pygame.font.SysFont(None, 30)
        self.clock = pygame.time.Clock()
        self.is_running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()
        if keys[pygame.K_UP]:
            self.player.move_up()
        if keys[pygame.K_DOWN]:
            self.player.move_down()
        if keys[pygame.K_SPACE]:
            self.player.shoot()

    def update(self):
        # Create obstacles randomly
        if random.randint(0, 100) < 2:
            x = random.randint(0, WIDTH - 50)
            width = random.randint(30, 70)
            height = random.randint(30, 70)
            vel = random.randint(2, 4)
            self.obstacles.append(Obstacle(x, 0, width, height, vel))

        # Create bonus points randomly
        if random.randint(0, 300) < 1:
            x = random.randint(0, WIDTH - 10)
            y = random.randint(0, HEIGHT - 10)
            radius = 10
            vel = random.randint(2, 4)
            self.bonuses.append(Bonus(x, y, radius, vel))

        # Update obstacle positions and check collisions with the player and bullets
        for obstacle in self.obstacles:
            if obstacle.y > HEIGHT:
                self.obstacles.remove(obstacle)
            if (
                obstacle.x < self.player.x + self.player.width
                and obstacle.x + obstacle.width > self.player.x
                and obstacle.y < self.player.y + self.player.height
                and obstacle.y + obstacle.height > self.player.y
            ):
                self.lives -= 1
                self.obstacles.remove(obstacle)
            for bullet in self.player.bullets:
                if (
                    obstacle.x < bullet.x < obstacle.x + obstacle.width
                    and obstacle.y < bullet.y < obstacle.y + obstacle.height
                ):
                    self.obstacles.remove(obstacle)
                    self.player.bullets.remove(bullet)
                    self.score += 1
            obstacle.move()

        # Update bonus positions and check collisions with the player
        for bonus in self.bonuses:
            if (
                bonus.x < self.player.x + self.player.width
                and bonus.x + bonus.radius > self.player.x
                and bonus.y < self.player.y + self.player.height
                and bonus.y + bonus.radius > self.player.y
            ):
                self.score += 10
                self.bonuses.remove(bonus)
            bonus.move()

        # Update bullet positions
        for bullet in self.player.bullets:
            bullet.move()

        # Check game over conditions
        if self.lives == 0:
            self.is_running = False

    def draw(self):
        win.fill((0, 0, 0))

        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw()

        # Draw bonus points
        for bonus in self.bonuses:
            bonus.draw()

        # Draw player
        self.player.draw()

        # Draw bullets
        for bullet in self.player.bullets:
            bullet.draw()

        # Draw score and lives
        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        lives_text = self.font.render("Lives: " + str(self.lives), True, WHITE)
        win.blit(score_text, (10, 10))
        win.blit(lives_text, (10, 40))

        pygame.display.update()

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

# Create an instance of the Game class and start the game
game = Game()
game.run()
