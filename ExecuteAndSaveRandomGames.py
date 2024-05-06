from takethem.game import Game
from takethem.agents.RandomAgent import RandomAgent
from takethem.agents.RandomSavingAgent import RandomSavingAgent

import os
import time

def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix-based systems (Linux, macOS)
    else:
        os.system('clear')

game=Game(player1=RandomSavingAgent,otherplayers=RandomAgent,automaticRestart=False)
playagain=True
while playagain:
    game.printPlayersHands()
    game.playerAction()
    clear_screen()
    game.printPlayedCards()
    game.resolveTurn()
    clear_screen()
    playagain=game.checkGameCanContinue()
