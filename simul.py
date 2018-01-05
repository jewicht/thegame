from __future__ import print_function

import sys
import logging

import numpy as np
import matplotlib.pyplot as plt

from thegame.thegame import TheGame
    
def main():

    if len(sys.argv) != 3:
        print(sys.argv[0] + " number of players number of games")
        return

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    nplayers = int(sys.argv[1])
    ngames = int(sys.argv[2])

    vec = np.empty(ngames)
    for cnt in range(ngames):
        thegame = TheGame(nplayers)
        r = thegame.play()
        vec[cnt] = r

    vicperc = 100.* np.sum(vec == 0) / ngames
    print("%.1f%% of games won" %  vicperc)
    
    plt.hist(vec, bins=int(np.max(vec))+1)
    plt.show()
        
if __name__ == "__main__":
    main()
