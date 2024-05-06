import random

"""This class defines an agent for the game with a minimum of internal logic.
This type of player chooses a good card from their own hand, if they are sure
it will not lead to overflow on the of the rows on the table.
If the card has a small number, it chooses a the row that leads
to the smallest penalty. Once the game has finished,
the agent asks for a new match."""

class MinimumLogicAgent:
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
    
    def processGameStatus(self):
        """Retrieve relevant information from game status:
        - last card in a row
        - row length
        - discarded cards
        
        Returns a list with the following elements:
        [ - the list of card numbers that are not in the enemis' hands
          - the length of each row on the table
          - the last number of each row on the table]"""
        
        status=self.game.status()
        
        #These "non problematic" cards are all the cards that can't be played
        #by the other players.
        #Discarded + used at the beginning of the row + player's hand
        NonProblematicCards=[card.n for card in status[1]]
        for row in status[0]:
            NonProblematicCards+=[card.n for card in row]
        NonProblematicCards+=[card.n for card in self.hand]
        NonProblematicCards.sort()
        
        rowLengths=[len(row) for row in status[0]]
        rowEnds=[row[-1].n for row in status[0]]

        return [NonProblematicCards,rowLengths,rowEnds]
    
    def findGoodCards(self):
        """Given the list of cards not available to enemies, the length of
           the rows, and the number of the card of the end of the rows,
           finds the card numbers that can be played almost without risks.
           
           (i.e., the ones that for sure can be placed at the end row without reaching
           a row length of six.)
        """
        goodCards=[]
        processedStatus=self.processGameStatus()
        for rowIndex in range(4):
            lastCard=processedStatus[2][rowIndex]
            rowLength=processedStatus[1][rowIndex]
            hand=[card.n for card in self.hand]
            i=1
            while rowLength<6:
                if lastCard+i in processedStatus[0]:
                    if lastCard+i in hand:
                        goodCards.append(lastCard+i)
                else:
                    rowLength+=1
                i+=1
        return goodCards
    
    def playCard(self):
        """Mimics player's turn by playing a safe card (if possible, placed without risk)
        or a random card from the hand."""
        
        goodCards=self.findGoodCards()
        if len(self.hand)>0:
            for cardIndexToPlay,card in enumerate(self.hand):
                if card.n in goodCards:
                    return self.hand.pop(cardIndexToPlay)
            cardIndexToPlay=random.randrange(0,len(self.hand))
            return self.hand.pop(cardIndexToPlay)
    
    def resolveSmallNumberCard(self,card):
        """Handles a chosen card with a small number.

        The card triggers penalties from randomly chosen rows.

        Args:
            card (Card): The previously chosen card.
        """
        
        rowToTake=0
        penalty=100
        for rowIndex in range(4):
            row=self.game.tableRows[rowIndex]
            penalties=[card.penalty for card in row]
            sumOfPenalties=sum(penalties)
            if sumOfPenalties<penalty:
                rowToTake=rowIndex
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
    