from engine.curses.input import *
from engine.curses.display import *
from engine.curses.base import *

from engine.characters.tiles import *
from engine.characters.input import *
from engine.characters.npcs import *
from engine.characters.auto.move import RandomMove, TrackerMove

from engine.tilemaps import WalkingFunctions, BaseTileMap

from engine.debug import clear_debug_log, debug_log

import curses
#from math import ceil
import sys

# ------------------------
# Some classes that MUST be defined:

class Skeleton(EntityCharacter):

    def start(self):

        self.name = 'Skeleton'
        self.hp = 24
        self.damage_min = 8
        self.damage_max = 12
        self.damage_type = "physical"
        self.armor = .1
        self.description = ""

        self.auto.add(TrackerMove(Player))


class TestEnemy(EntityCharacter):
    
    """
    Dummy enemy for testing purposes
    """

    def __init__(self):

        super().__init__()

        self.name = 'Enemy'
        self.char = 'E'
        self.attrib.append("red")
        self.priority = 18


def add(obj, x, y, win):

    win.tilemap.add(obj, x, y)


def dummy(win, test):

    win.win.addstr("This is a test! You should have pressed F1!")
    win.win.addstr("Here is the argument supplied: {}".format(test))

    return


def callback_test(win):  # PASSED

    while True:

        # Creating CHAS windows

        chas = BaseWindow(win)

        # Adding callback for the F1 key

        chas.add_key(curses.KEY_F1, dummy, pass_self=True, args=['testing!'])

        # Getting input and printing input:

        inp = chas.get_input()

        if inp == 'q':

            return

        if inp:

            win.addstr(inp)


def center_test(win):  # PASSED

    # Create a centered window and write stuff to it

    win.bkgd('/')

    win.refresh()

    max_y, max_x = win.getmaxyx()

    print("Max X:" + str(max_x))
    print("Max Y:" + str(max_y))

    # Creating centred window:

    chas = BaseWindow.create_subwin_at_pos(win, 10, 50, position=BaseWindow.CENTERED)

    chas.win.bkgd(' ')
    chas.win.addstr("This is a test of the centered window!")

    chas.win.refresh()
    win.refresh()

    chas.get_input()


def single_position_test(win):  # PASSED

    # Renders text at multiple parts of the master window

    text = ['Top Left', 'Top Right', 'Bottom Left', 'Bottom Right', 'Centered']

    win.bkgd('/')

    chas = BaseWindow.create_subwin_at_pos(win, 20, 50, position=BaseWindow.CENTERED)

    chas.bkgd(' ')

    for num, val in enumerate(text):

        # Render text in window

        chas.addstr(val, position=num)

        chas.refresh()

        chas.get_input()

    win.getch()


def multi_position_test(win):  # PASSED

    # Renders windows at multiple points, and text at multiple points within them

    text = ['Top Left', 'Top Right', 'Bottom Left', 'Bottom Right', 'Centered']
    ntext = ['Top left', 'Top Right', 'Bottom Left', 'Bottom Right', 'Centered']
    wins = []

    win.bkgd('/')

    for i in range(5):

        # Create and render a window at a position

        new_win = BaseWindow.create_subwin_at_pos(win, 17, 50, position=i)

        new_win.bkgd(' ')

        wins.append(new_win)

        for num, val in enumerate(ntext):

            # Render content at locations in window

            new_win.addstr(val, position=num)

            new_win.refresh()

    #win.addstr(0, 0, "TESTING!")
    win.getch()


def position_wrap_test(win):  # PASSED

    # Wraps content around when using positions

    win.bkgd('/')

    chas = BaseWindow.create_subwin_at_pos(win, 17, 50, position=4)

    chas.bkgd(" ")

    thing = "THis text should be bigger than 17 characters! Don't believe me? Check out the curses window," \
            "Should take multiple lines if working correctly!"

    chas.addstr(thing, position=3)

    chas.refresh()

    win.getch()


