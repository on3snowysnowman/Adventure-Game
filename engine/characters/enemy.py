"""
Classes that represent hostile characters on the screen.

Are these redundant?

Perhaps implementing some more features into EntityCharacter would be better?
Something like a move algorithm, which if specified,
will be used to determine where the character will move.

# TODO: Figure these out!

Then, instead of creating a whole new class for a tracker enemy,  
one could just attach a 'random_move' move 'module' to the entity in question.
Will take some time to hash this out.

Should custom enemies be included?
Whats our distribution strategy?
Will users/developers be excpected to provide their own external enemies
and load them into the engine? What would this look like?
"""

import random

from engine.characters.base import EntityCharacter
from engine.characters.auto.move import TrackerMove
#from engine.characters.input import Player


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