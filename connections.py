# NYT Connections Recreation - Samantha Song - started 2025.01.23

# Recreate Wordle
# Get Yellow, Green, Blue, Purple sets
#   Yellow - Easiest
#   Green - Easy
#   Blue - Medium
#   Purple - Hardest
# Initialize Buttons & Randomize order
# Show Buttons in grid
# Allow user to click on up to 4 buttons from set
# Buttons at bottom of screen:
#   Deselect - Deselect all selected
#   Shuffle - randomizes order of options
#   Submit -
#       Check to see if set is already guessed
#       If set already guessed, let user know & don't subtract guess
#       If set not already guessed, check to see if correct
#       If set has 3 correct, let user know
#       If set is fully correct, color & move to top of grid


# Import
import numpy as np
import random
import pygame
import sys
sys.path.append('Classes')
from pygame_button import Button

pygame.init()
random.seed()

# Screen, Cards, Buttons Variables
s_width = 600
s_height = 700
screen = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Connections')

# Maximum # Allowed Guesses
max_guess = 6

spacing = s_width / 40
header_space = s_width / 10
guess_space = s_width / 20

h_height = header_space
h_y_pos = spacing
c_width = int((s_width - spacing*5) / 4)
c_height = int((s_width - spacing*5 - 100) / 4)
b_y_pos = header_space + spacing*6 + guess_space + c_height*4
b_width = int((s_width - spacing*4) / 3)
b_height = s_height - b_y_pos - spacing
g_y_pos = header_space + spacing*(11/2) + c_height*4

yellow = np.array(['bubble', 'globe', 'marble', 'pearl'])
green = np.array(['foam', 'froth', 'head', 'lather'])
blue = np.array(['build', 'grow', 'mount', 'swell'])
purple = np.array(['aces', 'neato', 'nifty', 'keen'])

white_color = (255, 255, 252)
yellow_color = (246, 209, 127)
green_color = (171, 190, 132)
blue_color = (145, 186, 222)
purple_color = (142, 142, 194)
light_brown_color = (205, 188, 179)
brown_color = (173, 156, 148)
dark_brown_color = (127, 115, 109)
colors = [yellow_color, green_color, blue_color, purple_color]

bg_color = light_brown_color
hover_color = brown_color
disable_color = dark_brown_color
screen_color = white_color

# Unshuffled Words: Numpy Array (string)
connections = np.concatenate((yellow, green, blue, purple))
# Unshuffled cards: Numpy Array (Button)
cards = np.array([])
# Shuffled Index of Cards: List (int)
# Example: if order[0] = 12, then in grid, [0][0] is cards[12]
order = list(range(16))
# Guesses
guesses = np.empty((0,4), int)
g_color_inds = np.empty((0,4), int)
guess_cards = np.array([])
guess = np.array([])
correct_inds = np.array([])

# Buttons for User
shuffle = Button(screen, name='Shuffle', 
                 x_pos=spacing, y_pos=b_y_pos,
                 width=b_width, height=b_height,
                 bg_color=bg_color, t_color=disable_color,
                 hover_bg_color=hover_color, hover_t_color=screen_color,
                 disable_bg_color=disable_color, disable_t_color=screen_color)
deselect = Button(screen, name='Deselect', 
                  x_pos=(spacing*2 + b_width), y_pos=b_y_pos,
                  width=b_width, height=b_height,
                  bg_color=bg_color, t_color=disable_color,
                  hover_bg_color=hover_color, hover_t_color=screen_color,
                  disable_bg_color=disable_color, disable_t_color=screen_color)
confirm = Button(screen, name='Confirm', 
                 x_pos=(spacing*3 + b_width*2), y_pos=b_y_pos,
                 width=b_width, height=b_height,
                 bg_color=bg_color, t_color=disable_color,
                 hover_bg_color=hover_color, hover_t_color=screen_color,
                 disable_bg_color=disable_color, disable_t_color=screen_color)
show_guesses = Button(screen, name='Show Guesses', 
                      x_pos=(spacing*2 + b_width/2), y_pos=b_y_pos,
                      width=b_width*2, height=b_height,
                      bg_color=bg_color, t_color=disable_color,
                      hover_bg_color=hover_color, hover_t_color=screen_color,
                      disable_bg_color=disable_color, disable_t_color=screen_color)

# Header
header = Button(screen, name='Connections', y_pos=h_y_pos,
                width=s_width, height=h_height,
                disable_bg_color=screen_color, 
                disable_t_color=disable_color,
                clickable=False)

