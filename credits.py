import pygame
from pygame.locals import *


def end_credits(screen):
    """Титры и рестарт игры"""

    screen_r = screen.get_rect()
    font = pygame.font.Font('data/fonts/MidnightMinutes.otf', 36)
    clock = pygame.time.Clock()

    smallfont = pygame.font.SysFont(None, 60)
    is_intro = True
    while is_intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                print(1)
                if event.key == pygame.K_ESCAPE:
                    is_intro = False
                elif event.key == pygame.K_SPACE:
                    return
        screen.fill((255, 255, 255))
        text = smallfont.render("Press ESC to finish game", True, (0, 0, 0))
        text2 = smallfont.render("Press SPACE to restart", True, (0, 0, 0))
        screen.blit(text, [140, 240])
        screen.blit(text2, [140, 310])
        pygame.display.update()

    credit_list = [" ", " ", "DODGING ROCKS", " ", " ",
                   "DEVELOPMENT", "FOMIN NIKITA", "ROMANOV SEMEN", " ",
                   "IDEA", "ROMANOV SEMEN", "FOMIN NIKITA", " ",
                   "TESTING", "FOMIN NIKITA", "ROMANOV SEMEN", " ",
                   "SPECIAL THANKS", " ", "ROMANOV SEMEN", "FOMIN NIKITA", " ",
                   ]

    texts = []

    for i, line in enumerate(credit_list):
        s = font.render(line, 1, (10, 10, 10))
        r = s.get_rect(centerx=screen_r.centerx, y=screen_r.bottom + i * 45)
        texts.append((r, s))

    while True:
        for e in pygame.event.get():
            if e.type == QUIT or e.type == KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        screen.fill((255, 255, 255))

        for r, s in texts:
            r.move_ip(0, -1)
            screen.blit(s, r)

        if not screen_r.collidelistall([r for (r, _) in texts]):
            break

        pygame.display.flip()
        clock.tick(60)
