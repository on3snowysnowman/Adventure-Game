import random
from MethodFiles import *
from chascurses import *
from threading import *
import cursor
import curses

#pause()
cursor.hide()

key = ""
i = 0
runningLoop = False

# Threads


def BaseCheck():

    global oilTank, rawAlloyStorage, rawAlloyStorageCapacity, playerBombs, playerPower, alloyStorage
    global alloyStorageCapacity, runningLoop, i

    while True:

        if continueLoop:

            runningLoop = True

            playerPower = 0
            j = 0

            # Cycling through Utility lists to find which ones need power

            totalPowerNeeded = 0

            #Oil Wells
            for x in oilWellList:

                if x.health > 0 and x.activated is True and x.playerActivated is True:

                    totalPowerNeeded += x.powerReq

            # Oil Refineries:
            '''
            for x in oilRefineryList:

                if x.health > 0 and x.activated is True and x.playerActivated is True:
                    totalPowerNeeded += x.powerReq

                runningLoop = True
            '''

            # Alloy Refineries
            for x in alloyRefineryList:

                if x.health > 0 and x.activated is True and x.playerActivated is True and x.rawAlloy >= 2:

                    totalPowerNeeded += x.powerReq

            #Deactivating Reactors
            for x in reactorList:

                x.activated = False

            #Reactivating Reactors until reached requirement
            currentPowerNum = 0

            for x in reactorList:

                if currentPowerNum < totalPowerNeeded:

                    x.activated = True
                    currentPowerNum += x.powerGen

            # Generating Power
            if len(reactorList) > 0:

                while j < len(reactorList):

                    if reactorList[j].health > 0 and reactorList[j].playerActivated is True and reactorList[
                        j].fuel - 2 >= 0 \
                            and totalPowerNeeded != 0:

                        playerPower += reactorList[j].powerGen
                        reactorList[j].fuel -= 2

                    elif reactorList[j].health > 0 and reactorList[j].playerActivated is True and reactorList[j].fuel - 2 >= 0 \
                            and totalPowerNeeded != 0 and playerPower + reactorList[j].powerGen <= totalPowerNeeded:

                        playerPower += reactorList[j].powerGen
                        reactorList[j].fuel -= 2

                    j += 1

            # Oil Well------------------------------------------------------------------------------------------------------------

            # Resetting all Power to wells
            for x in oilWellList:
                x.activePower = 0

            # Deactivating Oil Wells if it's full
            for x in oilWellList:

                if x.oil == x.oilCapacity:

                    x.activated = False

            # Reactivating Oil Wells if its not full
            for x in oilWellList:

                if x.oil != x.oilCapacity: x.activated = True

            # Adding Power to Wells
            x = 0

            while playerPower > 0 and x != len(oilWellList):

                if oilWellList[x].playerActivated is True and oilWellList[x].activated is True and oilWellList[
                    x].health > 0:

                    playerPower -= oilWellList[x].powerReq
                    oilWellList[x].activePower = oilWellList[x].powerReq

                x += 1

            # Extracting Oil
            if len(oilWellList) > 0:

                j = 0

                while j < len(oilWellList):

                    if oilWellList[j].health > 0 and oilWellList[j].playerActivated is True and oilWellList[
                        j].activated is True:

                        if oilWellList[j].activePower >= oilWellList[j].powerReq and oilWellList[j].oil + 6 > oilWellList[j].oilCapacity:

                            oilWellList[j].oil = oilWellList[j].oilCapacity

                        elif oilWellList[j].activePower >= oilWellList[j].powerReq:

                            oilWellList[j].oil += oilWellList[j].oilGeneration

                    j += 1

                j = 0

            # ---------------------------------------------------------------------------------------------------------------

            # Oil Refinery---------------------------------------------------------------------------------------------------

            '''
            #Resetting Power to Refineries
            for x in oilRefineryList:
 
                x.activePower = 0
 
            #Deactivating Oil Refineries if tank(s) is full
            for x in oilRefineryList:
 
                if x.lightOilCapacity + x.lightOilGeneration > x.lightOilCapacity or \
                        x.heavyOilCapacity + x.heavyOilGeneration > x.heavyOilCapacity: x.activated = False
 
            #Reactivating Oil Refineries if tank(s) are not full
            for x in oilRefineryList:
 
                if x.lightOilCapacity + x.lightOilGeneration <= x.lightOilCapacity or \
                        x.heavyOilCapacity + x.heavyOilGeneration <= x.heavyOilCapacity: x.activated = True
 
            #Adding power to Oil Refineries
            x = 0
 
            while playerPower > 0 and x != len(oilRefineryList):
 
                if oilRefineryList[x].playerActivated is True and oilRefineryList[x].activated is True and oilRefineryList[
                    x].health > 0:
                    playerPower -= oilRefineryList[x].powerReq
                    oilRefineryList[x].activePower = oilRefineryList[x].powerReq
 
                x += 1
 
 
            #Refining Oil
            if len(oilRefineryList) > 0 and lightOilTank + oilRefinery.lightOilGeneration <= lightOilTankCapacity\
                    and heavyOilTank + oilRefinery.heavyOilGeneration <= heavyOilTankCapacity:
 
                j = 0
 
                while oilTank + oilWell.oilGeneration <= oilTankCapacity and j < len(oilWellList):
 
                    if oilWellList[j].health > 0 and oilWellList[j].playerActivated is True and oilWellList[
                        j].activated is True:
 
                        if oilWellList[j].activePower >= oilWellList[j].powerReq:
                            oilWellList[j].oil += 6
 
                    j += 1
 
                j = 0
 
            '''
            # Alloy Mines----------------------------------------------------------------------------------------------------

            # Deactivating Alloy Mines if storage is full
            for x in alloyMineList:

                if x.rawAlloy + x.rawAlloyGeneration > x.rawAlloyCapacity: x.activated = False

            # Reactivating Alloy Mines if storage is not full
            for x in alloyMineList:

                if x.rawAlloy + x.rawAlloyGeneration <= x.rawAlloyCapacity: x.activated = True

            # Generating Raw Alloy
            if len(alloyMineList) > 0:

                j = 0

                while j < len(alloyMineList):

                    if alloyMineList[j].health > 0 and alloyMineList[j].activated is True and alloyMineList[
                        j].playerActivated is True:

                        if alloyMineList[j].fuel > 0:
                            alloyMineList[j].rawAlloy += alloyMineList[j].rawAlloyGeneration
                            alloyMineList[j].fuel -= 1

                    j += 1

            # ---------------------------------------------------------------------------------------------------------------

            # Alloy Refineries-----------------------------------------------------------------------------------------------

            # Resetting power to Refineries

            for x in alloyRefineryList:
                x.activePower = 0

            x = 0

            # Deactivating Alloy Refineries

            for x in alloyRefineryList: x.activated = False

            # Activating Refineries if storage is not full or they are filled
            for x in alloyRefineryList:

                if x.alloy + x.alloyGeneration <= x.alloyCapacity and x.rawAlloy >= 2:

                    x.activated = True

            x = 0

            # Adding Power to Refineries
            while x != len(alloyRefineryList):

                if alloyRefineryList[x].playerActivated is True and alloyRefineryList[x].activated is True and \
                        alloyRefineryList[x].health > 0 \
                        and playerPower - alloyRefineryList[x].powerReq >= 0:

                    playerPower -= alloyRefineryList[x].powerReq
                    alloyRefineryList[x].activePower = alloyRefineryList[x].powerReq

                x += 1

            # Refining Raw Alloy
            if len(alloyRefineryList) > 0:

                j = 0

                while j < len(alloyRefineryList) and alloyStorage + 2 < alloyStorageCapacity:

                    if alloyRefineryList[j].health > 0 and alloyRefineryList[j].activated is True and alloyRefineryList[
                        j].playerActivated is True:

                        if alloyRefinery.activePower >= alloyRefinery.powerReq:

                            alloyStorage += alloyRefineryList[j].alloyOut

                    j += 1


            # ---------------------------------------------------------------------------------------------------------------

            sleep(1)


