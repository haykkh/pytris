import math
from random import randrange, sample
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
            in a random color

            Attributes:
                coords (list):  list of coordinates of block in form
                                [(x, y), (x, y) ... (x, y), (cX, cY)]
                    (x, y) (int):    tuple representing x & y coord
                    (cX, cY) (int):  tuple representing center for rotation
                x (int):        randomly assigned x position of block in window
                                (in multiples of 4)
                y (int):        y position of block in window
                vy (int):       frame interval between 4 pixel drops
                color (int):    color of block (default pyxel color values)
                width (int):    width of block
                height (int):   height of block
                frame (int):    frame of last update
                falling (Bool): whether or not block is still falling
        """
        self.coords = c[:4]
        self.center = c[4]

        # init width and height of block
        widthAndHeight(self)

        self.x = randrange((pyxel.width - self.width)/4)
        self.y = 0
        self.vy = 32
        self.falling = True

        # init random color
        self.color = randrange(2, 15)

        # Add block to posMap
        mapAdd(self, theFallen)

        self.frame = pyxel.frame_count

    def drop(self):
        """Drops block 4 pixels if frame_count is a multiple of self.vy"""
        if (pyxel.frame_count % self.vy) == 0:
            mapDel(self, theFallen)
            self.y = (self.y + 1)
            mapAdd(self, theFallen)

    def keyLeft(self):
        """Moves left

            if left key pressed & block can move left, move left

        """
        if pyxel.btnp(pyxel.KEY_LEFT, 10, 1) and not mapCheck(self, theFallen, -1, 0):
            mapDel(self, theFallen)
            self.x = max(-self.left, self.x - 1)
            mapAdd(self, theFallen)

    def keyRight(self):
        """Moves right

            if right key pressed & block can move right, move right
        """
        if pyxel.btnp(pyxel.KEY_RIGHT, 10, 1) and not mapCheck(self, theFallen, 1, 0):
            mapDel(self, theFallen)
            self.x = min(self.x + 1,  -self.left + (pyxel.width - self.width) // 4)
            mapAdd(self, theFallen)

    def rotater(self, direction):
        """Rotates in direction (unless 'O' block)

            Args:
                direction (int):  direction of rotation
                                    clockwise      ->  -1
                                    anti-clockwise ->  1
        """
        if self.center:
            mapDel(self, theFallen)
            rotate(self, direction)
            mapAdd(self, theFallen)

    def keyUp(self):
        """Rotate clockwise if up key pressed"""
        if pyxel.btnp(pyxel.KEY_UP):
            self.rotater(-1)

    def keyZ(self):
        """Rotate anti-clockwise if Z key pressed"""
        if pyxel.btnp(pyxel.KEY_Z):
            self.rotater(1)

    def update(self):
        """Updates block

            if not at bottom of screen OR clashing with other block:
                falls
                checks for any of the keys pressed
                updates block's frame counter
            else
                grace period of 16 frames where it can still move
                then -> not falling
        """

        if ((((self.y + self.top) * 4) + self.height) < pyxel.height) and not mapCheck(self, theFallen, 0, 1):

            self.drop()

            self.keyLeft()
            self.keyRight()
            self.keyUp()
            self.keyZ()

            # soft drop, 4 pixels per frame update
            if pyxel.btnp(pyxel.KEY_DOWN):
                self.vy = 1

            self.frame = pyxel.frame_count

        else:

            # if in grace period
            if pyxel.frame_count < self.frame + 16:
                self.keyLeft()
                self.keyRight()
                self.keyUp()
                self.keyZ()
            else:
                self.coords = []
                self.falling = False
                clear()

    def draw(self):
        """Draws blocks rectangle by rectangle (from self.rects)"""
        #for (x, y) in self.coords:
        #    pyxel.rect(
        #        (x + self.x) * 4,
        #        (y + self.y) * 4,
        #        (x + self.x) * 4 + 3,
        #        (y + self.y) * 4 + 3,
        #        self.color)


class App:
    """Main app"""

    def __init__(self):
        """
            - inits the window
            - loads the graphics
            - generates random 7 bag
            - adds a block
            - runs update & draw
        """

        pyxel.init(windowWidth, windowHeight)

        # generates randomly ordered list of [0, 1, 2, 3, 4, 5, 6, 7]
        self.bag = sample(list(range(7)), 7)

        # generates a block from last element of self.bag into self.blocks
        self.block = Block(blockData[self.bag.pop()])

        pyxel.run(self.update, self.draw)

    def update(self):

        # generates a new block if last block has stopped falling
        if not self.block.falling:

            # if self.bag empty, generate new bag
            if not self.bag:
                self.bag = sample(list(range(7)), 7)

            # generate new block
            self.block = Block(blockData[self.bag.pop()])

            # set it to fall
            self.block.falling = True

        # update all blocks
        self.block.update()

        # if key 'q' is pressed, quit
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def drawTheFallen(self):
        for j in range(len(theFallen)):
            for i in range(len(theFallen[j])):
                if theFallen[j][i]:
                    pyxel.rect(
                        i * 4,
                        j * 4,
                        (i * 4) + 3,
                        (j * 4) + 3,
                        theFallen[j][i])

    def draw(self):

        # clear screen w/ black
        pyxel.cls(0)

        self.drawTheFallen()

        # draw all blocks


################
#    blocks    #
################

""" (x, y), (x, y), (x, y), (x, y)

    (centerX, centerY)
