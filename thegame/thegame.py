from __future__ import print_function, absolute_import

from random import shuffle
import logging

from thegame.playerai import SimplePlayer


class TheGame:

    def __init__(self, nplayers):
        self.nplayers = nplayers
        
        self.ncards = 7
        self.nobligplay = 2
        

        self.cards = list(range(1, 100))
        shuffle(self.cards)

        self.stacks = [[0], [0], [100], [100]]
        self.warn = [None, None, None, None]       

        self.players = []
        for i in range(self.nplayers):
            player = SimplePlayer(i)
            player.pickcards(self.cards, self.ncards)
            self.players.append(player)


    def display(self):
        logging.debug("%5s %5s %5s %5s %5s" % ("STACK", "UP", "UP", "DOWN", "DOWN"))
        string = "%5d" % len(self.cards)
        
        # for player in players:
        #     print("%5d" % len(player._cards), end=" ")
        
        for s in self.stacks:
            string += "%5d" % s[-1]

        logging.debug(string)
            

            
    def play(self):

        while True:

            thisround = 0
            
            for cnt, player in enumerate(self.players):
                logging.debug(player.name)
                nplay = 0 
                while player.play(self.stacks, nplay < self.nobligplay) != 0:

                    #other players can look at the board and warn
                    for cnt2, player2 in enumerate(self.players):
                        if cnt != cnt2:
                            player2.warn()
                
                    self.display()
                    nplay += 1
                    thisround += 1

                player.pickcards(self.cards, nplay)

            cardsingame = len(self.cards)
            for player in self.players:
                cardsingame += len(player.cards)


            #victory
            if cardsingame == 0:
                logging.debug("\n\nYou won")
                return 0
        
            
            #nobody could play, defeat
            if thisround == 0:
                logging.debug("\n\nYou lost")
                logging.debug("%d card(s) left in the stack" % len(self.cards))
                for player in self.players:
                    logging.debug("%s has %d cards left" % (player.name, len(player.cards)))
                return cardsingame
     
