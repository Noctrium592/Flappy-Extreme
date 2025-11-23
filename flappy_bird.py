import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Game settings
GRAVITY = 0.5
FLAP_POWER = -10
OBSTACLE_WIDTH = 70
OBSTACLE_GAP = 150
OBSTACLE_SPEED = 4
FPS = 60

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird - Green Girl Edition')

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.width = 40
        self.height = 40
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def flap(self):
        self.velocity = FLAP_POWER
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        self.rect.topleft = (self.x, int(self.y))
        
    def draw(self, surface):
        # Representing the bird as a green girl shape: a green circle with a triangular "hair" shape
        pygame.draw.ellipse(surface, GREEN, self.rect)  # body as ellipse
        # Draw a little triangle as "hair" on top to represent girl style
        points = [
            (self.x + self.width // 2, self.y - 10),
            (self.x + self.width // 2 - 10, self.y + 10),
            (self.x + self.width // 2 + 10, self.y + 10),
        ]
        pygame.draw.polygon(surface, GREEN, points)

class Obstacle:
    def __init__(self, x):
        self.x = x
        self.width = OBSTACLE_WIDTH
        self.gap = OBSTACLE_GAP
        self.top_height = random.randint(50, SCREEN_HEIGHT - self.gap - 50)
        self.bottom_height = SCREEN_HEIGHT - self.top_height - self.gap
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.bottom_height, self.width, self.bottom_height)

    def update(self):
        self.x -= OBSTACLE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        if self.x + self.width < 0:
            self.x = SCREEN_WIDTH
            self.top_height = random.randint(50, SCREEN_HEIGHT - self.gap - 50)
            self.bottom_height = SCREEN_HEIGHT - self.top_height - self.gap
            self.top_rect.height = self.top_height
            self.bottom_rect.y = SCREEN_HEIGHT - self.bottom_height
            self.bottom_rect.height = self.bottom_height

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.top_rect)
        pygame.draw.rect(surface, WHITE, self.bottom_rect)

def main():
    bird = Bird()
    obstacles = [Obstacle(SCREEN_WIDTH + i * (SCREEN_WIDTH // 2)) for i in range(2)]
    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.flap()
                elif event.key == pygame.K_r and game_over:
                    # Restart game
                    bird = Bird()
                    obstacles = [Obstacle(SCREEN_WIDTH + i * (SCREEN_WIDTH // 2)) for i in range(2)]
                    score = 0
                    game_over = False

        if not game_over:
            bird.update()

            for obstacle in obstacles:
                obstacle.update()
                # Check scoring: bird passes obstacle
                if obstacle.x + obstacle.width == bird.x:
                    score += 1

            # Collision detection
            for obstacle in obstacles:
                if bird.rect.colliderect(obstacle.top_rect) or bird.rect.colliderect(obstacle.bottom_rect):
                    game_over = True

            # Check if bird hits the ground (bottom of the screen)
            if bird.y + bird.height > SCREEN_HEIGHT:
                game_over = True

        # Draw background (red surroundings)
        screen.fill(RED)

        # Draw obstacles (white barriers)
        for obstacle in obstacles:
            obstacle.draw(screen)

        # Draw bird (green girl)
        bird.draw(screen)

        # Draw score
        draw_text(f"Score: {score}", font, BLACK, screen, SCREEN_WIDTH // 2, 30)

        if game_over:
            draw_text("Game Over! Press R to Restart", font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
