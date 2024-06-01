import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tower Defense Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)


# 타워 정의
class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# 적 정의
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 0.55

    def update(self):
        self.rect.x += self.speed

# 타워 생성
towers = pygame.sprite.Group()

# 적 생성
enemies = pygame.sprite.Group()
enemy = Enemy(0, 300)
enemies.add(enemy)

def place_tower(x, y):
    tower = Tower(x, y)
    towers.add(tower)

place_tower(400, 300)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    enemies.update()

    screen.fill(GRAY) 
    towers.draw(screen)
    enemies.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()

