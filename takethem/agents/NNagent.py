import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import itertools


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
        self.training=False
        self.distances=[]
        try:
          self.model = tf.keras.models.load_model("takethem/agents/NNagent.keras")
        except:
            input("(press Enter to train new model)")
            self.model = self.createModel()
        try:
            self.history=list(np.load("takethem/agents/NNagent.history.npy"))

        except:
            input("(press Enter to save new history for AI agent)")
            self.history=[]
        
        self.figure=None
        self.last_played_card=None
        self.n_turns=0
        
    def createModel(self):
        model = tf.keras.Sequential([
                tf.keras.layers.Input(shape=(187,)),
                tf.keras.layers.BatchNormalization(),
                tf.keras.layers.Dense(units=32, activation='leaky_relu'),   # Dense hidden layer
                tf.keras.layers.Dense(units=16, activation='leaky_relu'),   # Dense hidden layer
                tf.keras.layers.Dense(units=16, activation='leaky_relu'),   # Dense hidden layer
                tf.keras.layers.Dense(units=1, activation='leaky_relu')   # Output layer for regression with linear activation
                ])
        model.compile(optimizer='adam', loss='mse', metrics=['mae'], weighted_metrics=['mae'])
        return model
    
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
            
            
    def descriptGame(self,status):
        encoded=[]   
        #status[0] contains four lists with the card objects in each row table
        #status[2] contains all the discarded cards
        
        #add row lengths, number of discarded card, number of cards in hand
        for i in range(4):
            encoded+=[len(status[0][i])]
        encoded+=[len(status[2])]
        encoded+=[len(self.hand)]
        
        
        for row in status[0]:
            numbers=[card.n for card in row]
            while len(numbers)<5:
                numbers+=[0]
            encoded+=[x for x in numbers]
        
        hand_numbers=[card.n for card in self.hand]
        while len(hand_numbers)<10:
             hand_numbers+=[0]
        encoded+=[x for x in hand_numbers]
        

        discarded=[card.n for card in status[2]]  
        card_in_discarded1=[int(n+1 in discarded) for n in encoded[6:36]]
        card_in_discarded2=[int(n+2 in discarded) for n in encoded[6:36]]
        card_in_discarded3=[int(n+3 in discarded) for n in encoded[6:36]]
        card_in_discarded4=[int(n+4 in discarded) for n in encoded[6:36]]

        encoded+=card_in_discarded1          
        encoded+=card_in_discarded2        
        encoded+=card_in_discarded3          
        encoded+=card_in_discarded4    
        #encoded+=[i+1 in discarded for i in range(64)]
        
        for row in status[0]:
             penalties=[card.penalty for card in row]
             while len(penalties)<5:
                 penalties+=[0]
             encoded+=[n for n in penalties]
        
        
        
        hand_penalties=[card.penalty for card in self.hand]
        while len(hand_penalties)<10:
             hand_penalties+=[0]
        encoded+=[n for n in hand_penalties]
        return encoded
    

    
    def predictPenalty(self):
        
        if len(self.history)>0:
            if self.n_turns%10!=0:
                for i in range(24):
                    self.history[-1-i]+=[self.last_played_card.n]
                    #self.history[-1-i]+=[self.last_played_card.penalty/7]
                    self.history[-1*(i+1)]+=[(self.penalties-self.previous_penalties)]
            self.previous_penalties=self.penalties+0
            self.distances.append([(self.penalties-p.penalties)/(p.penalties+0.01)*100 for p in self.game.players[1:]])
        status=self.game.status()
        permutations=itertools.permutations(status[0])
        for p in list(permutations):
            encoded=self.descriptGame([p]+status[1:])
            self.history.append(encoded)
            
        encodedHandCards=[]
        for card in self.hand:
            encodedHandCards.append(encoded.copy())
            encodedHandCards[-1]+=[card.n]
            #encodedHandCards[-1]+=[card.penalty/7]
            
        self.n_turns+=1
        
        predictions=self.model.predict(np.array(encodedHandCards),verbose=False)
        return list(predictions)
    

    def playCard(self):        
        "Plays the card that minimizes the penalties in the game."
        cardIndexToPlay=0
        penalties=self.predictPenalty()
        #print(penalties)
        #input("...")
        if len(self.hand)>0:
            cardIndexToPlay=penalties.index(min(penalties))
            self.last_played_card= self.hand.pop(cardIndexToPlay)
            return self.last_played_card
    
    def resolveSmallNumberCard(self,card):
        """Handles a chosen card with a small number.

        The card triggers penalties from a chosen rows.
        The row is choses to minimize the penaltie

        Args:
            card (Card): The previously chosen card.
        """
        
        rows=self.game.tableRows
        penalties=np.array([sum([card.penalty for card in row]) for row in rows])
        minimum=np.min(penalties)
        choices=np.array([0,1,2,3])[penalties==minimum]
        rowToTake=np.random.choice(choices)
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
    
    def plotFit(self):
        if not self.figure:
                self.figure=plt.figure()
        dataset=np.array(self.history,dtype=np.float16)
        y_pred=self.model.predict(dataset[-24000:,:-1])
        plt.subplot(1,2,1)
        plt.cla()
        plt.scatter(dataset[-24000:,-1],y_pred,s=.1,c=np.array([(x%240)//24 for x in range(len(y_pred))]))
        plt.scatter(dataset[-240:,-1],y_pred[-240:],s=.5,c='black')
        plt.plot([0,15],[0,15],c='black')
        plt.xlabel("Real penalty")
        plt.ylabel("Predicted penalty")
        plt.subplot(1,2,2)
        plt.cla()
        for i in range(5):
            plt.plot([x/10 for x in range(len(self.distances))],np.array(self.distances)[:,i],alpha=0.3)
        plt.plot([x/10 for x in range(len(self.distances))],np.array(self.distances).mean(axis=1),c="black")
        plt.ylim(-100,150)
        plt.plot([0,len(self.distances)/10],[0,0],c="black")
        plt.xlabel("Match number")
        plt.ylabel("Relative distance to enemy (%)")
        plt.legend([2,3,4,5,6])
        plt.tight_layout()
        plt.draw()
        plt.pause(0.01)
        
    def playAgain(self):
        """Determines whether the player wants to play again.

        Returns:
            bool: True to play again at the end of the game.
        """
        for i in range(24):
            self.history[-1-i]+=[self.last_played_card.n]
            #self.history[-1-i]+=[self.last_played_card.penalty/7]
        for i in range(24):
            self.history[-1*(i+1)]+=[(self.penalties-self.previous_penalties)]
        self.previous_penalties=self.penalties+0
        dataset=np.array(self.history,dtype=np.float32)
        self.distances.append([(self.penalties-p.penalties)/(p.penalties+0.01)*100 for p in self.game.players[1:]])
        if self.n_turns%10==0 and self.training and len(self.history)>100:
            
            early_stopping = tf.keras.callbacks.EarlyStopping(
                             monitor='val_loss',  # Monitor the validation loss
                             patience=15,          # Number of epochs with no improvement after which training will be stopped
                             restore_best_weights=True  # Restore the best model weights
                            )
            self.model.fit(dataset[:,:-1], dataset[:,-1], epochs=10, batch_size=24000, sample_weight=np.array([(x%240)//24+1 for x in range(len(dataset))]))

            np.save("takethem/agents/NNagent.history.npy",dataset)
            self.model.save("takethem/agents/NNagent.keras")
        self.plotFit()
        return True
    