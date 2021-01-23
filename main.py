import pygame
import random
import os
import sys
import credits

from main_menu import main_menu

import sqlite3

con = sqlite3.connect('rating.db')
cur = con.cursor()

WIDTH, HEIGHT = 800, 600  # Размеры экрана
FPS = 60

FLOOR = HEIGHT * 0.85  # Расположение пола
PLAYER_SIZE = (40, 56)  # Размеры игрока

GRAVITY = 0.25  # Гравитация
PLAYER_SPEED = 6  # Скорость игрока
PLAYER_JUMP_FORCE = -9  # Сила прыжка игрока


class Player(pygame.sprite.Sprite):
    """Класс игрока"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.idle_images = []
        self.run_left_images = []
        self.run_right_images = []

        for i in range(3):
            self.idle_images.append(pygame.transform.scale(
                pygame.image.load(f'data/sprites/character/idle/adventurer-idle-0{i}.png'), PLAYER_SIZE))

        for i in range(6):
            self.run_right_images.append(
                pygame.transform.scale(pygame.image.load(f'data/sprites/character/run/adventurer-run-0{i}.png'),
                                       PLAYER_SIZE))
            self.run_left_images.append(pygame.transform.flip(self.run_right_images[i], True, False))

        self.image = self.idle_images[0]

        self.index = 0
        self.u = 0

        self.rect = self.image.get_rect()
        self.step = 3
        self.vx = 0
        self.vy = 0

    def calc_grav(self):
        """Расчитываем гравитацию"""
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

        'Анимация'
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

        'Не даем игроку уйти за края экрана'
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.left < 0:
            self.rect.left = 0


class Rock(pygame.sprite.Sprite):
    """Класс падающих камней"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        'В зависимости от уровня выбираем изображение'
        if level_theme == 1:
            self.image = pygame.transform.scale(pygame.image.load('data/sprites/rocks/rock.png'), rock_size)
        elif level_theme == 2:
            self.image = pygame.transform.scale(pygame.image.load('data/sprites/rocks/flax.png'), rock_size)
        elif level_theme == 3:
            self.image = pygame.transform.scale(pygame.image.load('data/sprites/rocks/rock3.png'), rock_size)
        self.orig_image = self.image.copy()

        self.rect = self.image.get_rect()

        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = 0

        self.touches = 0

        self.vx = random.randint(-4, 4)
        self.vy = 0

    def update(self):
        self.vy += GRAVITY + rock_acceleration
        self.rect.x += self.vx
        self.rect.y += self.vy

        'Если камень касается игрока, то убиваем игрока'
        if pygame.sprite.collide_mask(self, player):
            player.kill()
            particle.kill()

        'Не даем улететь за края экрана'
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vx = -self.vx

        if self.touches < 1 and pygame.sprite.collide_rect(self, floor):
            if level_theme == 1:
                rock_fall_sound.play()
            elif level_theme == 2:
                random.choice(cat_fall_sounds).play()
            else:
                blob_sound.play()

            'Создаем частицы'
            create_particles(self.rect.midbottom)

            'Отскок от пола'
            self.touches += 1
            self.rect.bottom = floor.rect.top
            self.vy = -self.vy * 0.5

        'Если камень улетает вниз экрана, то удаляем его'
        if self.rect.top >= HEIGHT:
            self.kill()


class Floor(pygame.sprite.Sprite):
    def __init__(self, h):
        pygame.sprite.Sprite.__init__(self)

        self.themes = [pygame.image.load('data/sprites/floor/floor.png'),
                       pygame.transform.scale(pygame.image.load('data/sprites/floor/floor2.1.png'), (900, 100)),
                       pygame.transform.scale(pygame.image.load('data/sprites/floor/floor3.2.png'), (900, 100))]

        self.image = self.themes[0]
        self.rect = self.image.get_rect()
        self.rect.y = h

    def update(self):
        'В зависимости от уровня меняем изображение'
        if level_theme == 1:
            self.image = self.themes[0]
        elif level_theme == 2:
            self.image = self.themes[1]
        elif level_theme == 3:
            self.image = self.themes[2]


