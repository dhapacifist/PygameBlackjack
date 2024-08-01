#verplichte imports

import copy
import random
import pygame

pygame.init()

#variables blackjack

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4
game_deck = copy.deepcopy(decks * one_deck)
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Welcome to Blackjack!')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
active = False


# game condities & buttons
def draw_game(act):
    button_list = [] 
    #on startup (not active) deal new game
    if not act:
        deal = pygame.rect.Rect




#main game loop: keeps looping while game is running

run = True
while  run:
    # game at framerate & bg col
    timer.tick(fps)
    screen.fill('green')
    buttons = draw_game(active)
    #events during game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update ipv flip, tests later
    pygame.display.update()
pygame.quit
