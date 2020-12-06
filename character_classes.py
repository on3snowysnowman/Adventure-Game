"""
Classes representing classes drawn on the screen.

Each class has some logic that allows it to interact,
and interact with, the DisplayWindow.
"""

import random
import queue
from item_classes import *
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
        self.text_win = None

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


# Custom CharacterClasses - probably wont live here

class Player(EntityCharacter):

    """
    Player class, moves and gets controlled by the user.
    """

    def __init__(self):

        super().__init__()

        self.inventory = []
        self.inventory_space = 0
        self.inventory_space_max = 30

        self.char = 'C'
        self.name = 'Player'
        self.attrib.append("green")
        self.priority = 0
        self.move_priority = 30

        self.keys = ['w', 'a', 's', 'd', 'q', 'e', 'z', 'c', 'p', 'i']

    def move(self):

        """
        Moves the character across the screen, or executes choices the player wants to make

        We accept input from the DisplayWindow here.
        """

        # Get input from the DisplayWindow

        #time.sleep(3)

        inp = self.get_input()

        # Get our cordnets:

        tile = self.tilemap.find_object(self)

        if inp == 'w':

            # Move up:

            for x in self.tilemap.get(tile.x, tile.y - 1):

                if isinstance(x.obj, Chest):

                    self.pickup_item(x.obj.open_chest())
                    for j in self.tilemap.get(tile.x, tile.y - 1): print(x.obj)
                    self.tilemap.removeObj_by_coords(tile.x, tile.y - 1)
                    return

            if self.check_tile(tile.x, tile.y - 1):

                self.tilemap.move(self, tile.x, tile.y - 1)

        elif inp == 'a':

            # Move right

            if self.check_tile(tile.x - 1, tile.y):

                self.tilemap.move(self, tile.x-1, tile.y)

        elif inp == 's':

            # Move down

            if self.check_tile(tile.x, tile.y + 1):

                self.tilemap.move(self, tile.x, tile.y+1)

        elif inp == 'd':

            # Move right

            if self.check_tile(tile.x + 1, tile.y):

                self.tilemap.move(self, tile.x+1, tile.y)

        elif inp == 'q':

            # Move diagonal up left

            if self.check_tile(tile.x - 1, tile.y - 1):

                self.tilemap.move(self, tile.x - 1, tile.y - 1)

        elif inp == 'e':

            # Move diagonal up right

            if self.check_tile(tile.x + 1, tile.y - 1):
                self.tilemap.move(self, tile.x + 1, tile.y - 1)

        elif inp == 'z':

            # Move diagonal down left

            if self.check_tile(tile.x - 1, tile.y + 1):
                self.tilemap.move(self, tile.x - 1, tile.y + 1)

        elif inp == 'c':

            # Move diagonal down right

            if self.check_tile(tile.x + 1, tile.y + 1):
                self.tilemap.move(self, tile.x + 1, tile.y + 1)

        elif inp == 'p':

            self.pickup_first_item()

        elif inp == 'i':

            self.text_win.add_content("Inventory: ")

            for x in self.inventory:

                if isinstance(x, Item):

                    self.text_win.add_content(x.name)
            self.text_win.add_content("")

    def check_inventory_bounds(self, obj):

        if self.inventory_space + obj.size > self.inventory_space_max:

            return False

        return True

    def pickup_first_item(self):

        """
        Adds the first item in the tile list to player inventory if there is enough space
        :return:
        """

        playerObj = self.tilemap.find_object_type(Player)
        targObj = self.tilemap.get(playerObj.x, playerObj.y, 1).obj

        # Checks if the item is of Class Item

        if isinstance(targObj, Item):

            # Checks if the object is allowed to be picked up

            if targObj.can_player_pickup:

                if self.check_inventory_bounds(targObj):

                    self.inventory.append(targObj)
                    self.inventory_space += targObj.size
                    self.tilemap.removeObj(targObj)
                    self.text_win.add_content(targObj.name + " added to inventory")


        pass

    def pickup_item(self, targObj):

        if isinstance(targObj, Item):

            # Checks if the object is allowed to be picked up

            if targObj.can_player_pickup:

                if self.check_inventory_bounds(targObj):

                    self.inventory.append(targObj)
                    self.inventory_space += targObj.size
                    self.text_win.add_content(targObj.name + " added to inventory")

    def get_item(self, targObj):

        if isinstance(targObj, Item):

            if not self.check_inventory_bounds(targObj):

                playerPos = self.tilemap.get(self)
                self.tilemap.add(targObj, playerPos.x, playerPos.y)
                self.text_win.add_content(f"You don't have enough space for the {targObj.name}")

            else:

                self.inventory.append(targObj)
                self.inventory_space += targObj.size
                self.text_win.add_content(targObj.name + " added to inventory")


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
        self.priority = 18

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

            if self.check_tile(targ[0], targ[1]):

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
        self.priority = 18

    def move(self):

        enemyTile = self.tilemap.find_object(self)
        playerTile = self.tilemap.find_object_type(Player)

        x, y = enemyTile.x, enemyTile.y
        targX, targY = playerTile.x, playerTile.y

        moveOptions = self.tilemap.get_around(x, y)
        validCoords = []
        for i in moveOptions:
            for j in i:
                validCoords.append([j.x, j.y])

        # Left Up
        if targX < x and targY < y:

            # Checking if player is directly next to the player diagnonaly
            if x - 1 == targX and y - 1 == targY:

                secondaryValidCoords = []

                if [x - 1, y] in validCoords and self.check_tile(x - 1, y):
                    secondaryValidCoords.append([x - 1, y])

                if [x, y - 1] in validCoords and self.check_tile(x, y - 1):
                    secondaryValidCoords.append([x, y - 1])

                if len(secondaryValidCoords) > 0:
                    nextMove = random.choice(secondaryValidCoords)
                    self.tilemap.move(self, nextMove[0], nextMove[1])

            elif [x - 1, y - 1] in validCoords and self.check_tile(x - 1, y - 1):

                self.tilemap.move(self, x - 1, y - 1)

            else:
                self.blocked_move("left_up")

        # Left
        elif targX < x and targY == y:

            if [x - 1, y] in validCoords and self.check_tile(x - 1, y):

                self.tilemap.move(self, x - 1, y)

            else:
                self.blocked_move("left")

        # Left Down
        elif targX < x and targY > y:

            # Checking if player is directly next to the player diagnonaly
            if x - 1 == targX and y + 1 == targY:

                secondaryValidCoords = []

                if [x - 1, y] in validCoords and self.check_tile(x - 1, y):
                    secondaryValidCoords.append([x - 1, y])

                if [x, y + 1] in validCoords and self.check_tile(x, y + 1):
                    secondaryValidCoords.append([x, y + 1])

                if len(secondaryValidCoords) > 0:
                    nextMove = random.choice(secondaryValidCoords)
                    self.tilemap.move(self, nextMove[0], nextMove[1])

            if [x - 1, y + 1] in validCoords and self.check_tile(x - 1, y + 1):

                self.tilemap.move(self, x - 1, y + 1)

            else:
                self.blocked_move("left_down")

        # Down
        elif targY > y and targX == x:

            if [x, y + 1] in validCoords and self.check_tile(x, y + 1):

                self.tilemap.move(self, x, y + 1)

            else:
                self.blocked_move("down")

        # Right Down
        elif targX > x and targY > y:

            # Checking if player is directly next to the player diagnonaly
            if x + 1 == targX and y + 1 == targY:

                secondaryValidCoords = []

                if [x + 1, y] in validCoords and self.check_tile(x + 1, y):
                    secondaryValidCoords.append([x + 1, y])

                if [x, y + 1] in validCoords and self.check_tile(x, y + 1):
                    secondaryValidCoords.append([x, y + 1])

                if len(secondaryValidCoords) > 0:
                    nextMove = random.choice(secondaryValidCoords)
                    self.tilemap.move(self, nextMove[0], nextMove[1])

            if [x + 1, y + 1] in validCoords and self.check_tile(x + 1, y + 1):

                self.tilemap.move(self, x + 1, y + 1)

            else:
                self.blocked_move("right_down")

        # Right
        elif targX > x and targY == y:

            if [x + 1, y] in validCoords and self.check_tile(x + 1, y):

                self.tilemap.move(self, x + 1, y)

            else:
                self.blocked_move("right")

        # Right Up
        elif targX > x and targY < y:

            # Checking if player is directly next to the player diagnonaly
            if x + 1 == targX and y - 1 == targY:

                secondaryValidCoords = []

                if [x + 1, y] in validCoords and self.check_tile(x + 1, y):
                    secondaryValidCoords.append([x + 1, y])

                if [x, y - 1] in validCoords and self.check_tile(x, y - 1):
                    secondaryValidCoords.append([x, y - 1])

                if len(secondaryValidCoords) > 0:
                    nextMove = random.choice(secondaryValidCoords)
                    self.tilemap.move(self, nextMove[0], nextMove[1])

            if [x + 1, y - 1] in validCoords and self.check_tile(x + 1, y - 1):

                self.tilemap.move(self, x + 1, y - 1)

            else:
                self.blocked_move("right_up")

        # Up
        elif targY < y and targX == x:

            if [x, y - 1] in validCoords and self.check_tile(x, y - 1):

                self.tilemap.move(self, x, y - 1)

            else:
                self.blocked_move("up")

    def blocked_move(self, direction):

        enemyTile = self.tilemap.find_object(self)
        playerTile = self.tilemap.find_object_type(Player)
        x, y = enemyTile.x, enemyTile.y

        if direction == "left_up":

            validCoords = []
            for j in range(x, -1, -1):

                if self.check_tile(j, y - 1):

                    validCoords.append([j, y - 1])

            if len(validCoords) == 0:

                for j in range(x, self.tilemap.width):

                    if self.check_tile(j, y - 1):

                        validCoords.append([j, y - 1])

            if len(validCoords) != 0:

                if len(validCoords) > 1:

                    pass

                else:

                    nextMove = random.choice(validCoords)
                    targX, targY = nextMove[0], nextMove[1]
                    if x == targX and y - 1 == targY:

                        if self.check_tile(x, y - 1): self.tilemap.move(self, x, y - 1)


                    elif targX > x:

                        if x + 1 == targX:

                            if self.check_tile(x + 1, y - 1): self.tilemap.move(self, x + 1, y - 1)

                        elif self.check_tile(x + 1, y): self.tilemap.move(self, x + 1, y)

                    else:

                        if x - 1 == targX:

                            if self.check_tile(x - 1, y - 1): self.tilemap.move(self, x - 1, y - 1)

                        elif self.check_tile(x - 1, y): self.tilemap.move(self, x - 1, y)


        elif direction == "left":

            validCoords = []
            for j in range(y, -1, -1):

                if self.check_tile(x - 1, j):
                    validCoords.append([x - 1, j])

            if len(validCoords) == 0:

                for j in range(y, self.tilemap.height):

                    if self.check_tile(x - 1, j):
                        validCoords.append([x - 1, j])

            if len(validCoords) != 0:

                if len(validCoords) > 1:

                    pass

                else:

                    nextMove = random.choice(validCoords)
                    targX, targY = nextMove[0], nextMove[1]
                    if y == targY and x - 1 == targX:

                        if self.check_tile(x - 1, y): self.tilemap.move(self, x - 1, y)

                    elif targY > y:

                        if y + 1 == targY:

                            if self.check_tile(x - 1, y + 1): self.tilemap.move(self, x - 1, y + 1)

                        elif self.check_tile(x, y + 1):

                            self.tilemap.move(self, x, y + 1)

                    else:

                        if y - 1 == targY:

                            if self.check_tile(x - 1, y - 1): self.tilemap.move(self, x - 1, y - 1)

                        elif self.check_tile(x, y - 1):
                            self.tilemap.move(self, x, y - 1)


        elif direction == "left_down":

            pass


        elif direction == "down":

            pass


        elif direction == "right_down":

            pass


        elif direction == "right":

            pass


        elif direction == "right_up":

            pass


        elif direction == "up":

            pass


        pass


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


class Chest(BaseCharacter):

    def start(self):

        self.char = 'C'
        self.name = 'Chest'
        self.attrib.append("brown")
        self.priority = 19

        #Disabling traversal mode

        self.can_traverse = False

    def open_chest(self):

        posTile = self.tilemap.find_object(self)
        contents = [Sword(), Chestplate()]
        self.tilemap.add(Enemy(), posTile.x, posTile.y)
        self.tilemap.removeObj(self)
        return random.choice(contents)


class OpenedChest(BaseCharacter):

    def start(self):

        self.char = "C"
        self.name = "Opened Chest"
        self.attrib.append("light_brown")
        self.priority = 19

        # Disabling traversal mode

        self.can_traverse = False


class Floor(BaseCharacter):

    """
    Represents a floor. Player can move over it.
    """

    def start(self):

        self.char = '0'
        self.name = 'Floor'
        self.attrib.append("blue")

