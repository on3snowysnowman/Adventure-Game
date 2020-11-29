from time import sleep
import os, sys, copy, curses


def clearScreen(time = .5):

   os.system('cls')
   sleep(time)


def pause(time = .5, newLine = True):

   sleep(time)

   if newLine is True:

       print("\n")

   os.system('pause')
   clearScreen()


def beforeInputPrint(strName, time = .03, sleepTime = .2):

   for letter in strName:

       sys.stdout.write(letter)
       sys.stdout.flush()
       sleep(time)

   sleep(sleepTime)
   print("\n" * 1)


def slowPrint(strName, pauseBool = True, clearBool = True, pauseTime = .05, numNewLine = 0):

   for letter in strName:

       sys.stdout.write(letter)
       sys.stdout.flush()
       sleep(.03)

   print("\n" * numNewLine)

   if pauseBool is True:

       pause(pauseTime, newLine = False)

   if clearBool is True:

       clearScreen()


def slowPrintCustom(strName, time= .03, newLine = False, numNewLine = 0, sleepTime = .5, pauseBool = True, clearBool = True):

   for letter in strName:

       sys.stdout.write(letter)
       sys.stdout.flush()
       sleep(time)

   if newLine is True:


       print("\n" * numNewLine)

   if pauseBool is True:

       pause()

   if clearBool is True:

       clearScreen()


   sleep(sleepTime)


def waitPrint(strName):

   for letter in strName:

       sys.stdout.write(letter)
       sys.stdout.flush()
       sleep(.03)

   sleep(.3)


def screenPrint(strName, screenName):

   screenName.addstr(strName)


def newLinePrint(num = 0):

   print("\n" * num)


def printList(targetList, pauseBool = False, typeFunction = "print"):

   if typeFunction == "slowPrint":

       i = 0

       while True:

           if i != len(targetList) - 1:

               slowPrintCustom(targetList[i] + ", ", sleepTime = 0, pauseBool = False, clearBool = False)
               i += 1

           elif i == len(targetList) - 1:

               slowPrintCustom(targetList[i], newLine = True, sleepTime = 0, pauseBool = False, clearBool = False)
               break

       if pauseBool is True:

           sleep(.5)

   elif typeFunction == "print":

       i = 0

       while True:

           targetList[i] = str(targetList[i])

           if i != len(targetList) - 1:

               print(targetList[i] + ", ")
               i += 1

           elif i == len(targetList) - 1:

               try:


                   slowPrintCustom(targetList[i], newLine = True, time = 0, sleepTime = 0, pauseBool = False, clearBool = False)
                   break

               except TypeError:

                   slowPrintCustom(targetList[i].name, newLine = True, time = 0, sleepTime = 0, pauseBool = False, clearBool = False)
                   break


def numberList(seekNum, startNum, endNum):

   numList = []
   i = startNum

   while i != endNum + 1:

       numList.append(i)
       i += 1

   if seekNum in numList:

       numList.clear()
       return True

   return False


def objectCopy(targ):

   return copy.deepcopy(targ)


def printC(string, screenWin, color="", newLine=True):

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, 10, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, 9, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, 11, curses.COLOR_BLACK)

    if newLine is True:

        if string == "\n":

            screenWin.addstr("\n")
            return

        if color == "":

            screenWin.addstr(str(string) + "\n")

        elif str.lower(color) == "red":

            screenWin.addstr(str(string)+ "\n", curses.color_pair(1) | curses.A_BOLD)

        elif str.lower(color) == "green":

            screenWin.addstr(str(string) + "\n", curses.color_pair(2) | curses.A_BOLD)

        elif str.lower(color) == "yellow":

            screenWin.addstr(str(string) + "\n", curses.color_pair(3))

        elif str.lower(color) == "blue":

            screenWin.addstr(str(string) + "\n", curses.color_pair(4) | curses.A_BOLD)

        elif str.lower(color) == "magenta":

            screenWin.addstr(str(string) + "\n", curses.color_pair(5) | curses.A_BOLD)

        elif str.lower(color) == "orange":

            screenWin.addstr(str(string) + "\n", curses.color_pair(6) | curses.A_BOLD)

    else:

        if color == "":

            screenWin.addstr(str(string))

        elif str.lower(color) == "red":

            screenWin.addstr(str(string), curses.color_pair(1) | curses.A_BOLD)

        elif str.lower(color) == "green":

            screenWin.addstr(str(string), curses.color_pair(2) | curses.A_BOLD)

        elif str.lower(color) == "yellow":

            screenWin.addstr(str(string), curses.color_pair(3) | curses.A_BOLD)

        elif str.lower(color) == "blue":

            screenWin.addstr(str(string), curses.color_pair(4) | curses.A_BOLD)

        elif str.lower(color) == "magenta":

            screenWin.addstr(str(string), curses.color_pair(5) | curses.A_BOLD)

        elif str.lower(color) == "orange":

            screenWin.addstr(str(string), curses.color_pair(6) | curses.A_BOLD)


def createColor():

    #9 = Bright Blue
    curses.init_color(9, 0, 400, 1000)

    #10 Bright Green
    curses.init_color(10, 0, 1000, 400)

    #11 = Orange
    curses.init_color(11, 1000, 600, 0)