def input_test(win):  # PASSED

    # Tests the CHAS input widget

    win.bkgd('/')

    win.refresh()

    inp = InputWindow.create_subwin_at_pos(win, 10, 50, position=BaseWindow.CENTERED)

    inp.bkgd(" ")

    thing = inp.input(prompt='Input:', add='Test')

    print(thing)

    # Lets run the same window again, and see if it fails:

    thing2 = inp.input(prompt='Input2:')

    print(thing2)


def scroll_window_test(win):  # PASSED

    # Tests the CHAS scroll window

    win.bkgd('/')

    win.refresh()

    conwin = ScrollWindow.create_subwin_at_pos(win, 10, 50, position=ScrollWindow.CENTERED)

    conwin.bkgd(' ')

    content = []
    index = 0

    for i in range(100):

        content.append("This is value: {}".format(i))

    conwin.run_display(content)

    conwin.block()


def scroll_window_wrapping_test(win):  # PASSED

    # Tests the CHAS wrapping function

    content = ['THis should be on -\nMulitple lines!', 'This should be a multi line statement, as this '
                                                       'test is in fact very long. This should not hinder the '
                                                       'windows ability to not only handle it, but wrap it.',
               'This is - \n - Two lines!']

    win.bkgd('/')

    win.refresh()

    conwin = ScrollWindow.create_subwin_at_pos(win, 10, 10, position=ScrollWindow.CENTERED)

    conwin.bkgd(' ')

    conwin.run_display(content)

    conwin.block()


def border_test(win):

    # Tests the border feature of BaseWindow

    win.bkgd('/')

    win.refresh()

    chas = BaseWindow.create_subwin_at_pos(win, 20, 50, position=BaseWindow.CENTERED)

    chas.bkgd(' ')

    chas.border()

    chas.addstr("This should be in content window!")

    chas.refresh()

    chas.get_input()


def header_test(win):

    # Testing the header/sub-header functionality for BaseWindow

    win.bkgd('/')

    win.refresh()

    chas = BaseWindow.create_subwin_at_pos(win, 20, 50, position=BaseWindow.CENTERED)

    chas.bkgd(' ')

    chas.border(header_len=3, sub_len=3)

    chas.addstr("This should be in the content!")

    chas.header.addstr("This should be in the header!")

    chas.sub_header.addstr("This should be in the sub-header!")

    chas.refresh()

    chas.get_input()


def simple_selection_test(win):

    # Tests out the simple selection feature of CHAS OptionWindow

    options = []

    for i in range(0, 100):

        options.append("Option {}".format(i))

    win.bkgd('/')

    win.refresh()

    optionwin = OptionWindow.create_subwin_at_pos(win, 20, 50, position=OptionWindow.CENTERED)

    optionwin.bkgd(' ')

    optionwin.add_options(options)

    out = optionwin.display()

    print(out)


def mulit_selection_test(win):

    # Tests out the window selection types.

    options = {'Manual': 'Testing', 'Boolean': False, 'Value': ['1', '2', '3', '4'], 'Null': None, 'Sub':
               {'Manual': 'Testing', 'Boolean': False, 'Value': ['1', '2', '3', '4']},
               'This is a very long option name, and should be shortened accordingly. Seeing names like this in '
               'production should be very rare, but things like this could happen, so we need to be ready.': False}

    win.bkgd('/')

    win.refresh()

    optionwin = OptionWindow.create_subwin_at_pos(win, 20, 50, position=OptionWindow.CENTERED)

    optionwin.bkgd(' ')

    optionwin.add_options(options)

    opt = optionwin.display()

    print(opt)


def run_dummy():

    # Prints run dummy

    print("Run Dummy!")


def run_window_test(win):

    # Tests the run option

    win.bkgd('/')

    win.refresh()

    optionwin = OptionWindow.create_subwin_at_pos(win, 20, 50, position=OptionWindow.BOTTOM_LEFT)

    optionwin.bkgd(' ')

    optionwin.add_option("Run Dummy!", optionwin.RUN_OPTION, value=run_dummy)

    optionwin.display()


