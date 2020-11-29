"""
Classes representing classes drawn on the screen.

Each class has some logic that allows it to interact,
and interact with, the DisplayWindow.
"""

import random
import queue
import time


class BaseCharacter(object):

    """
    BaseCharacter class all sub-characters must inherit.

    We offer some useful functionality, as well as define some use cases
    """

    def __init__(self):

        self.char = ''  # Character to draw
        self.contains_color = True
        self.color = ""
        self.attrib = []
        self.name = 'BaseCharacter'   # Name of the character
        self.can_traverse = True  # Boolean determining if things can walk their
        self.priority = 20  # Value determining object stacking priority
        self.can_move = False
        self.move_priority = 20

        self.keys = []  # List of keys we care about
        self.inp = queue.SimpleQueue()  # Input queue

        self.tilemap = None  # Tilemap instance
        self.win = None  # DisplayWindow instance

        # Calling meta start method:

        self._start()

        # Calling user start method:

        self.start()

    def _bind(self, win, tilemap):

        """
        Binds the DisplayWindow and Tilemap
        objects to this character.

        :param win: DisplayWindow instance
        :type win: DisplayWindow
        :param tilemap: tilemap instance
        :type tilemap: BaseTileMap
        """

        self.win = win
        self.tilemap = tilemap

    def _start(self):

        """
        Meta start method, used by child characters.
        """

        pass

    def start(self):

        """
        Start method called when the object is instantiated.

        Allows child characters to set parameters to the way that they like.
        """

        pass

    def get_input(self, block=True, timeout=None, return_ascii=False):

        """
        Gets input from the input queue for this character.

        :param block: Boolean determining if we should block
        :type block: bool
        :param timeout: Timeout value in seconds for the blocking operation
        :type timeout: int, None
        :param return_ascii: Boolean determining if we should return ASCII codes instead of strings
        :return: Input from the input queue
        :rtype: int
        """

        # Get and return value from the queue:

        inp = self.inp.get(block=block, timeout=timeout)

        if inp is None:

            # We are done here, exit and do something:

            pass

        try:

            if not return_ascii and inp < 225:

                # input is valid string, return in string format:

                return chr(inp)

        except TypeError:

            pass

        # Return ASCII code

        return inp

    def add_input(self, inp):

        """
        Adds input to the input queue.

        :param inp: Input to add to the queue
        :type inp: int
        """

        self.inp.put(inp)

    def interact(self, char):

        """
        Method called when an Entity attempts to move into this object.

        :param char: Character interacting with this object
        :type char: BaseCharacter
        """

        pass


class EntityCharacter(BaseCharacter):

    """
    Class representing an entity that can move across the screen.
    """

    def _start(self):

        """
        Meta start method, updating some parameters.
        """

        self.can_move = True  # Enabling move mode
        self.can_traverse = False  # Disabling traversal mode

    def move(self):

        """
        Class called when the entity can move.
        """

        pass

    def check_next_tile(self, x, y):

        if (x >= self.tilemap.width or x < 0) or (y >= self.tilemap.height or y < 0):

            return False

        for tile in self.tilemap.get(x, y):

            if not tile.obj.can_traverse:

                return False

        return True


# Custom CharacterClasses - probably wont live here


class Player(EntityCharacter):

    """
    Player class, moves and gets controlled by the user.
    """

    def start(self):

        self.char = 'C'
        self.name = 'Player'
        self.attrib.append("green")
        self.priority = 0
        self.move_priority = 30

        self.keys = ['w', 'a', 's', 'd']

    def move(self):

        """
        Moves the character across the screen.

        We accept input from the DisplayWindow here.
        """

        # Get input from the DisplayWindow

        #time.sleep(3)

        inp = self.get_input()

        # Get our cordnets:

        tile = self.tilemap.find_object(self)

        if inp == 'w':

            # Move up:

            if self.check_next_tile(tile.x, tile.y - 1):

                self.tilemap.move(self, tile.x, tile.y-1)

        elif inp == 'a':

            # Move right

            if self.check_next_tile(tile.x - 1, tile.y):

                self.tilemap.move(self, tile.x-1, tile.y)

        elif inp == 's':

            # Move down

            if self.check_next_tile(tile.x, tile.y + 1):

                self.tilemap.move(self, tile.x, tile.y+1)

        elif inp == 'd':

            # Move right

            if self.check_next_tile(tile.x + 1, tile.y):

                self.tilemap.move(self, tile.x+1, tile.y)


