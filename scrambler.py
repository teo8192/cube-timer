import random

MOVES = ["R", "L", "U", "D", "F", "B"]
DIR = ["", "'", "2"]

def scramble(slen=None):
    if slen == None:
        slen = random.randint(25, 28)

    scr = ""
    last_move = -1
    rmov = -1

    for _ in range(0, slen):
        while rmov == last_move:
            rmov = random.randint(0, len(MOVES) - 1)

        last_move = rmov

        mod = random.choice(DIR)
        scr += MOVES[rmov] + mod + " "
    
    return scr