# Subheaders
guess_subhead = Button(screen, name='Guesses Left: ', y_pos=g_y_pos,
                       width = s_width, height=guess_space,
                       disable_bg_color=screen_color,
                       disable_t_color=disable_color,
                       clickable=False)
of_a_kind_3 = Button(screen, name='3 of the 4 are correct', 
                     y_pos=(header_space),
                     width=s_width, height=(spacing*2),
                     disable_bg_color=screen_color,
                     disable_t_color=screen_color,
                     clickable=False)
already_guessed = Button(screen, name='Already Guessed', 
                         y_pos=(header_space),
                         width=s_width, height=(spacing*2),
                         disable_bg_color=screen_color,
                         disable_t_color=screen_color,
                         clickable=False)
game_over = Button(screen, name='Game Over',
                   y_pos=(header_space),
                   width=s_width, height=(spacing*2),
                   disable_bg_color=screen_color,
                   disable_t_color=screen_color,
                   clickable=False)

# Create connections cards -> then shuffle
def create_cards():
    global screen, cards
    for card_name in connections:
        name = card_name
        card = Button(screen, name=name, width=c_width, height=c_height,
                      bg_color=bg_color, hover_bg_color=hover_color,
                      t_color=disable_color, hover_t_color=screen_color,
                      disable_bg_color=disable_color, disable_t_color=screen_color)
        cards = np.append(cards, card)
    shuffle_order()

# Shuffles order of incorrect cards -> then update position
def shuffle_order():
    global order
    not_guessed = np.setdiff1d(order, correct_inds)
    random.shuffle(not_guessed)
    order = np.append(correct_inds, not_guessed)
    update_pos()

# Update x_pos and y_pos of each incorrect card
def update_pos():
    global order
    for i in range(16):
        card_ind = int(order[i])
        row = int(i / 4) % 4
        col = i % 4
        x_pos = spacing + ((c_width + spacing)*col)
        y_pos = ((h_height + spacing*2) + 
                 ((c_height + spacing)*row))
        cards[card_ind].update_position(x_pos, y_pos)

# Display cards - connections cards or guesses
def show_cards(mouse_pos):
    global end_screen, cards, guess_cards
    stack = cards
    if end_screen:
        stack = guess_cards
    for card in stack:
        card.show(mouse_pos)

# Check to see if guess is correct
#   curr_guess: np.array - index of cards of current guess
def check(cur_guess):
    global guesses, g_color_inds, of_a_kind_3, already_guessed
    # Order of guess does not matter
    cur_guess = np.sort(cur_guess)
    # Check to see if guessed before
    if cur_guess.tolist() in guesses.tolist():
        already_guessed.disable_t_color = hover_color
    # If not already guessed before
    else:
        # Add guess to total guesses
        guesses = np.vstack([guesses, cur_guess]) 
        # Convert guesses to color indexes
        guess_ci = ((cur_guess/4).astype(int)%4)
        # Get unique color indexes & counts
        unique_ci, counts = np.unique(guess_ci, return_counts=True)
        # If close to correct (3 of a kind)
        if 3 in counts:
            of_a_kind_3.disable_t_color = hover_color
        # If correct (4 of a kind)
        if 4 in counts:
            correct(unique_ci[0], cur_guess)
        # Add guess colors to total guess colors
        g_color_inds = np.vstack([g_color_inds, guess_ci])
        update_guess_num()
        deselect_all()
    return 0

# Guess is correct
#   color_ind: int - index of color
#   curr_guess: np.array - index of cards of current guess
def correct(color_ind, cur_guess):
    global correct_inds, cards
    correct_inds = np.append(correct_inds, cur_guess)
    cur_guess = cur_guess.astype(int)
    for ind in cur_guess:
        cards[ind].clickable = False
        cards[ind].disable_bg_color = colors[color_ind]
    shuffle_order()
        
# Deselect all cards
def deselect_all():
    global guess
    guess = np.array([])
    clickable_inds = np.setdiff1d(order, correct_inds)
    clickable_inds = clickable_inds.astype(int)
    for ind in clickable_inds:
        cards[ind].clickable = True

