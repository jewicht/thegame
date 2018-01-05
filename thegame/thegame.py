from __future__ import print_function, absolute_import

from random import shuffle
import logging

from thegame.playerai import AbsPlayer


class TheGame:

    def __init__(self, playerclass, nplayers):

        if not issubclass(playerclass, AbsPlayer):
            raise Exception("Not a valid player")

        nplayers = int(nplayers)
        if nplayers <=0:
            raise Exception("Invalid number of players")
        
        self.ncards = 7
        self.nobligplay = 2
        

        self.pile = list(range(1, 100))
        shuffle(self.pile)

        self.stacks = [[0], [0], [100], [100]]
        self.wstacks = [-1, -1, -1, -1]

        self.players = []
        for i in range(nplayers):
            player = playerclass(i, self.pile, self.stacks, self.wstacks)
            player.pickcards(self.ncards)
            self.players.append(player)


    def display(self):
        logging.debug("%6s %6s %6s %6s %6s" % ("STACK", "UP", "UP", "DOWN", "DOWN"))
        string = "%6d" % len(self.pile)
        
        for s in self.stacks:
            string += "%6d" % s[-1]
        logging.debug(string)

        string = "%6s" % ""
        for w in self.wstacks:
            string += "%6d" % w
        logging.debug(string)

            
    def play(self):

        while True:

            thisround = 0
            
            for cnt, player in enumerate(self.players):
                logging.debug(player.name)
                nplay = 0 
                while player.play(nplay < self.nobligplay) != 0:

                    #other players can look at the board and warn
                    for cnt2, player2 in enumerate(self.players):
                        if cnt != cnt2:
                            player2.warn()
                
                    self.display()
                    nplay += 1
                    thisround += 1

                player.pickcards(nplay)

            cardsingame = len(self.pile)
            for player in self.players:
                cardsingame += len(player.cards)


            #victory
            if cardsingame == 0:
                logging.debug("\n\nYou won")
                return 0
        
            
            #nobody could play, defeat
            if thisround == 0:
                logging.debug("\n\nYou lost")
                logging.debug("%d card(s) left in the stack" % len(self.pile))
                for player in self.players:
                    logging.debug("%s has %d cards left" % (player.name, len(player.cards)))
                return cardsingame
     
