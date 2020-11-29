from MethodFiles import *
from chascurses import *
import random

tilesX = []
tilesY = []
tilesZ = []

charIndexX = 0
charIndexY = 0


class Character:

    def __init__(self, display):

        self.display = display


class Wall:

    def __init__(self, display):

        self.display = display


class Weapon:

    def __init__(self, display, name):

        self.display = display
        self.name = name


class Enemy:

    def __init__(self, display, name):

        self.display = display
        self.name = name


character = Character("Character")
wall = Wall("Wall")
sword = Weapon("Weapon", "Sword")
goblin = Enemy("Enemy", "Goblin")
skeleton = Enemy("Enemy", "Skeleton")

tupleClasses = (Character, Wall, Enemy)
enemyBlockList = (Character, Wall, Enemy)


def mapDisplay(screenWin):

    global tilesY

    while True:

        screenWin.erase()
        for i in tilesY:

            for j in i:

                if j[len(j) - 1] == 0:

                    printC(j[len(j) - 1], screenWin, "blue", newLine = False)

                if isinstance(j[len(j) - 1], Character):

                    printC("C", screenWin, "green", newLine=False)

                elif isinstance(j[len(j) - 1], Wall):

                    printC("W", screenWin, "yellow", newLine=False)

                elif isinstance(j[len(j) - 1], Weapon):

                    printC("I", screenWin, "orange", newLine = False)

                elif isinstance(j[len(j) - 1], Enemy):

                    printC("E", screenWin, "red", newLine=False)


            printC("\n", screenWin)

        printC(f"Character : {tilesY[charIndexY][charIndexX]}", screenWin)
        enemyPos = findEnemies()

        i = 0

        while i < len(enemyPos):

            printC(f"Enemy {tilesY[enemyPos[i][0]][enemyPos[i][1]][len(tilesY[enemyPos[i][0]][enemyPos[i][1]]) - 1].name}: "
                   f"{tilesY[enemyPos[i][0]][enemyPos[i][1]]}", screenWin)
            i += 1
        printC(enemyPos, screenWin)
        #printC(charIndexY, screenWin)
        #printC(charIndexX, screenWin)

        key = screenWin.getkey()

        if key == "q":

            curses.endwin()
            break

        if move(key, screenWin):

            enemyMove(screenWin)

        sleep(.01)


