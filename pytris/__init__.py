import math
import random
import pyxel

__author__ = "Hayk Khachatryan"
__version__ = '0.1.0'
__license__ = "MIT"

#########################
#                       #
#                       #
#        classes        #
#                       #
#                       #
#########################


class Block:
    """The blocks we know and love.

    """
    def __init__(self, u, w, h):
        """
            Initialises a block at (random x location, top of window)

            Attributes:
                x (int):        randomly assigned x position of block in window
                                (in multiples of 4)
                y (int):        y position of block in window
                u (int):        x location of start of block in image bank
                width (int):    width of block
                height (int):   height of block
                falling (Bool): whether or not block is still falling
        """
        self.x = random.randrange((pyxel.width - w)/4) * 4
        self.y = 0
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
        
        if ((self.y + 8) < pyxel.height):
            self.y = (self.y + 1)
        else:
            self.falling = False


class App:
    """Main app
    
    """
    blockData = [     # List of [u, w, h] (see Block.__doc__) for the 7 blocks
        [0,  12, 4],  # I
        [12, 12, 8],  # J
        [24, 12, 8],  # L
        [36,  8, 8],  # O
        [44, 12, 8],  # S
        [56, 12, 8],  # T
        [68, 12, 8]   # Z
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
        self.blocks = [Block(*App.blockData[random.randrange(7)])]

        pyxel.run(self.update, self.draw)

    def update(self):

        # generates a new block if last block has stopped falling
        if not self.blocks[-1].falling:
            self.blocks.append(Block(*App.blockData[random.randrange(7)]))
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

        for block in self.blocks:
            pyxel.blt(block.x, block.y, 0, block.u, 0, block.width, block.height, 0)




#########################
#                       #
#      run baby         #
#                       #
#                       #
#########################

if __name__ == '__main__':
    
    App()

