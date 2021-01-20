import pygame
import random
import os
import sys
import credits

WIDTH, HEIGHT = 800, 600
FPS = 60

FLOOR = HEIGHT * 0.85
# ROCK_SIZE = (100, 100)
ROCK_SIZE = (80, 80)
PLAYER_SIZE = (40, 56)

GRAVITY = 0.25
PLAYER_SPEED = 6
PLAYER_JUMP_FORCE = -10

fall_time = 1500  # задержка между камнями в миллисекундах


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.idle_images = []
        self.run_left_images = []
        self.run_right_images = []

        for i in range(3):
            self.idle_images.append(pygame.transform.scale(
                pygame.image.load(f'data/character/idle/adventurer-idle-0{i}.png'), PLAYER_SIZE))

        for i in range(6):
            self.run_right_images.append(
                pygame.transform.scale(pygame.image.load(f'data/character/run/adventurer-run-0{i}.png'), PLAYER_SIZE))
            self.run_left_images.append(pygame.transform.flip(self.run_right_images[i], True, False))

        self.image = self.idle_images[0]

        self.index = 0
        self.u = 0

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

        if self.rect.bottom <= floor.rect.top:
            if pygame.sprite.collide_rect(self, floor) and self.vy >= 0:
                self.vy = 0
                self.rect.bottom = floor.rect.top

        elif pygame.sprite.collide_rect(self, floor) and self.rect.bottom >= floor.rect.top and self.vy >= 0:
            self.vy = 0
            self.rect.bottom = floor.rect.top + 1

    def go_left(self):
        self.vx = -PLAYER_SPEED

    def go_right(self):
        self.vx = PLAYER_SPEED

    def stop(self):
        self.vx = 0

    def jump(self):
        if self.rect.bottom >= FLOOR:
            self.vy = PLAYER_JUMP_FORCE

    def update(self):
        self.calc_grav()

        self.index += 1
        if self.index >= 60:
            self.index = 0
            self.u += 1
            if self.u == 2:
                self.u = 0

        if self.vx < 0:
            self.image = self.run_left_images[self.index // 10]
        elif self.vx > 0:
            self.image = self.run_right_images[self.index // 10]
        else:
            self.image = self.idle_images[self.u]

        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.y > HEIGHT:
            self.rect.x = 100
            self.rect.y = 100

        if player.rect.right > WIDTH:
            player.rect.right = WIDTH

        if player.rect.left < 0:
            player.rect.left = 0


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

        self.vx = random.randint(-4, 4)
        self.vy = 0

    def update(self):

        self.vy += GRAVITY
        self.rect.x += self.vx
        self.rect.y += self.vy

        if pygame.sprite.collide_mask(self, player):
            player.kill()
            particle.kill()

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vx = -self.vx

        if self.touches < 1 and pygame.sprite.collide_rect(self, floor):
            self.touches += 1
            self.rect.bottom = floor.rect.top
            self.vy = -self.vy * 0.5
        if self.rect.top >= HEIGHT:
            # print('kill')
            # print(rocks_group)
            self.kill()


class Floor(pygame.sprite.Sprite):
    def __init__(self, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/floor.png')
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


class Particle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_to_left = pygame.transform.scale(pygame.image.load('data/particle.png'), (40, 30))
        self.image = self.image_to_left
        self.image_to_right = pygame.transform.scale(pygame.image.load('data/particle_r.png'), (40, 30))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.bottom = player.rect.bottom
        if player.vx > 0:
            self.rect.right = player.rect.left
            self.image = self.image_to_right
        else:
            self.rect.left = player.rect.right
            self.image = self.image_to_left


# !!!!
class ParticleStone(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.images = [
        #     c,
        #     pygame.transform.scale(pygame.image.load('data/rock_particles/particle2.png'), (15, 15)),
        #     pygame.transform.scale(pygame.image.load('data/rock_particles/particle3.png'), (15, 15)),
        #     pygame.transform.scale(pygame.image.load('data/rock_particles/particle4.png'), (15, 15)),
        #     pygame.transform.scale(pygame.image.load('data/rock_particles/particle5.png'), (15, 15))
        # ]
        # self.image = random.choice(self.images)
        self.image = pygame.transform.scale(pygame.image.load('data/rock_particles/particle2.png'), (50, 50))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.bottom = Rock().rect.bottom
        if Rock().vy > 0:
            self.rect.right = Rock().rect.left
            self.image = random.choice(self.images)
        else:
            self.rect.left = Rock().rect.right
            self.image = random.choice(self.images)
        if pygame.sprite.collide_rect(Rock(), floor):
            print(1, Rock().rect.bottom, floor.rect.top)
            Rock().rect.bottom = floor.rect.top
            print(2, Rock().rect.bottom, floor.rect.top)
            print(Rock().vy)
            Rock().vy = -Rock().vy * 0.6
            print(Rock().vy)


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

bg = pygame.transform.scale(pygame.image.load('data/backgrounds/cave.jpg'), (WIDTH, HEIGHT))
floor = pygame.image.load('data/floor.jpg')
floor = pygame.transform.scale(floor, (WIDTH, floor.get_height()))

player = Player()
player_group = pygame.sprite.Group(player)

particle = Particle()
particle_group = pygame.sprite.Group(particle)
# !!!!!
particle_stone = ParticleStone()
particle_stone_group = pygame.sprite.Group(particle_stone)

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

            if event.key == pygame.K_SPACE:
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
    if now < 5000:
        fall_time = 99999
    elif now < 10000:
        fall_time = 1500
    elif now < 15000:
        fall_time = 1200
    elif now < 20000:
        fall_time = 1000
    elif now < 25000:
        fall_time = 900
    elif now < 30000:
        fall_time = 800
    else:
        fall_time = 700

    if now - last_time >= fall_time:
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

    if player.vx and player.rect.bottom >= floor.rect.top:
        particle_group.update()
        particle_group.draw(screen)

    # screen.blit(bg, (0, FLOOR))
    # screen.blit(floor, (0, FLOOR))

    pygame.draw.rect(screen, (255, 255, 255), (0, HEIGHT - 50, 125, HEIGHT))

    if player_group:
        screen.blit(font.render(f'{now / 1000:06.1f}s', True, (0, 0, 0)), (5, HEIGHT - 48))
    elif not time:
        time = now
    else:
        screen.blit(font.render(f'{time / 1000:06.1f}s', True, (0, 0, 0)), (5, HEIGHT - 48))

    if not player_group:
        credits.end_credits()

    pygame.display.flip()
    print(clock.get_fps())

    clock.tick(FPS)

pygame.quit()
