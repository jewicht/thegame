from __future__ import print_function, absolute_import

from abc import ABCMeta, abstractmethod
from six import with_metaclass

class AbsPlayer(object, with_metaclass(ABCMeta)):

    def __init__(self, __id, pile, stacks, wstacks):
        self._cards = []
        self._id = __id
        self._pile = pile
        self._stacks = stacks
        self._wstacks = wstacks

        
    @property
    def id(self):
        return self._id
        
    @property
    def name(self):
        return "Player #" + str(self.id)

    @property
    def cards(self):
        return self._cards

    @property
    def stacks(self):
        return self._stacks
    
    def pickcards(self, ncards):
        for i in range(ncards):
            if len(self._pile) == 0:
                return
            self._cards.append(self._pile.pop())
            sorted(self._cards)

    @abstractmethod
    def play(self, mandatory):
        pass

    @abstractmethod
    def warn(self):
        pass

    def playthiscard(self, cc, stack):
        self._stacks[stack].append( self._cards[cc] )
        del self._cards[cc]

    def findplayablecards(self):
        playablecards = []
        for cc, c in enumerate(self.cards):
            stack=None
            for cs, s in enumerate(self.stacks):
            
                if cs < 2:#UP
                    d = c - s[-1]
                else: #DOWN
                    d = s[-1] - c
                if d > 0:
                    playablecards.append( (cc, d, cs) )

        return sorted(playablecards, key=lambda card: card[1])

    def findtencards(self):
        result = []
        for cc, c in enumerate(self.cards):
            for cs, s in enumerate(self.stacks):
                if cs < 2:#UP
                    if s[-1] - c == 10:
                        result.append( (cc, cs) )
                else: #DOWN
                    if c - s[-1] == 10:
                        result.append( (cc, cs) )
        return result




class SimplePlayer(AbsPlayer):

    # max distance when we are warned not to play on this stack
    maxdwithwarning = 2
    # max distance when it's not mandatory to play
    maxdnotmandatory = 4
    # max distance to warn other players
    maxdwarn = 3
    
    def __init__(self, _id, pile, stacks, warn):
        super(SimplePlayer, self).__init__(_id, pile, stacks, warn)


    def play(self, mandatory):

        if len(self._cards) == 0:
            return 0

        #reset self warning stacks
        for cnt, w in enumerate(self._wstacks):
            if w == self.id:
                self._wstacks[cnt] = -1

        tencards = self.findtencards()
        if len(tencards) > 0:
            for tencard in tencards:
                #print("ten rule mother fucker")
                self.playthiscard(tencard[0], tencard[1])
                return 1


        #try to avoid stacks with warning
        playablecards = self.findplayablecards()
        for cc, distance, stack in playablecards:
            if self._wstacks[stack] >= 0:
                continue
            if distance > self.maxdwithwarning:
                continue
            self.playthiscard(cc, stack)
            return 1            
        

        #otherwise, play the best one
        playablecards = self.findplayablecards()

        # can't play
        if len(playablecards) == 0:
            return 0
        
        cc, distance, stack = playablecards[0]

        #can't play
        if stack is None:
            return 0

        # we stop playing
        if not mandatory and distance > self.maxdnotmandatory:
            return 0

        self.playthiscard(cc, stack)
        return 1


    def warn(self):
        if len(self._cards) == 0:
            return

        tencards = self.findtencards()
        for cc, cs in tencards:
            self._wstacks[cs] = self.id

        playablecards = self.findplayablecards()
        for cc, distance, stack in playablecards:
            if distance < self.maxdwarn:
                self._wstacks[stack] = self.id
