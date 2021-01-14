"""
Classes representing classes drawn on the screen.

Each class has some logic that allows it to interact,
and interact with, the DisplayWindow.
"""

import random
import queue
from item_classes import *

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

        self.debug_move = False

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

    def look(self, obj, targs):

        objects = []

        objTile = self.tilemap.find_object(self)
        for x in self.tilemap.get_around(objTile.x, objTile.y, 5):

            for j in x:

                if isinstance(j.obj, targs):

                    objPos = [j.x, j.y]
                    startPos = [objTile.x, objTile.y]

                    isWall = False

                    # Check Above
                    if j.y < objTile.y:

                        #While the starting position of player does not equal the targeted object's position
                        while startPos[1] != objPos[1]:

                            #Cycling through the tile list of our value startPos
                            for i in self.tilemap.get(startPos[0], startPos[1]):

                                if isinstance(i.obj, Wall):

                                    isWall = True
                                    break

                            startPos[1] -= 1

                    if not isWall: objects.append(j.obj.name)

        return objects

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

    def find_quickest_path(self, targObj):

        selfTile = self.tilemap.find_object(self)

        startPosX, startPosY = targObj.x, targObj.y

        booleanTileMap = []
        numberTileMap = []

        #Number of tiles we can fill
        numMoves = 0

        y, x = 0, 0

        #Creating BooleanTileMap
        for line in range(self.tilemap.height):

            booleanTileMap.append([])

            for col in range(self.tilemap.width):

                for i in self.tilemap.get(x, y):

                    if not i.obj.can_traverse:

                        booleanTileMap[line].append(False)
                        break

                    else:

                        booleanTileMap[line].append(True)
                        numMoves += 1
                        break

                x += 1

            x = 0
            y += 1

        #Creating NumberTileMap
        for line in range(self.tilemap.height):

            numberTileMap.append([])

            for col in range(self.tilemap.width):

                numberTileMap[line].append(-1)

        numberCoords = {0 : [startPosX, startPosY]}

        currentNum = 0
        nextNum = 1

        currentX = numberCoords[0][0]
        currentY = numberCoords[0][1]

        while currentNum < numMoves:

            #Check Right
            if self.check_tile(currentX + 1, currentY) and booleanTileMap[currentY][currentX + 1]:

                numberTileMap[currentY][currentX + 1] = nextNum
                numberCoords[nextNum] = [currentX + 1, currentY]
                booleanTileMap[currentY][currentX + 1] = False
                nextNum += 1

            #Check Right Up
            elif self.check_tile(currentX + 1, currentY - 1) and booleanTileMap[currentY - 1][currentX + 1]:

                numberTileMap[currentY - 1][currentX + 1] = nextNum
                numberCoords[nextNum] = [currentX + 1, currentY - 1]
                booleanTileMap[currentY - 1][currentX + 1] = False
                nextNum += 1

            #Check Up
            elif self.check_tile(currentX, currentY - 1) and booleanTileMap[currentY - 1][currentX]:

                numberTileMap[currentY - 1][currentX] = nextNum
                numberCoords[nextNum] = [currentX, currentY - 1]
                booleanTileMap[currentY - 1][currentX] = False
                nextNum += 1

            #Check Left Up
            elif self.check_tile(currentX - 1, currentY - 1) and booleanTileMap[currentY - 1][currentX - 1]:

                numberTileMap[currentY - 1][currentX - 1] = nextNum
                numberCoords[nextNum] = [currentX - 1, currentY - 1]
                booleanTileMap[currentY - 1][currentX - 1] = False
                nextNum += 1

            #Check Left
            elif self.check_tile(currentX - 1, currentY) and booleanTileMap[currentY][currentX - 1]:

                numberTileMap[currentY][currentX - 1] = nextNum
                numberCoords[nextNum] = [currentX - 1, currentY]
                booleanTileMap[currentY][currentX - 1] = False
                nextNum += 1

            #Check Down Left
            elif self.check_tile(currentX - 1, currentY + 1) and booleanTileMap[currentY + 1][currentX - 1]:

                numberTileMap[currentY + 1][currentX - 1] = nextNum
                numberCoords[nextNum] = [currentX - 1, currentY + 1]
                booleanTileMap[currentY + 1][currentX - 1] = False
                nextNum += 1

            #Check Down
            elif self.check_tile(currentX, currentY + 1) and booleanTileMap[currentY + 1][currentX]:

                numberTileMap[currentY + 1][currentX] = nextNum
                numberCoords[nextNum] = [currentX, currentY + 1]
                booleanTileMap[currentY + 1][currentX] = False
                nextNum += 1

            #Check Down Right
            elif self.check_tile(currentX + 1, currentY + 1) and booleanTileMap[currentY + 1][currentX + 1]:

                numberTileMap[currentY + 1][currentX + 1] = nextNum
                numberCoords[nextNum] = [currentX + 1, currentY + 1]
                booleanTileMap[currentY + 1][currentX + 1] = False
                nextNum += 1

            else:

                currentNum += 1
                currentX = numberCoords[currentNum][0]
                currentY = numberCoords[currentNum][1]

            breakWhileLoop = False

            surroundingTiles = self.tilemap.get_around(currentX, currentY)
            for l in surroundingTiles:

                for i in l:

                    if i.obj == self:
                        breakWhileLoop = True
                        break

                if breakWhileLoop: break

            if breakWhileLoop: break

        return numberTileMap

