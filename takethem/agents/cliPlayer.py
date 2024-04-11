class cliPlayer:
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
        Asks for user input and "plays" (returns) a card.
        """
        cardIndexToPlay=42
        while cardIndexToPlay>len(self.hand):
            userInput=input(f"Which card do you want to play? (enter number 1-{len(self.hand)})\n")
            try:
                int(userInput)
            except:
                print(f"That is not a valid integer.")
                userInput=42

            if int(userInput)>len(self.hand):
                print(f"The chosen number is too large. Max is {len(self.hand)}")
            
            else:
                cardIndexToPlay=int(userInput)-1
                return self.hand.pop(cardIndexToPlay)
    
    def resolveSmallNumberCard(self,card):
        """The chosen card has a number smaller than
        the ones found at the end of all rows. Choose
        which rows to take penalties from.

        Args:
            card (Card): The previosly chosen card.
        """
        rowToTake=42
        while rowToTake>3:
            rowToTake=input("Chosen card has a small number.\n"+
                            "Which row do you want to take?\n")
            try:
                int(rowToTake)
            except:
                print(f"That is not a valid integer.")
                rowToTake=42
        
            rowToTake=int(rowToTake)-1
            if rowToTake>3:
                print(f"The chosen number is too large. Max is 4")
        
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
        
        self.game.tableRows[rowIndex]=[card]

        