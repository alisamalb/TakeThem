import tensorflow as tf
import numpy as np

"""This agent employs a neural network with 25,000 parameters to inform its decision-making process.
Given the current game state and a chosen card, the neural network predicts the penalties likely to be incurred. 
The agent then selects the card that minimizes penalties.
Its approach is straightforward, focusing on avoiding row overflow and prioritizing cards with minimal penalty outcomes.
After each game, the agent eagerly anticipates the next match."."""

class AIagent:
    def __init__(self,game):
        """Initializes a random agent for the game.

        Args:
            game: An instance of the game environment.
        """
        self.game=game
        self.hand=[]
        self.penalties=0
        self.previous_penalties=0
        try:
            self.model = tf.keras.models.load_model("takethem/agents/25Kparms_nn.keras")
        except:
            input("...")
            self.model = tf.keras.Sequential([
                    tf.keras.layers.Input(shape=(68,)),  # Input layer with 95 features
                    tf.keras.layers.Dense(units=128, activation='leaky_relu'),   # Dense hidden layer with ReLU activation

                    tf.keras.layers.Dense(units=128, activation='leaky_relu'),   # Dense hidden layer with ReLU activation
                    tf.keras.layers.Dense(units=128, activation='leaky_relu'),   # Dense hidden layer with ReLU activation
                    tf.keras.layers.Dense(units=64, activation='leaky_relu'),   # Dense hidden layer with ReLU activation
                    tf.keras.layers.Dense(units=32, activation='leaky_relu'),   # Dense hidden layer with ReLU activation
                    tf.keras.layers.Dense(units=16, activation='leaky_relu'),   # Dense hidden layer with ReLU activation
                    tf.keras.layers.Dense(units=8, activation='leaky_relu'),   # Dense hidden layer with ReLU activation
                    tf.keras.layers.Dense(units=1, activation='linear')   # Output layer for regression with linear activation
                ])
            self.model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

# Compile the model
        try:
            self.history=list(np.load("takethem/agents/25Kparms_nn.history.npy"))
        except:
            input("...")
            self.history=[]
        self.last_played_card=None
        self.n_turns=0
        
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
            
    def writeHistory(self,encoded):
        if len(self.history)>0:
            if self.n_turns%10!=0:
                self.history[-1]+=[self.last_played_card.n/64]
                self.history[-1]+=[self.last_played_card.penalty/7]
        self.history.append(encoded)
        self.n_turns+=1

            
    def descriptGame(self,status):
        encoded=[]   
        
        #add row lengths, number of discarded card, number of cards in hand
        for i in range(4):
            encoded+=[len(status[0][i])/5]
        encoded+=[len(status[1])/64]
        encoded+=[len(self.hand)/10]
        
        for row in status[0]:
            numbers=[card.n for card in row]
            while len(numbers)<5:
                numbers+=[0]
            encoded+=[x/64 for x in numbers]
        
        for row in status[0]:
            penalties=[card.penalty for card in row]
            while len(penalties)<5:
                penalties+=[0]
            encoded+=[n/7 for n in penalties]
        
        hand_numbers=[card.n for card in self.hand]
        while len(hand_numbers)<10:
            hand_numbers+=[0]
        encoded+=[x/64 for x in hand_numbers]
        
        hand_penalties=[card.penalty for card in self.hand]
        while len(hand_penalties)<10:
            hand_penalties+=[0]
        encoded+=hand_penalties
        return encoded
    
    
    # def encode(self,status):
    #     encoded=[]
    #     for row in status[0]:
    #         encoded+=[card.n for card in row]
    #         for i in range(5-len(row)):
    #             encoded+=[0]
        
    #     zeros=[0 for i in range(64)]
    #     for card in status[1]:
    #         zeros[card.n-1]=64
        
    # #    encoded+=zeros
        
    #     encoded+=[card.n for card in self.hand]
    #     encoded+=[0 for i in range(10-len(self.hand))]
    #     return encoded
    
    def predictPenalty(self):
        status=self.game.status()
        #encoded=self.encode(status)
        encoded=self.descriptGame(status)
        self.writeHistory(encoded)
        
        encodedHandCards=[]
        for card in self.hand:
            encodedHandCards.append(encoded.copy())
            encodedHandCards[-1]+=[card.n/64]
            encodedHandCards[-1]+=[card.penalty/7]
            #encodedHandCards[-1]=[x/64 for x in encodedHandCards[-1]]        
        
        prediction=self.model.predict(encodedHandCards,verbose=False)[0]
        return list(prediction)
             


    def playCard(self):
        """Mimics player's turn by playing a safe card (if possible, placed without risk)
        or a random card from the hand."""
        
        cardIndexToPlay=0

        penalties=self.predictPenalty()

        
        if len(self.hand)>0:
            cardIndexToPlay=penalties.index(min(penalties))
            self.last_played_card= self.hand.pop(cardIndexToPlay)
            return self.last_played_card
    
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
        self.history[-1]+=[self.last_played_card.n/64]
        self.history[-1]+=[self.last_played_card.penalty/7]
        for i in range(10):
            self.history[-1*(i+1)]+=[(self.penalties-self.previous_penalties)/40]
        self.previous_penalties=self.penalties+0
        dataset=tf.convert_to_tensor(self.history,dtype=tf.float32)
        if len(self.history)>200:
            self.model.fit(dataset[:,:-1], dataset[:,-1], epochs=20, batch_size=len(self.history))
        if self.n_turns%30==10:
            np.save("takethem/agents/25Kparms_nn.history.npy",np.array(self.history))
            self.model.save("takethem/agents/25Kparms_nn.keras")
        return True
    