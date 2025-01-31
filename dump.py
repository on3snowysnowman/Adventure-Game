"""
This file contains raw dumps from the engine.

These components were likely removed or trimmed out.
They are backed up here for future reference.

I know the format of this file is not formatted correctly.
I will be fixing this at a later date.
"""

# -----------------------
# Camera
# -----------------------

class Camera(object):

    def __init__(self, tilemap, win):

        self.tilemap = tilemap  # Full tilemap
        self.win = win  # DisplayWindow in use
        self.displayArea = []  # Visual tilemap area will will display, based on full tilemap
        self.focusObject = None  # Object that the camera is focused on
        self.focusPoint = [0, 0]  # Coordinate point of the focused object
        self.radius = 0  # Amount of tiles that we will be rendering around the focus object

    def set_focus_object(self, obj):

        """
        Sets the focus point of the camera onto an object of Tile class in the tilemap

        :param obj: Object being set as the focus point
        :type obj : Tile
        """

        objTile = self.tilemap.find_object(obj)

        self.focusObject = objTile
        self.focusPoint = [objTile.x, objTile.y]

    def refresh_focus_position(self):

        """
        Finds the focus object position in the tilemap and resets the focus point to its position
        """

        self.focusObject = self.tilemap.find_object(self.focusObject.obj)
        self.focusPoint = [self.focusObject.x, self.focusObject.y]

        # print("Camera self.tilemap: " + str(self.tilemap))
        # print("Camera self.displayArea: " + str(self.displayArea))

    def set_radius(self, radius):

        """
        Sets the radius of the display area

        :param radius: New number of tiles to be displayed around the focus object
        :type radius: Int
        """

        self.radius = radius

    def update(self):

        """
        Fills the tilemap with fog to block the player's vision relative to walls
        """
        #playerTile = self.tilemap.find_object_type(Player)
        #self.radius = playerTile.obj.radius

        # TODO: Is the correct implementation?:

        self.radius = self.focusObject.obj.radius

        self.refresh_focus_position()
        self.create_display()

        #playerTile.obj.look(self.displayArea)

        self.focusObject.obj.look(self.displayArea)

    def create_display(self):

        """
        Creates the display area based on the radius, using our tilemap
        """

        if (self.radius * 2) + 1 >= self.tilemap.height:

            height = self.tilemap.height

        else:

            height = (self.radius * 2) + 1

        if (self.radius * 2) + 1 >= self.tilemap.width:

            width = self.tilemap.width

        else:

            width = (self.radius * 2) + 1

        # Clearing our displayArea
        del self.displayArea
        self.displayArea = BaseTileMap(height, width, self.win)

        # Creating the starting x position of our display zone
        startX = self.focusPoint[0] - self.radius

        # Creating the ending x position of our display zone
        if self.focusPoint[0] + self.radius > len(self.tilemap.tilemap[self.focusPoint[1]]) - 1:

            endX = len(self.tilemap.tilemap[self.focusPoint[1]]) - 1
            startX -= ((self.focusPoint[0] + 1) + self.radius) - len(self.tilemap.tilemap[self.focusPoint[1]])

            if startX < 0:

                startX = 0

        else:

            endX = self.focusPoint[0] + self.radius

        if startX < 0:

            endX += abs(startX)
            if endX > len(self.tilemap.tilemap[self.focusPoint[1]]) - 1:

                endX = len(self.tilemap.tilemap[self.focusPoint[1]]) - 1

            startX = 0

        # Creating the starting y position of our display zone
        startY = self.focusPoint[1] - self.radius

        # Creating the ending y position of our display zone
        if self.focusPoint[1] + self.radius > len(self.tilemap.tilemap) - 1:

            endY = len(self.tilemap.tilemap) - 1
            startY -= ((self.focusPoint[1] + 1) + self.radius) - len(self.tilemap.tilemap)

            if startY < 0:

                startY = 0

        else:

            endY = self.focusPoint[1] + self.radius

        if startY < 0:

            endY += abs(startY)
            if endY > len(self.tilemap.tilemap) - 1:

                endY = len(self.tilemap.tilemap) - 1

            startY = 0

        yIndex = 0
        xIndex = 0

        # Adding Tiles to the displayArea tilemap from our main tilemap
        while yIndex + startY <= endY:

            while xIndex + startX <= endX:

                for obj in self.tilemap.tilemap[yIndex + startY][xIndex + startX]:

                    self.displayArea.add(obj, xIndex, yIndex, bind=False)

                xIndex += 1

            yIndex += 1
            xIndex = 0