# Custom CharacterClasses - probably wont live here

class Player(EntityCharacter):

    """
    Player class, moves and gets controlled by the user.
    """

    def __init__(self):

        super().__init__()

        self.see_list = (Item, Enemy, TrackerEnemy, Chest, OpenedChest)

        self.inventory = []
        self.inventory_space = 0
        self.inventory_space_max = 30

        self.char = 'C'
        self.name = 'Player'
        self.attrib.append("green")
        self.priority = 0
        self.move_priority = 18

        self.keys = ['w', 'a', 's', 'd', 'q', 'e', 'z', 'c', 'p', 'i', 'l', 'o', 'y']

    def move(self):

        """
        Moves the character across the screen, or executes choices the player wants to make

        We accept input from the DisplayWindow here.
        """

        # Get input from the DisplayWindow

        #time.sleep(3)

        inp = self.get_input()

        # Get our coordnates:

        playerTile = self.tilemap.find_object(self)

        if inp == 'w':

            # Move up:

            #Checks if the player is moving into a tile with a chest. If so, open it
            self.check_chest(playerTile.x, playerTile.y - 1)

            if self.check_tile(playerTile.x, playerTile.y - 1):

                self.tilemap.move(self, playerTile.x, playerTile.y - 1)

        elif inp == 'a':

            # Move right

            # Checks if the player is moving into a tile with a chest. If so, open it
            self.check_chest(playerTile.x - 1, playerTile.y)

            if self.check_tile(playerTile.x - 1, playerTile.y):

                self.tilemap.move(self, playerTile.x-1, playerTile.y)

        elif inp == 's':

            # Move down

            # Checks if the player is moving into a tile with a chest. If so, open it
            self.check_chest(playerTile.x, playerTile.y + 1)

            if self.check_tile(playerTile.x, playerTile.y + 1):

                self.tilemap.move(self, playerTile.x, playerTile.y+1)

        elif inp == 'd':

            # Move right

            # Checks if the player is moving into a tile with a chest. If so, open it
            self.check_chest(playerTile.x + 1, playerTile.y)

            if self.check_tile(playerTile.x + 1, playerTile.y):

                self.tilemap.move(self, playerTile.x+1, playerTile.y)

        elif inp == 'q':

            # Move diagonal up left

            if self.check_tile(playerTile.x - 1, playerTile.y - 1):

                self.tilemap.move(self, playerTile.x - 1, playerTile.y - 1)

        elif inp == 'e':

            # Move diagonal up right


            if self.check_tile(playerTile.x + 1, playerTile.y - 1):
                self.tilemap.move(self, playerTile.x + 1, playerTile.y - 1)

        elif inp == 'z':

            # Move diagonal down left

            if self.check_tile(playerTile.x - 1, playerTile.y + 1):
                self.tilemap.move(self, playerTile.x - 1, playerTile.y + 1)

        elif inp == 'c':

            # Move diagonal down right

            if self.check_tile(playerTile.x + 1, playerTile.y + 1):
                self.tilemap.move(self, playerTile.x + 1, playerTile.y + 1)

        elif inp == 'p':

            self.pickup_first_item()

        elif inp == 'i':

            if len(self.inventory) == 0:

                self.text_win.add_content("Your inventory is empty", attrib="white")

            else:

                self.text_win.add_content("Inventory: ", attrib = "white")

                for x in self.inventory:

                    if isinstance(x, Item):

                        self.text_win.add_content(x.name)

                self.text_win.add_content("\n" * 0)

        elif inp == 'l':

            objects = self.look(self, self.see_list)

            if len(objects) > 0:

                self.text_win.add_content("Things you see in this room: ", "white")
                self.text_win.add_content(objects)
                self.text_win.add_content("\n" * 0)

            else: self.text_win.add_content("You don't see any objects in this room", "white")

        elif inp == 'o':

            groundContents = []

            for x in self.tilemap.get(playerTile.x, playerTile.y):

                if not isinstance(x.obj, Player) and not isinstance(x.obj, Floor):

                    groundContents.append(x)

            if len(groundContents) > 0:

                self.text_win.add_content("Things on the ground: ", "white")

                for x in groundContents:

                    if not isinstance(x.obj, Player):

                        self.text_win.add_content(x.obj.name)

                self.text_win.add_content("\n" * 0)

        elif inp == 'y':
            
            self.tilemap.toggle_enemy_movement()

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

    def check_chest(self, xPos, yPos):

        if self.tilemap._bound_check(xPos, yPos):

            for i in self.tilemap.get(xPos, yPos):

                if isinstance(i.obj, Chest):

                    item = i.obj.open_chest()

                    if isinstance(item, Item):
                        self.text_win.add_content(f"You found a {item.name} in a chest! ")
                        self.pickup_item(item)
                        self.tilemap.removeObj_by_coords(xPos, yPos)
                        self.tilemap.add(OpenedChest(), xPos, yPos)


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
        self.move_priority = 19

    def move(self):


        if self.debug_move:

            numberTileMap = self.find_quickest_path(self.tilemap.find_object_type(Player))
            selfTile = self.tilemap.find_object(self)

            posX = selfTile.x
            posY = selfTile.y

            final = []

            for x in range(8):

                final.append(-1)

            index = 0

            # Iterate over each value:

            for cur_y in range(posY - 1, posY + 2):

                for cur_x in range(posX - 1, posX + 2):

                    # Self Tile
                    if cur_y == posY and cur_x == posX:

                        continue

                    else:

                        if self.check_tile(cur_x, cur_y):

                            final[index] = (numberTileMap[cur_y][cur_x])

                    index += 1

            leastNum = float('inf')
            count = 0
            index = 0

            for num in final:

                if num != -1 and num < leastNum:

                    leastNum = num
                    count = index

                index += 1

            surroundingTiles = self.tilemap.get_around(posX, posY)

            shouldMove = True

            for tileList in surroundingTiles:

                for tile in tileList:

                   if isinstance(tile.obj, Player):

                       shouldMove = False

            if shouldMove:

                #Left Up
                if count == 0:

                    if self.check_tile(posX - 1, posY - 1): self.tilemap.move(self, posX - 1, posY - 1)

                #Up
                elif count == 1:

                    if self.check_tile(posX, posY - 1): self.tilemap.move(self, posX, posY - 1)

                #Right Up
                elif count == 2:

                    if self.check_tile(posX + 1, posY - 1): self.tilemap.move(self, posX + 1, posY - 1)

                #Right
                elif count == 4:

                    if self.check_tile(posX + 1, posY): self.tilemap.move(self, posX + 1, posY)

                #Right Down
                elif count == 7:

                    if self.check_tile(posX + 1, posY + 1): self.tilemap.move(self, posX + 1, posY + 1)

                #Down
                elif count == 6:

                    if self.check_tile(posX, posY + 1): self.tilemap.move(self, posX, posY + 1)

                #Left Down
                elif count == 5:

                    if self.check_tile(posX - 1, posY + 1): self.tilemap.move(self, posX - 1, posY + 1)

                #Left
                elif count == 3:

                    if self.check_tile(posX - 1, posY): self.tilemap.move(self, posX - 1, posY)


            playerTile = self.tilemap.find_object_type(Player)

            xPos = 0
            yPos = 0

            '''
            print("\n" * 2)
            for line in numberTileMap:
    
                for col in line:
    
                    if xPos == playerTile.x and yPos == playerTile.y:
                        print(" C", end="")
                    elif xPos == selfTile.x and yPos == selfTile.y:
                        print(" E", end="")
                    elif col != -1:
                        print(" " + str(col), end="")
                    else:
                        print(col, end="")
                    xPos += 1
    
                yPos += 1
                xPos = 0
                print("\n")
            '''

    def debug_move_toggle(self):

        if self.debug_move:

            self.debug_move = False

        else: self.debug_move = True


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
        self.attrib.append("gray_blue")

