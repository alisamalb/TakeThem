# TakeThem

TakeThem is a Python module for a strategic card game. This repository also offers a command-line interface (CLI) to play the game. The module is designed to be expandable with different computer agents that act as players. The game's mechanics are simple to understand but offer a depth of strategy as players must make decisions that influence the outcome in a dynamic playing environment.

## Features
- Simple yet strategic gameplay.
- Expandable with different computer agents.
- Command-line interface to play against various agents.

## Installation

To install and run TakeThem, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/TakeThem.git
    ```

2. Navigate to the TakeThem directory:

    ```bash
    cd TakeThem
    ```

3. Run the game:

    ```bash
    python TakeThem.py
    ```

## Requirements

The AI agent is the only sub-module with additional requirements:
- `tensorflow` and `numpy` for the proper execution.
- `matplotlib` to show the progress of training.

You can install these dependencies using pip:

```bash
pip install tensorflow numpy matplotlib
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

## Agents

At the moment, it is possible to play against:

- A player making random choices (RandomAgent)
- A player who plays cards that minimize the risk (MinimumLogicAgent)
- A neural network trained against RandomAgent and MinimumLogicAgent

The neural network agent is the default in the CLI game, and there is no user interface to change the selection. To use any of the other two agents, edit TakeThem.py and import the agents:

```python
from takethem.agents.MinimumLogicAgent import MinimumLogicAgent
from takethem.agents.RandomAgent import RandomAgent
```

Then, set the otherplayers argument in:

```python 
game = Game(otherplayers=[AIagent])
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

- Fork the repository.
- Create a new branch (git checkout -b feature-branch).
- Make your changes.
- Commit your changes (git commit -m 'Add some feature').
- Push to the branch (git push origin feature-branch).
- Open a pull request.

## To Do

- The game should call a player's action when cards are played but not yet disposed on the table. (use cases: a player's GUI might want to visualize the cards being played, an agent might want to take note of the other players' choices)
- Better handling of AI agent history and saved weights.
- Give options not to plot AI agent training.
- Rewrite modules for a number of players different than 6.
- Better comments and documentation.