def move(direction, screenWin):

    global tilesY, charIndexX, charIndexY, standingTile

    #Left
    if direction == "a":

        #Tries to move into an enemy

        if charIndexX - 1 >= 0 and isinstance(tilesY[charIndexY][charIndexX - 1][len(tilesY[charIndexY][charIndexX - 1]) - 1], Enemy):

            printC("You've encountered an enemy", screenWin)
            screenWin.getkey()

        #Checks tile if it's a class object

        elif charIndexX - 1 >= 0 and \
                isinstance(tilesY[charIndexY][charIndexX - 1][len(tilesY[charIndexY][charIndexX - 1]) - 1],
                           tupleClasses):

            #Checks if next tile is a wall

            if tilesY[charIndexY][charIndexX - 1][len(tilesY[charIndexY][charIndexX - 1]) - 1].display != wall.display:
                tilesY[charIndexY][charIndexX].remove(character)
                tilesY[charIndexY][charIndexX - 1].append(character)
                charIndexX -= 1

        #Moves to next tile

        else:

            if charIndexX - 1 >= 0:
                tilesY[charIndexY][charIndexX].remove(character)
                tilesY[charIndexY][charIndexX - 1].append(character)
                charIndexX -= 1

    #Right

    elif direction == "d":

        if charIndexX + 1 < len(tilesY[charIndexY]) and isinstance(tilesY[charIndexY][charIndexX + 1][len(tilesY[charIndexY][charIndexX + 1]) - 1], Enemy):

            printC("You've encountered an enemy", screenWin)
            screenWin.getkey()

        elif charIndexX + 1 < len(tilesY[charIndexY]) and \
                isinstance(tilesY[charIndexY][charIndexX + 1][len(tilesY[charIndexY][charIndexX + 1]) - 1], tupleClasses):

            if tilesY[charIndexY][charIndexX + 1][len(tilesY[charIndexY][charIndexX + 1]) - 1].display != wall.display:

                tilesY[charIndexY][charIndexX].remove(character)
                tilesY[charIndexY][charIndexX + 1].append(character)
                charIndexX += 1

        else:

            if charIndexX + 1 < len(tilesY[charIndexY]):

                tilesY[charIndexY][charIndexX].remove(character)
                tilesY[charIndexY][charIndexX + 1].append(character)
                charIndexX += 1

    #Up

    elif direction == "w":

        if charIndexY - 1 >= 0 and isinstance(tilesY[charIndexY - 1][charIndexX][len(tilesY[charIndexY - 1][charIndexX]) - 1], Enemy):

            printC("You've encountered an enemy", screenWin)
            screenWin.getkey()

        elif charIndexY - 1 >= 0 and \
                isinstance(tilesY[charIndexY - 1][charIndexX][len(tilesY[charIndexY - 1][charIndexX ]) - 1],
                           tupleClasses):

            if tilesY[charIndexY - 1][charIndexX][len(tilesY[charIndexY - 1][charIndexX]) - 1].display != wall.display:
                tilesY[charIndexY][charIndexX].remove(character)
                tilesY[charIndexY][charIndexX - 1].append(character)
                charIndexY -= 1

        else:

            if charIndexY - 1 >= 0:
                tilesY[charIndexY][charIndexX].remove(character)
                tilesY[charIndexY - 1][charIndexX ].append(character)
                charIndexY -= 1

    #Down

    elif direction == "s":

        if charIndexY + 1 < len(tilesY) and isinstance(tilesY[charIndexY + 1][charIndexX][len(tilesY[charIndexY + 1][charIndexX]) - 1], Enemy):

            printC("You've encountered an enemy", screenWin)
            screenWin.getkey()

        elif charIndexY + 1 < len(tilesY) and \
                isinstance(tilesY[charIndexY + 1][charIndexX][len(tilesY[charIndexY + 1][charIndexX]) - 1],
                           tupleClasses):

            if tilesY[charIndexY + 1][charIndexX][len(tilesY[charIndexY + 1][charIndexX]) - 1].display != wall.display:
                tilesY[charIndexY][charIndexX].remove(character)
                tilesY[charIndexY][charIndexX + 1].append(character)
                charIndexY += 1

        else:

            if charIndexY + 1 < len(tilesY):
                tilesY[charIndexY][charIndexX].remove(character)
                tilesY[charIndexY + 1][charIndexX].append(character)
                charIndexY += 1

    else: return False

    return True


