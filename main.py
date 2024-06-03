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

clock = pygame.time.Clock()

def draw_intro_screen():
    screen.fill(BLACK)
    title_text = font.render('Tower Defense Game', True, WHITE)
    press_space_text = font.render('Press Spacebar to Start', True, WHITE)
    instructions = [
        "Introduction:",
        "1. You can touch the mint circle to make tower",
        "2. Making a tower will cost 50 coins.",
        "3. Upgrading a tower will cost additional 50 coins each time.",
        "4. Enemies will respawn every 15 seconds.",
        "5. You will earn 10 coins each enemy is killed"
    ]

    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 200))
    screen.blit(press_space_text, (screen.get_width() // 2 - press_space_text.get_width() // 2, 300))

    for i, instruction in enumerate(instructions):
        instruction_text = font.render(instruction, True, WHITE)
        screen.blit(instruction_text, (50, 400 + i * 30))

    pygame.display.flip()

def main_game():
    class Tower(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.upgrade_level = -1
            self.shapes = ['square', 'triangle', 'pentagon', 'hexagon', 'heptagon']
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
            self.speed = 2 + (wave * 0.05) # 웨이브에 따라 속도 증가
            self.max_health = 40 + (wave * 2) # 웨이브에 따라 체력 증가
            self.health = self.max_health
            self.reached_end = False

        def update(self):
            if self.path_index < len(self.path) - 1:
                target = self.path[self.path_index + 1]
                direction = pygame.math.Vector2(target) - pygame.math.Vector2(self.rect.center)
                if direction.length() > self.speed:
                    direction = direction.normalize() * self.speed
                self.rect.move_ip(direction)
                if self.rect.center == target:
                    self.path_index += 1
            else:
                self.reached_end = True

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
        (100, 250), (200, 350), (300, 150), (400,300), (400, 550), (500, 150), (600, 350)
    ]

    global money
    global lives
    money = 50
    lives = 10

    def place_tower(x, y):
        tower = Tower(x, y)
        towers.add(tower)
        global money
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

    def spawn_enemy():
        enemy = Enemy(path)
        enemies.add(enemy)

    wave = 1
    enemies_spawned = 0
    next_wave_time = pygame.time.get_ticks() + 10000
    spawn_interval = 1000
    last_spawn_time = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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

        for enemy in enemies.copy():
            if enemy.reached_end:
                lives -= 1
                enemy.kill()
                if lives <= 0:
                    running = False

        wave_text = font.render(f'Wave: {wave}', True, WHITE)
        screen.blit(wave_text, (10, 10))
        money_text = font.render(f'Money: {money}', True, WHITE)
        screen.blit(money_text, (screen.get_width() - 150, 10))
        lives_text = font.render(f'Lives: {lives}', True, WHITE)
        screen.blit(lives_text, (screen.get_width() // 2 - lives_text.get_width() // 2, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

running = True
show_intro = True

while running:
    if show_intro:
        draw_intro_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if show_intro:
                show_intro = False
                main_game()

    pygame.display.flip()
    clock.tick(60)