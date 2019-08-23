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
        self.coords = c[:4]
        self.center = c[4]

        widthAndHeight(self)

        self.x = randrange((pyxel.width - self.width)/4)
        self.y = 0
        self.vy = 32
        self.falling = True

        self.color = randrange(2, 15)

        # Add block to posMap
        mapAdd(self, posMap)

        self.frame = pyxel.frame_count

    def drop(self):
        # self.vy: frame gap between drops
        if (pyxel.frame_count % self.vy) == 0:
            mapDel(self, posMap)
            self.y = (self.y + 1)
            mapAdd(self, posMap)

    def keyLeft(self):
        if pyxel.btnp(pyxel.KEY_LEFT, 10, 1) and not mapCheck(self, posMap, -1, 0):
            mapDel(self, posMap)
            self.x = max(-self.left, self.x - 1)
            mapAdd(self, posMap)

    def keyRight(self):
        if pyxel.btnp(pyxel.KEY_RIGHT, 10, 1) and not mapCheck(self, posMap, 1, 0):
            mapDel(self, posMap)
            self.x = min(self.x + 1,  -self.left + (pyxel.width - self.width) // 4)
            mapAdd(self, posMap)

    def keyUp(self):
        if pyxel.btnp(pyxel.KEY_UP):
            if not self.center:
                None
            else:
                mapDel(self, posMap)
                rotate(self)
                mapAdd(self, posMap)

    def update(self):
        """Updates block

            if not at bottom of screen OR clashing with other block:
                falls
            else
                not falling
        """

        if (((self.y * 4) + self.height) < pyxel.height) and not mapCheck(self, posMap, 0, 1):

            self.drop()
            self.keyLeft()
            self.keyRight()
            self.keyUp()

            if pyxel.btnp(pyxel.KEY_DOWN):
                self.vy = 1

            self.frame = pyxel.frame_count

        else:

            if pyxel.frame_count < self.frame + 16:
                self.keyLeft()
                self.keyRight()
                self.keyUp()
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
        (0, 1), (1, 1), (2, 1), (3, 1),

        (2, 2)
    ],
    [  # J
        (0, 0),
        (0, 1), (1, 1), (2, 1),

        (1, 1)
    ],
    [  # L
                        (2, 0),
        (0, 1), (1, 1), (2, 1),

        (1, 1)
    ],
    [  # O
        (0, 0), (1, 0),
        (0, 1), (1, 1),

        False
    ],
    [  # S
                (1, 0), (2, 0),
        (0, 1), (1, 1),

        (1, 1)
    ],
    [  # T
                (1, 0),
        (0, 1), (1, 1), (2, 1),

        (1, 1)
    ],
    [  # Z
        (0, 0), (1, 0),
                (1, 1), (2, 1),

        (1, 1)
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
        if x + block.x + changeX < len(posMap[0]):
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
    # SRS
    block.coords = [
        (
            int(block.center[0] - y + block.center[1]),
            int(block.center[1] + x - block.center[0])
            )
        for (x, y) in block.coords]
    widthAndHeight(block)


def widthAndHeight(block):
    block.left = min(list(zip(*block.coords))[0])
    block.right = max(list(zip(*block.coords))[0])
    block.top = min(list(zip(*block.coords))[1])
    block.bottom = max(list(zip(*block.coords))[1])
    block.width = (
        block.right +
        1
        ) * 4
    block.height = (
        block.bottom +
        1
        ) * 4

##################
#    run baby    #
##################

if __name__ == '__main__':

    App()
