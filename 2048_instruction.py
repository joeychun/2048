"""
2048 Game
    I. At first, generate two blocks at random
        -those two blocks are (2,2) (2,4) in random


       (Loop)  
    II. Response to direction key
        see if it can be added
            A. if True
                add it and move to that direction
            B. if False
                check if lane is full
                    (i) if True
                        pass, print("do diffrent move.")
                    (ii) if False
                        move to that direction
        ˚if it is moved, generate random block and make &history&
    III. Every time make a new block- 2 or 4
    IV. Game over
        ˚if you can not add and cant move YOU LOSE
"""
