# Connections
## Description
This is a recreating of NYT Connections using Pygame. 
The computer randomly chooses 4 sets from a CSV file, one from each level of difficulty (yellow, green, blue, purple).
The User then guesses 4 cards that they think is a set, and can click the `Confirm` button to submit their guess.
The User can also choose to `Shuffle` the cards, or `Deselect` the selected cards.
In the event that the User guesses correctly, the cards will become the color associated with their difficulty and move to the top of the remaining cards.
If the User guesses incorrectly, the will cards will be deselected and the number of remaining guesses will decrease by 1.
However, if the User has already made the guess before, the screen will display that the User has `Already Guessed` the set.
If the set contains 3 of 4 cards that belong to the same set, the screen will provide the hint `3 of the 4 are correct`.
Once all guesses have been depleated, or the User guesses all sets correctly, the correct answers will be displayed and the User has the option to view the history of guesses.
After the User views their history, they can choose to `Play Again` in which a new set of cards will be created randomly.

<img src="https://github.com/user-attachments/assets/3e910519-c2ae-43e0-a26d-06ce7a92185a" width="300" height="360" class="center">

## CSV Requirements
The CSV file requires 6 columns:
- `Difficulty` - The color representing the difficulty of the set (`yellow`, `green`, `blue`, `purple`)
- `Group Name` - The name representing how the words in the set are related
- `First Word` - The first word in the set
- `Second Word` - The second word in the set
- `Third Word` - The third word in the set
- `Fourth Word` - The fourth word in the set

>[!NOTE]
>By default, the program assumes that there are column names. Thus, the first row will not be tested.

## Adapting the Code
In the code, update the file name to the desired CSV file name `csv_name = '<filename>.csv'`.

In addition, the number of guesses can be easily adjusted for added difficulty/ease by changing `max_guess`

## Acknowledgements
This program relies on the [Pygame Button Class](https://github.com/ssam9423/pygame_button)[^1] and [Pygame Textbox Class](https://github.com/ssam9423/pygame_textbox)[^1] classes.

[^1]: by [Ssam9423](https://github.com/ssam9423/)
