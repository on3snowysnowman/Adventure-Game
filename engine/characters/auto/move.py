"""
This file will contain built in autoruns managing entity movement.

We currently have the following:

    > RandomMove - Randomly moves the entity to a position around it
"""

import random

from engine.characters.auto.base import BaseAutoRun


class RandomMove(BaseAutoRun):

    """
    RandomMove - Randomly moves the character to a position around it.
    """

    def run(self):
        
        # Find ourselves:

        entity = self.char.tilemap.find_object(self.char)

        # Get the tiles around us:

        tiles = self.char.tilemap.get_around(entity.x, entity.y)

        # Choose a random tile from the list:

        choice = random.choice(tiles)

        # Move the character to the location:

        self.char.tilemap.move(self.char, choice[0].x, choice[0].y)


class TrackerMove(BaseAutoRun):

    """
    Move towards a target
    """

    def __init__(self, target) -> None:
        super().__init__()

        self.target = target  # Target of the pathfinding, WILL BE A CHARACTER!

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

                        if not tile.obj.can_traverse and not isinstance(tile.obj, type(self)):
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

                        if isinstance(self.tilemap.get(x, y)[0].obj, self.target):

                            print("C   ", end="")
                            foundPlayer = True

                        elif isinstance(self.tilemap.get(x, y)[0].obj, type(self.char)):

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

            surroundingTiles = self.find_quickest_path(self.tilemap.find_object_type(self.target))
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

                    playerTile = self.tilemap.find_object_type(self.target)

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

                numberTileMap = self.find_quickest_path(self.tilemap.find_object_type(self.target), blocked=True)

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
