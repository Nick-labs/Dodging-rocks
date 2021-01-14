import pygame
import random
import os
import sys

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
        self.radius = ROCK_SIZE[0] // 2

        self.touches = 0

        self.vx = random.randint(-5, 5)
        self.vy = 0

    def update(self):

        self.vy += GRAVITY
        self.rect.x += self.vx
        self.rect.y += self.vy

        if pygame.sprite.collide_mask(self, player):
            player.kill()

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vx = -self.vx

        if self.touches < 2 and pygame.sprite.collide_rect(self, floor):
            self.touches += 1
            self.rect.bottom = floor.rect.top
            self.vy = -self.vy * 0.6
        if self.rect.top >= HEIGHT:
            # print('kill')
            # print(rocks_group)
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
        on_ground = pygame.sprite.collide_rect(self, floor)
        if not on_ground:
            if self.vy == 0:
                self.vy = 1
            else:
                self.vy += GRAVITY
        else:
            pass

        # Если уже на земле, то ставим позицию Y как 0
        if self.rect.bottom <= floor.rect.top:
            if pygame.sprite.collide_rect(self, floor) and self.vy >= 0:
                self.vy = 0
                self.rect.bottom = floor.rect.top

        if pygame.sprite.collide_rect(self, floor) and self.rect.bottom >= floor.rect.top and self.vy >= 0:
            self.vy = 0
            self.rect.bottom = floor.rect.top + 1

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

        if self.rect.y > HEIGHT:
            self.rect.x = 100
            self.rect.y = 100

        if player.rect.right > WIDTH:
            player.rect.right = WIDTH

        if player.rect.left < 0:
            player.rect.left = 0


class Floor(pygame.sprite.Sprite):
    def __init__(self, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH, 20))
        self.rect = self.image.get_rect()
        self.rect.y = h


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def intro():
    smallfont = pygame.font.SysFont(None, 30)
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                intro = False
        screen.fill((255, 255, 255))
        text = smallfont.render("press any key to continue", True, (0, 0, 0))
        screen.blit(text, [320, 240])
        pygame.display.update()
        clock.tick(15)


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dodging rocks')

clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 40)

intro()

bg = pygame.transform.scale(pygame.image.load('data/bg.jpg'), (WIDTH, HEIGHT))
floor = pygame.image.load('data/floor.jpg')
floor = pygame.transform.scale(floor, (WIDTH, floor.get_height()))

player = Player()
player_group = pygame.sprite.Group(player)
rocks_group = pygame.sprite.Group()

floor = Floor(FLOOR)
floor_group = pygame.sprite.Group(floor)

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

            if event.key == pygame.K_RIGHT:
                player.go_right()

            if event.key == pygame.K_UP:
                player.jump()

            if event.key == pygame.K_1:
                rocks_group.add(Rock())
                floor.rect.bottom = HEIGHT // 2
                # WIDTH, HEIGHT = 800, 600
                # FLOOR = HEIGHT * 8 // 10
                # floor.rect.y = FLOOR
                # ROCK_SIZE = (100, 100)
                # screen = pygame.display.set_mode((WIDTH, HEIGHT))

            if event.key == pygame.K_2:
                floor.rect.bottom = HEIGHT * 8 // 10
                # WIDTH, HEIGHT = 400, 400
                # FLOOR = HEIGHT * 8 // 10
                # floor.rect.y = FLOOR
                # ROCK_SIZE = (50, 50)
                # screen = pygame.display.set_mode((WIDTH, HEIGHT))

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.vx < 0:
                player.stop()

            if event.key == pygame.K_RIGHT and player.vx > 0:
                player.stop()

    if player.rect.right > WIDTH:
        player.rect.right = WIDTH

    if player.rect.left < 0:
        player.rect.left = 0

    now = pygame.time.get_ticks()

    if now - last_time >= FALL_TIME:
        rocks_group.add(Rock())
        last_time = now

    player_group.update()
    rocks_group.update()
    floor_group.update()

    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    player_group.draw(screen)
    rocks_group.draw(screen)
    floor_group.draw(screen)

    # screen.blit(bg, (0, FLOOR))
    # screen.blit(floor, (0, FLOOR))

    pygame.draw.rect(screen, (255, 255, 255), (0, HEIGHT - 50, 125, HEIGHT))

    if player_group:
        screen.blit(font.render(f'{now / 1000:06.1f}s', True, (0, 0, 0)), (5, HEIGHT - 48))
    elif not time:
        time = now
    else:
        screen.blit(font.render(f'{time / 1000:06.1f}s', True, (0, 0, 0)), (5, HEIGHT - 48))

    pygame.display.flip()

    print(clock.get_fps())
    clock.tick(FPS)

pygame.quit()
