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
YELLOW = (255, 255, 0)


class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.range = 150
        self.fire_rate = 60
        self.last_shot = pygame.time.get_ticks()


    def attack(self, enemies, projectiles):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.fire_rate:
            for enemy in enemies:
                distance = pygame.math.Vector2(self.rect.center).distance_to(enemy.rect.center)
                if distance <= self.range:
                    projectile = Projectile(self.rect.center, enemy)
                    projectiles.add(projectile)
                    self.last_shot = now
                    break


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 0.55
        self.max_health = 40  # 최대 체력
        self.health = self.max_health  # 현재 체력

    def update(self):
        self.rect.x += self.speed

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    #체력바
    def draw_health_bar(self, surface):
        if self.health > 0:
            health_ratio = self.health / self.max_health
            pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 10, 30, 5))
            pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y - 10, 30 * health_ratio, 5))


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, target):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.target = target
        self.speed = 5
        self.damage = 1

    def update(self):
        if self.target.alive():
            direction = pygame.math.Vector2(self.target.rect.center) - pygame.math.Vector2(self.rect.center)
            if direction.length() > self.speed:
                direction = direction.normalize() * self.speed
            self.rect.move_ip(direction)
            if self.rect.colliderect(self.target.rect):
                self.target.take_damage(self.damage)
                self.kill()
        else:
            self.kill()


towers = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy = Enemy(0, 300)
enemies.add(enemy)
projectiles = pygame.sprite.Group()

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
    projectiles.update()

    for tower in towers:
        tower.attack(enemies, projectiles)

    screen.fill(GRAY) 
    towers.draw(screen)
    enemies.draw(screen)
    projectiles.draw(screen)

    for enemy in enemies:
        enemy.draw_health_bar(screen)  # 체력바 그리기


    pygame.display.flip()
    clock.tick(60)

pygame.quit()