def map_window_test(win):

    # Tests the display window features

    map_win = DisplayWindow.create_subwin_at_pos(win, 11, 16)
    map_win.add_key('q', map_win.stop)

    curses.curs_set(0)

    # Create Colors

    map_win.init_colors()

    # Puts a player in top left corner of map:

    player = Player()
    ground = Floor()
    wall = Wall()
    player = Player()

    map_win.tilemap.fill(Floor)
    map_win.tilemap.add(player, 1, 1)
    map_win.tilemap.add(wall, 0, 1)
    map_win.tilemap.add(TestEnemy(), 6, 4)

    map_win.display()


def master_window_test(win):

    # Tests the MasterWindow functionality.

    master = MasterWindow(win)

    # Create menus:

    scroll1 = ScrollWindow.create_subwin_at_pos(master, 10, 50)
    map_win = DisplayWindow.create_subwin_at_pos(master, 50, 75, position=DisplayWindow.TOP_RIGHT)

    # Populate the scroll menus:

    content = []

    for i in range(100):

        content.append("This is value: {}".format(i))

    # Add stuff to DisplayWindow:

    map_win.add_key('f', master.stop)

    curses.curs_set(0)

    # Create Colors

    map_win.init_colors()

    # Puts a player in top left corner of map:

    player = Player()
    wall = Wall()
    enemy1 = TestEnemy()
    enemy2 = TestEnemy()

    #map_win.tilemap.fill(Floor)
    map_win.tilemap.add(player, 0, 0)
    map_win.tilemap.add(wall, 0, 1)
    map_win.tilemap.add(enemy1, 2, 2)
    map_win.tilemap.add(enemy2, 3, 3)

    # Add the scroll menus to the master window:

    master.add_subwin(scroll1)
    master.add_subwin(map_win)

    # Start the two scroll widows:

    scroll1.run_display(content)

    # Start the master window:

    display_thread = threading.Thread(target=map_win.display)
    display_thread.daemon = True
    display_thread.start()

    # Start the master window

    master.start()


def master_window_options_test(win):

    # Tests the MasterWindow functionality.

    master = MasterWindow(win)

    # Create menus:

    opt_win = OptionWindow.create_subwin_at_pos(master, 10, 30)
    map_win = DisplayWindow.create_subwin_at_pos(master, 10, 20, position=DisplayWindow.TOP_RIGHT)

    options = {"Boolean": True}

    # Add stuff to DisplayWindow:

    map_win.add_key('f', master.stop)

    curses.curs_set(0)

    # Create Colors
    map_win.init_colors()

    # Puts a player in top left corner of map:

    player = Player()
    wall = Wall()
    enemy1 = TestEnemy()
    enemy2 = TestEnemy()

    map_win.tilemap.fill(Floor)
    map_win.tilemap.add(player, 0, 0)
    map_win.tilemap.add(wall, 0, 1)
    map_win.tilemap.add(enemy1, 2, 2)
    map_win.tilemap.add(enemy2, 3, 3)

    # Add the scroll menus to the master window:

    master.add_subwin(opt_win)
    master.add_subwin(map_win)

    # Start the two scroll widows:
    opt_win.add_options(options)

    # Start the master window:

    master.start()

    # Create thread for option window:

    opt_win_thread = threading.Thread(target=opt_win.display)
    opt_win_thread.daemon = True
    opt_win_thread.start()

    map_win.display()
    opt_win_thread.join()


