__author__ = "Hayk Khachatryan"
__version__ = '0.1.0'
__license__ = "MIT"

import pyxel

#########################
#                       #
#                       #
#        classes        #
#                       #
#                       #
#########################


class Block:
    def __init__(self):
        self.y = 0

    def update(self):

        # if not at bottom of screen, fall
        if ((self.y + 8) < pyxel.height):
            self.y = (self.y + 1)


class App:
    def __init__(self):

        # init 160 by 120 space
        pyxel.init(160, 120)

        # load graphics
        pyxel.load("blocks.pyxel")

        # init 5 blocks
        self.blocks = [Block() for _ in range(5)]

        # offset block y pos by 16
        for i in range(5):
            self.blocks[i].y = -16 * i

        pyxel.run(self.update, self.draw)

    def update(self):

        # update all blocks
        for block in self.blocks:
            block.update()

        # if key 'q' is pressed, quit
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        
        # clear screen w/ black
        pyxel.cls(0)

        # load 5 blocks at centre of screen and drop them
        pyxel.blt(76, self.blocks[0].y, 0, 0, 0, 8, 8, 0)
        pyxel.blt(74, self.blocks[1].y, 0, 8, 0, 12, 8, 0)
        pyxel.blt(74, self.blocks[2].y, 0, 20, 0, 12, 8, 0)
        pyxel.blt(74, self.blocks[3].y, 0, 32, 0, 12, 8, 0)
        pyxel.blt(74, self.blocks[4].y, 0, 44, 0, 12, 4, 0)



#########################
#                       #
#      run baby         #
#                       #
#                       #
#########################

if __name__ == '__main__':
    
    App()

