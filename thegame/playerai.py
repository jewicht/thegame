from __future__ import print_function, absolute_import

from abc import ABCMeta, abstractmethod
from six import with_metaclass

from thegame.utils import findtencards, findplayablecards

class AbsPlayer(object, with_metaclass(ABCMeta)):

    def __init__(self, __id):
        self._cards = []
        self._id = __id

    @property
    def id(self):
        return self._id
        
    @property
    def name(self):
        return "Player" + str(self.id)

    @property
    def cards(self):
        return self._cards
    
    def pickcards(self, cards, ncards):
        for i in range(ncards):
            if len(cards) == 0:
                return
            self._cards.append(cards.pop())
            sorted(self._cards)

    @abstractmethod
    def play(self, mandatory):
        pass

    @abstractmethod
    def warn(self):
        pass

    def playthiscard(self, stacks, cc, stack):
        value = self._cards[cc]
        stacks[stack].append( value )
        del self._cards[cc]

    

class SimplePlayer(AbsPlayer):

    def __init__(self, id):
        super(SimplePlayer, self).__init__(id)


    def play(self, stacks, mandatory):

        if len(self._cards) == 0:
            return 0


        tencards = findtencards(stacks, self._cards)
        if len(tencards) > 0:
            for tencard in tencards:
                #print("ten rule mother fucker")
                self.playthiscard(stacks, tencard[0], tencard[1])
                return 1

        
        playablecards = findplayablecards(stacks, self._cards)
        ##        print(playablecards)

        
        #print("sorted")
        #print(playablecards)

        # can't play
        if len(playablecards) == 0:
            return 0
        
        cc, distance, stack = playablecards[0]

        #can't play
        if stack is None:
            return 0

        # we stop playing if distance > 3
        if not mandatory and distance > 3:
            return 0

        self.playthiscard(stacks, cc, stack)
        return 1


    def warn(self):
        pass