class Particle(pygame.sprite.Sprite):
    """Частица за игроком"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image_to_left = pygame.transform.scale(
            pygame.image.load('data/sprites/particles/particle.png'), (26, 26))
        self.image_to_right = pygame.transform.scale(
            pygame.image.load('data/sprites/particles/particle_r.png'), (26, 26))

        self.image = self.image_to_left
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.bottom = player.rect.bottom
        'Отрисовываем только если игрок движется'
        if player.vx > 0:
            self.rect.right = player.rect.left
            self.image = self.image_to_right
        else:
            self.rect.left = player.rect.right
            self.image = self.image_to_left


class RockParticle(pygame.sprite.Sprite):
    """Частицы камней"""
    images = []
    for i in range(1, 6):
        images.append(pygame.image.load(f'data/sprites/rock_particles/particle{i}.png'))

    def __init__(self, pos, dx, dy):
        super().__init__(rock_particles_group)
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        'Если частица улетает за экран, то удаляем ее'
        if not self.rect.colliderect(screen.get_rect()):
            self.kill()


def load_image(name, colorkey=None):
    'Загрузка изображений'
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


def create_particles(pos):
    """Создание частиц, отлетающих от камня"""
    for _ in range(random.randint(4, 13)):
        RockParticle(pos, random.randint(-8, 9), random.randint(-2, 8))


def draw_level_num(num):
    """Отрисовка номера уровня"""
    font = pygame.font.Font(None, 100)
    text = font.render(str(num), True, (248, 190, 5))
    screen.blit(text, (WIDTH - 50, 0))


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
end_time = 0

pygame.display.set_caption('Dodging rocks')  # Название игры и окна

clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 40)

'Подгружаем фоны'
bg = pygame.transform.scale(pygame.image.load('data/sprites/backgrounds/cave.jpg'), (WIDTH, HEIGHT))
bg2 = pygame.transform.scale(pygame.image.load('data/sprites/backgrounds/bg2.png'), (WIDTH, HEIGHT))
bg3 = pygame.transform.scale(pygame.image.load('data/sprites/backgrounds/bg3.png'), (WIDTH, HEIGHT))

'Подгружаем звуковые эффекты'
rock_fall_sound = pygame.mixer.Sound('data/sfx/fall.ogg')
cat_fall_sounds = [pygame.mixer.Sound('data/sfx/meow.ogg'), pygame.mixer.Sound('data/sfx/meow1.ogg'),
                   pygame.mixer.Sound('data/sfx/meow2.ogg'), pygame.mixer.Sound('data/sfx/meow3.ogg')]
blob_sound = pygame.mixer.Sound('data/sfx/water.ogg')

while True:
    main_menu(screen)  # Начальное меню
    'Создаем основные игровые объекты'
    player = Player()
    player_group = pygame.sprite.Group(player)

    floor = Floor(FLOOR)
    floor_group = pygame.sprite.Group(floor)

    particle = Particle()
    particle_group = pygame.sprite.Group(particle)

    rocks_group = pygame.sprite.Group()
    rock_particles_group = pygame.sprite.Group()

    level_theme = 1  # Тема уровня

    rock_size = (80, 80)  # Размеры камней
    fall_time = 1500  # Задержка между камнями в миллисекундах
    rock_acceleration = 0  # Ускорение падения камней

    last_time = 0
    time = 0
    timee = 0

    start_time = pygame.time.get_ticks()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            'Управление игроком'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()

                if event.key == pygame.K_RIGHT:
                    player.go_right()

                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    player.jump()

                elif event.key == pygame.K_1:
                    rocks_group.add(Rock())
                    floor.rect.bottom = HEIGHT // 2

                if event.key == pygame.K_2:
                    floor.rect.bottom = HEIGHT * 8 // 10

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.vx < 0:
                    player.stop()

                if event.key == pygame.K_RIGHT and player.vx > 0:
                    player.stop()

        'Высчитываем время с начала текущей игры'
        now = pygame.time.get_ticks() - start_time

        'Создаем камни'
        if now - last_time >= fall_time:
            rocks_group.add(Rock())
            last_time = now

        'Обновляем игровые объекты'
        player_group.update()
        rocks_group.update()
        floor_group.update()
        rock_particles_group.update()

        'Меняем тему и сложность в зависимости от прошедшего времени'
        if now < 2000:
            fall_time = 99999
            screen.blit(bg, (0, 0))

        elif now <= 10000:
            fall_time = 1500
            screen.blit(bg, (0, 0))
            rock_acceleration = 0.1

        elif now < 12000:
            fall_time = 99999
            screen.blit(bg, (0, 0))

        elif now < 20000:
            fall_time = 1000
            rock_size = (120, 120)
            rock_acceleration = 0
            screen.blit(bg2, (0, 0))
            level_theme = 2

        elif now < 22000:
            fall_time = 99999
            screen.blit(bg2, (0, 0))

        elif now <= 30000:
            fall_time = 700
            rock_size = (70, 70)
            rock_acceleration = 0.1
            screen.blit(bg3, (0, 0))
            level_theme = 3

        else:
            fall_time = 500
            rock_size = (70, 70)
            rock_acceleration = 0.1
            screen.blit(bg3, (0, 0))
            level_theme = 3

        'Рисуем все на экране'
        draw_level_num(level_theme)

        player_group.draw(screen)
        rocks_group.draw(screen)
        floor_group.draw(screen)
        rock_particles_group.draw(screen)

        'Рисуем частицу за игроком только если он не в прыжке'
        if player.vx and player.rect.bottom >= floor.rect.top:
            particle_group.update()
            particle_group.draw(screen)

        'Отображаем время, прошедшее с начала игры'
        pygame.draw.rect(screen, (255, 255, 255), (0, HEIGHT - 50, 125, HEIGHT))

        if player_group:
            screen.blit(font.render(f'{now / 1000:06.1f}s', True, (0, 0, 0)), (5, HEIGHT - 48))
        elif not time:
            time = now
        else:
            screen.blit(font.render(f'{time / 1000:06.1f}s', True, (0, 0, 0)), (5, HEIGHT - 48))

        'Если игрок умирает, запоминаем время смерти'
        if not player_group:
            if not timee:
                timee = now
            if now - timee >= 5000:
                break

        pygame.display.flip()
        # print(clock.get_fps())
        clock.tick(FPS)

    'Показываем титры'
    credits.end_credits(screen)
    rock_size = (80, 80)  # Размеры камней
    fall_time = 1500  # Задержка между камнями в миллисекундах
    rock_acceleration = 0  # Ускорение падения камней

    cur.execute(f"INSERT INTO columns(time) VALUES(?)", (str(timee),)).fetchall()
    con.commit()
    con.close()

    end_time = pygame.time.get_ticks()
    start_time = 0

con.close()
pygame.quit()