def OptionMenu(screenWin):

    global runningLoop

    runningLoop = True

    optionWin = OptionWindow.create_subwin_at_pos(screenWin, 12, 50, position=OptionWindow.BOTTOM_LEFT)
    #qoptionWin.add_options(recourceMenu)
    optionWin.add_option("test", optionWin.TOGGLE_SELECT)
    optionWin.add_option("Empty Oil", optionWin.RUN_OPTION, value=emptyOilWells)
    optionWin.display()

    runningLoop = False

# Curse Windows
'''
def displayRecourceMenu(screenWin):

    global key, continueLoop, playerPower, runningLoop

    menuThread = Thread(target=OptionMenu, args = [screenWin])
    menuThread.daemon = True
    menuThread.start()

    while True:

        curses.flushinp()
        curses.halfdelay(1)
        screenWin.clear()
        printC(f"Oil Tank: {oilTank}", screenWin, newLine = False)
        gaugeDisplay(oilTank, oilTankCapacity, screenWin)
        printC(f"{oilTankCapacity}", screenWin, newLine = False)
        printC("\n" * 1, screenWin)
        #printC(f"i: {i}")
        #printC("\n" * 1)
        checkOilWell(screen)
        #printC(f"ContinueLoop : {continueLoop}\n")
        printC("\n" * 1, screenWin)
        printC(f"Raw Alloy Storage: {rawAlloyStorage}", screenWin, newLine = False)
        gaugeDisplay(rawAlloyStorage, rawAlloyStorageCapacity, screenWin)
        printC(f"{rawAlloyStorageCapacity}", screenWin, newLine = False)
        printC("\n" * 1, screenWin)
        checkAlloyMines(screen)
        printC(f"Alloy Storage: {alloyStorage}", screenWin)
        printC("\n" * 1, screenWin)
        checkAlloyRefineries(screen)
        printC(f"Power Being Produced: {getTotalPower()}", screenWin)
        printC(f"Total Available Power: {playerPower}", screenWin)
        printC("\n" * 2, screenWin)
        checkReactors(screen)
        printC("\n" * 1, screenWin)
        #printC(f"Loop : {runningLoop}\n")
        printC("\n" * 1, screenWin)

        #printC("\n" * 1)
        printC(
            "1:Empty Oil Wells\n2:Empty Alloy Mines\n3:Fuel Alloy Mines\n4:Fill Alloy Refineries\n5:Fuel Alloy Refineries\n6:Fuel Reactors\nb:Break", screenWin)
        printC("\n", screenWin)
        screenWin.refresh()

        try:

            key = screen.getkey()

        except:

            continue

        if key == "1":

            emptyOilWells()


        elif key == "2":

            emptyAlloyMines()

        elif key == "3":

            fuelAlloyMines()

        elif key == "4":

            fillAlloyRefineries()

        elif key == "5":

            fuelAlloyRefineries()

        elif key == "6":

            fuelReactors()

        elif key == "b":

            break

        key = " "

    curses.endwin()
    
'''