# Updates number of (incorrect) guesses avaliable
#   If user guesses correctly, # of guesses avaiable does not go down
#   If no more guesses left -> end game
def update_guess_num():
    global guesses, guess_subhead, guesses_left
    num_guessed = int(len(guesses) - (len(correct_inds)/4))
    guesses_left = 'Guesses Left:'
    for i in range(max_guess - num_guessed):
        guesses_left += ' *'
    guess_subhead.name = guesses_left
    if num_guessed >= max_guess:
        guesses_left = False
        end_game()

# Show rest of the correct answers
def end_game():
    global game_over
    not_guessed = np.setdiff1d(order, correct_inds)
    not_guessed = np.sort(not_guessed)
    # Shows Correct Answers for each set
    for i in range(int(len(not_guessed)/4)):
        correct((int(not_guessed[i*4]/4)%4), 
                not_guessed[i*4:((i+1)*4)])
    game_over.disable_t_color = hover_color
    return 0

# Creates cards representing the user's history of guesses
def create_guesses():
    global guess_cards
    # Maximum number of rows is maximum # of guesses + 4 correct guesses
    max_num = 4 + max_guess
    gc_width = int((s_width - (c_width*2 + spacing*3)) / 4)
    gc_height = int((s_height -  
                     (h_height + spacing*(3+max_num))) / max_num)
    # Create Guess Color Cards
    for gc_row in range(len(g_color_inds)):
        for gc_col in range(4):
            guess_card = Button(screen, name='', 
                                width=gc_width, height=gc_height,
                                x_pos=(c_width+((gc_width+spacing)*gc_col)),
                                y_pos=((h_height+spacing*2) + 
                                       ((gc_height+spacing)*gc_row)),
                                disable_bg_color=colors[g_color_inds[gc_row][gc_col]], 
                                disable_t_color=screen_color,
                                clickable = False)
            guess_cards = np.append(guess_cards, guess_card)

# Start Program 
game_on = True
end_screen = False
guesses_left = True
header.auto_font_size()
guess_subhead.auto_font_size()
already_guessed.auto_font_size()
of_a_kind_3.auto_font_size()
create_cards()
update_guess_num()

while game_on:
    for event in pygame.event.get():
        screen.fill(screen_color)
        # Check to Quit Game 
        if event.type == pygame.QUIT:
            game_on = False
        # Check Cards clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Shuffle, Deselect, Confirm Buttons Clicked
            if shuffle.rect.collidepoint(event.pos):
                shuffle_order()
            elif (deselect.rect.collidepoint(event.pos) and
                  deselect.clickable):
                deselect_all()
            elif (confirm.rect.collidepoint(event.pos) and
                  confirm.clickable):
                check(guess)
            elif (show_guesses.rect.collidepoint(event.pos)):
                end_screen = True
                create_guesses()
            else:
                for i in range(16):
                    # If click on card & not already correct
                    if (cards[i].rect.collidepoint(event.pos) and 
                        cards[i].disable_bg_color == disable_color):
                        # Not yet selected & not guessed 4 - add to guess
                        if cards[i].clickable and len(guess) < 4:
                            guess = np.append(guess, i)
                            cards[i].clickable = False
                        # Already selected - remove from guess
                        else:
                            updated_guess = np.delete(guess, np.where(guess == i))
                            guess = updated_guess
                            cards[i].clickable = True

    # Show Header & Guesses Left
    header.show(pygame.mouse.get_pos())

    # Determine if Buttons & Hints are Visable/Clickable
    if len(guess) == 4:
        confirm.clickable = True
        of_a_kind_3.disable_t_color = screen_color
        already_guessed.show(pygame.mouse.get_pos())
    else:
        confirm.clickable = False
        already_guessed.disable_t_color = screen_color
        of_a_kind_3.show(pygame.mouse.get_pos())
    if len(guess) > 0:
        deselect.clickable = True
    else:
        deselect.clickable = False

    # Determines if on Game Screen or End Screen
    # Shows End Screen
    if end_screen:
        show_cards(pygame.mouse.get_pos())
        game_over.show(pygame.mouse.get_pos())
    else:
        # Show Buttons & Guesses Left if still guesses left
        if (guesses_left and (len(correct_inds) < 16)):
            confirm.show(pygame.mouse.get_pos())
            shuffle.show(pygame.mouse.get_pos())
            deselect.show(pygame.mouse.get_pos())
            guess_subhead.show(pygame.mouse.get_pos())
        else:
            show_guesses.show(pygame.mouse.get_pos())
            game_over.show(pygame.mouse.get_pos())
        # Show cards
        show_cards(pygame.mouse.get_pos())

    # Update Screen
    pygame.display.update()
