import random

class RandomAgent:
    def __init__(self,game):
        self.game=game
        self.hand=[]
        self.penalties=0
        
    def draw(self,n=1):
        """Draw n cards from the deck of the game.

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
        """Mimics player's turn.
        "Plays" (returns) a random card from the hand.
        """
        if len(self.hand)>0:
            cardIndexToPlay=random.randrange(0,len(self.hand))
            return self.hand.pop(cardIndexToPlay)
    
    def resolveSmallNumberCard(self,card):
        """The chosen card has a number smaller than
        the ones found at the end of all rows. Choose
        randomly which rows to take penalties from.

        Args:
            card (Card): The previosly chosen card.
        """
        
        rowToTake=random.randrange(0,3)
        self.takePenalty(rowToTake,card)

    def takePenalty(self,rowIndex,card):   
        """Sum the penalties for all the cards in the row
        with index rowIndex and add the penalty points
        to the player attribute.

        Args:
            rowIndex (int): The index of the row to replace with new card.
            card (Card): The card the led to taking the penalties.
        """
        row=self.game.tableRows[rowIndex]
        penalties=[card.penalty for card in row]
        sumOfPenalties=sum(penalties)
        self.penalties+=sumOfPenalties
        self.game.removedCards+=self.game.tableRows[rowIndex]
        self.game.tableRows[rowIndex]=[card]
    
    def PlayAgain(self):
        """Returns True to play again at the end of the game."""
        return True