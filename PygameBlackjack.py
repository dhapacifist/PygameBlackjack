#verplichte imports
import copy
import random
import pygame



pygame.init()
pygame.mixer.init()
#variables blackjack


pygame.mixer.music.load('background_music.mp3')  
pygame.mixer.music.set_volume(0.2) 
pygame.mixer.music.play(-1)

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
initial_deal = False  #aparte variable voor 1e deal, 2 kaarten
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
add_score = False
results = ['', 'YOU DIED', 'A WINNER IS YOU!', 'HOUSE WINS!', 'TIE']
records = [0, 0, 0]
player_score = 0 
dealer_score = 0
green = (0, 70, 20)
#functions

#deal cards by selecting randomly from deck, make function for one card at a time

def deal_cards(current_hand, current_deck):
    card = random.randint (0, len(current_deck) - 1)
    current_hand.append(current_deck[card])
    current_deck.pop(card)
  
    return current_hand, current_deck

# draw scores for player and dealer screen

def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (350, 100))
        
#draw cards on screen

def draw_card(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 455 + (5 * i), 120, 220], 0 , 5)
        screen.blit(font.render(player[i], True, 'black'), (75 + 70*i, 460 + 5*i))
        screen.blit(font.render(player[i], True, 'black'), (75 + 70*i, 630 + 5*i))
        pygame.draw.rect(screen, 'red', [70 + (70 * i), 455 + (5 * i), 120, 220], 5 , 5)

    # If player hasnt finished turn, dealer will hide card

    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 155 - (5 * i), 120, 220], 0 , 5)  # minus for symmetry
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70*i, 160 - 5*i))  
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70*i, 330 - 5*i))
        else:
            screen.blit(font.render('???', True, 'black'), (75 + 70*i, 160 - 5*i))
            screen.blit(font.render('???', True, 'black'), (75 + 70*i, 330 - 5*i))
        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 155 - (5 * i), 120, 220], 5 , 5)

#check endgame conditions function

def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    #check endgame scenarios is player stood, bosted or blackjack
    # result  1- player bust, 2-wins, 3-loss, 4-push
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <=  21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add
            
def draw_game(act, record, result):
    button_list = [] 
    #on startup (not active) deal new game
    if not act:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5 )
        pygame.draw.rect(screen, 'black', [150, 20, 300, 100], 3, 5 )
        deal_text = font.render('DEAL HAND', True, 'black' )
        screen.blit(deal_text, (165, 50))
        button_list.append(deal)
# once game started, hit and stand buttons and and win/loss records
    else:
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5 )
        pygame.draw.rect(screen, 'black', [0, 700, 300, 100], 3, 5 )
        hit_text = font.render('HIT ME', True, 'black' )
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)
        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5 )
        pygame.draw.rect(screen, 'black', [300, 700, 300, 100], 3, 5 )
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)
        score_text = smallfont.render(f'Wins: {record[0]}    Losses: {record[1]}    Ties: {record[2]}', True, 'white')
        screen.blit(score_text, (15, 840))
  # if theres an outcome for the hand played, display restart button & announce game result
    if result != 0:
        screen.blit(font.render(results[result], True, 'black'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 100], 0, 5 )
        pygame.draw.rect(screen, 'blue', [150, 220, 300, 100], 3, 5 )
        pygame.draw.rect(screen, 'black', [150, 220, 300, 100], 3, 5 )
        deal_text = font.render('NEW HAND', True, 'black' )
        screen.blit(deal_text, (165, 250))
        button_list.append(deal)
    return button_list

#pass in player or dealer hand and get best score possible
def calculate_score(hand):
    # Calculate hand score fresh every time, checking how many aces we have
    hand_score = 0
    aces_count = hand.count('A')
    
    for card in hand:
        # For 2,3,4,5,6,7,8,9 - add the number to total
        if card in cards[:9]:  # checking 2 to 9
            hand_score += int(card)
        # For 10 and face cards
        elif card in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        # For Aces, start by adding 11
        elif card == 'A':
            hand_score += 11

    # Determine how many aces needed to be 1 to be under 21
    while hand_score > 21 and aces_count > 0:
        hand_score -= 10  # Convert one Ace from 11 to 1
        aces_count -= 1

    return hand_score
                
#main game loop: keeps looping while game is running

run = True
while  run:
    # game at framerate & bg col
    timer.tick(fps)
    screen.fill(green)

    #inial deal to player and dealer
    if initial_deal:
        for i in range(2):
          my_hand, game_deck, deal_cards(my_hand, game_deck)
          dealer_hand, game_deck, deal_cards(dealer_hand, game_deck)
          initial_deal = False

    # once game is activated, and dealt, calculate score and display cards
    if active:
        player_score = calculate_score(my_hand)
        draw_card(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)
    buttons = draw_game(active, records, outcome)

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
                    outcome = 0   # second outcome 0 redudant in video?
                    hand_active = True
                    reveal_dealer = False
                    add_score = True
            else:
                # if player can hit, allow them to draw a card
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                    # allows player to end turn (stand)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint (event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        add_score = True
                        dealer_score = 0
                        player_score = 0

    # if player busts, automatically end turn, treat like a stand
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

    #update ipv flip, tests later
    pygame.display.update()
pygame.quit
