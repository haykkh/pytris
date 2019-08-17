import math
from random import randrange
import pyxel

__author__ = "Hayk Khachatryan"
__version__ = '0.1.0'
__license__ = "MIT"

#################
#    classes    #
#################


class Block:
    """The blocks we know and love."""

    def __init__(self, u, w, h):
        """
            Initialises a block at (random x location, top of window)

            Attributes:
                x (int):        randomly assigned x position of block in window
                                (in multiples of 4)
                y (int):        y position of block in window
                vy (int):       frame gap between 4 pixel drops
                u (int):        x location of start of block in image bank
                width (int):    width of block
                height (int):   height of block
                falling (Bool): whether or not block is still falling
        """

        self.x = randrange((pyxel.width - w)/4) * 4
        self.y = 0
        self.vy = 32
        self.u = u
        self.width = w
        self.height = h
        self.falling = True

    def update(self):
        """Updates block

            if not at bottom of screen:
                falls
            else
                not falling
        """
        
        if ((self.y + self.height) < pyxel.height):

            # self.vy: frame gap between drops
            if (pyxel.frame_count % self.vy) == 0:
                self.y = (self.y + 4)

            if pyxel.btnp(pyxel.KEY_LEFT, 10, 1):
                self.x = max(0, self.x - 4)
            
            if pyxel.btnp(pyxel.KEY_RIGHT, 10, 1):
                self.x = min(self.x + 4, pyxel.width - self.width)

            if pyxel.btnp(pyxel.KEY_DOWN):
                self.vy = 1

        else:
            self.falling = False


class App:
    """Main app"""

    blockData = [     # List of [u, w, h] (see Block.__doc__) for the 7 blocks
        [0,  16, 4],  # I
        [16, 12, 8],  # J
        [28, 12, 8],  # L
        [40,  8, 8],  # O
        [48, 12, 8],  # S
        [60, 12, 8],  # T
        [72, 12, 8]   # Z
    ]
   
    def __init__(self):
        """
            - inits the window
            - loads the graphics
            - adds a block
            - runs update & draw
        """

        # init 160 by 120 space
        pyxel.init(120, 80)

        # load graphics
        pyxel.load("blocks.pyxel")

        # init a random block
        self.blocks = [Block(*App.blockData[randrange(7)])]

        pyxel.run(self.update, self.draw)

    def update(self):

        # generates a new block if last block has stopped falling
        if not self.blocks[-1].falling:
            self.blocks.append(Block(*App.blockData[randrange(7)]))
            self.blocks[-1].falling = True

        # update all blocks
        for block in self.blocks:
            block.update()

        # if key 'q' is pressed, quit
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        
        # clear screen w/ black
        pyxel.cls(0)
        for (x, y), (w, h), col in blockDatann[6]:
            pyxel.rect(y, x, h, w, col)

        for block in self.blocks:
            pyxel.blt(block.x, block.y, 0, block.u, 0, block.width, block.height, 0)


#            rect(x, y, w, h, col)
################
#    blocks    #
################

blockDatann = [
    [  # I
        [(0, 0), (15, 3), 12]
    ],
    [  # J
        [(0, 0), (11, 3), 8],
        [(8, 4),  (11, 7), 8]
    ],
    [  # L
        [(0, 0), (11, 3), 11],
        [(0, 4),  (3, 7), 11]
    ],
    [  # O
        [(0, 0), (7, 7), 9]
    ],
    [  # S
        [(0, 0), (7, 3), 3],
        [(4, 4), (11, 7), 3]
    ],
    [  # T
        [(0, 0), (11, 3), 10],
        [(4, 4),  (7, 7), 10]
    ],
    [  # z
        [(4, 0), (11, 3), 14],
        [(0, 4), (7, 7), 14]
    ]
]

# I
# J
# L
# O
# S
# T
# Z
##################
#    run baby    #
##################

if __name__ == '__main__':
    
    App()