# -----------------------
# Pathfinding:
# -----------------------


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
                        if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][
                            currentX - 1] == -1:
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
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][
                        currentX] == -1:
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
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][
                        currentX + 1] == -1:
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
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][
                        currentX] == -1:
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
                        if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][
                            currentX + 1] == -1:
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
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][
                        currentX] == -1:
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
                    if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][
                        currentX - 1] == -1:
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
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][
                        currentX] == -1:
                        numberTileMap[currentY + 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY + 1]
                        nextNum += 1

                    # Check Down Right
                    if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][
                        currentX + 1] == -1:
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
                    if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][
                        currentX] == -1:

                        numberTileMap[currentY - 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY - 1]
                        nextNum += 1

                        if self.check_tile(currentX - 1, currentY - 1):

                            count += 1

                            if count == limit:
                                break

                    # Check Left
                    if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][
                        currentX - 1] == -1:

                        numberTileMap[currentY][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY]
                        nextNum += 1
                        if self.check_tile(currentX - 1, currentY):

                            count += 1

                            if count == limit:
                                break

                    # Check Down Left
                    if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][
                        currentX - 1] == -1:

                        numberTileMap[currentY + 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY + 1]
                        nextNum += 1

                        if self.check_tile(currentX - 1, currentY + 1):

                            count += 1

                            if count == limit:
                                break

                    # Check Down
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][
                        currentX] == -1:

                        numberTileMap[currentY + 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY + 1]
                        nextNum += 1

                        if self.check_tile(currentX, currentY + 1):

                            count += 1

                            if count == limit:
                                break

                    # Check Down Right
                    if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][
                        currentX + 1] == -1:

                        numberTileMap[currentY + 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY + 1]
                        nextNum += 1

                        if self.check_tile(currentX + 1, currentY + 1):

                            count += 1

                            if count == limit:
                                break

                    # Check Right
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][
                        currentX + 1] == -1:

                        numberTileMap[currentY][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY]
                        nextNum += 1

                        if self.check_tile(currentX + 1, currentY):

                            count += 1

                            if count == limit:
                                break

                    # Check Right Up
                    if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][
                        currentX + 1] == -1:

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
                        if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][
                            currentX - 1] == -1:
                            numberTileMap[currentY - 1][currentX - 1] = nextNum
                            numberCoords[nextNum] = [currentX - 1, currentY - 1]
                            nextNum += 1

                    else:

                        break

                    # Check Left
                    if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][
                        currentX - 1] == -1:

                        if currentY == selfTile.y and currentX - 1 == selfTile.x:
                            break

                        numberTileMap[currentY][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY]
                        # booleanTileMap[currentY][currentX - 1] = False
                        nextNum += 1

                    # Check Down Left
                    if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][
                        currentX - 1] == -1:

                        if currentY + 1 == selfTile.y and currentX - 1 == selfTile.x:
                            break

                        numberTileMap[currentY + 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY + 1]
                        # booleanTileMap[currentY + 1][currentX - 1] = False
                        nextNum += 1

                    # Check Down
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][
                        currentX] == -1:

                        if currentY + 1 == selfTile.y and currentX == selfTile.x:
                            break

                        numberTileMap[currentY + 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY + 1]
                        # booleanTileMap[currentY + 1][currentX] = False
                        nextNum += 1

                    # Check Down Right
                    if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][
                        currentX + 1] == -1:

                        if currentY + 1 == selfTile.y and currentX + 1 == selfTile.x:
                            break

                        numberTileMap[currentY + 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY + 1]
                        # booleanTileMap[currentY + 1][currentX + 1] = False
                        nextNum += 1

                    # Check Right
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][
                        currentX + 1] == -1:

                        if currentY == selfTile.y and currentX + 1 == selfTile.x:
                            break

                        numberTileMap[currentY][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY]
                        # booleanTileMap[currentY][currentX + 1] = False
                        nextNum += 1

                    # Check Right Up
                    if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][
                        currentX + 1] == -1:

                        if currentY - 1 == selfTile.y and currentX + 1 == selfTile.x:
                            break

                        numberTileMap[currentY - 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY - 1]
                        # booleanTileMap[currentY - 1][currentX + 1] = False
                        nextNum += 1

                    # Check Up
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][
                        currentX] == -1:

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
                        if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][
                            currentX - 1] == -1:
                            numberTileMap[currentY][currentX - 1] = nextNum
                            numberCoords[nextNum] = [currentX - 1, currentY]
                            nextNum += 1

                    else:

                        break

                    # Check Down Left
                    if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][
                        currentX - 1] == 1:
                        numberTileMap[currentY + 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY + 1]
                        nextNum += 1

                    # Check Down
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][
                        currentX] == -1:
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
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][
                        currentX + 1] == -1:
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
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][
                        currentX] == -1:
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

            # If Enemy is left down of the target
            elif selfTile.y > startPosY and selfTile.x < startPosX:

                numberTileMap[currentY][currentX] = currentNum

                while True:

                    if currentX - 1 != selfTile.x or currentY + 1 != selfTile.y:

                        # Check Down Left
                        if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][
                            currentX - 1] == -1:
                            numberTileMap[currentY + 1][currentX - 1] = nextNum
                            numberCoords[nextNum] = [currentX - 1, currentY + 1]
                            nextNum += 1

                    else:

                        break

                    # Check Down
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][
                        currentX] == -1:
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
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][
                        currentX + 1] == -1:
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
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][
                        currentX] == -1:
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
                    if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][
                        currentX - 1] == -1:
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
                        if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][
                            currentX] == -1:
                            numberTileMap[currentY + 1][currentX] = nextNum
                            numberCoords[nextNum] = [currentX, currentY + 1]
                            nextNum += 1

                    else:

                        break

                    # Check Down Right
                    if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][
                        currentX + 1] == -1:
                        numberTileMap[currentY + 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY + 1]
                        nextNum += 1

                    # Check Right
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][
                        currentX + 1] == -1:
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
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][
                        currentX] == -1:
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
                    if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][
                        currentX - 1] == -1:
                        numberTileMap[currentY][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY]
                        nextNum += 1

                    # Check Down Left
                    if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][
                        currentX - 1] == -1:
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
                    if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][
                        currentX + 1] == -1:

                        numberTileMap[currentY + 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY + 1]
                        nextNum += 1

                        if self.check_tile(currentX + 1, currentY + 1):

                            count += 1

                            if count == limit:
                                break

                    # Check Right
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][
                        currentX + 1] == -1:

                        numberTileMap[currentY][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY]
                        nextNum += 1
                        if self.check_tile(currentX + 1, currentY):
                            count += 1

                            if count == limit:
                                break

                    # Check Right Up
                    if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][
                        currentX + 1] == -1:

                        numberTileMap[currentY - 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY - 1]
                        nextNum += 1
                        if self.check_tile(currentX + 1, currentY - 1):

                            count += 1
                            if count == limit:
                                break

                    # Check Up
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][
                        currentX] == -1:

                        numberTileMap[currentY - 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY - 1]
                        nextNum += 1
                        if self.check_tile(currentX, currentY - 1):
                            count += 1
                            if count == limit:
                                break

                    # Check Left Up
                    if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][
                        currentX - 1] == -1:

                        numberTileMap[currentY - 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY - 1]
                        nextNum += 1
                        if self.check_tile(currentX - 1, currentY - 1):
                            count += 1
                            if count == limit:
                                break

                    # Check Left
                    if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][
                        currentX - 1] == -1:

                        numberTileMap[currentY][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY]
                        nextNum += 1
                        if self.check_tile(currentX - 1, currentY):

                            count += 1
                            if count == limit:
                                break

                    # Check Down Left
                    if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][
                        currentX - 1] == -1:

                        numberTileMap[currentY + 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY + 1]
                        nextNum += 1
                        if self.check_tile(currentX - 1, currentY + 1):
                            count += 1
                            if count == limit:
                                break

                    # Check Down
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][
                        currentX] == -1:

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
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][
                        currentX + 1] == -1:

                        numberTileMap[currentY][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY]
                        nextNum += 1

                        if self.check_tile(currentX + 1, currentY):

                            count += 1

                            if count == limit:
                                break

                    # Check Right Up
                    if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][
                        currentX + 1] == -1:

                        numberTileMap[currentY - 1][currentX + 1] = nextNum
                        numberCoords[nextNum] = [currentX + 1, currentY - 1]
                        nextNum += 1

                        if self.check_tile(currentX + 1, currentY - 1):

                            count += 1

                            if count == limit:
                                break

                    # Check Up
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][
                        currentX] == -1:

                        numberTileMap[currentY - 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY - 1]
                        nextNum += 1

                        if self.check_tile(currentX, currentY - 1):

                            count += 1

                            if count == limit:
                                break

                    # Check Left Up
                    if self.tilemap._bound_check(currentX - 1, currentY - 1) and numberTileMap[currentY - 1][
                        currentX - 1] == -1:

                        numberTileMap[currentY - 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY - 1]
                        nextNum += 1

                        if self.check_tile(currentX - 1, currentY - 1):

                            count += 1

                            if count == limit:
                                break

                    # Check Left
                    if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][
                        currentX - 1] == -1:

                        numberTileMap[currentY][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY]
                        nextNum += 1

                        if self.check_tile(currentX - 1, currentY):

                            count += 1

                            if count == limit:
                                break

                    # Check Down Left
                    if self.tilemap._bound_check(currentX - 1, currentY + 1) and numberTileMap[currentY + 1][
                        currentX - 1] == -1:

                        numberTileMap[currentY + 1][currentX - 1] = nextNum
                        numberCoords[nextNum] = [currentX - 1, currentY + 1]
                        nextNum += 1

                        if self.check_tile(currentX - 1, currentY + 1):

                            count += 1

                            if count == limit:
                                break

                    # Check Down
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][
                        currentX] == -1:

                        numberTileMap[currentY + 1][currentX] = nextNum
                        numberCoords[nextNum] = [currentX, currentY + 1]
                        nextNum += 1

                        if self.check_tile(currentX, currentY + 1):

                            count += 1

                            if count == limit:
                                break

                    # Check Down Right
                    if self.tilemap._bound_check(currentX + 1, currentY + 1) and numberTileMap[currentY + 1][
                        currentX + 1] == -1:

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
                        if self.tilemap._bound_check(currentX + 1, currentY - 1) and numberTileMap[currentY - 1][
                            currentX + 1] == -1:
                            numberTileMap[currentY - 1][currentX + 1] = nextNum
                            numberCoords[nextNum] = [currentX + 1, currentY - 1]
                            nextNum += 1

                    else:

                        break

                    # Check Up
                    if self.tilemap._bound_check(currentX, currentY - 1) and numberTileMap[currentY - 1][
                        currentX] == -1:
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
                    if self.tilemap._bound_check(currentX - 1, currentY) and numberTileMap[currentY][
                        currentX - 1] == -1:
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
                    if self.tilemap._bound_check(currentX, currentY + 1) and numberTileMap[currentY + 1][
                        currentX] == -1:
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
                    if self.tilemap._bound_check(currentX + 1, currentY) and numberTileMap[currentY][
                        currentX + 1] == -1:
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

    def run(self):

        if self.char.debug_move:

            selfTile = self.tilemap.find_object(self)

            posX = selfTile.x
            posY = selfTile.y

            startX = posX - 1 if posX - 1 >= 0 else 0
            endX = posX + 1 if posX + 1 < self.tilemap.width else self.tilemap.width - 1

            startY = posY - 1 if posY - 1 >= 0 else 0
            endY = posY + 1 if posY + 1 < self.tilemap.height else self.tilemap.height - 1

            surroundingTiles = self.find_quickest_path(self.tilemap.find_object_type(Player))
            smallestNum = 0

            for element in surroundingTiles:
                smallestNum = element
                break

            for num in surroundingTiles:

                if num < smallestNum:
                    smallestNum = num

            if len(surroundingTiles) != 0:

                xMove = surroundingTiles[smallestNum][0]
                yMove = surroundingTiles[smallestNum][1]

                if self.char.check_tile(xMove, yMove):

                    self.tilemap.move(self, xMove, yMove)

                else:

                    playerTile = self.tilemap.find_object_type(Player)

                    # Player is left below Enemy
                    if playerTile.x <= selfTile.x and playerTile.y >= selfTile.y:

                        if self.char.check_tile(xMove, yMove + 1):

                            self.tilemap.move(self, xMove, yMove + 1)

                        elif self.char.check_tile(xMove - 1, yMove):

                            self.tilemap.move(self, xMove - 1, yMove)

                    # Player is left above Enemy
                    if playerTile.x <= selfTile.x and playerTile.y <= selfTile.y:

                        if self.char.check_tile(xMove, yMove - 1):

                            self.tilemap.move(self, xMove, yMove - 1)

                        elif self.char.check_tile(xMove - 1, yMove):

                            self.tilemap.move(self, xMove - 1, yMove)

                    # Player is right above Enemy
                    if playerTile.x >= selfTile.x and playerTile.y <= selfTile.y:

                        if self.char.check_tile(xMove, yMove - 1):

                            self.tilemap.move(self, xMove, yMove - 1)

                        elif self.char.check_tile(xMove + 1, yMove):

                            self.tilemap.move(self, xMove + 1, yMove)

                    # Player is right below Enemy
                    if playerTile.x >= selfTile.x and playerTile.y >= selfTile.y:

                        if self.char.check_tile(xMove, yMove + 1):

                            self.tilemap.move(self, xMove, yMove + 1)

                        elif self.char.check_tile(xMove + 1, yMove):

                            self.tilemap.move(self, xMove + 1, yMove)

            else:

                numberTileMap = self.find_quickest_path(self.tilemap.find_object_type(Player), blocked=True)

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

                '''
                # Printing tilemap------------------------------------------------------------------
                print("\n" * 2)
                for line in numberTileMap:

                    for col in line:

                        if isinstance(self.tilemap.get(x, y)[0].obj, Player):

                            print("C   ", end="")
                            foundPlayer = True

                        elif isinstance(self.tilemap.get(x, y)[0].obj, Enemy):

                            print("E   ", end="")

                        elif isinstance(self.tilemap.get(x, y)[0].obj, Wall):

                            print("W   ", end="")

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

                dictCopy = []

                xIndex = startX
                yIndex = startY

                while yIndex <= endY:

                    while xIndex <= endX:

                        if yIndex != posY or xIndex != posX:

                            if numberTileMap[yIndex][xIndex] > 0:
                                surroundingTiles[numberTileMap[yIndex][xIndex]] = [xIndex, yIndex]
                                dictCopy.append(numberTileMap[yIndex][xIndex])

                        xIndex += 1

                    xIndex = startX
                    yIndex += 1

                while len(dictCopy) > 0:

                    smallestNum = dictCopy[0]

                    for num in dictCopy:

                        if num < smallestNum:
                            smallestNum = num

                    xMove = surroundingTiles[smallestNum][0]
                    yMove = surroundingTiles[smallestNum][1]

                    if self.char.check_tile(xMove, yMove):

                        self.tilemap.move(self, xMove, yMove)
                        break

                    else:

                        dictCopy.remove(smallestNum)

            '''
            final = []

            for x in range(8):
                final.append(-1)

            index = 0

            # Iterate over each value:
            # Plus 2, because builtin range function will stop at that number, and not include it

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

                if num > -1 and num < leastNum:
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

                # Left Up
                if count == 0:

                    if self.check_tile(posX - 1, posY - 1): self.tilemap.move(self, posX - 1, posY - 1)

                # Up
                elif count == 1:

                    if self.check_tile(posX, posY - 1): self.tilemap.move(self, posX, posY - 1)

                # Right Up
                elif count == 2:

                    if self.check_tile(posX + 1, posY - 1): self.tilemap.move(self, posX + 1, posY - 1)

                # Right
                elif count == 4:

                    if self.check_tile(posX + 1, posY): self.tilemap.move(self, posX + 1, posY)

                # Right Down
                elif count == 7:

                    if self.check_tile(posX + 1, posY + 1): self.tilemap.move(self, posX + 1, posY + 1)

                # Down
                elif count == 6:

                    if self.check_tile(posX, posY + 1): self.tilemap.move(self, posX, posY + 1)

                # Left Down
                elif count == 5:

                    if self.check_tile(posX - 1, posY + 1): self.tilemap.move(self, posX - 1, posY + 1)

                # Left
                elif count == 3:

                    if self.check_tile(posX - 1, posY): self.tilemap.move(self, posX - 1, posY)


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


