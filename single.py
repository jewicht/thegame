from __future__ import print_function

import sys

from thegame.thegame import TheGame
import logging        
    
def main():

    
    if len(sys.argv) != 2:
        print(sys.argv[0] + " number of players")
        return

    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    
    nplayers = int(sys.argv[1])

    thegame = TheGame(nplayers)
    thegame.play()

    
if __name__ == "__main__":
    main()
