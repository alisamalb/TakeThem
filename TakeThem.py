from takethem.game import Game
from takethem.agents.NNagent import AIagent
import os

def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix-based systems (Linux, macOS)
    else:
        os.system('clear')

game=Game(otherplayers=AIagent)
while True:
    game.printPlayersHands()
    game.playerAction()
    clear_screen()
    game.printPlayedCards()
    input("...")
    game.resolveTurn()
    clear_screen()
    game.checkGameCanContinue()