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
# determine how they are interpreted by the engine.
"""

import math

from queue import SimpleQueue


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

    def move(self):

        """
        Class called when the entity can move.
        """

        pass

    def look(self, tilemap):

        """
        Fills tiles on the map with fog based on where the wall is blocking view
        :param tilemap: tilemap that is being parsed
        """

        fog = Fog()

        selfTile = tilemap.find_object(self)

        xIt = 0
        yIt = 0

        toTop = False

        count = 0

        # Checking Walls
        for line in tilemap.tilemap:

            for col in line:

                for objTile in col:

                    if isinstance(objTile, Wall):

                        checkTop = False
                        toTop = False

                        # Y Position of character in relation to an origin at the bottom left
                        posY = (len(tilemap.tilemap) - 1) - selfTile.y
                        # X Position of character, irrelevant if origin is top left or bottom left
                        posX = selfTile.x

                        wallPosY = ((tilemap.height - 1) - yIt) - posY
                        wallPosX = xIt - posX

                        # Wall is on the same X Value, below us
                        if xIt == selfTile.x and yIt > selfTile.y:

                            pointsBlocked = []

                            # Right Half
                            equationRight = float(wallPosY / (wallPosX + 1))

                            yIndex = yIt + 1
                            xIndex = xIt

                            while yIndex < len(tilemap.tilemap):

                                # Tile directly above the wall, will always be blocked out
                                tilemap.add(fog, xIndex, yIndex)

                                xIndex += 1

                                # Incrementing along x axis until we reach the beginning tile of where the slope indexes
                                while xIndex < len(tilemap.tilemap[yIndex]) and (xIndex - xIt) < \
                                        math.floor((((len(tilemap.tilemap) - 1) - yIndex) - posY) / equationRight):

                                    tilemap.add(fog, xIndex, yIndex)

                                    if xIndex != selfTile.x:
                                        pointsBlocked.append([xIndex, yIndex])
                                        
                                    xIndex += 1

                                floatOutput = (((len(tilemap.tilemap) - 1) - yIndex) - posY) / equationRight

                                if math.floor((floatOutput % 1) * 10) / 10 >= .5 and xIndex < len(tilemap.tilemap[yIndex]):

                                    tilemap.add(fog, xIndex, yIndex)

                                    if xIndex != selfTile.x:
                                        pointsBlocked.append([xIndex, yIndex])
                                   
                                # Adding points that may extend beyond the boundary of the tilemap
                                while (xIndex - xIt) < math.floor(
                                        (((len(tilemap.tilemap) - 1) - yIndex) - posY) / equationRight):

                                    if xIndex != selfTile.x:
                                        pointsBlocked.append([xIndex, yIndex])

                                    xIndex += 1

                                yIndex += 1
                                xIndex = xIt

                            # Reflecting Points over the y axis
                            for point in pointsBlocked:

                                if xIt - (point[0] - xIt) >= 0 <= point[1]:

                                    tilemap.add(fog, xIt - (point[0] - xIt), point[1])

                        # Wall is on the same X Value, above us
                        elif xIt == selfTile.x and yIt < selfTile.y:

                            pointsBlocked = []

                            equationRight = float(wallPosY / (wallPosX + 1))

                            yIndex = yIt - 1
                            xIndex = xIt

                            while yIndex >= 0:

                                # Tile directly above the wall, will always be blocked out
                                tilemap.add(fog, xIndex, yIndex)

                                xIndex += 1

                                # Incrementing along x axis until we reach the beginning tile of where the slope indexes
                                while xIndex < len(tilemap.tilemap[yIndex]) and (xIndex - posX) < \
                                        math.floor((((len(tilemap.tilemap) - 1) - yIndex) - posY) / equationRight):

                                    tilemap.add(fog, xIndex, yIndex)

                                    if xIndex != selfTile.x:
                                        pointsBlocked.append([xIndex, yIndex])

                                    xIndex += 1

                                floatOutput = (((len(tilemap.tilemap) - 1) - yIndex) - posY) / equationRight

                                if math.floor((floatOutput % 1) * 10) / 10 >= .5 and xIndex < len(tilemap.tilemap[yIndex]):

                                    tilemap.add(fog, xIndex, yIndex)

                                    if xIndex != selfTile.x:
                                        pointsBlocked.append([xIndex, yIndex])
                                   
                                # Adding points that may extend beyond the boundary of the tilemap
                                while (xIndex - posX) < math.floor(
                                        (((len(tilemap.tilemap) - 1) - yIndex) - posY) / equationRight):

                                    if xIndex != selfTile.x:
                                        pointsBlocked.append([xIndex, yIndex])

                                    xIndex += 1

                                yIndex -= 1
                                xIndex = xIt

                            # Reflecting Points over the y axis
                            for point in pointsBlocked:

                                if xIt - (point[0] - xIt) >= 0 <= point[1]:

                                    tilemap.add(fog, xIt - (point[0] - xIt), point[1])

                        # Wall is on the same Y Value, left of us
                        elif yIt == selfTile.y and xIt < selfTile.x:

                            pointsBlocked = []

                            # Top Half
                            equationTop = float((wallPosY + 1) / wallPosX)
                            equationBottom = 0

                            yIndex = yIt
                            xIndex = xIt - 1

                            while xIndex >= 0:

                                # Bottom Line
                                floatOutput = equationBottom * (xIndex - posX)

                                if math.floor((floatOutput % 1) * 10) / 10 <= .5:

                                    tilemap.add(fog, xIndex, yIndex)

                                    # We've already blocked out all points on the same Y value as us,
                                    # so we check if y is not equal to us, then add to the points blocked list

                                    if yIndex != selfTile.y:
                                        pointsBlocked.append([xIndex, yIndex])

                                yIndex -= 1

                                # Top Line
                                while yIndex >= 0 and ((len(tilemap.tilemap) - 1) - yIndex) - posY < math.floor(
                                        equationTop * (xIndex - posX)):

                                    tilemap.add(fog, xIndex, yIndex)
                                    if yIndex != selfTile.y:
                                        pointsBlocked.append([xIndex, yIndex])

                                    yIndex -= 1

                                # Adding points that may extend beyond the boundary of the tilemap.tilemap
                                while ((len(tilemap.tilemap) - 1) - yIndex) - posY < math.floor(
                                        equationTop * (xIndex - posX)):

                                    if yIndex != selfTile.y:
                                        pointsBlocked.append([xIndex, yIndex])
                                    yIndex -= 1

                                floatOutput = equationTop * (xIndex - posX)

                                if math.floor((floatOutput % 1) * 10) / 10 >= .5 and yIndex >= 0:

                                    tilemap.add(fog, xIndex, yIndex)

                                    if yIndex != selfTile.y:
                                        pointsBlocked.append([xIndex, yIndex])

                                xIndex -= 1
                                yIndex = (len(tilemap.tilemap) - 1) - math.floor(
                                    equationBottom * (xIndex - posX) + posY)

                                if yIndex < 0:
                                    break

                            # Reflecting over the x axis
                            for point in pointsBlocked:

                                if point[1] < 0:

                                    if (selfTile.y * 2) + abs(point[1]) < len(tilemap.tilemap):

                                        tilemap.add(fog, point[0], (selfTile.y * 2) + abs(point[1]))

                                else:

                                    if (selfTile.y + (selfTile.y - point[1])) < len(tilemap.tilemap):

                                        tilemap.add(fog, point[0], selfTile.y + (selfTile.y - point[1]))

                        # Wall is on the same Y Value, right of us
                        elif yIt == selfTile.y and xIt > selfTile.x:

                            pointsBlocked = []

                            # Top Half
                            equationTop = float((wallPosY + 1) / wallPosX)
                            equationBottom = 0

                            yIndex = yIt
                            xIndex = xIt + 1

                            while xIndex < len(tilemap.tilemap[yIndex]):

                                # Bottom Line
                                floatOutput = equationBottom * (xIndex - posX)

                                if math.floor((floatOutput % 1) * 10) / 10 <= .5:

                                    tilemap.add(fog, xIndex, yIndex)

                                    # We've already blocked out all points on the same Y value as us,
                                    # so we check if y is not equal to us, then add to the points blocked list

                                    if yIndex != selfTile.y:
                                        pointsBlocked.append([xIndex, yIndex])

                                yIndex -= 1

                                # Top Line
                                while yIndex >= 0 and (
                                        (len(tilemap.tilemap) - 1) - yIndex) - posY < math.floor(
                                        equationTop * (xIndex - posX)):

                                    tilemap.add(fog, xIndex, yIndex)
                                    if yIndex != selfTile.y:
                                        pointsBlocked.append([xIndex, yIndex])

                                    yIndex -= 1

                                # Adding points that may extend beyond the boundary of the tilemap.tilemap
                                while ((len(tilemap.tilemap) - 1) - yIndex) - posY < math.floor(
                                        equationTop * (xIndex - posX)):

                                    if yIndex != selfTile.y:
                                        pointsBlocked.append([xIndex, yIndex])
                                    yIndex -= 1

                                floatOutput = equationTop * (xIndex - posX)

                                if math.floor((floatOutput % 1) * 10) / 10 >= .5 and yIndex >= 0:

                                    tilemap.add(fog, xIndex, yIndex)

                                    if yIndex != selfTile.y:
                                        pointsBlocked.append([xIndex, yIndex])

                                xIndex += 1
                                yIndex = (len(tilemap.tilemap) - 1) - math.floor(
                                    equationBottom * (xIndex - posX) + posY)
                                if yIndex < 0:
                                    break

                            # Reflecting over the x axis
                            for point in pointsBlocked:

                                if point[1] < 0:

                                    if (selfTile.y * 2) + abs(point[1]) < len(tilemap.tilemap):

                                        tilemap.add(fog, point[0], (selfTile.y * 2) + abs(point[1]))

                                else:

                                    if (selfTile.y + (selfTile.y - point[1])) < len(tilemap.tilemap):

                                        tilemap.add(fog, point[0], selfTile.y + (selfTile.y - point[1]))

                        # Wall is in Quadrant 1
                        elif xIt >= selfTile.x and yIt <= selfTile.y:

                            if tilemap._bound_check(xIt - 1, yIt) and xIt - 1 == selfTile.x:

                                for tile in tilemap.get(xIt - 1, yIt):

                                    if isinstance(tile.obj, Wall):

                                        toTop = True
                                        break

                            # If toTop is False, run like normal
                            if not toTop:

                                equationTop = float((wallPosY + 1) / wallPosX)
                                equationBottom = float(wallPosY / (wallPosX + 1))

                                if xIt == selfTile.x + 1:

                                    yIndex = yIt - 1
                                    xIndex = xIt

                                    for x in range(selfTile.y - yIt):

                                        if yIndex < 0: break

                                        tilemap.add(fog, xIndex, yIndex)
                                        yIndex -= 1

                                yIndex = yIt
                                xIndex = xIt + 1

                                # Checking if the bottom slope is greater than 1.0
                                if equationBottom >= 1.0:

                                    # Reassigning the bottom slope so that it's angled slightly more above the wall
                                    equationBottom = float((wallPosY + 1) / (wallPosX + 1))
                                    # Reassigning the yIndex to match where the new slope starts
                                    yIndex = yIt - 1

                                # Checking if the top slope is greater than 1.0
                                if equationTop > 1.0:

                                    checkTop = True

                                    # Reassigning the top slope so that it's angled more above the wall
                                    equationTop = float((wallPosY + 2) / wallPosX)

                                    # Reassigning the xIndex to allow the equation to check the x tile we start on
                                    xIndex = xIt

                                    if equationBottom < 1.0:
                                        # Reassigning the yIndex to start above the wall, and not on top of it
                                        yIndex = yIt - 1

                                if checkTop:

                                    # Top of Wall
                                    while ((len(tilemap.tilemap) - 1) - yIndex) - posY < math.floor(
                                            equationTop * (xIndex - posX)) and yIndex >= 0:

                                        tilemap.add(fog, xIndex, yIndex)
                                        yIndex -= 1

                                    floatOutput = equationTop * (xIndex - posX)

                                    if math.floor((floatOutput % 1) * 10) / 10 >= .5 and math.floor(
                                            (floatOutput % 1) * 10) / 10 != 0.0:

                                        if yIndex >= 0:

                                            tilemap.add(fog, xIndex, yIndex)

                                    xIndex += 1
                                    yIndex = (len(tilemap.tilemap) - 1) - (
                                            math.floor(equationBottom * (xIndex - posX)) + posY)

                                # BottomLine
                                while xIndex < len(tilemap.tilemap[yIndex]) and yIndex >= 0:

                                    # Bottom Line
                                    floatOutput = equationBottom * (xIndex - posX)

                                    if math.floor((floatOutput % 1) * 10) / 10 <= .5:

                                        foundWall = False

                                        for obj in tilemap.tilemap[yIndex][xIndex]:

                                            if isinstance(obj, Wall):

                                                foundWall = True

                                        if not foundWall:

                                            tilemap.add(fog, xIndex, yIndex)

                                    yIndex -= 1
                                    # Top Line

                                    while yIndex >= 0 and ((len(tilemap.tilemap) - 1) - yIndex) - posY < math.floor(
                                            equationTop * (xIndex - posX)):
                                        tilemap.add(fog, xIndex, yIndex)

                                        yIndex -= 1

                                    floatOutput = equationTop * (xIndex - posX)

                                    if math.floor((floatOutput % 1) * 10) / 10 >= .5 and yIndex >= 0:
                                        tilemap.add(fog, xIndex, yIndex)

                                    xIndex += 1
                                    yIndex = (len(tilemap.tilemap) - 1) - math.floor(
                                        equationBottom * (xIndex - posX) + posY)
                                    if yIndex < 0:
                                        break

                            # If toTop is True, fill fog to the top of the screen
                            else:

                                toTop = False

                                equationBottom = float(wallPosY / (wallPosX + 1))

                                yIndex = yIt - 1
                                xIndex = xIt

                                while yIndex >= 0:

                                    tilemap.add(fog, xIndex, yIndex)
                                    yIndex -= 1

                                yIndex = yIt
                                xIndex = xIt + 1

                                # Checking if the bottom slope is greater than 1.0
                                if equationBottom >= 1.0:
                                    # Reassigning the bottom slope so that it's angled slightly more above the wall
                                    equationBottom = float((wallPosY + 1) / (wallPosX + 1))
                                    # Reassigning the yIndex to match where the new slope starts
                                    yIndex = yIt - 1

                                # BottomLine
                                while xIndex < len(tilemap.tilemap[yIndex]) and yIndex >= 0:

                                    # Bottom Line
                                    floatOutput = equationBottom * (xIndex - posX)

                                    if math.floor((floatOutput % 1) * 10) / 10 <= .5:

                                        foundWall = False

                                        for tile in tilemap.get(xIndex, yIndex):

                                            if isinstance(tile.obj, Wall):
                                                foundWall = True

                                        if not foundWall:
                                            tilemap.add(fog, xIndex, yIndex)

                                    yIndex -= 1

                                    # Top Line
                                    while yIndex >= 0:

                                        tilemap.add(fog, xIndex, yIndex)

                                        yIndex -= 1

                                    xIndex += 1
                                    yIndex = (len(tilemap.tilemap) - 1) - math.floor(
                                        equationBottom * (xIndex - posX) + posY)

                                    if yIndex < 0:
                                        break

                        # Wall is in Quadrant 2
                        elif xIt <= selfTile.x and yIt <= selfTile.y:

                            if tilemap._bound_check(xIt + 1, yIt) and xIt + 1 == selfTile.x:

                                for tile in tilemap.get(xIt + 1, yIt):

                                    if isinstance(tile.obj, Wall):

                                        toTop = True

                                        break

                            pointsBlocked = []

                            if not toTop:

                                posX -= (wallPosX * 2) * -1

                                wallPosX = abs(wallPosX)
                                wallPosY = abs(wallPosY)

                                equationTop = float((wallPosY + 1) / wallPosX)
                                equationBottom = float(wallPosY / (wallPosX + 1))

                                if xIt == selfTile.x - 1:

                                    yIndex = yIt - 1
                                    xIndex = xIt

                                    for x in range(selfTile.y - yIt):

                                        if yIndex < 0: break

                                        tilemap.add(fog, xIndex, yIndex)
                                        yIndex -= 1

                                yIndex = yIt
                                xIndex = xIt + 1

                                # Checking if the bottom slope is greater than 1.0

                                if equationBottom >= 1.0:

                                    # Reassigning the bottom slope so that it's angled slightly more above the wall
                                    equationBottom = float((wallPosY + 1) / (wallPosX + 1))
                                    # Reassigning the yIndex to match where the new slope starts
                                    yIndex = yIt - 1

                                # Checking if the top slope is greater than 1.0
                                if equationTop > 1.0:

                                    checkTop = True

                                    # Reassigning the top slope so that it's angled more above the wall
                                    equationTop = float((wallPosY + 2) / wallPosX)

                                    # Reassigning the xIndex to allow the equation to check the x tile we start on
                                    xIndex = xIt

                                    if equationBottom < 1.0:
                                        # Reassigning the yIndex to start above the wall, and not on top of it
                                        yIndex = yIt - 1

                                if checkTop:

                                    # Top of Wall
                                    while ((len(tilemap.tilemap) - 1) - yIndex) - posY < math.floor(
                                            equationTop * (xIndex - posX)) and yIndex >= 0:
                                        pointsBlocked.append([xIndex, yIndex])
                                        yIndex -= 1

                                    floatOutput = equationTop * (xIndex - posX)

                                    if math.floor((floatOutput % 1) * 10) / 10 >= .5 and math.floor(
                                            (floatOutput % 1) * 10) / 10 != 0.0:

                                        if yIndex >= 0:
                                            pointsBlocked.append([xIndex, yIndex])

                                    xIndex += 1
                                    yIndex = (len(tilemap.tilemap) - 1) - (
                                            math.floor(equationBottom * (xIndex - posX)) + posY)

                                # BottomLine
                                while xIndex <= xIt * 2:

                                    # Bottom Line
                                    floatOutput = equationBottom * (xIndex - posX)

                                    if math.floor((floatOutput % 1) * 10) / 10 <= .5 and yIndex >= 0:

                                        foundWall = False

                                        for obj in tilemap.tilemap[yIndex][xIt - (xIndex - xIt)]:

                                            if isinstance(obj, Wall):
                                                foundWall = True

                                        if not foundWall:

                                            pointsBlocked.append([xIndex, yIndex])

                                    yIndex -= 1
                                    # Top Line

                                    while ((len(tilemap.tilemap) - 1) - yIndex) - posY < math.floor(
                                            equationTop * (xIndex - posX)) and yIndex >= 0:
                                        pointsBlocked.append([xIndex, yIndex])

                                        yIndex -= 1

                                    floatOutput = equationTop * (xIndex - posX)

                                    if math.floor((floatOutput % 1) * 10) / 10 >= .5 and yIndex >= 0:
                                        pointsBlocked.append([xIndex, yIndex])

                                    xIndex += 1
                                    yIndex = (len(tilemap.tilemap) - 1) - math.floor(
                                        equationBottom * (xIndex - posX) + posY)

                            else:

                                posX -= (wallPosX * 2) * -1

                                wallPosX = abs(wallPosX)
                                wallPosY = abs(wallPosY)

                                equationBottom = float(wallPosY / (wallPosX + 1))

                                yIndex = yIt - 1

                                xIndex = xIt

                                while yIndex >= 0:

                                    tilemap.add(fog, xIndex, yIndex)

                                    yIndex -= 1

                                yIndex = yIt

                                xIndex = xIt + 1

                                # Checking if the bottom slope is greater than 1.0

                                if equationBottom >= 1.0:
                                    # Reassigning the bottom slope so that it's angled slightly more above the wall

                                    equationBottom = float((wallPosY + 1) / (wallPosX + 1))

                                    # Reassigning the yIndex to match where the new slope starts

                                    yIndex = yIt - 1

                                # BottomLine

                                while xIndex <= xIt * 2:

                                    # Bottom Line

                                    floatOutput = equationBottom * (xIndex - posX)

                                    if math.floor((floatOutput % 1) * 10) / 10 <= .5:

                                        foundWall = False

                                        for tile in tilemap.get(xIt - (xIndex - xIt), yIndex):

                                            if isinstance(tile.obj, Wall):
                                                foundWall = True

                                        if not foundWall:

                                            pointsBlocked.append([xIndex, yIndex])

                                    yIndex -= 1

                                    # Top Line

                                    while yIndex >= 0:

                                        pointsBlocked.append([xIndex, yIndex])

                                        yIndex -= 1


                                    xIndex += 1

                                    yIndex = (len(tilemap.tilemap) - 1) - math.floor(

                                        equationBottom * (xIndex - posX) + posY)

                                    if yIndex < 0:
                                        break

                            # Reflecting points to the other side of the wall
                            for point in pointsBlocked:

                                if 0 <= point[1] < len(tilemap.tilemap) and len(tilemap.tilemap[point[1]]) > xIt - (
                                        point[0] - xIt) >= 0:

                                    tilemap.add(fog, xIt - (point[0] - xIt), point[1])

                        # Wall is in Quadrant 3
                        elif xIt <= selfTile.x and yIt >= selfTile.y:

                            if tilemap._bound_check(xIt + 1, yIt) and xIt + 1 == selfTile.x:

                                for tile in tilemap.get(xIt + 1, yIt):

                                    if isinstance(tile.obj, Wall):

                                        toTop = True

                                        break

                            pointsBlocked = []

                            if not toTop:

                                posY -= (wallPosY * 2) * -1
                                posX -= (wallPosX * 2) * -1

                                wallPosX = abs(wallPosX)
                                wallPosY = abs(wallPosY)

                                equationTop = float((wallPosY + 1) / wallPosX)
                                equationBottom = float(wallPosY / (wallPosX + 1))

                                if xIt == selfTile.x - 1:

                                    yIndex = yIt + 1
                                    xIndex = xIt

                                    for x in range(yIt - selfTile.y):

                                        if yIndex >= len(tilemap.tilemap): break

                                        tilemap.add(fog, xIndex, yIndex)
                                        yIndex += 1

                                yIndex = yIt
                                xIndex = xIt + 1

                                # Checking if the bottom slope is greater than 1.0

                                if equationBottom >= 1.0:

                                    # Reassigning the bottom slope so that it's angled slightly more above the wall
                                    equationBottom = float((wallPosY + 1) / (wallPosX + 1))
                                    # Reassigning the yIndex to match where the new slope starts
                                    yIndex = yIt - 1

                                # Checking if the top slope is greater than 1.0
                                if equationTop > 1.0:

                                    checkTop = True

                                    # Reassigning the top slope so that it's angled more above the wall
                                    equationTop = float((wallPosY + 2) / wallPosX)

                                    # Reassigning the xIndex to allow the equation to check the x tile we start on
                                    xIndex = xIt

                                    if equationBottom < 1.0:
                                        # Reassigning the yIndex to start above the wall, and not on top of it
                                        yIndex = yIt - 1

                                if checkTop:

                                    # Top of Wall
                                    while ((len(tilemap.tilemap) - 1) - yIndex) - posY < math.floor(
                                            equationTop * (xIndex - posX)) and yIndex >= 0:
                                        pointsBlocked.append([xIndex, yIndex])
                                        yIndex -= 1

                                    floatOutput = equationTop * (xIndex - posX)

                                    if math.floor((floatOutput % 1) * 10) / 10 >= .5 and math.floor(
                                            (floatOutput % 1) * 10) / 10 != 0.0:

                                        if yIndex >= 0:
                                            pointsBlocked.append([xIndex, yIndex])

                                    xIndex += 1
                                    yIndex = (len(tilemap.tilemap) - 1) - (
                                            math.floor(equationBottom * (xIndex - posX)) + posY)

                                # BottomLine
                                while xIndex <= xIt * 2:

                                    if yIndex < 0:

                                        if yIt + abs(yIndex) >= len(tilemap.tilemap) - yIt:
                                            xIndex += 1
                                            yIndex = (len(tilemap.tilemap) - 1) - math.floor(
                                                equationBottom * (xIndex - posX) + posY)
                                            continue

                                    else:

                                        if yIt + (yIt - yIndex) >= len(tilemap.tilemap):
                                            xIndex += 1
                                            yIndex = (len(tilemap.tilemap) - 1) - math.floor(
                                                equationBottom * (xIndex - posX) + posY)
                                            continue

                                    # Bottom Line
                                    floatOutput = equationBottom * (xIndex - posX)

                                    if math.floor((floatOutput % 1) * 10) / 10 <= .5:

                                        foundWall = False

                                        for obj in tilemap.tilemap[yIt + (yIt - yIndex)][xIt - (xIndex - xIt)]:

                                            if isinstance(obj, Wall):
                                                foundWall = True

                                        if not foundWall:
                                            pointsBlocked.append([xIndex, yIndex])

                                    yIndex -= 1
                                    # Top Line

                                    while ((len(tilemap.tilemap) - 1) - yIndex) - posY < math.floor(
                                            equationTop * (xIndex - posX)):

                                        if yIndex < 0:

                                            if yIt + abs(yIndex) >= len(tilemap.tilemap) - yIt:
                                                break

                                        else:

                                            if yIt + (yIt - yIndex) >= len(tilemap.tilemap):
                                                break

                                        pointsBlocked.append([xIndex, yIndex])

                                        yIndex -= 1

                                    floatOutput = equationTop * (xIndex - posX)

                                    if yIndex < 0:

                                        if yIt + abs(yIndex) >= len(tilemap.tilemap) - yIt:
                                            xIndex += 1
                                            yIndex = (len(tilemap.tilemap) - 1) - math.floor(
                                                equationBottom * (xIndex - posX) + posY)
                                            continue

                                    else:

                                        if yIt + (yIt - yIndex) >= len(tilemap.tilemap):
                                            xIndex += 1
                                            yIndex = (len(tilemap.tilemap) - 1) - math.floor(
                                                equationBottom * (xIndex - posX) + posY)
                                            continue

                                    if math.floor((floatOutput % 1) * 10) / 10 >= .5 and yIndex >= 0:
                                        pointsBlocked.append([xIndex, yIndex])

                                    xIndex += 1
                                    yIndex = (len(tilemap.tilemap) - 1) - math.floor(
                                        equationBottom * (xIndex - posX) + posY)

                            else:

                                posY -= (wallPosY * 2) * -1
                                posX -= (wallPosX * 2) * -1

                                wallPosX = abs(wallPosX)
                                wallPosY = abs(wallPosY)

                                equationBottom = float(wallPosY / (wallPosX + 1))

                                yIndex = yIt + 1
                                xIndex = xIt

                                while yIndex < tilemap.height:

                                    tilemap.add(fog, xIndex, yIndex)

                                    yIndex += 1

                                yIndex = yIt
                                xIndex = xIt + 1

                                # Checking if the bottom slope is greater than 1.0

                                if equationBottom >= 1.0:

                                    # Reassigning the bottom slope so that it's angled slightly more above the wall
                                    equationBottom = float((wallPosY + 1) / (wallPosX + 1))
                                    # Reassigning the yIndex to match where the new slope starts
                                    yIndex = yIt - 1

                                # BottomLine
                                while xIndex <= xIt * 2 and yIt + (yIt - yIndex) < tilemap.height:

                                    # Bottom Line
                                    floatOutput = equationBottom * (xIndex - posX)

                                    if math.floor((floatOutput % 1) * 10) / 10 <= .5:

                                        foundWall = False

                                        for obj in tilemap.tilemap[yIt + (yIt - yIndex)][xIt - (xIndex - xIt)]:

                                            if isinstance(obj, Wall):
                                                foundWall = True

                                        if not foundWall:
                                            pointsBlocked.append([xIndex, yIndex])

                                    yIndex -= 1
                                    # Top Line

                                    while yIndex >= yIt - (tilemap.height - yIt):

                                        pointsBlocked.append([xIndex, yIndex])

                                        yIndex -= 1

                                    xIndex += 1
                                    yIndex = (len(tilemap.tilemap) - 1) - math.floor(
                                        equationBottom * (xIndex - posX) + posY)

                                    if yIndex <= yIt - (tilemap.height - yIt):

                                        if yIt + (yIt + abs(yIndex)) >= tilemap.height:

                                            break

                            # Reflecting points to the other side of the wall
                            for point in pointsBlocked:

                                if 0 <= point[1] < len(tilemap.tilemap):

                                    if yIt + (yIt - point[1]) < len(tilemap.tilemap):

                                        tilemap.add(fog, xIt - (point[0] - xIt), yIt + (yIt - point[1]))

                                elif point[1] < 0:

                                    if yIt + (yIt + abs(point[1])) < len(tilemap.tilemap):

                                        tilemap.add(fog, xIt - (point[0] - xIt), yIt + (yIt + abs(point[1])))

                        # Wall is in Quadrant 4
                        elif xIt >= selfTile.x and yIt >= selfTile.y:

                            if tilemap._bound_check(xIt - 1, yIt) and xIt - 1 == selfTile.x:

                                for tile in tilemap.get(xIt - 1, yIt):

                                    if isinstance(tile.obj, Wall):

                                        toTop = True

                                        break

                            pointsBlocked = []

                            if not toTop:

                                pointsBlocked = []

                                posY -= abs(wallPosY * 2)

                                wallPosX = abs(wallPosX)
                                wallPosY = abs(wallPosY)

                                equationTop = float((wallPosY + 1) / wallPosX)
                                equationBottom = float(wallPosY / (wallPosX + 1))

                                if xIt == selfTile.x + 1:

                                    yIndex = yIt + 1
                                    xIndex = xIt

                                    for x in range(yIt - selfTile.y):

                                        if yIndex >= len(tilemap.tilemap): break

                                        tilemap.add(fog, xIndex, yIndex)
                                        yIndex += 1

                                yIndex = yIt
                                xIndex = xIt + 1

                                # Checking if the bottom slope is greater than 1.0

                                if equationBottom >= 1.0:

                                    # Reassigning the bottom slope so that it's angled slightly more above the wall
                                    equationBottom = float((wallPosY + 1) / (wallPosX + 1))
                                    # Reassigning the yIndex to match where the new slope starts
                                    yIndex = yIt - 1

                                # Checking if the top slope is greater than 1.0
                                if equationTop > 1.0:

                                    checkTop = True

                                    # Reassigning the top slope so that it's angled more above the wall
                                    equationTop = float((wallPosY + 2) / wallPosX)

                                    # Reassigning the xIndex to allow the equation to check the x tile we start on
                                    xIndex = xIt

                                    if equationBottom < 1.0:
                                        # Reassigning the yIndex to start above the wall, and not on top of it
                                        yIndex = yIt - 1

                                if checkTop:

                                    # Top of Wall
                                    while ((len(tilemap.tilemap) - 1) - yIndex) - posY < math.floor(
                                            equationTop * (xIndex - posX)) and yIndex >= 0:
                                        pointsBlocked.append([xIndex, yIndex])
                                        yIndex -= 1

                                    floatOutput = equationTop * (xIndex - posX)

                                    if math.floor((floatOutput % 1) * 10) / 10 >= .5 and math.floor(
                                            (floatOutput % 1) * 10) / 10 != 0.0:

                                        if yIndex >= 0:
                                            pointsBlocked.append([xIndex, yIndex])

                                    xIndex += 1
                                    yIndex = (len(tilemap.tilemap) - 1) - (
                                            math.floor(equationBottom * (xIndex - posX)) + posY)

                                # BottomLine
                                while xIndex < len(tilemap.tilemap[yIt]):

                                    if yIndex < 0:

                                        if yIt + abs(yIndex) >= len(tilemap.tilemap) - yIt:
                                            xIndex += 1
                                            yIndex = (len(tilemap.tilemap) - 1) - math.floor(
                                                equationBottom * (xIndex - posX) + posY)
                                            continue

                                    else:

                                        if yIt + (yIt - yIndex) >= len(tilemap.tilemap):
                                            xIndex += 1
                                            yIndex = (len(tilemap.tilemap) - 1) - math.floor(
                                                equationBottom * (xIndex - posX) + posY)
                                            continue

                                    # Bottom Line
                                    floatOutput = equationBottom * (xIndex - posX)

                                    if math.floor((floatOutput % 1) * 10) / 10 <= .5:

                                        foundWall = False

                                        for obj in tilemap.tilemap[yIt + (yIt - yIndex)][xIndex]:

                                            if isinstance(obj, Wall):
                                                foundWall = True

                                        if not foundWall:
                                            pointsBlocked.append([xIndex, yIndex])

                                    yIndex -= 1
                                    # Top Line

                                    while ((len(tilemap.tilemap) - 1) - yIndex) - posY < math.floor(
                                            equationTop * (xIndex - posX)):

                                        if yIndex < 0:

                                            if yIt + abs(yIndex) >= len(tilemap.tilemap) - yIt:
                                                break

                                        else:

                                            if yIt + (yIt - yIndex) >= len(tilemap.tilemap):
                                                break

                                        pointsBlocked.append([xIndex, yIndex])

                                        yIndex -= 1

                                    floatOutput = equationTop * (xIndex - posX)

                                    if yIndex < 0:

                                        if yIt + abs(yIndex) >= len(tilemap.tilemap) - yIt:
                                            xIndex += 1
                                            yIndex = (len(tilemap.tilemap) - 1) - math.floor(
                                                equationBottom * (xIndex - posX) + posY)
                                            continue

                                    else:

                                        if yIt + (yIt - yIndex) >= len(tilemap.tilemap):
                                            xIndex += 1
                                            yIndex = (len(tilemap.tilemap) - 1) - math.floor(
                                                equationBottom * (xIndex - posX) + posY)
                                            continue

                                    if math.floor((floatOutput % 1) * 10) / 10 >= .5 and yIndex >= 0:
                                        pointsBlocked.append([xIndex, yIndex])

                                    xIndex += 1
                                    yIndex = (len(tilemap.tilemap) - 1) - math.floor(
                                        equationBottom * (xIndex - posX) + posY)

                            else:

                                posY -= abs(wallPosY * 2)

                                wallPosX = abs(wallPosX)
                                wallPosY = abs(wallPosY)

                                equationBottom = float(wallPosY / (wallPosX + 1))

                                yIndex = yIt + 1
                                xIndex = xIt

                                while yIndex < tilemap.height:

                                    tilemap.add(fog, xIndex, yIndex)

                                    yIndex += 1

                                yIndex = yIt
                                xIndex = xIt + 1

                                # Checking if the bottom slope is greater than 1.0

                                if equationBottom >= 1.0:

                                    # Reassigning the bottom slope so that it's angled slightly more above the wall
                                    equationBottom = float((wallPosY + 1) / (wallPosX + 1))
                                    # Reassigning the yIndex to match where the new slope starts
                                    yIndex = yIt - 1

                                # BottomLine
                                while xIndex < tilemap.width and yIt + (yIt - yIndex) < tilemap.height:

                                    # Bottom Line
                                    floatOutput = equationBottom * (xIndex - posX)

                                    if math.floor((floatOutput % 1) * 10) / 10 <= .5:

                                        foundWall = False

                                        for obj in tilemap.tilemap[yIt + (yIt - yIndex)][xIndex]:

                                            if isinstance(obj, Wall):
                                                foundWall = True

                                        if not foundWall:
                                            pointsBlocked.append([xIndex, yIndex])

                                    yIndex -= 1
                                    # Top Line

                                    while yIndex >= yIt - (tilemap.height - yIt):

                                        pointsBlocked.append([xIndex, yIndex])

                                        yIndex -= 1

                                    xIndex += 1
                                    yIndex = (len(tilemap.tilemap) - 1) - math.floor(
                                        equationBottom * (xIndex - posX) + posY)

                                    if yIndex <= yIt - (tilemap.height - yIt):

                                        if yIt + (yIt + abs(yIndex)) >= tilemap.height:

                                            break

                            # Reflecting points to the other side of the wall
                            for point in pointsBlocked:

                                if point[0] >= 0 and len(tilemap.tilemap) > yIt + (yIt - point[1]) >= 0:

                                    tilemap.add(fog, point[0], yIt + (yIt - point[1]))

                        break

                xIt += 1

            xIt = 0
            yIt += 1

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

    def find_quickest_path(self, targObj, blocked=False):

        selfTile = self.tilemap.find_object(self)
        limit = 0
        count = 0

        if type(targObj) is list:

            startPosX = targObj[0][0]
            startPosY = targObj[0][1]
            limit = targObj[1]

        else:

            startPosX = targObj.x
            startPosY = targObj.y

        numberTileMap = []

        surroundingTiles = {}

        '''
        # Finding number of tiles we can fill
        for line in self.tilemap.tilemap:

            for col in line:

                for tile in col:

                    if not tile.can_traverse:

                        foundObstacle = True
                        break

                if foundObstacle:

                    foundObstacle = False
                    continue

                numMoves += 1
        '''

        x, y = 0, 0

        foundObstacle = False

        # Creating NumberTileMap
        if blocked:

            for y in range(self.tilemap.height):

                numberTileMap.append([])

                for x in range(self.tilemap.width):

                    numberTileMap[y].append(-1)

        else:

            for line in range(self.tilemap.height):

                numberTileMap.append([])

                for col in range(self.tilemap.width):

                    for tile in self.tilemap.get(x, y):

                        if not tile.obj.can_traverse and not isinstance(tile.obj, Enemy):

                            numberTileMap[line].append(-2)
                            foundObstacle = True
                            break

                    if foundObstacle:

                        foundObstacle = False
                        x += 1
                        continue

                    numberTileMap[line].append(-1)

                    x += 1

                x = 0
                y += 1

        numberCoords = {}
        numberCoords.clear()

        # Dictionary for the position of each number
        numberCoords = {0: [startPosX, startPosY]}

        # Number we are cycling around
        currentNum = 0

        # Next number we iterate to cycle around
        nextNum = 1

        # X position of the number we are cycling around
        currentX = numberCoords[0][0]
        # Y position of the number we are cycling around
        currentY = numberCoords[0][1]

        if not blocked:

            # '''
            # Printing tilemap------------------------------------------------------------------
            print("\n" * 2)
            for line in numberTileMap:

                for col in line:

                    if len(str(col)) == 1:
                        print(str(col) + "   ", end="")

                    elif len(str(col)) == 2:
                        print(str(col) + "  ", end="")

                    elif len(str(col)) == 3:
                        print(str(col) + " ", end="")

                print("\n")
            # -----------------------------------------------------------------------------
            # '''

            # If Enemy is left of the target
            if selfTile.x <= startPosX:

                numberTileMap[currentY][currentX] = currentNum

                while True:

                    if currentX - 1 != selfTile.x or currentY != selfTile.y:

                        # Check Left
                        if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:
                            numberTileMap[currentY][currentX - 1] = nextNum
                            numberCoords[nextNum] = [currentX - 1, currentY]
                            nextNum += 1

                    else:

                        break

                    # Check Down Left
                    if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][
                        currentX - 1] == -1:
                        numberTileMap[currentY + 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY + 1]
                        nextNum += 1

                    # Check Down
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:
                        numberTileMap[currentY + 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY + 1]
                        nextNum += 1

                    # Check Down Right
                    if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][
                        currentX + 1] == -1:
                        numberTileMap[currentY + 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY + 1]
                        nextNum += 1

                    # Check Right
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:
                        numberTileMap[currentY][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY]
                        nextNum += 1

                    # Check Right Up
                    if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][
                        currentX + 1] == -1:
                        numberTileMap[currentY - 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY - 1]
                        nextNum += 1

                    # Check Up
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:
                        numberTileMap[currentY - 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY - 1]
                        nextNum += 1

                    # Check Left Up
                    if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][
                        currentX - 1] == -1:

                        numberTileMap[currentY - 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY - 1]
                        nextNum += 1

                    currentNum += 1
                    currentX = numberCoords[currentNum][0]
                    currentY = numberCoords[currentNum][1]

                    if currentNum == nextNum - 1:

                        break

            # If Enemy is right of the target
            elif selfTile.x >= startPosX:

                numberTileMap[currentY][currentX] = currentNum

                while True:

                    if currentX + 1 != selfTile.x or currentY != selfTile.y:

                        # Check Right
                        if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:
                            numberTileMap[currentY][currentX + 1] = nextNum
                            numberCoords[nextNum] = [currentX + 1, currentY]
                            nextNum += 1

                    else:

                        break

                    # Check Right Up
                    if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][
                        currentX + 1] == -1:
                        numberTileMap[currentY - 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY - 1]
                        nextNum += 1

                    # Check Up
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:
                        numberTileMap[currentY - 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY - 1]
                        nextNum += 1

                    # Check Left Up
                    if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][
                        currentX - 1] == -1:
                        numberTileMap[currentY - 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY - 1]
                        nextNum += 1

                    # Check Left
                    if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:
                        numberTileMap[currentY][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY]
                        nextNum += 1

                    # Check Down Left
                    if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][
                        currentX - 1] == -1:
                        numberTileMap[currentY + 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY + 1]
                        nextNum += 1

                    # Check Down
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:
                        numberTileMap[currentY + 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY + 1]
                        nextNum += 1

                    # Check Down Right
                    if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][currentX + 1] == -1:
                        numberTileMap[currentY + 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY + 1]
                        nextNum += 1

                    currentNum += 1
                    currentX = numberCoords[currentNum][0]
                    currentY = numberCoords[currentNum][1]

                    if currentNum == nextNum - 1:

                        break

        else:

            # If Enemy is above target
            if selfTile.y < startPosY and selfTile.x == startPosX:

                numberTileMap[currentY][currentX] = currentNum

                while True:

                    # Check Up
                    if self.check_tile(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                        numberTileMap[currentY - 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY - 1]
                        nextNum += 1

                        if self.check_tile(currentX, currentY - 1):

                            count += 1

                            if count == limit:

                                break

                    # Check Left Up
                    if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                        numberTileMap[currentY - 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY - 1]
                        nextNum += 1

                        if self.check_tile(currentX - 1, currentY - 1):

                            count += 1

                            if count == limit:

                                break

                    # Check Left
                    if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:

                        numberTileMap[currentY][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY]
                        nextNum += 1
                        if self.check_tile(currentX - 1, currentY):

                            count += 1

                            if count == limit:

                                break

                    # Check Down Left
                    if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][currentX - 1] == -1:

                        numberTileMap[currentY + 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY + 1]
                        nextNum += 1

                        if self.check_tile(currentX - 1, currentY + 1):

                            count += 1

                            if count == limit:

                                break

                    # Check Down
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:

                        numberTileMap[currentY + 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY + 1]
                        nextNum += 1

                        if self.check_tile(currentX, currentY + 1):

                            count += 1

                            if count == limit:

                                break

                    # Check Down Right
                    if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][currentX + 1] == -1:

                        numberTileMap[currentY + 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY + 1]
                        nextNum += 1

                        if self.check_tile(currentX + 1, currentY + 1):

                            count += 1

                            if count == limit:

                                break

                    # Check Right
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:

                        numberTileMap[currentY][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY]
                        nextNum += 1

                        if self.check_tile(currentX + 1, currentY):

                            count += 1

                            if count == limit:

                                break

                    # Check Right Up
                    if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][currentX + 1] == -1:

                        numberTileMap[currentY - 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY - 1]
                        nextNum += 1

                        if self.check_tile(currentX + 1, currentY - 1):

                            count += 1

                            if count == limit:

                                break

                    currentNum += 1
                    currentX = numberCoords[currentNum][0]
                    currentY = numberCoords[currentNum][1]

                surroundingTiles = self.find_quickest_path([numberCoords[nextNum - 1], 0], blocked=False)

                if len(surroundingTiles) > 0:

                    return surroundingTiles

            # If Enemy is left above the target
            elif selfTile.y < startPosY and selfTile.x < startPosX:

                numberTileMap[currentY][currentX] = currentNum

                while True:

                    if currentX - 1 != selfTile.x or currentY - 1 != selfTile.y:

                        # Check Left Up
                        if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][currentX - 1] == -1:

                            numberTileMap[currentY - 1][currentX - 1] = nextNum
                            numberCoords[nextNum] = [currentX - 1, currentY - 1]
                            nextNum += 1

                    else:

                        break

                    # Check Left
                    if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:

                        if currentY == selfTile.y and currentX - 1 == selfTile.x:

                            break

                        numberTileMap[currentY][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY]
                        # booleanTileMap[currentY][currentX - 1] = False
                        nextNum += 1

                    # Check Down Left
                    if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][currentX - 1] == -1:

                        if currentY + 1 == selfTile.y and currentX - 1 == selfTile.x:

                            break

                        numberTileMap[currentY + 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY + 1]
                        # booleanTileMap[currentY + 1][currentX - 1] = False
                        nextNum += 1

                    # Check Down
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:

                        if currentY + 1 == selfTile.y and currentX == selfTile.x:
                            break

                        numberTileMap[currentY + 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY + 1]
                        # booleanTileMap[currentY + 1][currentX] = False
                        nextNum += 1

                    # Check Down Right
                    if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][currentX + 1] == -1:

                        if currentY + 1 == selfTile.y and currentX + 1 == selfTile.x:

                            break

                        numberTileMap[currentY + 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY + 1]
                        # booleanTileMap[currentY + 1][currentX + 1] = False
                        nextNum += 1

                    # Check Right
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:

                        if currentY == selfTile.y and currentX + 1 == selfTile.x:
                            break

                        numberTileMap[currentY][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY]
                        # booleanTileMap[currentY][currentX + 1] = False
                        nextNum += 1

                    # Check Right Up
                    if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][currentX + 1] == -1:

                        if currentY - 1 == selfTile.y and currentX + 1 == selfTile.x:
                            break

                        numberTileMap[currentY - 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY - 1]
                        # booleanTileMap[currentY - 1][currentX + 1] = False
                        nextNum += 1

                    # Check Up
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                        if currentY - 1 == selfTile.y and currentX == selfTile.x:
                            break

                        numberTileMap[currentY - 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY - 1]
                        # booleanTileMap[currentY - 1][currentX] = False
                        nextNum += 1

                    currentNum += 1
                    currentX = numberCoords[currentNum][0]
                    currentY = numberCoords[currentNum][1]

                    if currentNum == nextNum - 1:

                        break

            # If Enemy is left of the target
            elif selfTile.y == startPosY and selfTile.x < startPosX:

                numberTileMap[currentY][currentX] = currentNum

                while True:

                    if currentX - 1 != selfTile.x or currentY != selfTile.y:

                        # Check Left
                        if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:

                            numberTileMap[currentY][currentX - 1] = nextNum
                            numberCoords[nextNum] = [currentX - 1, currentY]
                            nextNum += 1

                    else:

                        break

                    # Check Down Left
                    if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][currentX - 1] == 1:

                        numberTileMap[currentY + 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY + 1]
                        nextNum += 1

                    # Check Down
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:

                        numberTileMap[currentY + 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY + 1]
                        nextNum += 1

                    # Check Down Right
                    if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][currentX + 1] == -1:

                        numberTileMap[currentY + 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY + 1]
                        nextNum += 1

                    # Check Right
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:

                        numberTileMap[currentY][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY]
                        nextNum += 1

                    # Check Right Up
                    if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][currentX + 1] == -1:

                        numberTileMap[currentY - 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY - 1]
                        nextNum += 1

                    # Check Up
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                        numberTileMap[currentY - 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY - 1]
                        nextNum += 1

                    # Check Left Up
                    if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][currentX - 1] == -1:

                        numberTileMap[currentY - 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY - 1]
                        nextNum += 1

                    currentNum += 1
                    currentX = numberCoords[currentNum][0]
                    currentY = numberCoords[currentNum][1]

                    if currentNum == nextNum - 1:

                        break

            # If Enemy is left down of the target
            elif selfTile.y > startPosY and selfTile.x < startPosX:

                numberTileMap[currentY][currentX] = currentNum

                while True:

                    if currentX - 1 != selfTile.x or currentY + 1 != selfTile.y:

                        # Check Down Left
                        if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][currentX - 1] == -1:

                            numberTileMap[currentY + 1][currentX - 1] = nextNum
                            numberCoords[nextNum] = [currentX - 1, currentY + 1]
                            nextNum += 1

                    else:

                        break

                    # Check Down
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:

                        numberTileMap[currentY + 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY + 1]
                        nextNum += 1

                    # Check Down Right
                    if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][currentX + 1] == -1:

                        numberTileMap[currentY + 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY + 1]
                        nextNum += 1

                    # Check Right
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:

                        numberTileMap[currentY][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY]
                        nextNum += 1

                    # Check Right Up
                    if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][currentX + 1] == -1:

                        numberTileMap[currentY - 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY - 1]
                        nextNum += 1

                    # Check Up
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                        numberTileMap[currentY - 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY - 1]
                        nextNum += 1

                    # Check Left Up
                    if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][currentX - 1] == -1:

                        numberTileMap[currentY - 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY - 1]
                        nextNum += 1

                    # Check Left
                    if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:
                        numberTileMap[currentY][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY]
                        nextNum += 1

                    currentNum += 1
                    currentX = numberCoords[currentNum][0]
                    currentY = numberCoords[currentNum][1]

                    if currentNum == nextNum - 1:

                        break

            # If Enemy is down of the target
            elif selfTile.y > startPosY and selfTile.x == startPosX:

                numberTileMap[currentY][currentX] = currentNum

                while True:

                    if currentX != selfTile.x or currentY + 1 != selfTile.y:

                        # Check Down
                        if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:

                            numberTileMap[currentY + 1][currentX] = nextNum
                            numberCoords[nextNum] = [currentX, currentY + 1]
                            nextNum += 1

                    else:

                        break

                    # Check Down Right
                    if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][currentX + 1] == -1:

                        numberTileMap[currentY + 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY + 1]
                        nextNum += 1

                    # Check Right
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:

                        numberTileMap[currentY][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY]
                        nextNum += 1

                    # Check Right Up
                    if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][currentX + 1] == -1:

                        numberTileMap[currentY - 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY - 1]
                        nextNum += 1

                    # Check Up
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                        numberTileMap[currentY - 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY - 1]
                        nextNum += 1

                    # Check Left Up
                    if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][currentX - 1] == -1:

                        numberTileMap[currentY - 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY - 1]
                        nextNum += 1

                    # Check Left
                    if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:
                        numberTileMap[currentY][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY]
                        nextNum += 1

                    # Check Down Left
                    if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][currentX - 1] == -1:
                        numberTileMap[currentY + 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY + 1]
                        nextNum += 1

                    currentNum += 1
                    currentX = numberCoords[currentNum][0]
                    currentY = numberCoords[currentNum][1]

                    if currentNum == nextNum - 1:

                        break

            # If Enemy is right down of the target
            elif selfTile.y > startPosY and selfTile.x > startPosX:

                numberTileMap[currentY][currentX] = currentNum

                while True:

                    # Check Down Right
                    if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][currentX + 1] == -1:

                        numberTileMap[currentY + 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY + 1]
                        nextNum += 1

                        if self.check_tile(currentX + 1, currentY + 1):

                            count += 1

                            if count == limit:

                                break

                    # Check Right
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:

                        numberTileMap[currentY][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY]
                        nextNum += 1
                        if self.check_tile(currentX + 1, currentY):
                            count += 1

                            if count == limit:

                                break

                    # Check Right Up
                    if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][currentX + 1] == -1:

                        numberTileMap[currentY - 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY - 1]
                        nextNum += 1
                        if self.check_tile(currentX + 1, currentY - 1):

                            count += 1
                            if count == limit:
                                break

                    # Check Up
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                        numberTileMap[currentY - 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY - 1]
                        nextNum += 1
                        if self.check_tile(currentX, currentY - 1):
                            count += 1
                            if count == limit:
                                break

                    # Check Left Up
                    if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][currentX - 1] == -1:

                        numberTileMap[currentY - 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY - 1]
                        nextNum += 1
                        if self.check_tile(currentX - 1, currentY - 1):
                            count += 1
                            if count == limit:
                                break

                    # Check Left
                    if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:

                        numberTileMap[currentY][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY]
                        nextNum += 1
                        if self.check_tile(currentX - 1, currentY):

                            count += 1
                            if count == limit:
                                break

                    # Check Down Left
                    if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][currentX - 1] == -1:

                        numberTileMap[currentY + 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY + 1]
                        nextNum += 1
                        if self.check_tile(currentX - 1, currentY + 1):
                            count += 1
                            if count == limit:
                                break

                    # Check Down
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:

                        numberTileMap[currentY + 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY + 1]
                        nextNum += 1
                        if self.check_tile(currentX, currentY + 1):
                            count += 1
                            if count == limit:
                                break

                    currentNum += 1
                    currentX = numberCoords[currentNum][0]
                    currentY = numberCoords[currentNum][1]

                surroundingTiles = self.find_quickest_path([numberCoords[nextNum - 1], 0], blocked=False)

                if len(surroundingTiles) > 0:

                    return surroundingTiles

            # If Enemy is right of the target
            elif selfTile.y == startPosY and selfTile.x > startPosX:

                numberTileMap[currentY][currentX] = currentNum

                while True:

                    # Check Right
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:

                        numberTileMap[currentY][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY]
                        nextNum += 1

                        if self.check_tile(currentX + 1, currentY):

                            count += 1

                            if count == limit:

                                break

                    # Check Right Up
                    if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][currentX + 1] == -1:

                        numberTileMap[currentY - 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY - 1]
                        nextNum += 1

                        if self.check_tile(currentX + 1, currentY - 1):

                            count += 1

                            if count == limit:

                                break

                    # Check Up
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                        numberTileMap[currentY - 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY - 1]
                        nextNum += 1

                        if self.check_tile(currentX, currentY - 1):

                            count += 1

                            if count == limit:

                                break

                    # Check Left Up
                    if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][currentX - 1] == -1:

                        numberTileMap[currentY - 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY - 1]
                        nextNum += 1

                        if self.check_tile(currentX - 1, currentY - 1):

                            count += 1

                            if count == limit:

                                break

                    # Check Left
                    if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:

                        numberTileMap[currentY][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY]
                        nextNum += 1

                        if self.check_tile(currentX - 1, currentY):

                            count += 1

                            if count == limit:

                                break

                    # Check Down Left
                    if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][currentX - 1] == -1:

                        numberTileMap[currentY + 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY + 1]
                        nextNum += 1

                        if self.check_tile(currentX - 1, currentY + 1):

                            count += 1

                            if count == limit:

                                break

                    # Check Down
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:

                        numberTileMap[currentY + 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY + 1]
                        nextNum += 1

                        if self.check_tile(currentX, currentY + 1):

                            count += 1

                            if count == limit:

                                break

                    # Check Down Right
                    if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][currentX + 1] == -1:

                        numberTileMap[currentY + 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY + 1]
                        nextNum += 1

                        if self.check_tile(currentX + 1, currentY + 1):

                            count += 1

                            if count == limit:

                                break

                    currentNum += 1
                    currentX = numberCoords[currentNum][0]
                    currentY = numberCoords[currentNum][1]

                # '''
                x, y = 0, 0

                # Printing tilemap------------------------------------------------------------------
                print("\n" * 2)
                for line in numberTileMap:

                    for col in line:

                        if isinstance(self.tilemap.get(x, y)[0].obj, Player):

                            print("C   ", end="")
                            foundPlayer = True

                        elif isinstance(self.tilemap.get(x, y)[0].obj, Enemy):

                            print("E   ", end="")

                        else:

                            if len(str(col)) == 1:
                                print(str(col) + "   ", end="")

                            elif len(str(col)) == 2:
                                print(str(col) + "  ", end="")

                            elif len(str(col)) == 3:
                                print(str(col) + " ", end="")

                        x += 1

                    x = 0
                    y += 1

                    print("\n")
                # -----------------------------------------------------------------------------
                # '''

                surroundingTiles = self.find_quickest_path([numberCoords[nextNum - 1], 0], blocked=False)

                '''
                # Printing tilemap------------------------------------------------------------------
                print("\n" * 2)
                for line in numberTileMap:

                    for col in line:

                        if len(str(col)) == 1:
                            print(str(col) + "   ", end="")

                        elif len(str(col)) == 2:
                            print(str(col) + "  ", end="")

                        elif len(str(col)) == 3:
                            print(str(col) + " ", end="")

                    print("\n")
                # -----------------------------------------------------------------------------
                # '''

                if len(surroundingTiles) > 0:

                    print(surroundingTiles)
                    return surroundingTiles

            # If Enemy is right up of the target
            elif selfTile.y < startPosY and selfTile.x > startPosX:

                numberTileMap[currentY][currentX] = currentNum

                while True:

                    if currentX + 1 != selfTile.x or currentY - 1 != selfTile.y:

                        # Check Right Up
                        if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][currentX + 1] == -1:

                            numberTileMap[currentY - 1][currentX + 1] = nextNum
                            numberCoords[nextNum] = [currentX + 1, currentY - 1]
                            nextNum += 1

                    else:

                        break

                    # Check Up
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                        numberTileMap[currentY - 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY - 1]
                        nextNum += 1

                    # Check Left Up
                    if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][currentX - 1] == -1:

                        numberTileMap[currentY - 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY - 1]
                        nextNum += 1

                    # Check Left
                    if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:
                        numberTileMap[currentY][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY]
                        nextNum += 1

                    # Check Down Left
                    if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][currentX - 1] == -1:
                        numberTileMap[currentY + 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY + 1]
                        nextNum += 1

                    # Check Down
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:

                        numberTileMap[currentY + 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY + 1]
                        nextNum += 1

                    # Check Down Right
                    if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][currentX + 1] == -1:

                        numberTileMap[currentY + 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY + 1]
                        nextNum += 1

                    # Check Right
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:

                        numberTileMap[currentY][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY]
                        nextNum += 1

                    currentNum += 1
                    currentX = numberCoords[currentNum][0]
                    currentY = numberCoords[currentNum][1]

                    if currentNum == nextNum - 1:

                        break

        posX = selfTile.x
        posY = selfTile.y

        startX = posX - 1 if posX - 1 >= 0 else 0
        endX = posX + 1 if posX + 1 < self.tilemap.width else self.tilemap.width - 1

        startY = posY - 1 if posY - 1 >= 0 else 0
        endY = posY + 1 if posY + 1 < self.tilemap.height else self.tilemap.height - 1

        xIndex = startX
        yIndex = startY

        while yIndex <= endY:

            while xIndex <= endX:

                if yIndex != posY or xIndex != posX:

                    if numberTileMap[yIndex][xIndex] >= 0:

                        surroundingTiles[numberTileMap[yIndex][xIndex]] = [xIndex, yIndex]

                xIndex += 1

            xIndex = startX
            yIndex += 1

        '''
        x, y = 0, 0
 
        # Printing tilemap------------------------------------------------------------------
        print("\n" * 2)
        for line in numberTileMap:

            for col in line:

                if isinstance(self.tilemap.get(x, y)[0].obj, Player):

                    print("C   ", end="")
                    foundPlayer = True

                elif isinstance(self.tilemap.get(x, y)[0].obj, Enemy):

                    print("E   ", end="")

                else:

                    if len(str(col)) == 1:
                        print(str(col) + "   ", end="")

                    elif len(str(col)) == 2:
                        print(str(col) + "  ", end="")

                    elif len(str(col)) == 3:
                        print(str(col) + " ", end="")

                x += 1

            x = 0
            y += 1

            print("\n")
        # -----------------------------------------------------------------------------
        # '''

        '''
        # Printing tilemap------------------------------------------------------------------
        print("\n" * 2)
        for line in numberTileMap:

            for col in line:

                if len(str(col)) == 1:
                    print(str(col) + "   ", end="")

                elif len(str(col)) == 2:
                    print(str(col) + "  ", end="")

                elif len(str(col)) == 3:
                    print(str(col) + " ", end="")

            print("\n")
        # -----------------------------------------------------------------------------
        # '''

        if len(surroundingTiles) == 0:

            surroundingTiles = self.find_quickest_path([numberCoords[1], currentNum], blocked=True)

        '''
        # If Enemy is above target
        if selfTile.y < startPosY and selfTile.x == startPosX:

            while currentNum < numMoves:

                if currentX != selfTile.x or currentY - 1 != selfTile.y:

                    # Check Up
                    if self.check_tile(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                        numberTileMap[currentY - 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY - 1]
                        nextNum += 1

                else:

                    break

                # Check Left Up
                if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                    numberTileMap[currentY - 1][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY - 1]
                    nextNum += 1

                # Check Left
                if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:

                    numberTileMap[currentY][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY]
                    nextNum += 1

                # Check Down Left
                if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][currentX - 1] == -1:

                    numberTileMap[currentY + 1][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY + 1]
                    nextNum += 1

                # Check Down
                if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:

                    numberTileMap[currentY + 1][currentX] = nextNum
                    numberCoords[nextNum] = [currentX, currentY + 1]
                    nextNum += 1

                # Check Down Right
                if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][currentX + 1] == -1:

                    numberTileMap[currentY + 1][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY + 1]
                    nextNum += 1

                # Check Right
                if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:

                    numberTileMap[currentY][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY]
                    nextNum += 1

                # Check Right Up
                if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][currentX + 1] == -1:

                    numberTileMap[currentY - 1][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY - 1]
                    nextNum += 1

                currentNum += 1
                currentX = numberCoords[currentNum][0]
                currentY = numberCoords[currentNum][1]

            return numberTileMap

        # If Enemy is left above the target
        elif selfTile.y < startPosY and selfTile.x < startPosX:

            while currentNum < numMoves:

                if currentX - 1 != selfTile.x or currentY - 1 != selfTile.y:

                    # Check Left Up
                    if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][currentX - 1] == -1:

                        numberTileMap[currentY - 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY - 1]
                        nextNum += 1

                else:

                    break

                # Check Left
                if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:

                    if currentY == selfTile.y and currentX - 1 == selfTile.x:

                        break

                    numberTileMap[currentY][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY]
                    # booleanTileMap[currentY][currentX - 1] = False
                    nextNum += 1

                # Check Down Left
                if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][currentX - 1] == -1:

                    if currentY + 1 == selfTile.y and currentX - 1 == selfTile.x:

                        break

                    numberTileMap[currentY + 1][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY + 1]
                    # booleanTileMap[currentY + 1][currentX - 1] = False
                    nextNum += 1

                # Check Down
                if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:

                    if currentY + 1 == selfTile.y and currentX == selfTile.x:
                        break

                    numberTileMap[currentY + 1][currentX] = nextNum
                    numberCoords[nextNum] = [currentX, currentY + 1]
                    # booleanTileMap[currentY + 1][currentX] = False
                    nextNum += 1

                # Check Down Right
                if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][currentX + 1] == -1:

                    if currentY + 1 == selfTile.y and currentX + 1 == selfTile.x:

                        break

                    numberTileMap[currentY + 1][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY + 1]
                    # booleanTileMap[currentY + 1][currentX + 1] = False
                    nextNum += 1

                # Check Right
                if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:

                    if currentY == selfTile.y and currentX + 1 == selfTile.x:
                        break

                    numberTileMap[currentY][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY]
                    # booleanTileMap[currentY][currentX + 1] = False
                    nextNum += 1

                # Check Right Up
                if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][currentX + 1] == -1:

                    if currentY - 1 == selfTile.y and currentX + 1 == selfTile.x:
                        break

                    numberTileMap[currentY - 1][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY - 1]
                    # booleanTileMap[currentY - 1][currentX + 1] = False
                    nextNum += 1

                # Check Up
                if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                    if currentY - 1 == selfTile.y and currentX == selfTile.x:
                        break

                    numberTileMap[currentY - 1][currentX] = nextNum
                    numberCoords[nextNum] = [currentX, currentY - 1]
                    # booleanTileMap[currentY - 1][currentX] = False
                    nextNum += 1

                currentNum += 1
                currentX = numberCoords[currentNum][0]
                currentY = numberCoords[currentNum][1]

            return numberTileMap

        # If Enemy is left of the target
        elif selfTile.y == startPosY and selfTile.x < startPosX:

            while currentNum < numMoves:

                if currentX - 1 != selfTile.x or currentY != selfTile.y:

                    # Check Left
                    if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:

                        numberTileMap[currentY][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY]
                        nextNum += 1

                else:

                    break

                # Check Down Left
                if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][currentX - 1] == 1:

                    numberTileMap[currentY + 1][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY + 1]
                    nextNum += 1

                # Check Down
                if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:

                    numberTileMap[currentY + 1][currentX] = nextNum
                    numberCoords[nextNum] = [currentX, currentY + 1]
                    nextNum += 1

                # Check Down Right
                if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][currentX + 1] == -1:

                    numberTileMap[currentY + 1][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY + 1]
                    nextNum += 1

                # Check Right
                if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:

                    numberTileMap[currentY][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY]
                    nextNum += 1

                # Check Right Up
                if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][currentX + 1] == -1:

                    numberTileMap[currentY - 1][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY - 1]
                    nextNum += 1

                # Check Up
                if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                    numberTileMap[currentY - 1][currentX] = nextNum
                    numberCoords[nextNum] = [currentX, currentY - 1]
                    nextNum += 1

                # Check Left Up
                if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][currentX - 1] == -1:

                    numberTileMap[currentY - 1][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY - 1]
                    nextNum += 1

                else:

                    currentNum += 1
                    currentX = numberCoords[currentNum][0]
                    currentY = numberCoords[currentNum][1]

            return numberTileMap

        # If Enemy is left down of the target
        elif selfTile.y > startPosY and selfTile.x < startPosX:

            while currentNum < numMoves:

                if currentX - 1 != selfTile.x or currentY + 1 != selfTile.y:

                    # Check Down Left
                    if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][currentX - 1] == -1:

                        numberTileMap[currentY + 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY + 1]
                        nextNum += 1

                else:

                    break

                # Check Down
                if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:

                    numberTileMap[currentY + 1][currentX] = nextNum
                    numberCoords[nextNum] = [currentX, currentY + 1]
                    nextNum += 1

                # Check Down Right
                if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][currentX + 1] == -1:

                    numberTileMap[currentY + 1][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY + 1]
                    nextNum += 1

                # Check Right
                if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:

                    numberTileMap[currentY][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY]
                    nextNum += 1

                # Check Right Up
                if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][currentX + 1] == -1:

                    numberTileMap[currentY - 1][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY - 1]
                    nextNum += 1

                # Check Up
                if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                    numberTileMap[currentY - 1][currentX] = nextNum
                    numberCoords[nextNum] = [currentX, currentY - 1]
                    nextNum += 1

                # Check Left Up
                if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][currentX - 1] == -1:

                    numberTileMap[currentY - 1][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY - 1]
                    nextNum += 1

                # Check Left
                if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:
                    numberTileMap[currentY][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY]
                    nextNum += 1

                currentNum += 1
                currentX = numberCoords[currentNum][0]
                currentY = numberCoords[currentNum][1]

            return numberTileMap

        # If Enemy is down of the target
        elif selfTile.y > startPosY and selfTile.x == startPosX:

            while currentNum < numMoves:

                if currentX != selfTile.x or currentY + 1 != selfTile.y:

                    # Check Down
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:

                        numberTileMap[currentY + 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY + 1]
                        nextNum += 1

                else:

                    break

                # Check Down Right
                if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][currentX + 1] == -1:

                    numberTileMap[currentY + 1][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY + 1]
                    nextNum += 1

                # Check Right
                if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:

                    numberTileMap[currentY][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY]
                    nextNum += 1

                # Check Right Up
                if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][currentX + 1] == -1:

                    numberTileMap[currentY - 1][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY - 1]
                    nextNum += 1

                # Check Up
                if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                    numberTileMap[currentY - 1][currentX] = nextNum
                    numberCoords[nextNum] = [currentX, currentY - 1]
                    nextNum += 1

                # Check Left Up
                if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][currentX - 1] == -1:

                    numberTileMap[currentY - 1][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY - 1]
                    nextNum += 1

                # Check Left
                if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:
                    numberTileMap[currentY][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY]
                    nextNum += 1

                # Check Down Left
                if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][currentX - 1] == -1:
                    numberTileMap[currentY + 1][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY + 1]
                    nextNum += 1

                try:

                    currentNum += 1
                    currentX = numberCoords[currentNum][0]
                    currentY = numberCoords[currentNum][1]

                except KeyError:

                    numSpaces = 0

                    for line in self.tilemap.tilemap:

                        for col in line:

                            if not isinstance(col, Wall) and not isinstance(col, Player):

                                numSpaces += 1

            return numberTileMap

        # If Enemy is right down of the target
        elif selfTile.y > startPosY and selfTile.x > startPosX:

            while currentNum < numMoves:

                if currentX + 1 != selfTile.x or currentY + 1 != selfTile.y:

                    # Check Down Right
                    if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][currentX + 1] == -1:

                        numberTileMap[currentY + 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY + 1]
                        nextNum += 1

                else:

                    break

                # Check Right
                if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:

                    numberTileMap[currentY][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY]
                    nextNum += 1

                # Check Right Up
                if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][currentX + 1] == -1:

                    numberTileMap[currentY - 1][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY - 1]
                    nextNum += 1

                # Check Up
                if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                    numberTileMap[currentY - 1][currentX] = nextNum
                    numberCoords[nextNum] = [currentX, currentY - 1]
                    nextNum += 1

                # Check Left Up
                if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][currentX - 1] == -1:

                    numberTileMap[currentY - 1][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY - 1]
                    nextNum += 1

                # Check Left
                if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:

                    numberTileMap[currentY][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY]
                    nextNum += 1

                # Check Down Left
                if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][currentX - 1] == -1:

                    numberTileMap[currentY + 1][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY + 1]
                    nextNum += 1

                # Check Down
                if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:

                    numberTileMap[currentY + 1][currentX] = nextNum
                    numberCoords[nextNum] = [currentX, currentY + 1]
                    nextNum += 1

                currentNum += 1
                currentX = numberCoords[currentNum][0]
                currentY = numberCoords[currentNum][1]

            # print(time.time() - initTime)

            return numberTileMap

        # If Enemy is right of the target
        elif selfTile.y == startPosY and selfTile.x > startPosX:

            while currentNum < numMoves:

                if currentX + 1 != selfTile.x or currentY != selfTile.y:

                    # Check Right
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:

                        numberTileMap[currentY][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY]
                        nextNum += 1

                else:

                    break

                # Check Right Up
                if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][currentX + 1] == -1:

                    numberTileMap[currentY - 1][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY - 1]
                    nextNum += 1

                # Check Up
                if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                    numberTileMap[currentY - 1][currentX] = nextNum
                    numberCoords[nextNum] = [currentX, currentY - 1]
                    nextNum += 1

                # Check Left Up
                if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][currentX - 1] == -1:

                    numberTileMap[currentY - 1][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY - 1]
                    nextNum += 1

                # Check Left
                if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:

                    numberTileMap[currentY][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY]
                    nextNum += 1

                # Check Down Left
                if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][currentX - 1] == -1:

                    numberTileMap[currentY + 1][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY + 1]
                    nextNum += 1

                # Check Down
                if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:

                    numberTileMap[currentY + 1][currentX] = nextNum
                    numberCoords[nextNum] = [currentX, currentY + 1]
                    nextNum += 1

                # Check Down Right
                if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][currentX + 1] == -1:

                    numberTileMap[currentY + 1][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY + 1]
                    nextNum += 1

                currentNum += 1
                currentX = numberCoords[currentNum][0]
                currentY = numberCoords[currentNum][1]

            return numberTileMap

        # If Enemy is right up of the target
        elif selfTile.y < startPosY and selfTile.x > startPosX:

            while currentNum < numMoves:

                if currentX + 1 != selfTile.x or currentY - 1 != selfTile.y:

                    # Check Right Up
                    if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][currentX + 1] == -1:

                        numberTileMap[currentY - 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY - 1]
                        nextNum += 1

                else:

                    break

                # Check Up
                if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][currentX] == -1:

                    numberTileMap[currentY - 1][currentX] = nextNum
                    numberCoords[nextNum] = [currentX, currentY - 1]
                    nextNum += 1

                # Check Left Up
                if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][currentX - 1] == -1:

                    numberTileMap[currentY - 1][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY - 1]
                    nextNum += 1

                # Check Left
                if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][currentX - 1] == -1:
                    numberTileMap[currentY][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY]
                    nextNum += 1

                # Check Down Left
                if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][currentX - 1] == -1:
                    numberTileMap[currentY + 1][currentX - 1] = nextNum
                    numberCoords[nextNum] = [currentX - 1, currentY + 1]
                    nextNum += 1

                # Check Down
                if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][currentX] == -1:

                    numberTileMap[currentY + 1][currentX] = nextNum
                    numberCoords[nextNum] = [currentX, currentY + 1]
                    nextNum += 1

                # Check Down Right
                if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][currentX + 1] == -1:

                    numberTileMap[currentY + 1][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY + 1]
                    nextNum += 1

                # Check Right
                if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][currentX + 1] == -1:

                    numberTileMap[currentY][currentX + 1] = nextNum
                    numberCoords[nextNum] = [currentX + 1, currentY]
                    nextNum += 1

                currentNum += 1
                currentX = numberCoords[currentNum][0]
                currentY = numberCoords[currentNum][1]

            return numberTileMap

        '''

        return surroundingTiles

# -------------------------------------------------------------------------------------------
"""
These components are placed here to resolve a circular dependency between tiles.py and this one.
They are only here to keep everything working until a solution is found.

