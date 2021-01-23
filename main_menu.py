import pygame
from pygame.locals import *
import os

font = "data/fonts/WarPriest.ttf"


def text_format(message, text_font, text_size, text_color):
    new_font = pygame.font.Font(text_font, text_size)
    new_text = new_font.render(message, 0, text_color)
    return new_text


def main_menu(screen):
    """Начальное меню игры"""

    menu = True
    selected = "start"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        return
                    if selected == "quit":
                        pygame.quit()
                        quit()

        screen.fill((0, 0, 0))
        title = text_format("Dodging rocks", font, 80, (255, 255, 255))
        if selected == "start":
            text_start = text_format("START", font, 75, (255, 255, 255))
        else:
            text_start = text_format("START", font, 75, (50, 50, 50))
        if selected == "quit":
            text_quit = text_format("QUIT", font, 75, (255, 255, 255))
        else:
            text_quit = text_format("QUIT", font, 75, (50, 50, 50))

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        screen.blit(title, (400 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (400 - (start_rect[2] / 2), 300))
        screen.blit(text_quit, (400 - (quit_rect[2] / 2), 360))

        pygame.display.update()
        pygame.time.Clock().tick(30)
        pygame.display.set_caption("Главное меню")