# -----------------------
# Enemy Stuff
# -----------------------


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
        self.radius = 20

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


class RandomEnemy(Enemy):

    def move(self):

        """
        Moves across the screen randomly.
        """

        # Get objects all around us:

        tile = self.tilemap.find_object(self)

        x = tile.x
        y = tile.y

        cords = [[x - 1, y], [x + 1, y], [x, y + 1], [x, y - 1], [x - 1, y - 1], [x + 1, y - 1], [x - 1, y + 1],
                 [x + 1, y + 1]]
        choices = []

        for targ in cords:

            if self.check_tile(targ[0], targ[1]):
                choices.append(targ)

        if len(choices) > 0:
            # Now, select a random choice from the options and move their:

            choice = random.choice(choices)

            self.tilemap.move(self, choice[0], choice[1])


"""
class TrackerEnemy(Enemy):

    def move(self):

        if self.debug_move:

            selfTile = self.tilemap.find_object(self)

            posX = selfTile.x
            posY = selfTile.y

            startX = posX - 1 if posX - 1 >= 0 else 0
            endX = posX + 1 if posX + 1 < self.tilemap.width else self.tilemap.width - 1

            startY = posY - 1 if posY - 1 >= 0 else 0
            endY = posY + 1 if posY + 1 < self.tilemap.height else self.tilemap.height - 1

            surroundingTiles = self.find_quickest_path(self.tilemap.find_object_type(Player))
            smallestNum = 0

            for element in surroundingTiles:

                smallestNum = element
                break

            for num in surroundingTiles:

                if num < smallestNum:

                    smallestNum = num

            if len(surroundingTiles) != 0:

                xMove = surroundingTiles[smallestNum][0]
                yMove = surroundingTiles[smallestNum][1]

                if self.check_tile(xMove, yMove):

                    self.tilemap.move(self, xMove, yMove)

                else:

                    playerTile = self.tilemap.find_object_type(Player)

                    # Player is left below Enemy
                    if playerTile.x <= selfTile.x and playerTile.y >= selfTile.y:

                        if self.check_tile(xMove, yMove + 1):

                            self.tilemap.move(self, xMove, yMove + 1)

                        elif self.check_tile(xMove - 1, yMove):

                            self.tilemap.move(self, xMove - 1, yMove)

                    # Player is left above Enemy
                    if playerTile.x <= selfTile.x and playerTile.y <= selfTile.y:

                        if self.check_tile(xMove, yMove - 1):

                            self.tilemap.move(self, xMove, yMove - 1)

                        elif self.check_tile(xMove - 1, yMove):

                            self.tilemap.move(self, xMove - 1, yMove)

                    # Player is right above Enemy
                    if playerTile.x >= selfTile.x and playerTile.y <= selfTile.y:

                        if self.check_tile(xMove, yMove - 1):

                            self.tilemap.move(self, xMove, yMove - 1)

                        elif self.check_tile(xMove + 1, yMove):

                            self.tilemap.move(self, xMove + 1, yMove)

                    # Player is right below Enemy
                    if playerTile.x >= selfTile.x and playerTile.y >= selfTile.y:

                        if self.check_tile(xMove, yMove + 1):

                            self.tilemap.move(self, xMove, yMove + 1)

                        elif self.check_tile(xMove + 1, yMove):

                            self.tilemap.move(self, xMove + 1, yMove)

            else:

                numberTileMap = self.find_quickest_path(self.tilemap.find_object_type(Player), blocked=True)

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

                '''
                # Printing tilemap------------------------------------------------------------------
                print("\n" * 2)
                for line in numberTileMap:

                    for col in line:

                        if isinstance(self.tilemap.get(x, y)[0].obj, Player):

                            print("C   ", end="")
                            foundPlayer = True

                        elif isinstance(self.tilemap.get(x, y)[0].obj, Enemy):

                            print("E   ", end="")

                        elif isinstance(self.tilemap.get(x, y)[0].obj, Wall):

                            print("W   ", end="")

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

                dictCopy = []

                xIndex = startX
                yIndex = startY

                while yIndex <= endY:

                    while xIndex <= endX:

                        if yIndex != posY or xIndex != posX:

                            if numberTileMap[yIndex][xIndex] > 0:

                                surroundingTiles[numberTileMap[yIndex][xIndex]] = [xIndex, yIndex]
                                dictCopy.append(numberTileMap[yIndex][xIndex])

                        xIndex += 1

                    xIndex = startX
                    yIndex += 1

                while len(dictCopy) > 0:

                    smallestNum = dictCopy[0]

                    for num in dictCopy:

                        if num < smallestNum:

                            smallestNum = num

                    xMove = surroundingTiles[smallestNum][0]
                    yMove = surroundingTiles[smallestNum][1]

                    if self.check_tile(xMove, yMove):

                        self.tilemap.move(self, xMove, yMove)
                        break

                    else:

                        dictCopy.remove(smallestNum)

            '''
            final = []

            for x in range(8):
                final.append(-1)

            index = 0

            # Iterate over each value:
            # Plus 2, because builtin range function will stop at that number, and not include it

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

                if num > -1 and num < leastNum:
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

                # Left Up
                if count == 0:

                    if self.check_tile(posX - 1, posY - 1): self.tilemap.move(self, posX - 1, posY - 1)

                # Up
                elif count == 1:

                    if self.check_tile(posX, posY - 1): self.tilemap.move(self, posX, posY - 1)

                # Right Up
                elif count == 2:

                    if self.check_tile(posX + 1, posY - 1): self.tilemap.move(self, posX + 1, posY - 1)

                # Right
                elif count == 4:

                    if self.check_tile(posX + 1, posY): self.tilemap.move(self, posX + 1, posY)

                # Right Down
                elif count == 7:

                    if self.check_tile(posX + 1, posY + 1): self.tilemap.move(self, posX + 1, posY + 1)

                # Down
                elif count == 6:

                    if self.check_tile(posX, posY + 1): self.tilemap.move(self, posX, posY + 1)

                # Left Down
                elif count == 5:

                    if self.check_tile(posX - 1, posY + 1): self.tilemap.move(self, posX - 1, posY + 1)

                # Left
                elif count == 3:

                    if self.check_tile(posX - 1, posY): self.tilemap.move(self, posX - 1, posY)

            
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

        else:
            self.debug_move = True
"""