def displayRecourceMenu(screenWin):

    global key, continueLoop, playerPower, runningLoop

    startCurs(screenWin)

    menuThread = Thread(target=OptionMenu, args=[screenWin])
    menuThread.daemon = False
    menuThread.start()

    subWin = screenWin.derwin(28, 100, 0, 0)

    subWin.scrollok(True)
    subWin.keypad(True)
    subWin.nodelay(True)

    while runningLoop:

        #curses.flushinp()
        curses.halfdelay(1)
        subWin.erase()
        printC(f"Oil Tank: {oilTank}", subWin, newLine=False)
        gaugeDisplay(oilTank, oilTankCapacity, subWin)
        printC(f"{oilTankCapacity}", subWin, newLine=False)
        printC("\n" * 1, subWin)
        #printC(f"i: {i}")
        #printC("\n" * 1)
        checkOilWell(subWin)
        #printC(f"ContinueLoop : {continueLoop}\n")
        printC("\n" * 1, subWin)
        printC(f"Raw Alloy Storage: {rawAlloyStorage}", subWin, newLine=False)
        gaugeDisplay(rawAlloyStorage, rawAlloyStorageCapacity, subWin)
        printC(f"{rawAlloyStorageCapacity}", subWin, newLine = False)
        printC("\n" * 1, subWin)
        checkAlloyMines(subWin)
        printC(f"Alloy Storage: {alloyStorage}", subWin)
        printC("\n" * 1, subWin)
        checkAlloyRefineries(subWin)
        printC(f"Power Being Produced: {getTotalPower()}", subWin)
        printC(f"Total Available Power: {playerPower}", subWin)
        printC("\n" * 2, subWin)
        checkReactors(subWin)
        printC("\n" * 1, subWin)
        #printC(f"Loop : {runningLoop}\n")
        printC("\n" * 1, subWin)

        subWin.refresh()