Ideally, our algorithms should not contain built in references to characters like walls and the sort.
What if the user wants raycasting to be valid for entities too?

We should figure out a way to move the raycasting logic out of our characters and somewhere else.
Perhaps a display changer that all entities can use to change the way the screen is viewed after they move? 

We should also find a way to move pathfinding and other big features elsware,
I don't think their logic belongs in the character classes.
They should be separate features that are added to characters.

We can also structure the project in a way that prevents these circular dependencies from happening.
"""


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


class Fog(BaseCharacter):

    def start(self):

        self.char = ' '
        self.name = 'Fog'
        self.priority = 1

    def clear(self):

        self.tilemap.remove_obj(self, True)


class Enemy(EntityCharacter):
    
    """
    Enemy that randomly moves across the screen.
    """

    def __init__(self):

        super().__init__()

        self.name = 'Enemy'
        self.char = 'E'
        self.attrib.append("red")
        self.priority = 18

        self.debug_move = True
        self.hp = 0
        self.damage_min = 0  # Minimum amount of damage that can be dealt
        self.damage_max = 0  # Maximum amount of damage that can be dealt
        self.damage_type = ""
        self.armor = 0  # Amount of physical damage resistance
        self.description = ""  # Description of enemy
        self.move_speed = 1  # How many times the enemy can move in one turn

        self.start()  # Calling user start method:

    def interact(self, char):

        if isinstance(char, Player):

            char.attack(self)

            if self.is_alive:

                self.attack(char)

    def death(self):

        deathMessages = ["You have slain the " + self.name, "You've slaughtered the " + self.name,
                         "The " + self.name + " falls to the ground, dead"]

        self.tilemap.scrollWin.add_content(random.choice(deathMessages))
        self.is_alive = False

    def attack(self, targ):

        amountDamage = random.randrange(self.damage_min, self.damage_max + 1)

        if self.damage_type == "physical":

            self.tilemap.scrollWin.add_content(
                "The " + self.name + " strikes you, dealing " + str(amountDamage) + " damage")

        targ.hp -= amountDamage

