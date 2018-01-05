def findplayablecards(stacks, cards):
    playablecards = []
    for cc, c in enumerate(cards):
        stack=None
        for cs, s in enumerate(stacks):
            
            if cs < 2:#UP
                d = c - s[-1]
            else: #DOWN
                d = s[-1] - c
            if d > 0:
                playablecards.append( (cc, d, cs) )

    return sorted(playablecards, key=lambda card: card[1])


def findtencards(stacks, cards):
    result = []
    for cc, c in enumerate(cards):
        for cs, s in enumerate(stacks):
            if cs < 2:#UP
                if s[-1] - c == 10:
                    result.append( (cc, cs) )
            else: #DOWN
                if c - s[-1] == 10:
                    result.append( (cc, cs) )
    return result
