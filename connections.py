"""NYT Connections Recreation - Samantha Song - started 2025.01.23"""

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
import random
import sys
import numpy as np
import pandas as pd
import pygame

sys.path.append('Classes')
from pygame_button import Button

# Initialize
pygame.init()
random.seed()

# Maximum Number of Allowed Guesses
MAX_GUESS = 4

# Sort Cards from CSV File
CVS_NAME = r"Connections\connections.csv"
c_set = pd.read_csv(CVS_NAME, skiprows=1, header=None)
yellows = np.empty((0, 4), dtype='<U10')
greens = np.empty((0, 4), dtype='<U10')
blues = np.empty((0, 4), dtype='<U10')
purples = np.empty((0, 4), dtype='<U10')

for i in range(c_set.shape[0]):
    if c_set.iloc[i][0].lower() == 'yellow':
        yellows = np.vstack([yellows, c_set.iloc[i, 2:]])
    elif c_set.iloc[i][0].lower() == 'green':
        greens = np.vstack([greens, c_set.iloc[i, 2:]])
    elif c_set.iloc[i][0].lower() == 'blue':
        blues = np.vstack([blues, c_set.iloc[i, 2:]])
    else:
        purples = np.vstack([purples, c_set.iloc[i, 2:]])

# Screen, Cards, Buttons Variables
S_WIDTH = 600
S_HEIGHT = 700
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
pygame.display.set_caption('Connections')

SPACING = S_WIDTH / 40
HEADER_SPACE = S_WIDTH / 10
GUESS_SPACE = S_WIDTH / 20

H_HEIGHT = HEADER_SPACE
H_Y_POS = SPACING
C_WIDTH = int((S_WIDTH - SPACING*5) / 4)
C_HEIGHT = int((S_WIDTH - SPACING*5 - 100) / 4)
B_Y_POS = HEADER_SPACE + SPACING*6 + GUESS_SPACE + C_HEIGHT*4
B_WIDTH = int((S_WIDTH - SPACING*4) / 3)
B_HEIGHT = S_HEIGHT - B_Y_POS - SPACING
G_Y_POS = HEADER_SPACE + SPACING*(11/2) + C_HEIGHT*4

# Color Variables
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

# Global Variables
# Unshuffled Words: Numpy Array (string)
connections = np.array([])
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

# Game State Variables
game_on = True
end_screen = False
guesses_left = True

# Buttons for User
shuffle = Button(screen, name='Shuffle',
                 x_pos=SPACING, y_pos=B_Y_POS,
                 width=B_WIDTH, height=B_HEIGHT,
                 bg_color=bg_color, t_color=disable_color,
                 hover_bg_color=hover_color, hover_t_color=screen_color,
                 disable_bg_color=disable_color, disable_t_color=screen_color)
deselect = Button(screen, name='Deselect',
                  x_pos=(SPACING*2 + B_WIDTH), y_pos=B_Y_POS,
                  width=B_WIDTH, height=B_HEIGHT,
                  bg_color=bg_color, t_color=disable_color,
                  hover_bg_color=hover_color, hover_t_color=screen_color,
                  disable_bg_color=disable_color, disable_t_color=screen_color)
confirm = Button(screen, name='Confirm',
                 x_pos=(SPACING*3 + B_WIDTH*2), y_pos=B_Y_POS,
                 width=B_WIDTH, height=B_HEIGHT,
                 bg_color=bg_color, t_color=disable_color,
                 hover_bg_color=hover_color, hover_t_color=screen_color,
                 disable_bg_color=disable_color, disable_t_color=screen_color)
show_guesses = Button(screen, name='Show Guesses',
                      x_pos=(SPACING*2 + B_WIDTH/2), y_pos=B_Y_POS,
                      width=B_WIDTH*2, height=B_HEIGHT,
                      bg_color=bg_color, t_color=disable_color,
                      hover_bg_color=hover_color, hover_t_color=screen_color,
                      disable_bg_color=disable_color, disable_t_color=screen_color)
play_again = Button(screen, name='Play Again',
                    x_pos=(SPACING*2 + B_WIDTH/2), y_pos=B_Y_POS,
                    width=B_WIDTH*2, height=B_HEIGHT,
                    bg_color=bg_color, t_color=disable_color,
                    hover_bg_color=hover_color, hover_t_color=screen_color,
                    disable_bg_color=disable_color, disable_t_color=screen_color)

# Header
header = Button(screen, name='Connections', y_pos=H_Y_POS,
                width=S_WIDTH, height=H_HEIGHT,
                disable_bg_color=screen_color,
                disable_t_color=disable_color,
                clickable=False)

