from takethem.game import Game
from takethem.agents.MinimumLogicAgent import MinimumLogicAgent
from takethem.agents.RandomAgent import RandomAgent

import os
import time

def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix-based systems (Linux, macOS)
    else:
        os.system('clear')

game=Game(player1=MinimumLogicAgent,otherplayers=RandomAgent,automaticRestart=False)
playagain=True
i=0
while playagain:
    game.printPlayersHands()
    game.playerAction()
    clear_screen()
    print(f"Match number {i//10 +1}")
    game.printPlayedCards()
    game.resolveTurn()
    time.sleep(.1)
    clear_screen()
    playagain=game.checkGameCanContinue()
    i+=1