"""
blockData = [
    [  # I
        (0, 1), (1, 1), (2, 1), (3, 1),

        (1.5, 1.5)
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

###################
#    functions    #
###################

""" Map of window

    Starts off with all 0s
    then updated to contain an int for color of block where one is present
"""
theFallen = [[0 for _ in range(windowWidth // 4)] for _ in range(windowHeight // 4)]


def clear():
    for row in range(len(theFallen)):
        if 0 not in theFallen[row]:
            for rowTop in range(row, 1, -1):
                theFallen[rowTop] = theFallen[rowTop - 1]


def mapCheck(block, posMap, changeX, changeY):
    """ Checks if moving block to new position (+changeX, +changeY)
        will clash with existing block

        Args:
            posMap (list)
            changeX (int): change in x direction
            changeY (int): change in y direction

        Returns:
            bool: True if clash, False otherwise
    """

    # remove block from posMap
    mapDel(block, posMap)
    for (x, y) in block.coords:

        # check if there will not be index error
        if x + block.x + changeX < len(posMap[0]) and y + block.y + changeY < len(posMap):

            """ if a block exists in (x + block.x + changeX, y + block.y + changeY)
                    add back to posMap
                    return True
            """
            if posMap[y + block.y + changeY][x + block.x + changeX]:
                mapAdd(block, posMap)
                return True
        else:  # if index error -> return True
            return True

    mapAdd(block, posMap)
    return False


def mapAdd(block, posMap):
    """Adds block to posMap"""
    for (x, y) in block.coords:
        posMap[y + block.y][x + block.x] = block.color


def mapDel(block, posMap):
    """Removes block from posMap"""
    for (x, y) in block.coords:
        posMap[y + block.y][x + block.x] = 0


def rotate(block, direction):
    """ Rotates blocks around their defined center position

        - translates (- centerX, - centerY)
        - rotates in direction
            (-1 for clockwise, 1 for anti-clockwise)
        - translates back (centerX, centerY)
        - recalculates width and height

        Args:
            direction (int): direction of rotation
                                clockwise      -> -1
                                anti-clockwise -> 1
    """
    block.coords = [
        (
            int(block.center[0] + direction * (y - block.center[1])),
            int(block.center[1] + direction * (block.center[0] - x))
            )
        for (x, y) in block.coords]
    widthAndHeight(block)


def widthAndHeight(block):
    """ Finds left, right, top, bottom of block
        then uses that to calculate block width and height
    """
    block.left = min(list(zip(*block.coords))[0])
    block.right = max(list(zip(*block.coords))[0])
    block.top = min(list(zip(*block.coords))[1])
    block.bottom = max(list(zip(*block.coords))[1])
    block.width = (
        block.right - block.left +
        1
        ) * 4
    block.height = (
        block.bottom - block.top +
        1
        ) * 4

##################
#    run baby    #
##################

if __name__ == '__main__':

    App()
