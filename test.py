#from chascurses import *
from chascurses import *
from item_classes import *
import curses
#from math import ceil


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

        chas.add_callback(curses.KEY_F1, dummy, pass_self=True, args=['testing!'])

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
    map_win.add_callback('q', map_win.stop)

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
    map_win.tilemap.add(TrackerEnemy(), 6, 4)

    map_win.display()


def master_window_test_theory(win):

    # Tests the master window concept

    chas = BaseWindow.create_subwin_at_pos(win, win.getmaxyx()[0], win.getmaxyx()[1])

    print(chas)

    scroll_win1 = ScrollWindow.create_subwin_at_pos(chas, 10, 40)
    scroll_win2 = ScrollWindow.create_subwin_at_pos(chas, 10, 40, position=BaseWindow.TOP_RIGHT)

    content = []

    for i in range(100):

        content.append("This is value: {}".format(i))

    scroll_win1.pause_input()
    scroll_win2.pause_input()

    chas.add_callback('s', scroll_win1._increment_scroll)
    chas.add_callback('w', scroll_win1._decrement_scroll)
    chas.add_callback('q', scroll_win1._render_content)
    chas.add_callback(curses.KEY_UP, scroll_win2._decrement_scroll)
    chas.add_callback(curses.KEY_DOWN, scroll_win2._increment_scroll)
    chas.add_callback('e', scroll_win2._render_content)

    scroll_win1.run_display(content)
    scroll_win2.run_display(content)

    while True:

        chas.get_input()


def master_window_test(win):

    # Tests the MasterWindow functionality.

    master = MasterWindow(win)

    # Create menus:

    scroll1 = ScrollWindow.create_subwin_at_pos(master, 10, 50)
    map_win = DisplayWindow.create_subwin_at_pos(master, 10, 20, position=DisplayWindow.TOP_RIGHT)

    # Populate the scroll menus:

    content = []

    for i in range(100):

        content.append("This is value: {}".format(i))

    # Add stuff to DisplayWindow:

    map_win.add_callback('q', map_win.stop)

    curses.curs_set(0)

    # Create Colors

    map_win.init_colors()

    # Puts a player in top left corner of map:

    player = Player()
    ground = Floor()
    wall = Wall()
    enemy1 = Enemy()
    enemy2 = Enemy()

    map_win.tilemap.fill(Floor)
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

    master.start()

    map_win.display()


def master_window_options_test(win):

    # Tests the MasterWindow functionality.

    master = MasterWindow(win)

    # Create menus:

    opt_win = OptionWindow.create_subwin_at_pos(master, 10, 30)
    map_win = DisplayWindow.create_subwin_at_pos(master, 10, 20, position=DisplayWindow.TOP_RIGHT)

    options = {"Boolean": True}

    # Add stuff to DisplayWindow:

    map_win.add_callback('q', map_win.stop)

    curses.curs_set(0)

    # Create Colors
    blue = Color(9, 1, "blue", 0, 300, 1000)
    green = Color(10, 2, "green", 0, 1000, 300)
    yellow = Color(11, 3, "yellow", 1000, 950, 0)
    red = Color(12, 4, "red", 1000, 0, 300)

    map_win.register_color("blue", blue)
    map_win.register_color("green", green)
    map_win.register_color("yellow", yellow)
    map_win.register_color("red", red)

    # Puts a player in top left corner of map:

    player = Player()
    ground = Floor()
    wall = Wall()
    enemy1 = Enemy()
    enemy2 = Enemy()

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


def mapping_text(win):

    # Tests the MasterWindow functionality.

    master = MasterWindow(win)

    # Create menus:

    text_win = TextDisplayWindow.create_subwin_at_pos(master, 35, 40)
    map_win = DisplayWindow.create_subwin_at_pos(master, 35, 20, position=DisplayWindow.TOP_RIGHT)

    map_win.tilemap.get_all()

    # Add stuff to DisplayWindow:

    map_win.add_callback('f', map_win.stop)

    curses.curs_set(0)
    # Create Colors
    map_win.init_colors()
    text_win.init_colors()

    # Puts a player in top left corner of map:

    player = Player()
    ground = Floor()
    wall = Wall()

    player.text_win = text_win

    map_win.tilemap.fill(Floor)
    add(player, 0, 0, map_win)
    add(Sword(), 3, 1, map_win)
    #add(Helmet(), 4, 3, map_win)
    #add(Chestplate(), 6, 4, map_win)
    #add(Chest(), 7, 5, map_win)
    add(TrackerEnemy(), 5, 4, map_win)
    add(Wall(), 5, 3, map_win)

    for x in range(6):

        add(Wall(), x, 2, map_win)

    # Add the scroll menus to the master window:
    master.add_subwin(text_win)
    master.add_subwin(map_win)

    # Start the master window:
    master.start()
    map_win.display()


def path_finding_test(win):

    map_win = DisplayWindow.create_subwin_at_pos(win, 50, 76, BaseWindow.TOP_LEFT)

    map_win.add_callback('f', map_win.stop)
    curses.curs_set(0)

    map_win.init_colors()

    map_win.tilemap.fill(Floor)

    player = Player()
    add(player, 9, 13, map_win)
    add(TrackerEnemy(), 2, 2, map_win)
    usedCoords = [[3, 1], [6, 6]]

    '''
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

    #Creating random walls on the x axis

    add(Wall(), 8, 0, map_win)
    add(Wall(), 7, 1, map_win)
    add(Wall(), 6, 2, map_win)
    add(Wall(), 5, 3, map_win)
    add(Wall(), 4, 4, map_win)
    add(Wall(), 3, 5, map_win)
    add(Wall(), 2, 6, map_win)
    add(Wall(), 1, 7, map_win)
    add(Wall(), 0, 8, map_win)
    add(Wall(), 2, 1, map_win)
    add(Wall(), 3, 0, map_win)
    add(Wall(), 4, 1, map_win)
    add(Wall(), 3, 2, map_win)
    add(Wall(), 4, 6, map_win)
    add(Wall(), 5, 6, map_win)
    add(Wall(), 5, 5, map_win)
    add(Wall(), 6, 5, map_win)
    add(Wall(), 7, 5, map_win)
    '''
    map_win.display()


def curses_standard_test(win):

    screen = curses.initscr()

    tilemap = BaseTileMap(60, 60, screen)

    tilemap.fill(Floor)
    player = Player()
    tilemap.add(player, 4, 13)
    tilemap.add(TrackerEnemy(), 2, 2)

    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)

    key = ''
    count = 0

    while key != 'f':

        yIndex = 0
        xIndex = 0

        for line in tilemap.tilemap:

            for col in line:

                renderChar = tilemap.tilemap[yIndex][xIndex][0].char

                if renderChar == '0': screen.addstr(renderChar, curses.color_pair(1))

                else: screen.addstr(renderChar)

                xIndex += 1

            screen.addstr("\n")
            xIndex = 0
            yIndex += 1

            continue

        screen.addstr(str(count))
        screen.refresh()
        screen.clear()
        count += 1


def all_tests(win):

    # Runs all tests

    tests = [callback_test, center_test, single_position_test, multi_position_test,
             position_wrap_test, input_test, scroll_window_test, scroll_window_wrapping_test, border_test, header_test,
             simple_selection_test, mulit_selection_test]

    for test in tests:

        test(win)

        win.erase()


curses.wrapper(path_finding_test)
