import random

"""This class defines a random agent for the game. This type of player
chooses a random card from their own hand. If the card has a small number,
it chooses a random row to take penalties from. Once the game has finished,
the agent asks for a new match."""

class RandomAgent:
    def __init__(self,game):
        """Initializes a random agent for the game.

        Args:
            game: An instance of the game environment.
        """
        self.game=game
        self.hand=[]
        self.penalties=0
        
    def draw(self,n=1):
        """Draws cards from the deck of the game.

        Args:
            n (int, optional): Number of cards to draw. Defaults to 1.
        """
        if n==1:
            self.hand.append(self.game.deck.draw_card())
        else:
            self.hand+=self.game.deck.draw_cards(n)
        
        self.hand.sort(key=lambda x: x.n)
        for card in self.hand:
            card.setOwner(self)
    
    def playCard(self):
        """Mimics player's turn by playing a random card from the hand."""
        if len(self.hand)>0:
            cardIndexToPlay=random.randrange(0,len(self.hand))
            return self.hand.pop(cardIndexToPlay)
    
    def resolveSmallNumberCard(self,card):
        """Handles a chosen card with a small number.

        The card triggers penalties from randomly chosen rows.

        Args:
            card (Card): The previously chosen card.
        """
        rowToTake=random.randrange(0,4)
        self.takePenalty(rowToTake,card)

    def takePenalty(self,rowIndex,card):   
        """Takes penalties from a row and updates player's penalty count.

        Args:
            rowIndex (int): Index of the row to replace with the new card.
            card (Card): The card that led to taking the penalties.
        """
        row=self.game.tableRows[rowIndex]
        penalties=[card.penalty for card in row]
        sumOfPenalties=sum(penalties)
        self.penalties+=sumOfPenalties
        self.game.removedCards+=self.game.tableRows[rowIndex]
        self.game.tableRows[rowIndex]=[card]
    
    def playAgain(self):
        """Determines whether the player wants to play again.

        Returns:
            bool: True to play again at the end of the game.
        """
        return True
    