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
MINT = (0, 255, 255)

font = pygame.font.SysFont(None, 36)

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.upgrade_level = -1
        self.shapes = ['triangle', 'square', 'pentagon', 'hexagon', 'heptagon']
        self.image = self.create_shape(self.shapes[self.upgrade_level])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.range = 150
        self.fire_rate = 60
        self.last_shot = pygame.time.get_ticks()

    def create_shape(self, shape):
        size = 50
        image = pygame.Surface((size, size), pygame.SRCALPHA)
        if shape == 'triangle':
            points = [(size // 2, 0), (size, size), (0, size)]
        elif shape == 'square':
            points = [(0, 0), (size, 0), (size, size), (0, size)]
        elif shape == 'pentagon':
            points = [(size // 2, 0), (size, size // 3), (2 * size // 3, size), (size // 3, size), (0, size // 3)]
        elif shape == 'hexagon':
            points = [(size // 2, 0), (size, size // 4), (size, 3 * size // 4), (size // 2, size), (0, 3 * size // 4), (0, size // 4)]
        elif shape == 'heptagon':
            points = [(size // 2, 0), (size, size // 6), (size, 5 * size // 6), (size // 2, size), (0, 5 * size // 6), (0, size // 6)]
        pygame.draw.polygon(image, BLUE, points)
        return image

    #업그레이드 정의
    def upgrade(self):
        self.upgrade_level += 1
        new_shape = self.shapes[min(self.upgrade_level, len(self.shapes) - 1)]
        self.image = self.create_shape(new_shape)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.range += 20
        self.fire_rate = max(10, self.fire_rate - 10)

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
    def __init__(self, path):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.path = path
        self.path_index = 0
        self.rect.center = self.path[self.path_index]
        self.speed = 2
        self.max_health = 40
        self.health = self.max_health

    def update(self):
        if self.path_index < len(self.path) - 1:
            target = self.path[self.path_index + 1]
            direction = pygame.math.Vector2(target) - pygame.math.Vector2(self.rect.center)
            if direction.length() > self.speed:
                direction = direction.normalize() * self.speed
            self.rect.move_ip(direction)
            if self.rect.center == target:
                self.path_index += 1

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True
        return False

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
                if self.target.take_damage(self.damage):
                    global money
                    money += 10
                self.kill()
        else:
            self.kill()

towers = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

path = [
    (0, 300), (50, 300), (50, 200), (150, 200), (150, 400),
    (250, 400), (250, 100), (350, 100), (350, 500), (450, 500),
    (450, 100), (550, 100), (550, 400), (650, 400), (650, 300), 
    (800, 300)
]

tower_positions = [
    (100, 250), (200, 350), (300, 150), (400, 550), (500, 150), (600, 350)
]

money = 150

def place_tower(x, y):
    tower = Tower(x, y)
    towers.add(tower)
    global money           #타워 추가 조건
    for tower in towers:
        if tower.rect.center == (x, y):
            if money >= 50:
                money -= 50
                tower.upgrade()
            return
    if money >= 50:
        money -= 50
        tower = Tower(x, y)
        towers.add(tower)

place_tower(400, 300)

def spawn_enemy():
    enemy = Enemy(path)
    enemies.add(enemy)

wave = 1
enemies_spawned = 0
next_wave_time = pygame.time.get_ticks() + 10000
spawn_interval = 1000
last_spawn_time = pygame.time.get_ticks()

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 좌클릭으로 타워 추가
            mouse_pos = pygame.mouse.get_pos()
            for pos in tower_positions:
                if pygame.math.Vector2(mouse_pos).distance_to(pos) < 25:
                    place_tower(*pos)
                    break

    current_time = pygame.time.get_ticks()
    if current_time >= next_wave_time:
        wave += 1
        enemies_spawned = 0
        next_wave_time = current_time + 20000

    if enemies_spawned < wave and current_time - last_spawn_time >= spawn_interval:
        spawn_enemy()
        enemies_spawned += 1
        last_spawn_time = current_time

    enemies.update()
    projectiles.update()

    for tower in towers:
        tower.attack(enemies, projectiles)

    screen.fill(GRAY)

    for i in range(len(path) - 1):
        pygame.draw.line(screen, BLACK, path[i], path[i + 1], 10)

    for pos in tower_positions:
        pygame.draw.circle(screen, MINT, pos, 25, 2)

    towers.draw(screen)
    enemies.draw(screen)
    projectiles.draw(screen)

    for enemy in enemies:
        enemy.draw_health_bar(screen)

    wave_text = font.render(f'Wave: {wave}', True, WHITE)
    screen.blit(wave_text, (10, 10))
    money_text = font.render(f'Money: {money}', True, WHITE)
    screen.blit(money_text, (screen.get_width() - 150, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()