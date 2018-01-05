from __future__ import print_function

import sys
import logging

import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool

from functools import partial

from thegame.thegame import TheGame
from thegame.playerai import SimplePlayer

def g(playerclass, nplayers, x):
    tg = TheGame(playerclass, nplayers)
    return tg.play()

def main():

    if len(sys.argv) != 3:
        print(sys.argv[0] + " number of players number of games")
        return

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    nplayers = int(sys.argv[1])
    ngames = int(sys.argv[2])

    f = partial(g, SimplePlayer, nplayers)
    p = Pool()
    vec = np.array(p.map(f, range(ngames)))
    
    vicperc = 100.* np.sum(vec == 0) / ngames
    print("%.1f%% of games won" %  vicperc)
    
    plt.hist(vec, bins=int(np.max(vec))+1)
    plt.show()
        
if __name__ == "__main__":
    main()
