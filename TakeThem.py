from takethem.game import Game
import os

def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix-based systems (Linux, macOS)
    else:
        os.system('clear')

game=Game()
while True:
    game.printPlayersHands()
    game.playerAction()
    clear_screen()
    game.printPlayedCards()
    input("...")
    #game.resolveTurn()
    clear_screen()