# Subheaders
guess_subhead = Button(screen, name='Guesses Left: ', y_pos=G_Y_POS,
                       width = S_WIDTH, height=GUESS_SPACE,
                       disable_bg_color=screen_color,
                       disable_t_color=disable_color,
                       clickable=False)
of_a_kind_3 = Button(screen, name='3 of the 4 are correct',
                     y_pos=(HEADER_SPACE),
                     width=S_WIDTH, height=(SPACING*2),
                     disable_bg_color=screen_color,
                     disable_t_color=screen_color,
                     clickable=False)
already_guessed = Button(screen, name='Already Guessed',
                         y_pos=(HEADER_SPACE),
                         width=S_WIDTH, height=(SPACING*2),
                         disable_bg_color=screen_color,
                         disable_t_color=screen_color,
                         clickable=False)
game_over = Button(screen, name='Game Over',
                   y_pos=(HEADER_SPACE),
                   width=S_WIDTH, height=(SPACING*2),
                   disable_bg_color=screen_color,
                   disable_t_color=hover_color,
                   clickable=False)

def select_cards():
    """Randomly selects one set from each difficulty level"""
    y = yellows[random.randint(0, len(yellows)-1)]
    g = greens[random.randint(0, len(greens)-1)]
    b = blues[random.randint(0, len(blues)-1)]
    p = purples[random.randint(0, len(purples)-1)]
    return np.concatenate((y, g, b, p))

def create_cards():
    """Creates connections cards -> shuffles"""
    global cards
    for card_name in connections:
        name = card_name
        card = Button(screen, name=name, width=C_WIDTH, height=C_HEIGHT,
                      bg_color=bg_color, hover_bg_color=hover_color,
                      t_color=disable_color, hover_t_color=screen_color,
                      disable_bg_color=disable_color, disable_t_color=screen_color)
        cards = np.append(cards, card)
    resize_font()
    shuffle_order()

def resize_font():
    """Resizes font to smallest auto font of all cards"""
    smallest_font = cards[0].font_size
    # Determine Smallest Auto Font Size
    for card in cards:
        card.auto_font_size()
        if card.font_size < smallest_font:
            smallest_font = card.font_size
    # Resize Font on all Cards to Smallest Auto Font Size
    for card in cards:
        card.update_font_size(smallest_font)

def shuffle_order():
    """Shuffles order of incorrect cards -> updates position"""
    global order
    not_guessed = np.setdiff1d(order, correct_inds)
    random.shuffle(not_guessed)
    order = np.append(correct_inds, not_guessed)
    update_pos()

def update_pos():
    """Updates x_pos and y_pos of each incorrect card"""
    for ind in range(16):
        card_ind = int(order[ind])
        row = int(ind / 4) % 4
        col = ind % 4
        x_pos = SPACING + ((C_WIDTH + SPACING)*col)
        y_pos = ((H_HEIGHT + SPACING*2) +
                 ((C_HEIGHT + SPACING)*row))
        cards[card_ind].update_position(x_pos, y_pos)

def show_cards(mouse_pos):
    """Displays cards - either connections cards or user's guesses"""
    stack = cards
    if end_screen:
        stack = guess_cards
    for card in stack:
        card.show(mouse_pos)


def check(cur_guess):
    """Checks to see if guess is correct"""
    global guesses, g_color_inds
    # Order of guess does not matter
    cur_guess = np.sort(cur_guess)
    # Check to see if guessed before
    # cur_guess: np.array - index of cards of current guess
    if cur_guess.tolist() in guesses.tolist():
        already_guessed.disable_t_color = hover_color
    # If not already guessed before
    else:
        # Add guess to total guesses
        guesses = np.vstack([guesses, cur_guess])
        # Convert guesses to color indexes
        guess_ci = (cur_guess/4).astype(int)%4
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

def correct(color_ind, cur_guess):
    """If guess is correct, make them unclickable and shuffle"""
    global correct_inds
    correct_inds = np.append(correct_inds, cur_guess)
    cur_guess = cur_guess.astype(int)
    for ind in cur_guess:
        cards[ind].clickable = False
        cards[ind].disable_bg_color = colors[color_ind]
    shuffle_order()

def deselect_all():
    """Deselect all cards"""
    global guess
    guess = np.array([])
    clickable_inds = np.setdiff1d(order, correct_inds)
    clickable_inds = clickable_inds.astype(int)
    for ind in clickable_inds:
        cards[ind].clickable = True