def trace_test(win):

    # Tests the trace capabilities of the tilemap:

    display = DisplayWindow.create_subwin_at_pos(win, 10, 30, position=DisplayWindow.TOP_LEFT)

    display.tilemap.fill(Floor)
    display.init_colors()

    # Diagonal down - Top Left

    for tile in display.tilemap.traverse_function(0, 0, WalkingFunctions.from_slope(1), par=True):

        # Draw in a wall in the position:

        display.tilemap.add(Wall(), tile[0].x, tile[0].y)

    # Diagonal down - Top Right

    for tile in display.tilemap.traverse_function(display.tilemap.width-1, 0,
                                                  WalkingFunctions.from_slope(-1), step_size=-1, par=True):

        # Draw in a wall in the position:

        display.tilemap.add(Wall(), tile[0].x, tile[0].y)

    # Diagonal Up - Bottom Left

    for tile in display.tilemap.traverse_function(0, display.tilemap.height-1, WalkingFunctions.from_slope(-1), par=True):

        # Draw a wall in the position:

        display.tilemap.add(Wall(), tile[0].x, tile[0].y)

    # Diagonal Up - Bottom Right

    for tile in display.tilemap.traverse_function(display.tilemap.width-1, display.tilemap.height-1,
                                                  WalkingFunctions.from_slope(1), par=True, step_size=-1):

        # Draw a wall in the position:

        display.tilemap.add(Wall(), tile[0].x, tile[0].y)

    # Vertical line:

    for tile in display.tilemap.traverse_function(int(display.tilemap.width/2), 0,
                                                  WalkingFunctions.from_slope(sys.maxsize), par=True):

        # Draw a wall in the position:

        display.tilemap.add(Wall(), tile[0].x, tile[0].y)

    # Horizontal line:

    for tile in display.tilemap.traverse_function(0, int(display.tilemap.height/2),
                                                  WalkingFunctions.from_slope(0), par=True):

        # Draw a wall in the position:

        display.tilemap.add(Wall(), tile[0].x, tile[0].y)

    display.add_key('q', display.stop)

    display.display()


def look_test(win):

    master = MasterWindow(win)

    map_win = DisplayWindow.create_subwin_at_pos(win, 21, 21)
    scroll_win = ScrollWindow.create_subwin_at_pos(win, master.max_y, int(master.max_x / 2), BaseWindow.TOP_RIGHT)

    map_win.add_key('f', map_win.stop)
    curses.curs_set(0)

    map_win.init_colors()

    map_win.tilemap.fill(Floor)

    # Creating random walls on the x axis
    for x in range(map_win.tilemap.get_height()):

        fillBool = random.choice([True, False])

        if fillBool:

            numWalls = random.randrange(2, int(map_win.tilemap.get_width(x) / 2))
            yCoord = x
            xCoord = random.randrange(0, map_win.tilemap.get_height())

            for i in range(numWalls):

                if map_win.tilemap._bound_check(xCoord, yCoord):

                    add(Wall(), xCoord, yCoord, map_win)
                    xCoord += 1

    availableCoordinates = []

    xCount = 0
    yCount = 0

    exemptFromList = False

    # Searching tilemap for traversable spots
    for line in map_win.tilemap.tilemap:

        for col in line:

            for tile in col:

                if not tile.can_traverse:

                    exemptFromList = True
                    break

            if not exemptFromList:

                availableCoordinates.append([xCount, yCount])

            exemptFromList = False
            xCount += 1

        yCount += 1
        xCount = 0

    player = Player()
    add(player, int(map_win.tilemap.get_width() / 2), int(map_win.tilemap.get_height() / 2), map_win)
    randomTile = random.choice(availableCoordinates)
    add(TestEnemy(), randomTile[0], randomTile[1], map_win)

    master.add_subwin(map_win)

    display_thread = threading.Thread(target=map_win.display)
    display_thread.daemon = True
    display_thread.start()

    player.scroll_win = scroll_win

    # Start the master window
    scroll_win.add_content("Scroll Window")
    scroll_win._render_content()
    master.start()


