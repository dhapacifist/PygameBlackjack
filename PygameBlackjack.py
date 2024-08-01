#verplichte imports

import copy
import random
import pygame

pygame.init()

#variables blackjack


cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Welcome to Blackjack!')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smallfont = pygame.font.Font('freesansbold.ttf', 36)
active = False
initial_deal = True     #aparte variable voor 1e deal, 2 kaarten
game_deck = copy.deepcopy(decks * one_deck)
my_hand = []
dealer_hand = []
outcome = 0

#scoreboard
records = [0, 0, 0]
player_ = 0 
dealer_score = 0


# game condities & buttons
def draw_game(act, record):
    button_list = [] 
    #on startup (not active) deal new game
    if not act:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5 )
        pygame.draw.rect(screen, 'black', [150, 20, 300, 100], 3, 5 )
        deal_text = font.render('DEAL HAND', True, 'black' )
        screen.blit(deal_text, (165, 50))
        button_list.append(deal)
        
# once game started, shot hit and stand buttons and and win/loss records
  
    #copy pasted deal, changing button loc
    else:
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5 )
        pygame.draw.rect(screen, 'black', [0, 700, 300, 100], 3, 5 )
        hit_text = font.render('HIT ME', True, 'black' )
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)
        
        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5 )
        pygame.draw.rect(screen, 'black', [300, 700, 300, 100], 3, 5 )
        stand_text = font.render('STAND', True, 'black' )
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)
        score_text = smallfont.render(f'Wins: {record[0]}    Losses: {record[1]}    Ties: {record[2]}', True, 'white')
        screen.blit(score_text, (15, 840))
    return button_list


#main game loop: keeps looping while game is running

run = True
while  run:
    # game at framerate & bg col
    timer.tick(fps)
    screen.fill('green')
    buttons = draw_game(active, records)

    #events during game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if event.type == pygame.MOUSEBUTTONUP:
        if not active:
            if buttons[0].collidepoint(event.pos):  #unclick op button event
                active = True
                initial_deal = True     #aparte variable voor 1e deal, 2 kaarten
                game_deck = copy.deepcopy(decks * one_deck)
                my_hand = []
                dealer_hand = []
                outcome = 0

    #update ipv flip, tests later
    pygame.display.update()
pygame.quit