def enemyMove(screenWin):

    enemyPos = findEnemies()
    i = 0

    while i < len(enemyPos):

        moveOptions = []

        #RIGHT
        #Checks if next tile is a class object
        if enemyPos[i][1] + 1 < len(tilesY[enemyPos[i][1]]) and \
                isinstance(tilesY[enemyPos[i][0]][enemyPos[i][1] + 1][len(tilesY[enemyPos[i][0]][enemyPos[i][1] + 1]) - 1], tupleClasses):

                #If next tile is NOT in enemyBlockList, add right to the move options
                if isinstance(tilesY[enemyPos[i][0]][enemyPos[i][1] + 1][len(tilesY[enemyPos[i][0]][enemyPos[i][1] + 1]) - 1], enemyBlockList) is False:

                    moveOptions.append("right")
        else:

            if enemyPos[i][1] + 1 < len(tilesY[enemyPos[i][1]]):

                moveOptions.append("right")

        #LEFT
        #Checks if next tile is a class object
        if enemyPos[i][1] - 1 >= 0 and \
                isinstance(tilesY[enemyPos[i][0]][enemyPos[i][1] - 1][len(tilesY[enemyPos[i][0]][enemyPos[i][1] - 1]) - 1], tupleClasses):

            # If next tile is NOT in enemyBlockList, add left to the move options
            if isinstance(tilesY[enemyPos[i][0]][enemyPos[i][1] - 1][len(tilesY[enemyPos[i][0]][enemyPos[i][1] - 1]) - 1], enemyBlockList) is False:

                moveOptions.append("left")
        else:

            if enemyPos[i][1] - 1 >= 0:

                moveOptions.append("left")

        #DOWN
        # Checks if next tile is a class object
        if enemyPos[i][0] + 1 < len(tilesY) and \
                isinstance(tilesY[enemyPos[i][0] + 1][enemyPos[i][1]][len(tilesY[enemyPos[i][0] + 1][enemyPos[i][1]]) - 1], tupleClasses):

            # If next tile is NOT in enemyBlockList, add down to the move options
            if isinstance(tilesY[enemyPos[i][0] + 1][enemyPos[i][1]][len(tilesY[enemyPos[i][0] + 1][enemyPos[i][1]]) - 1], enemyBlockList) is False:

                moveOptions.append("down")
        else:

            if enemyPos[i][0] + 1 < len(tilesY):

                moveOptions.append("down")

        #UP
        # Checks if next tile is a class object
        if enemyPos[i][0] - 1 >= 0 and \
                isinstance(tilesY[enemyPos[i][0] - 1][enemyPos[i][1]][len(tilesY[enemyPos[i][0] - 1][enemyPos[i][1]]) - 1], tupleClasses):

            # If next tile is NOT in enemyBlockList, add up to the move options
            if isinstance(tilesY[enemyPos[i][0] - 1][enemyPos[i][1]][len(tilesY[enemyPos[i][0] - 1][enemyPos[i][1]]) - 1], enemyBlockList) is False:

                moveOptions.append("up")
        else:

            if enemyPos[i][0] - 1 >= 0:

                moveOptions.append("up")

        #Stays in place
        moveOptions.append("stay")

        if len(moveOptions) > 0:

            moveDirection = random.choice(moveOptions)

            if moveDirection == "right":

                tilesY[enemyPos[i][0]][enemyPos[i][1] + 1].append(tilesY[enemyPos[i][0]][enemyPos[i][1]][len(tilesY[enemyPos[i][0]][enemyPos[i][1]]) - 1])
                del tilesY[enemyPos[i][0]][enemyPos[i][1]][len(tilesY[enemyPos[i][0]][enemyPos[i][1]]) - 1]

            elif moveDirection == "left":

                tilesY[enemyPos[i][0]][enemyPos[i][1] - 1].append(tilesY[enemyPos[i][0]][enemyPos[i][1]][len(tilesY[enemyPos[i][0]][enemyPos[i][1]]) - 1])
                del tilesY[enemyPos[i][0]][enemyPos[i][1]][len(tilesY[enemyPos[i][0]][enemyPos[i][1]]) - 1]

            elif moveDirection == "down":

                tilesY[enemyPos[i][0] + 1][enemyPos[i][1]].append(tilesY[enemyPos[i][0]][enemyPos[i][1]][len(tilesY[enemyPos[i][0]][enemyPos[i][1]]) - 1])
                del tilesY[enemyPos[i][0]][enemyPos[i][1]][len(tilesY[enemyPos[i][0]][enemyPos[i][1]]) - 1]

            elif moveDirection == "up":

                tilesY[enemyPos[i][0] - 1][enemyPos[i][1]].append(tilesY[enemyPos[i][0]][enemyPos[i][1]][len(tilesY[enemyPos[i][0]][enemyPos[i][1]]) - 1])
                del tilesY[enemyPos[i][0]][enemyPos[i][1]][len(tilesY[enemyPos[i][0]][enemyPos[i][1]]) - 1]

            elif moveDirection == "stay":

                pass

        i += 1


def countActiveEnemies():

    numActiveEnemies = 0

    for i in tilesY:

        for j in i:

            if isinstance(j[len(j) - 1], Enemy):

                numActiveEnemies += 1

    return numActiveEnemies


def findEnemies():

    enemyPos = []

    iCount = 0
    jCount = 0

    for i in tilesY:

        for j in i:

            if isinstance(j[len(j) - 1], Enemy):

                enemyPos.append([iCount, jCount])
            jCount += 1

        jCount = 0
        iCount += 1

    return enemyPos