def camera_test(win):

    master = MasterWindow(win)

    map_win = DisplayWindow.create_subwin_at_pos(win, 50, 50)

    map_win.add_key('f', map_win.stop)
    curses.curs_set(0)

    map_win.init_colors()

    map_win.tilemap.fill(Floor)

    player = Player()

    add(player, int(map_win.tilemap.get_width() / 2), int(map_win.tilemap.get_height() / 2), map_win)

    '''

    availableCoordinates = []

    xCount = 0
    yCount = 0

    exemptFromList = False

    # Searching tilemap for traversable spots
    for line in map_win.tilemap.tilemap:

        for col in line:

            for tile in col:

                if not tile.can_traverse:
                    exemptFromList = True
                    break

            if not exemptFromList:
                availableCoordinates.append([xCount, yCount])

            exemptFromList = False
            xCount += 1

        yCount += 1
        xCount = 0

    # Creating random walls on the x axis
    for x in range(map_win.tilemap.get_height()):

        fillBool = random.choice([True, False])

        if fillBool:

            numWalls = random.randrange(2, int(map_win.tilemap.get_width(x) / 2))
            yCoord = x
            xCoord = random.randrange(0, map_win.tilemap.get_height())

            for i in range(numWalls):

                if map_win.tilemap._bound_check(xCoord, yCoord) and [xCoord, yCoord] in availableCoordinates:
                    add(Wall(), xCoord, yCoord, map_win)
                    availableCoordinates.remove([xCoord, yCoord])
                    xCoord += 1
                    
    randomCoord = random.choice(availableCoordinates)
    availableCoordinates.remove(randomCoord)
    add(RandomEnemy(), randomCoord[0], randomCoord[1], map_win) 
    
    randomCoord = random.choice(availableCoordinates)
    availableCoordinates.remove(randomCoord)
    add(TrackerEnemy(), randomCoord[0], randomCoord[1], map_win)
    
    randomCoord = random.choice(availableCoordinates)
    availableCoordinates.remove(randomCoord)
    add(TrackerEnemy(), randomCoord[0], randomCoord[1], map_win)
   
    '''

    map_win.camera.set_focus_object(player)
    map_win.camera.set_radius(6)
    # map_win.camera.set_radius(int(map_win.max_x / 2) - 5)

    display_thread = threading.Thread(target=map_win.display)
    display_thread.daemon = True
    display_thread.start()

    master.add_subwin(map_win)
    master.start()


def battle_test(win):

    master = MasterWindow(win)

    y, x = win.getmaxyx()

    map_win = DisplayWindow.create_subwin_at_pos(win, y, int(x / 2), BaseWindow.TOP_LEFT)

    scroll_win = ScrollWindow.create_subwin_at_pos(win, y, map_win.max_x, BaseWindow.TOP_RIGHT)

    map_win.tilemap.set_scroll_win(scroll_win)

    map_win.add_key('f', master.stop)
    curses.curs_set(0)

    map_win.init_colors()

    map_win.tilemap.fill(Floor)

    player = Player()
    player.active_weapon = Sword()

    availableCoordinates = []

    xCount = 0
    yCount = 0

    exemptFromList = False

    add(player, 0, 0, map_win)

    add(Skeleton(), 4, 4, map_win)

    add(Wall(), 3, 0, map_win)
    add(Wall(), 3, 1, map_win)
    add(Wall(), 3, 2, map_win)
    add(Wall(), 3, 3, map_win)

    add(Wall(), 0, 3, map_win)
    add(Wall(), 1, 3, map_win)
    add(Wall(), 2, 3, map_win)
    add(Wall(), 0, 3, map_win)

    '''
    # Searching tilemap for traversable spots
    for line in map_win.tilemap.tilemap:

        for col in line:

            for tile in col:

                if not tile.can_traverse:
                    exemptFromList = True
                    break

            if not exemptFromList:
                availableCoordinates.append([xCount, yCount])

            exemptFromList = False
            xCount += 1

        yCount += 1
        xCount = 0

    spot = random.choice(availableCoordinates)

    add(Skeleton(), spot[0], spot[1], map_win)

    availableCoordinates.remove(spot)

    # Creating random walls on the x axis
    for x in range(map_win.tilemap.get_height()):

        fillBool = random.choice([True, False])

        if fillBool:

            numWalls = random.randrange(2, int(map_win.tilemap.get_width(x) / 2))
            yCoord = x
            xCoord = random.randrange(0, map_win.tilemap.get_height())

            for i in range(numWalls):

                if map_win.tilemap._bound_check(xCoord, yCoord) and [xCoord, yCoord] in availableCoordinates:
                    add(Wall(), xCoord, yCoord, map_win)
                    availableCoordinates.remove([xCoord, yCoord])
                    xCoord += 1
    # '''

    map_win.camera.set_focus_object(player)
    player.radius = 20

    display_thread = threading.Thread(target=map_win.display)
    display_thread.daemon = True
    display_thread.start()

    master.add_subwin(map_win)
    master.add_subwin(scroll_win)
    master.start()

    '''
    for line in player.tilemap.tilemap:

        for col in line:

            print(col[0].char, end='')

        print()
    '''