class Enemy(EntityCharacter):

    """
    Enemy that randomly moves across the screen.
    """

    def start(self):

        """
        Sets our name and character.
        """

        self.name = 'Enemy'
        self.char = 'E'
        self.attrib.append("red")
        self.priority = 19

    def move(self):

        """
        Moves across the screen randomly.
        """

        # Get objects all around us:

        tile = self.tilemap.find_object(self)

        x = tile.x
        y = tile.y

        cords = [[x-1, y], [x+1, y], [x, y+1], [x, y-1], [x-1, y-1], [x+1, y-1], [x-1, y+1], [x+1, y+1]]
        choices = []

        for targ in cords:

            if self.check_next_tile(targ[0], targ[1]):

                choices.append(targ)

        if len(choices) > 0:

            # Now, select a random choice from the options and move their:

            choice = random.choice(choices)

            self.tilemap.move(self, choice[0], choice[1])


class TrackerEnemy(EntityCharacter):

    """
    Enemy that follows the player
    """

    def start(self):

        """
        Sets our name and character
        """

        self.name = 'Enemy'
        self.char = 'E'
        self.attrib.append("red")
        self.priority = 19

    def move(self):

        enemyTile = self.tilemap.find_object(self)
        playerTile = self.tilemap.find_object_type(Player)
        xPos, yPos = enemyTile.x, enemyTile.y

        pxPos, pyPos = playerTile.x, playerTile.y

        moveOptions = self.tilemap.get_around(xPos, yPos)
        print(self.tilemap.get_around(xPos, yPos))
        validCoords = []
        for x in moveOptions:
            for j in x:
                validCoords.append([j.x, j.y])

        #Left Up
        if pxPos < xPos and pyPos < yPos:

            #Checking if player is directly next to the player diagnonaly
            if xPos - 1 == pxPos and yPos - 1 == pyPos:

                secondaryValidCoords = []

                if[xPos - 1, yPos] in validCoords and self.check_next_tile(xPos - 1, yPos):

                       secondaryValidCoords.append([xPos - 1, yPos])

                if [xPos, yPos - 1] in validCoords and self.check_next_tile(xPos, yPos - 1):

                        secondaryValidCoords.append([xPos, yPos - 1])

                if len(secondaryValidCoords) > 0:

                    nextMove = random.choice(secondaryValidCoords)
                    self.tilemap.move(self, nextMove[0], nextMove[1])

            elif [xPos - 1, yPos - 1] in validCoords and self.check_next_tile(xPos - 1, yPos - 1):

                self.tilemap.move(self, xPos - 1, yPos - 1)

        #Left
        elif pxPos < xPos and pyPos == yPos:
            if [xPos - 1, yPos] in validCoords and self.check_next_tile(xPos - 1, yPos):

                self.tilemap.move(self, xPos - 1, yPos)

        #Left Down
        elif pxPos < xPos and pyPos > yPos:

            if [xPos - 1, yPos + 1] in validCoords and self.check_next_tile(xPos - 1, yPos + 1):

                self.tilemap.move(self, xPos - 1, yPos + 1)

        #Down
        elif pyPos > yPos and pxPos == xPos:

            if [xPos, yPos + 1] in validCoords and self.check_next_tile(xPos, yPos + 1):

                self.tilemap.move(self, xPos, yPos + 1)

        #Right Down
        elif pxPos > xPos and pyPos > yPos:

            if [xPos + 1, yPos + 1] in validCoords and self.check_next_tile(xPos + 1, yPos + 1):

                self.tilemap.move(self, xPos + 1, yPos + 1)

        #Right
        elif pxPos > xPos and pyPos == yPos:

            if [xPos + 1, yPos] in validCoords and self.check_next_tile(xPos + 1, yPos):

                self.tilemap.move(self, xPos + 1, yPos)

        #Right Up
        elif pxPos > xPos and pyPos < yPos:

            if [xPos + 1, yPos - 1] in validCoords and self.check_next_tile(xPos + 1, yPos - 1):

                self.tilemap.move(self, xPos + 1, yPos - 1)

        #Up
        elif pyPos < yPos and pxPos == xPos:

            if [xPos, yPos - 1] in validCoords and self.check_next_tile(xPos, yPos - 1):

                self.tilemap.move(self, xPos, yPos - 1)


class Wall(BaseCharacter):

    """
    Represents a wall. Player can't move past it.
    """

    def start(self):

        self.char = 'W'
        self.name = 'Wall'
        self.attrib.append("yellow")
        self.priority = 19

        # Disabling traversal mode:

        self.can_traverse = False


class Floor(BaseCharacter):

    """
    Represents a floor. Player can move over it.
    """

    def start(self):

        self.char = '0'
        self.name = 'Floor'
        self.attrib.append("blue")

