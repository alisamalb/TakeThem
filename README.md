# TakeThem

TakeThem is python module for a a strategic card game. This repository also offers a command-line interface (CLI) to play the game. The module is designed to be expandable with different computer agents that act as players. The game's mechanics are simple to understand but offer a depth of strategy as players must make decisions that influence the outcome in a dynamic playing environment.

## How to install
Git clone the repository, and then run in the TakeThem directory:

```bash
python TakeThem.py
```

## How to Play

### Objective

The objective of "TakeThem" is to avoid collecting cards, as each card carries a certain number of penalty points and the aim is to have the fewest points by the end of the game.

### Game Setup

- The game is played using a deck of numbered cards, each card having a penalty value.
- The total number of cards is 10 for each player + 4
- At the start, each player is dealt 10 cards.
- Four cards are placed face-up to form the beginning of four rows.

### Playing a Turn

1. **Select a Card:** Each player chooses one card from their hand. The card is place in a list of chosen cards.
2. **Reveal and Place Cards:** All chosen cards are revealed and placed on the rows following these rules:
   - A card must be placed on the row where it follows the highest number that is still lower than the played card.
   - If the played card is lower than all end cards on the table, the player picks a row and collects all its cards, placing their card down as the new row starter.
   - If placing a card completes a row with six cards, the player collects the first five cards and leaves their played card as the start of a new row.


