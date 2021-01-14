import pygame
import random

WIDTH, HEIGHT = 800, 600
FPS = 60

FLOOR = HEIGHT * 8 // 10
ROCK_SIZE = (100, 100)

GRAVITY = 0.25
PLAYER_SPEED = 6
PLAYER_JUMP_FORCE = -8

FALL_TIME = 1500  # задержка между камнями в миллисекундах


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('data/flax.png'), ROCK_SIZE)
        self.orig_image = self.image.copy()
        self.rect = self.image.get_rect()

        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = 0

        self.touches = 0

        self.vx = random.randint(-5, 5)
        self.vy = 0

    def update(self):
        self.vy += GRAVITY
        self.rect.x += self.vx
        self.rect.y += self.vy

        if pygame.sprite.collide_mask(self, player):
            player.kill()
            particle.kill()  # когда умирает player тогда исчестает след бега

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vx = -self.vx

        if self.touches < 2:
            if self.rect.bottom >= FLOOR:
                self.touches += 1
                self.rect.bottom = FLOOR
                self.vy = -self.vy * 0.6
        elif self.rect.top >= HEIGHT:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('data/box.jpg'), (40, 80))
        self.rect = self.image.get_rect()
        self.step = 3
        self.vx = 0
        self.vy = 0

    def calc_grav(self):
        if self.vy == 0:
            self.vy = 1
        else:
            self.vy += GRAVITY

        # Если уже на земле, то ставим позицию Y как 0
        if self.rect.bottom >= FLOOR and self.vy >= 0:
            self.vy = 0
            self.rect.bottom = FLOOR

    def go_left(self):
        self.vx = -PLAYER_SPEED
        # self.image = pygame.image.load('images/player_left.png')
        # if self.right:  # Проверяем куда он смотрит
        #     self.right = False

    def go_right(self):
        self.vx = PLAYER_SPEED
        # self.image = pygame.image.load('images/player_right.png')
        # if not self.right:
        #     self.right = True

    def stop(self):
        # self.image = pygame.image.load('images\\player_stop.png')
        self.vx = 0

    def jump(self):
        if self.rect.bottom >= FLOOR:
            self.vy = PLAYER_JUMP_FORCE

    def update(self):
        self.calc_grav()
        self.rect.x += self.vx
        self.rect.y += self.vy

        if player.rect.right > WIDTH:
            player.rect.right = WIDTH

        if player.rect.left < 0:
            player.rect.left = 0


class Particle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.right = True
        self.image = pygame.transform.scale(pygame.image.load('data/particle.png'), (26, 26))
        self.rect = self.image.get_rect()
        self.step = 3
        self.vx = 0
        self.vy = 0

    def calc_grav(self):
        if self.vy == 0:
            self.vy = 1
        else:
            self.vy += GRAVITY

        # Если уже на земле, то ставим позицию Y как 0
        if self.rect.bottom >= FLOOR and self.vy >= 0:
            self.vy = 0
            self.rect.bottom = FLOOR

    def go_left(self):
        self.vx = -PLAYER_SPEED

        if self.right:  # Проверяем куда он смотрит
            self.right = False

    def go_right(self):
        self.vx = PLAYER_SPEED

        if not self.right:
            self.right = True

    def update(self, x, x1, f):
        flag = f
        self.calc_grav()
        if flag:
            self.rect.x = x[0] - 1
            if self.right:
                self.image = pygame.transform.scale(pygame.image.load('data/particle_r.png'), (26, 26))
            else:
                self.image = pygame.transform.scale(pygame.image.load('data/particle.png'), (26, 26))

        else:
            self.rect.x = x1[0] - 25
            if self.right:
                self.image = pygame.transform.scale(pygame.image.load('data/particle_r.png'), (26, 26))
            else:
                self.image = pygame.transform.scale(pygame.image.load('data/particle.png'), (26, 26))

        self.rect.x += self.vx
        self.rect.y += self.vy

        if particle.rect.right > WIDTH:
            particle.rect.right = WIDTH - 1

        if particle.rect.left < 0:
            particle.rect.left = 0


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dodging rocks')

clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 40)

bg = pygame.transform.scale(pygame.image.load('data/bg.jpg'), (WIDTH, FLOOR))
floor = pygame.image.load('data/floor.jpg')
floor = pygame.transform.scale(floor, (WIDTH, floor.get_height()))

player = Player()
player_group = pygame.sprite.Group(player)

particle = Particle()
particle_group = pygame.sprite.Group(particle)

"""flag для изменения спрайта(стороны)
flag_movement для понятие двигаеться ли player или нет"""

flag = True
flag_movement = False

rocks_group = pygame.sprite.Group()

last_time = 0
time = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
                flag_movement = True
                particle.go_left()
                flag = True

            if event.key == pygame.K_RIGHT:
                player.go_right()
                flag_movement = True
                particle.go_right()
                flag = False

            if event.key == pygame.K_UP:
                player.jump()
                flag_movement = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.vx < 0:
                player.stop()
                flag_movement = False

            if event.key == pygame.K_RIGHT and player.vx > 0:
                player.stop()
                flag_movement = False

    if player.rect.right > WIDTH:
        player.rect.right = WIDTH
        particle.rect.right = WIDTH

    if player.rect.left < 0:
        player.rect.left = 0
        particle.rect.left = 0

    now = pygame.time.get_ticks()

    if now - last_time >= FALL_TIME:
        rocks_group.add(Rock())
        last_time = now

    player_group.update()
    # rocks_group.update()

    """передает координаты чтобы следы были прямо за объектом player"""
    particle_group.update(player.rect.bottomright, player.rect.bottomleft, flag)

    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    player_group.draw(screen)
    rocks_group.draw(screen)

    """Будет рисовать следы если только двтгаеться"""
    if not flag_movement or player.rect.bottom < 480:
        pass
    else:
        particle_group.draw(screen)

    # screen.blit(bg, (0, FLOOR))
    screen.blit(floor, (0, FLOOR))

    pygame.draw.rect(screen, (255, 255, 255), (0, HEIGHT - 50, 125, HEIGHT))

    if player_group:
        screen.blit(font.render(f'{now / 1000:06.1f}s', True, (0, 0, 0)), (5, HEIGHT - 48))
    elif not time:
        time = now
    else:
        screen.blit(font.render(f'{time / 1000:06.1f}s', True, (0, 0, 0)), (5, HEIGHT - 48))

    pygame.display.flip()
    # print(clock.get_fps())
    clock.tick(FPS)
pygame.quit()
