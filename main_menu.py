import pygame
from pygame.locals import *
import os
import sqlite3


"""берем из базы данных лучшие время"""
con = sqlite3.connect('rating.db')
cur = con.cursor()
result = cur.execute("""SELECT time FROM columns;""").fetchall()
score = []
for i in result:
    score.append(int(i[0]) / 1000)
score = sorted(score, reverse=True)
score = score[:6]
con.close()


def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)

    return newText


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
font_score = "data/fonts/WarPriestRotalic.ttf"


# Main Menu
def main_menu(screen):
    menu = True
    selected = "start"
    clock = pygame.time.Clock()
    count_num_score = 0

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

        text_score = text_format("rating", font, 50, white)
        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (400 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (400 - (start_rect[2] / 2), 300))
        screen.blit(text_quit, (400 - (quit_rect[2] / 2), 360))
        screen.blit(text_score, (30, 200, 100, 100))

        # вывод в меню рейтинг времени
        height_score = 220
        for num in score:
            height_score += 40
            scores = text_format(f"{str(num)} second", font_score, 30, red)
            screen.blit(scores, (30, height_score, 100, 100))


        # screen.blit(title, (WIDTH / 2 - (title_rect[2] / 2), 80))
        # screen.blit(text_start, (WIDTH / 2 - (start_rect[2] / 2), 300))
        # screen.blit(text_quit, (WIDTH / 2 - (quit_rect[2] / 2), 360))

        pygame.display.update()
        pygame.time.Clock().tick(30)
        pygame.display.set_caption("Python - Pygame Simple Main Menu Selection")