class Skeleton(Enemy):

    def start(self):

        self.name = 'Skeleton'
        self.hp = 24
        self.damage_min = 8
        self.damage_max = 12
        self.damage_type = "physical"
        self.armor = .1
        self.description = ""

        self.auto.add(TrackerMove())


class Goblin(Enemy):

    def start(self):

        self.name = 'Goblin'
        self.hp = 24
        self.damage_min = 8
        self.damage_max = 12
        self.damage_type = "physical"
        self.armor = .1
        self.description = ""

        self.auto.add(TrackerMove())

# -------------------
# Look method
# -------------------

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

# --------------------------
# Old BaseWindow components
# --------------------------

def add_callback(self, key, call, pass_self=False, args=None):

    """
    Adds callback to be called when specified key is pressed.
    We accept functions, and can optionally pass a collection of arguments.

    :param key: Key to be pressed, can be string or list, special characters included
    :param call: Function to be called
    :param pass_self: Value determining if we should pass this object to the callback.
    :param args: Args to be passed to the function
        """

    if args is None:
        args = []

    if pass_self:
            args = [self] + args

    # Convert key to string

    if type(key) == list:

        # Working with a list

        for val in key:

            if type(val) == str:
                # Convert string into ascii value

                val = ord(val)

            self._calls[val] = {'call': call, 'args': args}

        return

    # Working with a single string here

    if type(key) == str:
        # Convert string into ascii value

        key = ord(key)

    # Add key/function/args to dictionary of keys to handle

    self._calls[key] = {'call': call, 'args': args}

    return