def update_guess_num():
    """Updates the number of incorrect guesses avaliable"""
    global guesses_left
    # If user guesses correctly, # of guesses avaiable does not go down
    num_guessed = int(len(guesses) - (len(correct_inds)/4))
    g_hint = 'Guesses Left:'
    for _ in range(MAX_GUESS - num_guessed):
        g_hint += ' *'
    guess_subhead.name = g_hint
    # If no more guesses left -> end game
    if num_guessed >= MAX_GUESS:
        guesses_left = False
        end_game()

def end_game():
    """Show rest of the correct answers"""
    global game_over
    not_guessed = np.setdiff1d(order, correct_inds)
    not_guessed = np.sort(not_guessed)
    # Shows Correct Answers for each set
    for diff_set in range(int(len(not_guessed)/4)):
        correct((int(not_guessed[diff_set*4]/4)%4),
                not_guessed[diff_set*4:((diff_set+1)*4)])
    return 0

def create_guesses():
    """Creates cards representing the user's history of guesses"""
    global guess_cards
    # Maximum number of rows is maximum # of guesses + 4 correct guesses
    max_num = 3 + MAX_GUESS
    gc_width = int((S_WIDTH - (C_WIDTH*2 + SPACING*3)) / 4)
    gc_height = int((S_HEIGHT -
                     (H_HEIGHT + SPACING*(3+max_num) + B_HEIGHT)) / max_num)
    # Create Guess Color Cards
    for gc_row, _ in enumerate(g_color_inds):
        for gc_col in range(4):
            guess_card = Button(screen, name='',
                                width=gc_width, height=gc_height,
                                x_pos=(C_WIDTH+((gc_width+SPACING)*gc_col)),
                                y_pos=((H_HEIGHT+SPACING*2) +
                                       ((gc_height+SPACING)*gc_row)),
                                disable_bg_color=colors[g_color_inds[gc_row][gc_col]],
                                disable_t_color=screen_color,
                                clickable = False)
            guess_cards = np.append(guess_cards, guess_card)

def restart():
    """Resets variables and creates new cards to restart game"""
    global connections, cards, order
    global guesses, g_color_inds, guess_cards, guess
    global correct_inds, end_screen, guesses_left
    global already_guessed, of_a_kind_3
    # Get New Yellow, Green, Blue, Purple Cards
    connections = select_cards()
    # Reset Global Variables
    cards = np.array([])
    order = list(range(16))
    guesses = np.empty((0,4), int)
    g_color_inds = np.empty((0,4), int)
    guess_cards = np.array([])
    guess = np.array([])
    correct_inds = np.array([])
    # Reset Buttons
    show_guesses.clickable = False
    end_screen = False
    guesses_left = True
    # Reset Hints
    already_guessed.disable_t_color = screen_color
    of_a_kind_3.disable_t_color = screen_color
    # Create New Cards
    create_cards()
    update_guess_num()

# Start Program
header.auto_font_size()
guess_subhead.auto_font_size()
already_guessed.auto_font_size()
of_a_kind_3.auto_font_size()
restart()

while game_on:
    for event in pygame.event.get():
        screen.fill(screen_color)
        # Check to Quit Game
        if event.type == pygame.QUIT:
            game_on = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # During End Screen
            if end_screen:
                if play_again.rect.collidepoint(event.pos):
                    restart()
            # During Play Screen
            else:
                if shuffle.rect.collidepoint(event.pos):
                    shuffle_order()
                if (deselect.rect.collidepoint(event.pos) and
                    deselect.clickable):
                    deselect_all()
                if (confirm.rect.collidepoint(event.pos) and
                    confirm.clickable):
                    check(guess)
                if (show_guesses.rect.collidepoint(event.pos) and
                    show_guesses.clickable):
                    end_screen = True
                    create_guesses()
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
    # Shows End Screen - User's guesses
    if end_screen:
        show_cards(pygame.mouse.get_pos())
        game_over.show(pygame.mouse.get_pos())
        play_again.show(pygame.mouse.get_pos())
    else:
        # Show Buttons & Guesses Left if still guesses left
        if (guesses_left and (len(correct_inds) < 16)):
            confirm.show(pygame.mouse.get_pos())
            shuffle.show(pygame.mouse.get_pos())
            deselect.show(pygame.mouse.get_pos())
            guess_subhead.show(pygame.mouse.get_pos())
        # No Guesses left or all guessed correctly
        else:
            show_guesses.clickable = True
            show_guesses.show(pygame.mouse.get_pos())
            game_over.show(pygame.mouse.get_pos())
        # Show cards
        show_cards(pygame.mouse.get_pos())

    # Update Screen
    pygame.display.update()
