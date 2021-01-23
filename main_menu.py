import pygame
from pygame.locals import *
import os


def text_format(message, text_font, text_size, text_color):
    new_font = pygame.font.Font(text_font, text_size)
    new_text = new_font.render(message, 0, text_color)
    return new_text


# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Game Fonts
font = "data/fonts/WarPriest.ttf"


# Main Menu
def main_menu(screen):
    menu = True
    selected = "start"
    # clock = pygame.time.Clock()

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
                        print("Start")
                        return
                    if selected == "quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        screen.fill(blue)
        title = text_format("Dodging rocks", font, 80, yellow)
        if selected == "start":
            text_start = text_format("START", font, 75, white)
        else:
            text_start = text_format("START", font, 75, black)
        if selected == "quit":
            text_quit = text_format("QUIT", font, 75, white)
        else:
            text_quit = text_format("QUIT", font, 75, black)

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (400 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (400 - (start_rect[2] / 2), 300))
        screen.blit(text_quit, (400 - (quit_rect[2] / 2), 360))

        # screen.blit(title, (WIDTH / 2 - (title_rect[2] / 2), 80))
        # screen.blit(text_start, (WIDTH / 2 - (start_rect[2] / 2), 300))
        # screen.blit(text_quit, (WIDTH / 2 - (quit_rect[2] / 2), 360))

        pygame.display.update()
        pygame.time.Clock().tick(30)
        pygame.display.set_caption("Главное меню")