# Classes


class Fighter:

    def __init__(self, name, health, healthMax, damage, fuel, fuelMax):
        self.name = name
        self.health = health
        self.healthMax = healthMax
        self.damage = damage

    def attack(self, dam, tar):
        tar -= random.randrange(dam - 3, dam + 3)

    def getHealth(self, h):
        slowPrint(f"This Fighter is at {h} Health")

    def getFuel(self, f):
        slowPrint(f"This Fighter has {f} Fuel")


class Bomber:

    def __init__(self, name, health, healthMax, damage, fuel, fuelMax):

        self.name = name
        self.health = health
        self.healthMax = healthMax
        self.damage = damage

    def shipCheck(self, target):

        if target in bomberShipList: return True

        return False

    def munitionCheck(self, amount):

        if amount <= 0: return False

        return True

    def getHealth(self, h, ):

        slowPrint(f"This Bomber is at {h} Health")

    def getFuel(self, f, ):

        slowPrint(f"This Bomber has {f} Fuel")

    def attack(self, dam, tar, amount):

        tar -= random.randrange(dam - 3, dam + 3)
        amount -= 1


class Interceptor:

    def __init__(self, name, health, healthMax, damage, fuel, fuelMax):
        self.name = name
        self.health = health
        self.healthMax = healthMax
        self.damage = damage

    def attack(self, dam, tar):
        tar -= random.randrange(tar - 3, tar + 3)

    def getHealth(self, h):
        slowPrint(f"This Interceptor is at {h} Health")

    def getFuel(self, f):
        slowPrint(f"This Interceptor has {f} Fuel")


class Freighter:

    def __init__(self, name, alloyCargo, alloyCargoMax, oilCargo, oilCargoMax, health, healthMax, fuel, fuelMax):

        self.name = name
        self.alloyCargo = alloyCargo
        self.alloyCargoMax = alloyCargoMax
        self.oilCargo = oilCargo
        self.oilCargoMax = oilCargoMax
        self.health = health
        self.healthMax = healthMax
        self.fuel = fuel
        self.fuelMax = fuelMax

    def getAlloyCargo(self, aC, ):

        if aC > 1:
            slowPrint(f"This Freighter contains {aC} Alloy")

        slowPrint("This Freighter contains no Alloy")

    def getFuelCargo(self, fC):

        if fC > 1:
            return f"This Freighter contains {fC} Fuel"

        return "This Freighter has no fuel"

    def getHealth(self, h):

        slowPrint(f"This Freighter is at {h} Health")

    def getFuel(self, f):

        slowPrint(f"This Freighter has {f} Fuel")


class Dreadnaught:

    def __init__(self, name, health, damage, fuel, fuelMax, oilCargo, oilCargoMax, alloyCargo, alloyCargoMax):
        self.name = name
        self.health = health
        self.damage = damage
        self.fuel = fuel
        self.fuelMax = fuelMax
        self.oilCargo = oilCargo
        self.oilCargoMax = oilCargoMax
        self.alloyCargo = alloyCargo
        self.alloyCargoMax = alloyCargoMax

    def getHealth(self, h):
        slowPrint(f"This Dreadnaught is at {h} Health")


class Reactor:

    def __init__(self, health, powerGen, fuel, fuelMax, activated, playerActivated):

        self.health = health
        self.powerGen = powerGen
        self.fuel = fuel
        self.fuelMax = fuelMax
        self.activated = activated
        self.playerActivated = playerActivated

    def getHealth(self, h, targType=0):

        if targType == "str":
            slowPrint(f"This Reactor has {h} Health")
            return

        return h

    def getPower(self, p, targType=0):

        if targType == "str":
            slowPrint(f"This Reactor generates {p} Power")
            return

        return p