def large_test(win):

    # Tests to make sure we can handle very large windows:

    master = MasterWindow(win)

    # Create menus:

    map_win = DisplayWindow.create_subwin_at_pos(master, 50, 75, position=MasterWindow.TOP_RIGHT)

    # Add stuff to DisplayWindow:

    map_win.add_key('f', map_win.stop)

    curses.curs_set(0)
    curses.delay_output(1)

    # Create Colors

    map_win.init_colors()

    # Puts a player in top left corner of map:

    player = Player()
    wall = Wall()
    enemy1 = TestEnemy()
    enemy2 = TestEnemy()

    map_win.tilemap.fill(Floor)
    map_win.tilemap.add(player, 0, 0)
    map_win.tilemap.add(wall, 0, 1)
    map_win.tilemap.add(enemy1, 2, 2)
    map_win.tilemap.add(enemy2, 3, 3)

    # Add the map window:

    master.add_subwin(map_win)

    # Start the master window:

    master.start()

    map_win.display()


def curses_standard_test(win):

    screen = curses.initscr()

    tilemap = BaseTileMap(60, 60, screen)

    tilemap.fill(Floor)
    player = Player()
    tilemap.add(player, 4, 13)
    tilemap.add(TestEnemy(), 2, 2)

    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)

    key = ''
    count = 0

    while key != 'f':

        yIndex = 0
        xIndex = 0

        for line in tilemap.tilemap:

            for col in line:

                renderChar = tilemap.tilemap[yIndex][xIndex][0].char

                if renderChar == '0': screen.addstr(yIndex, xIndex, renderChar, curses.color_pair(1))

                else: screen.addstr(yIndex, xIndex, renderChar)

                xIndex += 1

            xIndex = 0
            yIndex += 1

            continue

        screen.addstr(str(count))
        screen.refresh()
        screen.clear()
        count += 1


def autorun_test(win):

    # Tests the autorun feature

    # Create our windows:

    master = MasterWindow(win)

    display = DisplayWindow.create_subwin_at_pos(win, 20, 20, DisplayWindow.TOP_LEFT)

    # Add them to the master window:

    master.add_subwin(display)

    # Final window configuration:

    display.init_colors()

    display.tilemap.fill(Floor)

    display.add_key('f', master.stop)

    # Create an entity:

    enemy = TestEnemy()

    # +==============================================+
    # Attach the RandomMove autorun to the character to enable random movement
    # This is how attaching any autorun will work.
    # Autoruns can optionally ask for arguments

    enemy.auto.add(RandomMove())

    # +==============================================+


    # Add the random enemy:

    add(enemy, 1, 1, display)

    # Run the windows:

    display_thread = threading.Thread(target=display.display)
    display_thread.daemon = True
    display_thread.start()

    master.start()


def all_tests(win):

    # Runs all tests

    tests = [callback_test, center_test, single_position_test, multi_position_test,
             position_wrap_test, input_test, scroll_window_test, scroll_window_wrapping_test, border_test, header_test,
             simple_selection_test, mulit_selection_test]

    for test in tests:

        test(win)

        win.erase()


# Enable log debuging:

debug_log()

# Clean the log:

clear_debug_log()

# Run the test:

curses.wrapper(master_window_test)