# --------------------------
# Old Player Class
# --------------------------

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
        self.move_priority = 18

        self.hp = 100
        self.active_weapon = None

        self.radius = 3

        self.keys = ['w', 'a', 's', 'd', 'q', 'e', 'z', 'c', 'p', 'i', 'l', 'o', 'y', ",", "."]

    def move(self):

        """
        Moves the character across the screen, or executes choices the player wants to make

        We accept input from the DisplayWindow here.
        """

        # Get input from the DisplayWindow

        inp = self.get_input()

        logging.info("Got input from queue: {}".format(inp))

        # Get our coordinates:

        playerTile = self.tilemap.find_object(self)

        if inp == 'w':

            # Move up:

            # Checks if the player is moving into a tile with a chest. If so, open it
            self.check_chest(playerTile.x, playerTile.y - 1)

            # Checks if the player is moving into a tile with an entity. If so, interact with it
            self.check_entity(playerTile.x, playerTile.y - 1)

            if self.check_tile(playerTile.x, playerTile.y - 1):
                self.tilemap.move(self, playerTile.x, playerTile.y - 1)

        elif inp == 'a':

            # Move left

            # Checks if the player is moving into a tile with a chest. If so, open it
            self.check_chest(playerTile.x - 1, playerTile.y)

            # Checks if the player is moving into a tile with an entity. If so, interact with it
            self.check_entity(playerTile.x - 1, playerTile.y)

            if self.check_tile(playerTile.x - 1, playerTile.y):
                self.tilemap.move(self, playerTile.x - 1, playerTile.y)

        elif inp == 's':

            # Move down

            # Checks if the player is moving into a tile with a chest. If so, open it
            self.check_chest(playerTile.x, playerTile.y + 1)

            # Checks if the player is moving into a tile with an entity. If so, interact with it
            self.check_entity(playerTile.x, playerTile.y + 1)

            if self.check_tile(playerTile.x, playerTile.y + 1):
                self.tilemap.move(self, playerTile.x, playerTile.y + 1)

        elif inp == 'd':

            # Move right

            # Checks if the player is moving into a tile with a chest. If so, open it
            self.check_chest(playerTile.x + 1, playerTile.y)

            # Checks if the player is moving into a tile with an entity. If so, interact with it
            self.check_entity(playerTile.x + 1, playerTile.y)

            if self.check_tile(playerTile.x + 1, playerTile.y):
                self.tilemap.move(self, playerTile.x + 1, playerTile.y)

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
                self.tilemap.scrollWin.add_content("Your inventory is empty", attrib="white")

            else:

                self.tilemap.scrollWin.add_content("Inventory: ", attrib="white")

                for x in self.inventory:

                    if isinstance(x, Item):
                        self.tilemap.scrollWin.add_content(x.name)

                self.tilemap.scrollWin.add_content("\n" * 0)

        elif inp == 'l':

            self.look(100)

            # self.tilemap.scrollWin.add_content("You don't see any objects in this room", "white")

        elif inp == 'o':

            groundContents = []

            for x in self.tilemap.get(playerTile.x, playerTile.y):

                if not isinstance(x.obj, Player) and not isinstance(x.obj, Floor):

                    groundContents.append(x)

            if len(groundContents) > 0:

                self.tilemap.scrollWin.add_content("Things on the ground: ", "white")

                for x in groundContents:

                    if not isinstance(x.obj, Player):
                        self.tilemap.scrollWin.add_content(x.obj.name)

                self.tilemap.scrollWin.add_content("\n" * 0)

        elif inp == 'y':

            self.tilemap.toggle_enemy_movement()

        elif inp == ',':

            if self.radius - 1 >= 0:

                self.radius -= 1

        elif inp == '.':

            if self.radius + 1 >= int(self.win.max_y / 2) - 1 or self.radius + 1 >= int(self.win.max_x / 2) - 1:

                if int(self.win.max_x / 2) - 1 < int(self.win.max_y / 2) - 1:

                    self.radius = int(self.win.max_x / 2) - 1

                else:

                    self.radius = int(self.win.max_y / 2) - 1

            elif self.radius + 1 >= int(self.tilemap.height / 2) and self.radius + 1 >= int(self.tilemap.width / 2):

                if int(self.tilemap.width / 2) < int(self.tilemap.height / 2):

                    self.radius = int(self.tilemap.height / 2)

                else:

                    self.radius = int(self.tilemap.width / 2)

            else:

                self.radius += 1

    def attack(self, targ):

        amountDamage = random.randrange(self.active_weapon.damage_min, self.active_weapon.damage_max + 1)

        if self.active_weapon.damage_type == "physical":

            self.tilemap.scrollWin.add_content("You strike the " + targ.name + " dealing, " + str(amountDamage) + " damage")

        targ.hp -= amountDamage

        if targ.hp < 0:

            targ.death()

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
                    self.tilemap.scrollWin.add_content(targObj.name + " added to inventory")

    def pickup_item(self, targObj):

        if isinstance(targObj, Item):

            # Checks if the object is allowed to be picked up

            if targObj.can_player_pickup:

                if self.check_inventory_bounds(targObj):
                    self.inventory.append(targObj)
                    self.inventory_space += targObj.size
                    self.tilemap.scrollWin.add_content(targObj.name + " added to inventory")

    def get_item(self, targObj):

        if isinstance(targObj, Item):

            if not self.check_inventory_bounds(targObj):

                playerPos = self.tilemap.get(self)
                self.tilemap.add(targObj, playerPos.x, playerPos.y)
                self.tilemap.scrollWin.add_content(f"You don't have enough space for the {targObj.name}")

            else:

                self.inventory.append(targObj)
                self.inventory_space += targObj.size
                self.tilemap.scrollWin.add_content(targObj.name + " added to inventory")

    def check_chest(self, xPos, yPos):

        if self.tilemap._bound_check(xPos, yPos):

            for i in self.tilemap.get(xPos, yPos):

                if isinstance(i.obj, Chest):

                    item = i.obj.open_chest()

                    if isinstance(item, Item):
                        self.tilemap.scrollWin.add_content(f"You found a {item.name} in a chest! ")
                        self.pickup_item(item)
                        self.tilemap.removeObj_by_coords(xPos, yPos)
                        self.tilemap.add(OpenedChest(), xPos, yPos)

    def check_entity(self, xPos, yPos):

        if self.tilemap._bound_check(xPos, yPos):

            for tile in self.tilemap.get(xPos, yPos):

                if isinstance(tile.obj, EntityCharacter):

                    tile.obj.interact(self)