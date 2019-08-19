import math
from random import randrange
import pyxel

__author__ = "Hayk Khachatryan"
__version__ = '0.1.0'
__license__ = "MIT"


###################
#    constants    #
###################

windowHeight = 120
windowWidth = 80


#################
#    classes    #
#################

class Block:
    """The blocks we know and love."""

    def __init__(self, c):
        """
            Initialises a block at (random x location, top of window)

            Attributes:
                x (int):        randomly assigned x position of block in window
                                (in multiples of 4)
                y (int):        y position of block in window
                vy (int):       frame interval between 4 pixel drops
                r (list):       list of rectangles representing block [(x, y), (w, h), col] values
                    x (int):    x coord of starting point of rectangle
                    w (int):    x coord of ending point of rectangle
                    y (int):    y coord of starting point of rectangle
                    h (int):    y coord of ending point of rectangle
                    col (int):  color of block
                width (int):    width of block
                height (int):   height of block
                falling (Bool): whether or not block is still falling
        """
        self.coords = c

        self.width = (max(list(zip(*self.coords))[0]) + 1) * 4
        self.height = (max(list(zip(*self.coords))[1]) + 1) * 4

        self.x = randrange((pyxel.width - self.width)/4)
        self.y = 0
        self.vy = 32
        self.falling = True

        self.color = randrange(2, 15)

        # Add block to posMap
        mapAdd(self, posMap)

    def update(self):
        """Updates block

            if not at bottom of screen OR clashing with other block:
                falls
            else
                not falling
        """

        if (((self.y * 4) + self.height) < pyxel.height) and not mapCheck(self, posMap, 0, 1):

            # self.vy: frame gap between drops
            if (pyxel.frame_count % self.vy) == 0:
                mapDel(self, posMap)
                self.y = (self.y + 1)
                mapAdd(self, posMap)

            if pyxel.btnp(pyxel.KEY_LEFT, 10, 1):
                mapDel(self, posMap)
                self.x = max(0, self.x - 1)
                mapAdd(self, posMap)

            if pyxel.btnp(pyxel.KEY_RIGHT, 10, 1):
                mapDel(self, posMap)
                self.x = min(self.x + 1, (pyxel.width - self.width) // 4)
                mapAdd(self, posMap)

            if pyxel.btnp(pyxel.KEY_DOWN):
                self.vy = 1

            if pyxel.btnp(pyxel.KEY_UP):
                mapDel(self, posMap)
                rotate(self)
                mapAdd(self, posMap)

        else:
            self.falling = False

    def draw(self):
        """Draws blocks rectangle by rectangle (from self.rects)"""
        for (x, y) in self.coords:
            pyxel.rect(
                (x + self.x) * 4,
                (y + self.y) * 4,
                (x + self.x) * 4 + 3,
                (y + self.y) * 4 + 3,
                self.color)


class App:
    """Main app"""

    def __init__(self):
        """
            - inits the window
            - loads the graphics
            - adds a block
            - runs update & draw
        """

        pyxel.init(windowWidth, windowHeight)

        # init a random block
        self.blocks = [Block(blockData[randrange(7)])]

        pyxel.run(self.update, self.draw)

    def update(self):

        # generates a new block if last block has stopped falling
        if not self.blocks[-1].falling:
            self.blocks.append(Block(blockData[randrange(7)]))
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

        # draw all blocks
        for block in self.blocks:
            block.draw()


################
#    blocks    #
################

blockData = [  # (x, y)
    [  # I
        (0, 0), (1, 0), (2, 0), (3, 0)
    ],
    [  # J
        (0, 0), (1, 0), (2, 0),
                        (2, 1)
    ],
    [  # L
        (0, 0), (1, 0), (2, 0),
        (0, 1)
    ],
    [  # O
        (0, 0), (1, 0),
        (0, 1), (1, 1)
    ],
    [  # S
        (0, 0), (1, 0),
                (1, 1), (2, 1)
    ],
    [  # T
        (0, 0), (1, 0), (2, 0),
                (1, 1)
    ],
    [  # Z
                (1, 0), (2, 0),
        (0, 1), (1, 1)
    ]
]

#############
#    map    #
#############

# generates 2D array consisting of 0s
posMap = [[0 for _ in range(windowWidth // 4)] for _ in range(windowHeight // 4)]


def mapCheck(block, posMap, changeX, changeY):
    """Checks if moving block to new position (+changeX, +changeY) will clash with existing block"""

    mapDel(block, posMap)
    for (x, y) in block.coords:
        if posMap[y + block.y + changeY][x + block.x + changeX]:
            mapAdd(block, posMap)
            return True
    mapAdd(block, posMap)
    return False


def mapAdd(block, posMap):
    """Adds block to posMap"""
    for (x, y) in block.coords:
        posMap[y + block.y][x + block.x] = 1


def mapDel(block, posMap):
    """Removes block from posMap"""
    for (x, y) in block.coords:
        posMap[y + block.y][x + block.x] = 0


def rotate(block):
    # https://stackoverflow.com/questions/9389453/rotation-matrix-with-center
    centerX = block.width // 8
    centerY = block.height // 8
    block.coords = [
        (
            centerX - y + centerY,
            centerY + x - centerX
            )
        for (x, y) in block.coords]
    h = block.height
    block.height = block.width
    block.width = h


##################
#    run baby    #
##################

if __name__ == '__main__':

    App()