class OilWell:

    def __init__(self, health, activePower, powerReq, oilGeneration, activated, playerActivated, oil, oilCapacity):
        self.health = health
        self.activePower = activePower
        self.powerReq = powerReq
        self.oilGeneration = oilGeneration
        self.activated = activated
        self.playerActivated = playerActivated
        self.oil = oil
        self.oilCapacity = oilCapacity

    def getOilGen(self, generation, targType=0):
        slowPrint(f"This Oil Well generates {generation}")

    def getHealth(self, h, targType=0):
        slowPrint(f"This Oil Well is at {h} Health")


class OilRefinery:

    def __init__(self, health, activePower, powerReq, lightOilGeneration, heavyOilGeneration, activated,
                 playerActivated, oil, lightOil, heavyOil, oilCapacity, lightOilCapacity, heavyOilCapacity,
                 typeConversion):
        self.health = health
        self.activePower = activePower
        self.powerReq = powerReq
        self.lightOilGeneration = lightOilGeneration
        self.heavyOilGeneration = heavyOilGeneration
        self.playerActivated = playerActivated
        self.oil = oil
        self.lightOil = lightOil
        self.heavyOil = heavyOil
        self.oilCapacity = oilCapacity
        self.lightOilCapacity = lightOilCapacity
        self.heavyOilCapacity = heavyOilCapacity
        self.typeConversion = typeConversion


class AlloyMine:

    def __init__(self, health, healthMax, fuel, fuelMax, rawAlloy, rawAlloyCapacity, rawAlloyGeneration,
                 playerActivated):

        self.health = health
        self.healthMax = healthMax
        self.fuel = fuel
        self.fuelMax = fuelMax
        self.rawAlloy = rawAlloy
        self.rawAlloyCapacity = rawAlloyCapacity
        self.rawAlloyGeneration = rawAlloyGeneration
        self.playerActivated = playerActivated

    def getRawAlloy(self, a, targType=0):

        slowPrint(f"This Alloy Mine contains {a} Raw Alloy")

    def getRawAlloyCapacity(self, aC):

        slowPrint(f"This Alloy Mine Capacity is {aC} Raw Alloy")

    def getHealth(self, h):

        slowPrint(f"This Alloy Mine is at {h} Health")

    def getFuel(self, f):

        slowPrint(f"This Alloy Mine contains {f} Fuel")

    def getRawAlloyGeneration(self, rAG):

        slowPrint(f"This Alloy Mine generates {rAG}")

    def getActivated(self, active):

        if active is True:

            slowPrint("This Alloy Mine is active")

        else:
            slowPrint("This Alloy Mine is not activated")

    def activateMine(self, activator):

        activator = True


class AlloyRefinery:

    def __init__(self, health, powerReq, activePower, rawAlloy, rawAlloyCapacity,
                 rawAlloyTakeIn, alloyGeneration, alloy, alloyCapacity, activated, playerActivated):
        self.health = health
        self.powerReq = powerReq
        self.activePower = activePower
        self.rawAlloy = rawAlloy
        self.rawAlloyCapacity = rawAlloyCapacity
        self.rawAlloyTakeIn = rawAlloyTakeIn
        self.alloyGeneration = alloyGeneration
        self.alloy = alloy
        self.alloyCapacity = alloyCapacity
        self.activated = activated
        self.playerActivated = playerActivated


# Functions
def startCurs(subWin):
    global continueLoop

    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)

    curses.noecho()
    curses.cbreak()
    subWin.scrollok(True)
    subWin.keypad(True)
    subWin.nodelay(True)
    continueLoop = True


def endCurs():
    curses.endwin()
    curses.echo()
    curses.nocbreak()
    screen.scrollok(False)
    screen.keypad(False)
    screen.nodelay(False)


def repair(h, hM, pA):
    h = hM
    pA -= 4 * (hM - h)


def emptyOilWells():

    global oilTank, continueLoop

    oil = 0
    j = 0

    while j < len(oilWellList) and oilTank + oilWellList[j].oil <= oilTankCapacity:
        oil += oilWellList[j].oil
        oilTank += oilWellList[j].oil
        oilWellList[j].oil = 0
        j += 1

    if oil > 0:

        '''
        clearScreen()
        slowPrintCustom("Emptying Fuel Wells", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        clearScreen(.3)
        '''

    else:

        clearScreen()
        slowPrint("Your Oil Wells are empty! ")

    startCurs(displayRecourceMenu)


