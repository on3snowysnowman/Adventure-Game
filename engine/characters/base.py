"""
Tilemap characters - Items displayed to the screen.

A charcater is something that is displayed on the screen.
A character can be many things, it takes up one or more positionson the screen,
and they are represented by ASCII characters.

A character also contains logic on how other characters interact with them,
such as weather it is traversable, and what happens when something moves into it.
These are usually chests, walls, signs, ect.

Characters are REACTIVE, 
meaning that they are only given an opportunity to do something unless something else invokes them.

Entities are very similar to characters, 
except that they are given the ability to think each round,
and react to their environment.
These are usually enemies that can traverse the landscape,
or players that are controlled by external input.

Entities are PROACTIVE,
they have the option to do things each round based upon their state and environment.

All characters should inherit these classes, as the class they inherit will
determine how they are interpreted by the engine.
"""

import math

from queue import SimpleQueue

from engine.characters.auto.base import AutoRunHandler


class BaseCharacter(object):

    """
    BaseCharacter class all sub-characters must inherit.

    We define features that all characters must implement,
    and provide a framework for functionality.

    Characters are encouraged to use the 'start()' method to set parameters,
    as characters don't accept values from init.
    """

    def __init__(self):
        """

        :rtype: object
        """
        self.char = ''  # Character to draw
        self.contains_color = True  # Determines if this character has color attributes
        self.color = ""  # Color of this object
        self.attrib = []  # Color/terminal attributes to draw this character with
        self.name = 'BaseCharacter'  # Name of the character
        self.can_traverse = True  # Boolean determining if other characters can move on our position
        self.priority = 20  # Value determining object stacking priority
        self.can_move = False  # Determines if this character can move
        self.move_priority = 20  # Determines order of movement

        self.is_alive = True  # Determines if this object is alive

        self.debug_move = False

        self.keys = []  # List of keys we care about
        self.inp = SimpleQueue()  # Input queue

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

        USERS AND DEVELOPERS SHOULD NOT OVERLOAD THIS METHOD!
        (Unless they are creating a new character type)

        Most child characters(Like EntityCharacter) rely on this method to operate.
        Instead, you should use the normal 'start' method.
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
        self.is_alive = True  # Enabling the object to act

        self.auto = AutoRunHandler(self)  # Autorun handler for managing autoruns

    def _run(self):

        """
        Executes the autoruns attached to this entity.
        """

        self.auto.run()

    def move(self):

        """
        Class called when the entity can move.
        """

        pass

    def check_tile(self, x, y):

        """
        Checks if tile is in bounds, and traversable by cycling through the tile list

        :param x: X coordinate
        :param y: Y coordinate
        :return: Boolean if the tile is traversable or not
        """

        if (x >= self.tilemap.width or x < 0) or (y >= self.tilemap.height or y < 0):
            return False

        for tile in self.tilemap.get(x, y):

            if not tile.obj.can_traverse:
                return False

        return True