def emptyAlloyMines():

    global rawAlloyStorage, rawAlloyStorageCapacity, continueLoop

    endCurs()

    continueLoop = False

    alloy = 0
    j = 0

    while j < len(alloyMineList) and rawAlloyStorage + alloyMineList[j].rawAlloy <= rawAlloyStorageCapacity:
        alloy += alloyMineList[j].rawAlloy
        rawAlloyStorage += alloyMineList[j].rawAlloy
        alloyMineList[j].rawAlloy = 0
        j += 1

    alloyNum = alloyStorageCapacity - rawAlloyStorage

    for x in alloyMineList:

        if x.rawAlloy >= alloyNum and rawAlloyStorage != alloyStorageCapacity:
            rawAlloyStorage = alloyStorageCapacity
            x.rawAlloy -= alloyNum

    if alloy > 0:

        clearScreen()
        slowPrintCustom("Emptying Alloy Mines", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        clearScreen(.3)

    elif rawAlloyStorage == rawAlloyStorageCapacity:

        clearScreen()
        slowPrint("Your Alloy Mines are empty! ")

    else:

        clearScreen()
        slowPrint("Your Raw Alloy Storage is full! ")

    startCurs(displayRecourceMenu)


def fuelAlloyMines():
    global oilTank, continueLoop

    endCurs()

    continueLoop = False

    j = 0
    fuelNeeded = 0

    while j < len(alloyMineList):

        fuelNeeded = alloyMineList[j].fuelMax - alloyMineList[j].fuel

        if oilTank - fuelNeeded >= 0:

            alloyMineList[j].fuel += fuelNeeded
            oilTank -= fuelNeeded

        else:

            alloyMineList[j].fuel = alloyMineList[j].fuel + oilTank
            oilTank = 0

        j += 1

    if fuelNeeded > 0 and oilTank != 0:

        clearScreen()
        slowPrintCustom("Fueling Alloy Mines", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        clearScreen(.3)

    else:

        clearScreen()
        slowPrint("Your Oil Tank is empty! ")

    startCurs(displayRecourceMenu)


def fuelAlloyRefineries():
    global oilTank, continueLoop

    endCurs()

    continueLoop = False

    fuelNeeded = 0

    if oilTank == 0:
        clearScreen()
        slowPrint("Your Oil Tank is empty!")
        startCurs(displayRecourceMenu)

    for x in alloyRefineryList:

        fuelNeeded = x.fuelMax - x.fuel

        if oilTank - fuelNeeded >= 0:

            x.fuel += fuelNeeded
            oilTank -= fuelNeeded

        else:

            x.fuel += oilTank
            oilTank = 0

    if fuelNeeded > 0:

        clearScreen()
        slowPrintCustom("Fueling Alloy Refineries", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        clearScreen(.3)

    else:

        clearScreen()
        slowPrint("Your Oil Tank is empty! ")

    startCurs(displayRecourceMenu)


def fillAlloyRefineries():
    global rawAlloyStorage, continueLoop

    endCurs()

    continueLoop = False

    if rawAlloyStorage <= 0:
        clearScreen()
        slowPrint("Your Raw Alloy storage is empty! ")
        continueLoop = True
        curses.wrapper(displayRecourceMenu)

    alloy = 0
    alloyNeeded = 0

    for x in alloyRefineryList:

        alloyNeeded = x.rawAlloyCapacity - x.rawAlloy

        if rawAlloyStorage - alloyNeeded >= 0:

            x.rawAlloy += alloyNeeded
            rawAlloyStorage -= alloyNeeded
            alloy += alloyNeeded

        elif rawAlloyStorage - alloyNeeded < 0:

            x.rawAlloy += rawAlloyStorage
            rawAlloyStorage = 0
            alloy += alloyNeeded

    if alloy > 0 and alloyNeeded > 0:

        clearScreen()
        slowPrintCustom("Filling Alloy Refineries", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        clearScreen(.3)

    else:

        clearScreen()
        slowPrint("Your Refineries are full! ")

    startCurs(displayRecourceMenu)


def fuelReactors():
    global oilTank, continueLoop

    endCurs()

    continueLoop = False

    if oilTank == 0:
        clearScreen()
        slowPrintCustom("Your Oil Tank is empty! ", pauseBool=False, clearBool=False)
        clearScreen(.3)
        startCurs(displayRecourceMenu)
        return

    j = 0
    fuelNeeded = 0

    while j < len(reactorList):

        fuelNeeded = reactorList[j].fuelMax - reactorList[j].fuel

        if oilTank - fuelNeeded >= 0:

            reactorList[j].fuel += fuelNeeded
            oilTank -= fuelNeeded

        else:

            reactorList[j].fuel = reactorList[j].fuel + oilTank
            oilTank = 0

        j += 1

    if fuelNeeded > 0:

        clearScreen()
        slowPrintCustom("Fueling Reactors", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        slowPrintCustom(".", pauseBool=False, clearBool=False, sleepTime=.4)
        clearScreen(.3)

    elif fuelNeeded == 0:

        clearScreen()
        slowPrint("Your Reactors are fully fueled already!")

    startCurs(displayRecourceMenu)


def getTotalPower():

    totalPower = 0

    for x in reactorList:

        if x.fuel > 0 and x.activated is True and x.playerActivated is True:
            totalPower += x.powerGen

    return totalPower


# Ships
fighter = Fighter("Fighter", 10, 10, 5, 100, 100)
bomber = Bomber("Bomber", 30, 30, 50, 100, 100)
finterceptor = Interceptor("Interceptor", 50, 50, 40, 50, 50)
freighter = Freighter("Freighter", 0, 1000, 0, 1000, 800, 800, 2000, 2000)

# Base Objects
reactor = Reactor(500, 1000, 300, 300, True, True)
upgradedReactor = Reactor(1000, 400, 500, 500, True, True)
oilWell = OilWell(300, 0, 100, 6, True, True, 0, 500)
oilRefinery = OilRefinery(300, 0, 200, 7, 5, True, True, 0, 0, 0, 500, 300, 300, 0)
upgradedOilWell = OilWell(600, 0, 200, 15, True, True, 0, 1000)
alloyMine = AlloyMine(500, 500, 200, 200, 0, 500, 10, True)
upgradedAlloyMine = AlloyMine(1000, 1000, 400, 400, 0, 1000, 20, True)
alloyRefinery = AlloyRefinery(1000, 400,  4, 0, 800, 2, 1, 0, 400, True, True)

# Bomber Targets
bomberShipList = ["Freighter", "BattleShip", "Dreadnaught"]

# Player Collectives
playerPower = 0
playerBombs = 1

# Player Fleet
fighterList = []
bomberList = []
freighterList = []

# Enemy Fleet
enemyFighterList = []
enemyBomberList = []
enemyFreighterList = []

# Base Objects List
reactorList = []
oilWellList = []
oilRefineryList = []
alloyMineList = []
alloyRefineryList = []

# Raw Alloy
rawAlloyStorage = 500
rawAlloyStorageCapacity = 2000

# Alloy
alloyStorage = 0
alloyStorageCapacity = 2000

# Oil
oilTank = 0
oilTankCapacity = 2000
lightOilTank = 0
lightOilTankCapacity = 2000
heavyOilTank = 0
heavyOilTankCapacity = 2000

# Loop Booleans
continueLoop = True

# Upgrades
availableUpgrades = ["reinforced alloy", "ship shields", "faster production", "improved reactor efficiency",
                     "fighter damage upgrade", "ion bombs", "improved ion bombs"]
activeUpgrades = []

# Research
researchPoints = 0

#Dictionary for displayRecourceMenu
recourceMenu = {"Empty Oil Wells" : emptyOilWells}


for i in range(1):
    reactorList.append(objectCopy(reactor))
    oilWellList.append(objectCopy(oilWell))
    #oilRefineryList.append(objectCopy(oilRefinery))
    alloyMineList.append(objectCopy(alloyMine))
    alloyRefineryList.append(objectCopy(alloyRefinery))


def displayReactors():
    powerCount = 0
    rCount = len(reactorList)

    for x in reactorList:
        powerCount += reactor.powerGen

    if rCount == 0:
        slowPrint("You have no Reactors")

    elif rCount == 1:

        waitPrint("You have 1 Reactor,")
        slowPrint(f" generating {powerCount} Power")

    else:
        slowPrint(f"You have {rCount} Reactors, generating {powerCount} Power")


def displayOilWells():
    oilCount = 0
    oCount = len(oilWellList)

    for x in oilWellList:
        oilCount += oilWell.oilGeneration
    if oCount == 0:
        slowPrint("You have no Oil Wells")

    elif oCount == 1:

        waitPrint("You have 1 Oil Well,")
        slowPrint(f" extracting {oilWell.oilGeneration} Oil per second")

    else:
        slowPrint(f"You have {oCount} Oil Wells, exctracting {oilCount} Oil per second")


def checkOilWell(screenWin):

    global key

    key = " "
    j = 1

    if len(oilWellList) == 0:
        printC("No Oil Wells", screenWin)
        return

    for x in oilWellList:

        if x.oil == x.oilCapacity:
            printC(f"Oil Well(Full), {j}: {x.oil}", screenWin, newLine = False)
            gaugeDisplay(x.oil, x.oilCapacity, screenWin)
            printC(f"{x.oilCapacity}\n", screenWin, newLine = False)

        elif x.activePower != x.powerReq:
            printC(f"Oil Well(Unpowered), {j}: {x.oil}", screenWin, newLine = False)
            gaugeDisplay(x.oil, x.oilCapacity, screenWin)
            printC(f"{x.oilCapacity}\n", screenWin, newLine = False)

        else:
            printC(f"Oil Well {j}: {x.oil}", screenWin, newLine = False)
            gaugeDisplay(x.oil, x.oilCapacity, screenWin)
            printC(f"{x.oilCapacity}\n", screenWin, newLine = False)

        j += 1


def checkAlloyMines(screenWin):
    j = 1

    if len(alloyMineList) == 0:
        printC("No Alloy Mines", screenWin)
        return

    for x in alloyMineList:

        printC(f"Alloy Mine {j}: {x.rawAlloy}", screenWin, newLine = False)
        gaugeDisplay(x.rawAlloy, x.rawAlloyCapacity, screenWin)
        printC(f"{x.rawAlloyCapacity}, Fuel: {x.fuel}", screenWin, newLine = False)
        gaugeDisplay(x.fuel, x.fuelMax, screenWin)
        printC(f"{x.fuelMax}", screenWin)
        j += 1


def checkAlloyRefineries(screenWin):
    j = 1

    if len(alloyRefineryList) == 0:
        printC("No Alloy Refineries", screenWin)

    for x in alloyRefineryList:

        if x.activePower != x.powerReq:
            printC(
                f"Alloy Refinery(Unpowered) {j}: Alloy: {x.alloy}, Raw Alloy: {x.rawAlloy}", screenWin)

        else:
            printC(f"Alloy Refinery {j}: Alloy: {x.alloy}, Raw Alloy: {x.rawAlloy}", screenWin)

        j += 1


def checkReactors(screenWin):

    j = 1

    if len(reactorList) == 0:
        printC("No Reactors", screenWin)

    for x in reactorList:

        if x.fuel > 0:

            printC(f"Reactor {str(j)}: Generating {str(x.powerGen)} Power, Fuel: {x.fuel}", screenWin, newLine = False)
            gaugeDisplay(x.fuel, x.fuelMax, screenWin)
            printC(f"{x.fuelMax}", screenWin, newLine = False)
            j += 1

        else:

            printC(f"Reactor {str(j)}: Generating no Power, Fuel: {str(x.fuel)}", screenWin, newLine = False)
            gaugeDisplay(x.fuel, x.fuelMax, screenWin)
            printC(f"{x.fuelMax}", screenWin)
            j += 1


def gaugeDisplay(minNum, maxNum, screenWin):

    amount = int((minNum / maxNum * 10))
    printC("[", screenWin, newLine = False)

    for x in range(amount):

        if amount <= 3:

            printC("|", screenWin, color = "red", newLine = False)

        elif 3 < amount <= 6:

            printC("|", screenWin, color = "yellow", newLine = False)


        else:

            printC("|", screenWin, color = "green", newLine = False)

    for x in range(10 - amount):
        printC(" ", screenWin, newLine = False)

    printC("]", screenWin, newLine = False)

update = Thread(target=BaseCheck)
update.daemon = True
update.start()

curses.wrapper(displayRecourceMenu)
curses.endwin()
#optionWin.display()