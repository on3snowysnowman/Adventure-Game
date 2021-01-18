import curses
import curses.panel
from math import ceil, floor
import threading
from inspect import isfunction
from queue import Queue, Empty

from character_classes import *
from tilemaps import BaseTileMap, Tile

"""
Curses wrappings.
Includes special curses operations,
As well as custom curses windows to use.
The most important bit is the BaseWindow, which should 
act as the parent for all CHAS curses operations.
"""


class BaseWindow:

    """
    Custom CURSES wrappings.

    We try to make curses development as simple as possible,
    while emulating the normal curses options as much as possible.

    Handles the following actions:
    1. Writing content to a window
    2. Creating subwindows
    3. Handling borders/headers/subheaders
    4. Handling colors and text attributes
    5. Getting inputs and using callbacks to handle inputs
    6. Rendering content at specific locations on the screen

    #TODO: Look at these
    Things I would like supported, but are not critical:

    1. Mouse Support
    2. Better interface for handling color and attributes
    """

    # Constants for defining render location:

    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3
    CENTERED = 4

    def __init__(self, win):

        self.win = win  # Curses window to do our operations on, provided to us
        self.color = False  # Value determining if we have color
        self._calls = {}  # List of callbacks to be called given a keypress

        self.colorPairs = {}

        self.managed = False  # Value  determining if our input is handled
        self.input_queue = None  # Queue to store inputs - only relevant if we are managed!
        self.master = None  # Instance of MasterWindow controlling us - only relevant if we are managed!

        max_y, max_x = win.getmaxyx()

        self.max_x = max_x  # Maximum X cordnet
        self.max_y = max_y  # Maximum Y cordnet

        self.parent = None  # Parent window, used for bordering so we can keep track of it.
        self.header = None  # Header window
        self.sub_header = None  # Sub-header window

        self._init_screen()  # Initialise the screen with good curses defaults

    def _init_screen(self):

        """
        Function for setting parameters,
        And preparing the window to be written to.

        Lot's of good curses defaults here,
        and some mandatory features for BaseWindow to work.
        """

        # Turning off the echoing of keys

        curses.noecho()

        # Enabling cbreak mode, disables buffered input

        curses.cbreak(True)

        # Start Keypad handling

        self.win.keypad(True)

        # Allowing scrolling

        self.win.scrollok(True)

        # Allow hardware line editing facilities

        #self.win.idlok(True)

        curses.start_color()
        self.color = True

    @staticmethod
    def _get_start_cords(start, max_y, max_x, y_len, x_len):

        """
        Calculates the starting cordnets for rendering content at certain positions on the screen.

        :param start: Location to render content
        :param max_y: Maximum y value
        :param max_x: Maximum x value
        :param y_len: Height of content to render
        :param x_len: Length of content to render
        :return: Starting y cordnet, starting x cordnet
        """

        if start == BaseWindow.TOP_LEFT:
            # User wants content in the upper left hand corner: 0, 0

            return 0, 0

        if start == BaseWindow.TOP_RIGHT:
            # User wants content in the upper right hand corner

            return 0, max_x - x_len

        if start == BaseWindow.BOTTOM_LEFT:
            # User wants content in bottom left hand corner

            return max_y - y_len, 0

        if start == BaseWindow.BOTTOM_RIGHT:
            # User wants content in bottom right hand corner

            return max_y - y_len, max_x - x_len

        if start == BaseWindow.CENTERED:
            # User wants content centered

            return (ceil(max_y / 2)) - (ceil(y_len / 2)), (ceil(max_x / 2)) - (ceil(x_len / 2))

    def getmaxyx(self):

        """
        Returns the max y and x coordinates respectively.

        :return: Y and X
        """

        return self.win.getmaxyx()

    def derwin(self, nlines, ncols, begin_y, begein_x):

        """
        # TODO: FInish this
        :param nlines:
        :param ncols:
        :param begin_y:
        :param begein_x:
        :return:
        """

        return self.win.derwin(nlines, ncols, begin_y, begein_x)

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

    def handle_key(self, key):

        """
        Handles a specified key.

        :param key: Key to be handled
        """

        if key in self._calls:
            func = self._calls[key]['call']
            args = self._calls[key]['args']

            # Running callback, with args specified

            func(*args)

            return True

        return False

    def _get_input(self):

        """
        Gets input from the curses window directly and returns it.

        :return: Curses input
        """

        # Check if we have special input handling:

        if self.managed:

            # Wait until input from our queue is received:

            return self.input_queue.get()

        # Getting keypress and returning it

        return self.win.getch()

    def refresh(self):

        """
        Refreshes the curses screen,
        and by extension, the BaseWindow parent window and headers.

        If we are managed by a MasterWindow,
        then we simply call 'noutrefresh()',
        which only refreshes the virtual screen.

        We then mark the MasterWindow for refresh,
        which calls 'doupdate()' as soon as possible.
        """

        if self.managed:

            # We are managed, update the virtual screen and prompt for update:

            self.win.noutrefresh()

            # Mark the master window for refresh:

            self.master.need_refresh = True

            return

        self.win.refresh()

    def addstr(self, content, ystart=-1, xstart=-1, position=-1, attrib=None):

        """
        Renders content on the screen.
        Supports rendering content at specific cordnets or positions

        :param content: Content to render
        :param ystart: starting y cordnet
        :param xstart: starting x cordnet
        :param position: Position to render content
        :param attrib: Attributes to apply to the text
        :return: Normal curses returncodes
        """
        if attrib is None:

            attrib = []

        for index, targ in enumerate(attrib):

            if type(targ) == str:

                attrib[index] = self.colorPairs[targ]

            if isinstance(attrib[index], Color):

                attrib[index] = attrib[index].resolvedColor

        if position != -1:

            # We want to render in a special location

            x_len = len(content)
            y_len = 1

            if len(content) >= self.max_x:
                # Content is bigger than lines, must figure out how many lines it takes up

                y_len = ceil(len(content) / self.max_x)
                x_len = self.max_x

            ystart, xstart = self._get_start_cords(position, self.max_y, self.max_x, y_len, x_len)

            # Add a 'normal' character to this position to reset our terminal state:

            self.win.addstr(ystart, xstart, ' ', curses.A_NORMAL)

            if position == BaseWindow.BOTTOM_RIGHT and x_len < self.max_x:

                # We have to do some special formatting stuff to get the cursor to work

                return self.win.insstr(ystart, xstart - 1, " ")

            return self.win.addstr(ystart, xstart, content, *attrib)

        if ystart != -1 and xstart != -1:

            # Lets check if we are out of bouds:

            if len(content) + xstart >= self.max_x and ystart == self.max_y - 1:

                # We have to do something special to prevent the cursor from messing us up:

                return self.win.insstr(ystart, xstart, content, *attrib)

            else:

                # user wants to render content at specific cordnets

                return self.win.addstr(ystart, xstart, content, *attrib)

        # Lets curses handle it, user doesn't care

        return self.win.addstr(content, *attrib)

    def register_color(self, name, value):

        self.colorPairs[name] = value

    def bkgd(self, val):

        """
        Changes the window background to a specified value.

        :param val: Value to set the background to
        :return: standard curses returncodes
        """

        return self.win.bkgd(val)

    def border(self, ls=0, rs=0, ts=0, bs=0, tl=0, tr=0, bl=0, br=0, top_line='-', bottom_line='-',
               header_len=0, sub_len=0):

        """
        Generates the boarder and sets the necessary parameters to the new values.
        We also use this function to generate headers and sub-headers.
        Headers can be as tall as the user wants, and support all BaseWindow features.
        Content on the screen may be removed or messed up for borders and headers,
        So this should be called before any content is written to the window.

        :param ls: Left Side
        :param rs: Right Side
        :param ts: Top
        :param bs: Bottom
        :param tl: Upper left cornet
        :param tr: Upper right corner
        :param bl: Bottom left corner
        :param br: Bottom right corner
        :param top_line: Character used for rendering line for header
        :param bottom_line: Character used for rendering line for sub-header
        :param header_len: Height of header
        :param sub_len: Height of sub-header
        """

        # Rendering border

        self.win.border(ls, rs, ts, bs, tl, tr, bl, br)

        self.win.refresh()

        self.parent = self.win

        if header_len > 0:
            # User wants to render in a header

            self.header = BaseWindow.create_subwin_at_cord(self.win, header_len, self.max_x - 2, 1, 1)

            # Now we draw the vertical line beneath the window:

            self.parent.hline(header_len + 1, 1, top_line, self.max_x - 2)

            self.header.refresh()

        if sub_len:
            # User wants to render in a sub-header

            self.sub_header = BaseWindow.create_subwin_at_cord(self.win, sub_len, self.max_x - 2,
                                                               self.max_y - 1 - sub_len, 1)

            # Draw the sub-header line:

            self.parent.hline(self.max_y - 2 - sub_len, 1, bottom_line, self.max_x - 2)

            self.sub_header.refresh()

        # Creating subwindow

        max_y, max_x = self.parent.getmaxyx()

        self.win = self.parent.derwin((max_y - 3 - sub_len if sub_len > 0 else max_y - 2), max_x - 2,
                                      1 + (header_len + 1 if header_len > 0 else 0), 1)

        self.max_y, self.max_x = self.win.getmaxyx()

    def clear(self):

        """
        Clears all content from the curses window.

        :return: Standard curses returncodes
        """

        return self.win.erase()

    def manage(self, master):

        """
        Sets the window mode ot 'managed'. This does a few things:

        1. Create an input queue
        2. Pull values from said input queue on each 'get_input()' call
        3. Refresh the virtual screen and mark for physical upon 'refresh()' calls
        4. Add MasterWindow instance to this window

        This allows us to play nicely with other windows that are also managed by MasterWindow.

        :param master: Instance of MasterWindow that is managing us
        :type master: MasterWindow
        """

        # Set us to managed mode:

        self.managed = True

        # Create an input queue for this window:

        self.input_queue = Queue()

        # Add instance of the master window:

        self.master = master

    def un_manage(self):

        """
        Reverts the BaseWindow back to normal operation.
        We undo much of what has been done in the 'manage()' method.

        THIS WILL REMOVE ALL INPUT IN THE INPUT QUEUE, SO USE WITH CAUTION!
        """

        # Set our status:

        self.managed = False

        # Remove input queue:

        self.input_queue = None

        # Remove MasterWindow instance:

        self.master = None

    def add_input(self, key):

        """
        Adds input to the BaseWindow input buffer.

        Great for if we are under special input handling.

        :param key: Key to be added to the input buffer
        :type key: int
        """

        # Add the key to the input queue:

        self.input_queue.put(key)

    def get_input(self, return_ascii=False, ignore_special=False, no_calls=False):

        """
        Gets key from curses, sends it though the callbacks, and returns the key if not handled.

        We offer the ability to automatically decode inout characters to their ascii values.
        We also offer the ability to ignore special characters, returning False in their place.

        :param return_ascii: Value determining if we should return the ascii number of the key
        :type return_ascii: bool
        :param ignore_special: Determines if we should ignore special characters(ASCII values > 255)
        :type ignore_special: bool
        :param no_calls: Determines if we should pass the input through the callbacks
        :type no_calls: bool
        :return: Key that isn't handled by a callback
        """

        key = self._get_input()

        if not no_calls and self.handle_key(key):

            # Key was handled by a callback, return nothing

            return False

        if key == curses.ERR:

            # Curses error value. Return False

            return False

        if ignore_special and key > 255:

            # Key is a special key that we don't care about:

            return False

        if return_ascii:

            return key

        return chr(key)

    def init_colors(self):

        # Registers the default colors to the BaseWindow

        blue = Color(9, 1, "blue", 0, 300, 1000)
        green = Color(10, 2, "green", 0, 1000, 0)
        yellow = Color(11, 3, "yellow", 1000, 950, 0)
        red = Color(12, 4, "red", 1000, 0, 300)
        orange = Color(13, 5, "orange", 980, 533, 0)
        light_blue = Color(14, 6, "light_blue", 0, 446, 1000)
        brown = Color(15, 7, "brown", 550, 350, 0)
        light_brown = Color(16, 8, "light_brown", 527, 492, 425)
        white = Color(17, 9, "white", 1000, 1000, 1000)
        gray_blue = Color(18, 10, "gray_blue", 371, 496, 858)

        self.register_color("blue", blue)
        self.register_color("green", green)
        self.register_color("yellow", yellow)
        self.register_color("red", red)
        self.register_color("orange", orange)
        self.register_color("light_blue", light_blue)
        self.register_color("brown", brown)
        self.register_color("light_brown", light_brown)
        self.register_color("white", white)
        self.register_color("gray_blue", gray_blue)

    @classmethod
    def create_subwin_at_pos(cls, win, y_len, x_len, position=0):

        """
        Creates a subwindow at the given position using the window provided.

        :param win: curses window
        :param y_len: height of window to create
        :param x_len: width of window to create
        :param position: Position to render the subwindow, defaults to upper left
        :return: CHAS Window object
        """

        # Get cords:

        max_y, max_x = win.getmaxyx()

        start_y, start_x = cls._get_start_cords(position, max_y, max_x, y_len, x_len)

        # Creating subwindow:

        newwin = win.derwin(y_len, x_len, start_y, start_x)

        return cls(newwin)

    @classmethod
    def create_subwin_at_cord(cls, win, y_len, x_len, starty, startx):

        """
        Creates a subwindow from the window provided at the cordnets provided.

        :param win: Window to create subwindow from
        :param starty: Starting y cordnet
        :param startx: Starting x cordnet
        :param y_len: y length
        :param x_len: x length
        """

        return cls(win.derwin(y_len, x_len, starty, startx))


class MasterWindow(BaseWindow):

    """
    CHAS Master window.

    We handle the location of subwindows registered to us,
    as well as taking over the input for each window.

    We also handle the process of focusing windows.
    When a window(s) is focused, then we direct all input towards that specific window(s).
    Otherwise, we direct input to the windows that request it.

    We also handle the process of refreshing windows,
    specifically physically updating the entire screen when a sub-window requests it.
    This removes a lot of drawing latency, and greatly reduces screen flicker.
    """

    def __init__(self, win):

        super(MasterWindow, self).__init__(win)

        self.win = win  # Master window to do our operations on

        self.thread = None  # Threading object
        self.input_queue = queue.Queue()  # Input queue
        self._win_calls = {}  # Mapping inputs to windows

        self.need_refresh = False  # Value determining if we need to physically refresh the screen

        self.run = False  # Value determining if we are running

        self.subwins = []  # List of subwindows
        self.focus = []  # Sub-windows to send ALL inputs to

    def add_subwin(self, subwin):

        """
        Adds a subwindow to the Sub Window list.

        We pause the input and extract callbacks from the given window.

        :param subwin: Subwindow being added to the Master Window list
        :type subwin: BaseWindow
        """

        # Pause the sub-window input:

        subwin.manage(self)

        # Extract the sub-window callbacks:

        self.extract_callback(subwin)

        # Add the subwindow to the MasterWindow:

        self.subwins.append(subwin)

    def extract_callback(self, subwin):

        """
        Extracts the callbacks from a specified window,
        and adds it to our collection.

        :param subwin: Subwidow to extract callbacks from
        :type subwin: BaseWindow
        """

        for key in subwin._calls:

            if key in self._win_calls.keys():

                # Key is present in window callbacks already, lets add it:

                print("Key {} present with {}, adding {}".format(key, self._win_calls[key], subwin))

                self._win_calls[key].append(subwin)

            else:

                # Key is NOT present, lets make a new entry:

                print("Adding key {} with {}".format(key, subwin))

                self._win_calls[key] = [subwin]

        print(self._win_calls)

    def _start_thread(self):

        """
        Starts the MasterWindow thread,
        thus allowing sub windows to accept input.
        """

        # Starting our object:

        self.run = True

        # Creating a thread of the input event loop:

        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def start(self):

        """
        Starts the MasterWindow input thread,
        and starts handling operations on sub-windows.

        This is not a very good implementation.
        Perhaps asyncio would be more appropriate?
        """

        # Start the input thread:

        self._start_thread()

        # Iterate over our event loop:

        while self.run:

            # Get input from our input queue:

            try:

                inp = self.input_queue.get_nowait()

                # Send input to focused window(If any):

                if self.focus:

                    # Focused windows, iterate over them and send input:

                    for win in self.focus:

                        win.add_input(inp)

                else:

                    # Send the input to relevant window only:

                    if inp in self._win_calls.keys():

                        # Key is present, lets send it over:

                        for win in self._win_calls[inp]:

                            # Add the input to the specified window:

                            win.add_input(inp)

            except Empty:

                # Queue is empty, do nothing

                pass

            # Check if any windows need to be refreshed:

            if self.need_refresh:

                # Refresh the physical screen:

                curses.doupdate()

    def stop(self):

        """
        Stops all MasterWindow components,
        specifically the input loop and event loop.
        """

        self.run = False

    def _run(self):

        """
        Main event loop, continuously extracts input from CURSES and passes it to the relevant windows.
        """

        while self.run:

            self.input_queue.put(self.get_input(return_ascii=True, no_calls=True))


class DisplayWindow(BaseWindow):

    """
    New display window for testing.

    Supports modular character drawing and enhanced tilemaps.
    """

    def __init__(self, win):

        super(DisplayWindow, self).__init__(win)

        self.win = win  # CURSES window instance

        # We simply create a tilemap with our width and height,
        # as the DisplayWindow is not smart enough to handle anything different

        self.tilemap = BaseTileMap(self.max_y, self.max_x, self)  # Tilemap storing game info
        self.run = True  # Value determining if we are running

        self.thread = None  # Treading instance of the input loop

    def _render(self):

        """
        Renders the tilemap content to our screen.
        """

        self.clear()

        for x, y, z, obj in self.tilemap._iterate():

            # Render the character at specified position. We don't care about secondary characters!

            if z == 0:

                self.addstr(obj.char, y, x, attrib=obj.attrib)
                #self.addstr(obj.char, y, x)

            continue

        # Refresh the window:

        self.refresh()

    def display(self):

        """
        Displays the tilemap to the screen,
        refreshing it each loop.

        This allows enemies and the player to move.
        """

        self.run = True

        # Start our thread:

        self.thread = threading.Thread(target=self._input_loop)
        self.thread.daemon = True
        self.thread.start()

        self._render()

        while self.run:

            # Update the tilemap:

            self.tilemap.update()

            self._render()

    def _add_key(self, key, obj):

        """
        Adds the key to the object.

        :param key: Key to add
        :type key; int
        :param obj: Object to add the key to
        :type obj: BaseCharacter
        """

        # Add the key to the object:

        obj.add_input(key)

    def _input_loop(self):

        """
        Continuously accepts input from the queue,
        adding keys to the relevant characters.
        """

        while self.run:

            # Get a key and handle it:

            inp = self.get_input()

    def stop(self):

        """
        Stops the DisplayWindow event loop.
        """

        self.run = False

        # Add a 'None' object to each input queue to clear the inputs

        for key, call in self._calls.items():

            if call['call'] == self._add_key:

                # Add 'None' to the input queue:

                call['args'][1].add_input(None)


class TextDisplayWindow(BaseWindow):

    def __init__(self, win):

        super(TextDisplayWindow, self).__init__(win)
        self.attrib = []
        self.win = win
        self.run = True

    def add_content(self, content, attrib = "light_blue", newLine = True):

        self.attrib = [attrib]

        if type(content) == str:

            self.addstr(str(content), attrib = self.attrib)

        if type(content) == list:

            if len(content) == 1:

                if isinstance(content[0], Tile):

                    self.addstr(str(content[0].obj.name) + ", " + str(content[0].x) + ", " + str(content[0].y), attrib=self.attrib)

                else:

                    self.addstr(str(content[0]), attrib = self.attrib)

            elif len(content) > 0:

                for x in content:

                    if isinstance(x, Tile):

                        self.addstr(str(x.obj.name) + ", " + str(x.x) + ", " + str(x.y), attrib = self.attrib)
                        self.addstr("\n")

                    else:

                        self.addstr(str(x), attrib=self.attrib)
                        self.addstr("\n")

        if newLine:

            self.addstr("\n")

        self.refresh()


class InputWindow(BaseWindow):

    """
    CHAS Input window
    Allows for the input of multiple characters, and scrolling
    Will use the ENTIRE window
    """

    def __init__(self, win):

        self.win = win  # Curses window provided

        super(InputWindow, self).__init__(win)  # Passing window to super class

        self.run = True  # Value determining if we are capturing input

        self.curs_x = 0  # Cursor x position
        self.curs_y = 0  # Cursor y position

        self.scroll = 0  # Number of lines we scrolled down

        self.inp = []  # Input data, each entry is a separate character

        self.prompt_len = 0  # Prompt for input system

        # Enabling cursor

        curses.curs_set(True)

        # Adding the necessary callbacks

        self.add_callback(curses.KEY_RIGHT, self._increment_cursor)
        self.add_callback(curses.KEY_LEFT, self._decrement_cursor)
        self.add_callback(curses.KEY_UP, self._decrement_cursor_line)
        self.add_callback(curses.KEY_DOWN, self._increment_cursor_line)
        self.add_callback([curses.KEY_BACKSPACE, 8], self._decrement_delete)
        self.add_callback([curses.KEY_ENTER, 10, 13], self._stop)

    def input(self, prompt="", add=''):

        """
        Starts recording input from user.
        We block until the user exist the window.

        :param prompt: Prompt to display
        :param add: Adds the specified input to the window. Unlike the prompt, can be edited.
        :return: Input in our collection
        """

        # Resetting the object

        self._reset_object()

        # Getting the length of the prompt and setting it

        self.prompt_len = len(prompt)

        for i in list(prompt):
            # Adds the prompt to the internal collection:

            self.inp.append(i)

        self.curs_x = self.prompt_len % self.max_x
        self.curs_y = floor(self.prompt_len / self.max_x)

        for i in list(add):
            # Adds the editable content to the internal collection:

            self.inp.append(i)

        self._render()

        while self.run:

            # Getting key

            key = self.get_input(ignore_special=True)

            # Interpreting key

            if not key:
                # Key has been handled, render screen and continue

                self._render()

                continue

            # Key has not been handled, is string we can work with

            # Altering internal collection of inputs:

            index = self._calc_pos()

            self.inp.insert(index, key)

            # Render in the data and increment the cursor

            self._increment_cursor()
            self._render()

        return self._combine()

    def _reset_object(self):

        """
        Resets the input system and all internal attributes
        """

        self.inp = []  # Clearing internal input
        self.run = True  # Setting run value to True

        self.curs_x = 0  # Setting cursor x to 0
        self.curs_y = 0  # Setting cursor y to 0

        self.scroll = 0  # Setting scroll to zero

        self.win.clear()  # Clears the window

        self.refresh()  # Refreshes window to make changes final

    def _get_lines(self):

        """
        Gets the number of lines the internal input will take up.

        :return: Number of lines will be used
        """

        return ceil(len(self.inp) / self.max_x)

    def _calc_pos(self):

        """
        Function for calculating the position of a character in the list,
        Uses cursor position.

        :return: Index in input list
        """

        return ((self.curs_y + self.scroll) * self.max_x) + self.curs_x

    def _increment_cursor(self):

        """
        Increments the cursor, moves to new line if necessary.
        """

        # Check if we are moving past our text:

        if self.curs_x == len(self.inp) % self.max_x and self.curs_y == self._get_lines() - 1:
            # Going to be too big, do not increment!

            return

        # Check if we have to move to a new line

        if self.curs_x == self.max_x - 1:

            # Move cursor to new line

            if self.curs_y == self.max_y - 1 and self._get_lines() > self.curs_y + self.scroll:

                # Scrolling data down one

                self.scroll = self.scroll + 1
                self.curs_x = 0

            elif self.curs_y != self.max_y - 1:

                self.curs_x = 0
                self.curs_y = self.curs_y + 1

        else:

            # Move cursor forward one

            self.curs_x = self.curs_x + 1

    def _decrement_cursor(self):

        """
        Decrements the cursor, moves up lines if necessary.
        """

        if self.curs_x == 0:

            # Move cursor down one line

            if self.curs_y == 0:

                # Scroll content upwards

                self.scroll = (self.scroll - 1 if self.scroll > 0 else 0)
                self.curs_x = (self.max_x - 1 if self.scroll > 0 else self.prompt_len - 1)

            else:

                # Move cursor up one line

                self.curs_y = self.curs_y - 1
                self.curs_x = self.max_x - 1

        elif self.curs_y + self.scroll == floor(self.prompt_len / self.max_x):

            # Make sure we don't go over our prompt

            self.curs_x = (self.curs_x - 1 if self.curs_x > self.prompt_len % self.max_x
                           else self.prompt_len % self.max_x)

        elif self.curs_x != 0:

            # Move cursor back one

            self.curs_x = self.curs_x - 1

    def _decrement_cursor_line(self):

        """
        Decrements the cursor by one line
        """

        if self.curs_y + self.scroll == floor(self.prompt_len / self.max_x):

            # Input prompt is on our line, see if we can scroll!

            if self.scroll > 0:
                # We can scroll down, do it:

                self.curs_y = self.curs_y + 1
                self.scroll = self.scroll - 1

            return

        if self.curs_y == 0 and self.scroll > 0:

            # Scroll upwards:

            self.scroll = self.scroll - 1
            self.curs_x = (self.curs_x if self.curs_x > self.prompt_len % self.max_x else self.prompt_len % self.max_x)

        elif self.curs_y > 0:

            # Scroll cursor up one

            self.curs_y = self.curs_y - 1
            self.curs_x = (self.curs_x if self.curs_y + self.scroll > floor(self.prompt_len / self.max_x)
                           else self.curs_x if self.curs_x > self.prompt_len % self.max_x
            else self.prompt_len % self.max_x)

    def _increment_cursor_line(self):

        """
        Increments the cursor by one line
        :return:
        """

        if self.curs_y == self.max_y - 1 and self._get_lines() - 1 > self.curs_y + self.scroll:

            # Bottom of the screen, scroll content up by one line

            self.scroll = self.scroll + 1

        elif self.curs_y < self.max_y - 1 and self._get_lines() - 1 > self.curs_y:

            # Move cursor up by one line

            self.curs_y = self.curs_y + 1

    def _decrement_delete(self):

        """
        Decrements the cursor and deletes the character at the position,
        effectively deleting the previous character.
        """

        if len(self.inp) - self.prompt_len == 0:
            # Nothing left, return

            return

        # Moving the cursor back

        self._decrement_cursor()

        # Deleting the character

        self._delete()

    def _delete(self):

        """
        Deletes a character at the given cursor position.
        """

        # Removing character from internal input

        if self.curs_x + ((self.curs_y + self.scroll) * self.max_x) < len(self.inp):
            # Position is within range, removing character

            self.inp.pop(self._calc_pos())

            # Deleting character at cursor position:

            self.win.delch(self.curs_y, self.curs_x)

        return

    def _combine(self):

        """
        Returns the combined list of inputs.

        :return: String of all combined inputs
        """

        return "".join(self.inp)[self.prompt_len:]

    def _render(self):

        """
        Renders the internal input to screen
        Uses cursor pos, scroll level, and max cords.
        """

        # Clear the window

        self.clear()

        # Calculate start index

        start = (self.scroll * self.max_x)
        end = (start + (self.max_y * self.max_x))

        # Getting output from list

        out = self.inp[start:end]

        for ind, char in enumerate(out):
            # Calculating x and y values for current character

            y = floor(ind / self.max_x)
            x = ind - (y * self.max_x)

            # Adding character to window

            self.win.insstr(y, x, char)

        # TODO: Remove this section
        '''
        # Some debug info,
        # TODO: REMOVE THIS SECTION!!!

        self.sub_header.clear()
        self.sub_header.addstr(f"X: {self.curs_x} ; Y: {self.curs_y} ; SCROLL: {self.scroll}")
        '''

        # Moving cursor to set position

        self.win.move(self.curs_y, self.curs_x)

        # Refreshing window, so changes are shown

        self.refresh()

        return

    def _stop(self):

        """
        Stops the input and any services that need to be stopped.
        """

        self.run = False


class ScrollWindow(BaseWindow):
    """
    A curses window for handling content scrolling.
    """

    def __init__(self, win):

        # Constructs the BaseWindow

        super(ScrollWindow, self).__init__(win)

        self.pos = 0  # Scroll position we are at

        self.content = []  # Content to render
        self.running = False  # Value determining if we are running

        self.thread = None  # Threading instance for frontend

        self.keys = queue.Queue()  # Queue for holding keypress

        # Adding callbacks:

        self.add_callback(curses.KEY_DOWN, self._increment_scroll)
        self.add_callback(curses.KEY_UP, self._decrement_scroll)
        self.add_callback('r', self._render_content)
        self.add_callback([curses.KEY_END, curses.KEY_EXIT, 'f'], self.stop)

    def get_key(self, block=True, timeout=None):

        """
        Gets a key from the key queue
        :return: Key from queue, or common queue returncodes
        """

        return self.keys.get(block=block, timeout=timeout)

    def run_display(self, content):

        """
        Starts a thread to render in front end, and allow the backend to continue to operate
        :param content: Content to render
        """

        if type(content) == list:

            # Working with a list of content:

            for i in content:

                temp = self._split_content(i)

                for v in temp:
                    self.content.append(v)

        else:

            self.content.append(self._split_content(content))

        self.thread = threading.Thread(target=self._display_content)

        self.running = True

        self.thread.start()

    def stop(self):

        """
        Stops the thread and stops rendering content
        """

        if not self.running:
            return

        self.running = False

    def block(self):

        """
        Blocks until the scroll window is stopped by the user
        """

        self.thread.join()

    def is_running(self):

        """
        Checks if the thread is still running
        :return: True for is running, False for is not running
        """

        return self.running

    def _display_content(self):

        """
        Displays content on a scrollable window.
        Can move up or down to see content.
        Content MUST be in list form, each value being on a separate line.
        :return:
        """

        self.win.refresh()

        while self.running:
            # Get key and handle it:

            key = self.get_input()

    def add_content(self, content):

        """
        Adds content to the internal collection.
        Handles the formatting of newlines and splitting content that is too big for the screen.
        :param content: Content to add
        """

        split = []

        # Getting split content:

        if type(content) == list:

            # Working with a list:

            for i in content:

                temp = self._split_content(i)

                for v in temp:
                    split.append(v)

        else:

            split = self._split_content(content)

        # Adding content to the end of the collection

        for i in split:
            self.content.append(i)

        return

    def clear(self):

        """
        Clears the internal collection.
        """

        self.content = []

    def _split_content(self, content):

        """
        Splits up strings based on newlines, and if they are too big for the window.
        :param content: Content to split
        :return: List of split content
        """

        lines = content.split('\n')
        new = []

        for line in lines:

            # Check if line is larger than the width

            if len(line) > self.max_x:

                # Content is bigger, do something about it

                num = ceil(len(line) / self.max_x)

                for i in range(num):
                    # Iterate over each section and separate it

                    new.append(line[i * self.max_x:(i + 1) * self.max_x])

                continue

            new.append(line)

        return new

    def _increment_scroll(self):

        """
        Increments the scroll by one, does not increase if it is greater than the content provided
        """

        if len(self.content) - 1 > self.pos:
            # Increase the position, it is valid

            self.pos = self.pos + 1

        # Render the content

        self._render_content()

    def _decrement_scroll(self):

        """
        Decrements the scroll by one, does not decrease if it is zero.
        """

        if self.pos > 0:
            self.pos = self.pos - 1

        # Render the content

        self._render_content()

    def _render_content(self):

        """
        Renders the content to the screen based on the position.
        We make a point not to touch the bottom line, as scrolling messes things up.
        """

        # Clearing window:

        self.win.erase()

        # Getting content to render:

        content = self.content[self.pos:self.max_y + self.pos - 1]

        for num, val in enumerate(content):
            self.addstr(val, num, 0)

        self.refresh()


class OptionWindow(BaseWindow):
    """
    Displays a list of options to the user.
    Support simple selection, boolean selection, and value selection.  
    """

    NULL_OPTION = 0
    EXIT_OPTION = 1
    SIMPLE_SELECT = 2
    TOGGLE_SELECT = 3
    VALUE_SELECT = 4
    MANUAL_SELECT = 5
    SUB_MENU = 6
    RUN_OPTION = 7

    def __init__(self, win):

        super(OptionWindow, self).__init__(win)

        self.option_position = 0  # Option to select on screen

        self.scroll_position = 0  # Scroll level we are currently on

        self.options = []  # List of options, must abide by the CHASOptions convention

        self.run = True  # Value determining if we are running

        self.simple = False  # Determining if we are working with Simple Selection

        self.selected = None  # Selected option, used only for simple selection

        self.title = ''  # Title of our window

        # Adding necessary callbacks:

        self.add_callback(['q', 'e'], self._stop)
        self.add_callback(curses.KEY_UP, self._decrement_cursor)
        self.add_callback(curses.KEY_DOWN, self._increment_cursor)
        self.add_callback([curses.KEY_ENTER, 10, 13], self._handle_selection)
        self.add_callback('r', self.refresh)

    def display(self, no_return=False, title='Option Window'):

        """
        Displays the options in our collection, run until we exit
        :param no_return: Determines if we should return values. Great for menus that might need to display
        content multiple times.
        :param title: Will render in a title in the header of the window.
        :return: Option selected, or in dictionary format
        """

        # We add an Exit value to the window, so the user can easily exit

        self.add_option('Exit', OptionWindow.EXIT_OPTION)

        # Render in header and border:

        if self.header is None and self.sub_header is None:
            self.border(header_len=1, sub_len=1)

        self.title = title

        self.header.addstr(title)

        # Starting the window:

        self.run = True

        while self.run:
            # Getting key from user:

            self._render()

            key = self.get_input(return_ascii=True)

        self.options.pop(len(self.options) - 1)

        if no_return:
            # Return nothing, we are done here

            return

        if self.simple:
            # Simple selection, return selected value

            return self.selected

        # Otherwise, we return the options, they are edited as the user wants them to be.

        return self._convert()

    def add_option(self, name, option_type, desc='', value=None):

        """
        Adds a singular option to the collection.
        If no value is specified, then a default one will be selected.
        :param name: Name of the option
        :param option_type: Type of the option
        :param desc: Description of the option
        :param value: Value of the option
        """

        if option_type == OptionWindow.SIMPLE_SELECT:
            # Working with simple select, make sure this object knows that

            self.simple = True

        if option_type == OptionWindow.VALUE_SELECT:
            # We need to use a special format for selecting values:

            value = [value, value[0]]

        if option_type == OptionWindow.SUB_MENU and type(value) is not OptionWindow:
            # We need to create an OptionWindow instance to work with:

            new = OptionWindow.create_subwin_at_pos(self.parent, self.parent.getmaxyx()[0], self.parent.getmaxyx[1])

            new.add_options(value)

            value = new

        if option_type == OptionWindow.MANUAL_SELECT and value is None:
            value = ''

        self.options.append({'name': name, 'type': option_type, 'desc': desc, 'value': value})

    def add_options(self, options):

        """
        Gets a list/dictionary of options and creates an option menu that conforms to the list/dictionary format.
        If the value provided is a list of values, then OptionWindow will make a simple
        selection menu with those values.
        If the value provided is a dictionary, then OptionWindow will attempt to create options with the best
        corresponding values.
        If you don't like OptionWindow's interpretation of your values, you should add them manually.
        :param options: List/dictionary of options
        """

        if type(options) == list:

            # Working with a list, make them all simple selection

            for opt in options:
                self.add_option(opt, OptionWindow.SIMPLE_SELECT)

        if type(options) == dict:

            # Working with dict, dynamically select the appropri1ate option for each value

            for opt in options:

                # Check which type opt is, and handle accordingly

                val = options[opt]

                if type(val) == str:
                    # Create a manual selection option

                    self.add_option(opt, OptionWindow.MANUAL_SELECT, value=val)

                    continue

                if type(val) == list:
                    # Create a Value Select option

                    self.add_option(opt, OptionWindow.VALUE_SELECT, value=val)

                    continue

                if type(val) == bool:
                    # Create a Toggle Select

                    self.add_option(opt, OptionWindow.TOGGLE_SELECT, value=val)

                if type(val) == dict:
                    # Create a sub-menu

                    new = OptionWindow.create_subwin_at_pos(self.win, self.max_y - 1, self.max_x - 1)

                    new.add_options(val)

                    self.add_option(opt, OptionWindow.SUB_MENU, value=new)

                    continue

                if isfunction(val):
                    self.add_option(opt, OptionWindow.RUN_OPTION, value=val)

                    continue

                if val is None:
                    # Create a Null Selection

                    self.add_option(opt, OptionWindow.NULL_OPTION)

                    continue

    def get_options(self):

        """
        Calls the underlying _convert method and returns the internal collection of options in dictionary format.
        :return: Dictionary of options
        """

        if self.simple:
            # Simple selection, return selected

            return self.selected

        # Something else, return it:

        return self._convert()

    def _convert(self):

        """
        Converts the internal collection of options into dictionary format.
        :return: Options in dictionary format
        """

        # Iterate over each option and handle them accordingly

        done = {}

        for opt in self.options:

            if opt['type'] == OptionWindow.EXIT_OPTION or opt['type'] == OptionWindow.NULL_OPTION:
                # We don't care about these values, continue:

                continue

            if opt['type'] == OptionWindow.VALUE_SELECT:
                # Value uses a special format, pull out the necessary values:

                done[opt['name']] = opt['value'][1]

                continue

            if opt['type'] == OptionWindow.SUB_MENU:
                # We need to pull the options out of the sub menu:

                done[opt['name']] = opt['value'].get_options()

                continue

            done[opt['name']] = opt['value']

        return done

    def _calc_position(self):

        """
        Calculates the position in the list based on scroll level and scroll position
        :return: Index of selected position in the list
        """

        return (self.scroll_position * self.max_y) + self.option_position

    def _increment_cursor(self):

        """
        Moves the cursor up 1, and scrolls the screen if necessary.
        :return:
        """

        if self.option_position < self.max_y - 1 and self.option_position + (self.scroll_position * self.max_y) < \
                len((self.options if len(self.options) > 1 else 2)) - 1:
            # Less than the window, move option selection up one.

            self.option_position = self.option_position + 1

            return

        if len(self.options) - 1 > (self.max_y * self.scroll_position) + self.option_position:
            # We have to scroll the window upwards

            self.scroll_position = self.scroll_position + 1

            self.option_position = 0

        return

    def _decrement_cursor(self):

        """
        Moves the cursor down 1, scrolls the screen if necessary.
        :return:
        """

        if self.option_position > 0:
            # We are good to move the option position down

            self.option_position = self.option_position - 1

            return

        # We have to scroll the window down:

        if self.scroll_position > 0:
            # Scroll the window down

            self.scroll_position = self.scroll_position - 1

            self.option_position = self.max_y - 1

            return

        return

    def _get_type_name(self, opt):

        """
        Gets a type name from the option provided.
        :param opt: Option provided.
        :return: Preview value   
        """

        opt_type = opt['type']

        if OptionWindow.TOGGLE_SELECT == opt_type:

            # Working with a toggle, determine if we are rendering true/false

            if opt['value']:
                # Render in a True

                return '[True]'

            return '[False]'

        if OptionWindow.MANUAL_SELECT == opt_type:
            # Render in 'Enter, subject to change

            return '[Enter]'

        if OptionWindow.SUB_MENU == opt_type or OptionWindow.VALUE_SELECT == opt_type:
            # Render in '>', subject to change

            return '[>]'

        if OptionWindow.RUN_OPTION == opt_type:
            # Display a simple '[run]'

            return '[Run]'

        # No special preview name required!

        return ''

    def _get_shortened_name(self, opt, num):

        """
        Gets a shortened name from the option given.
        This is calculated from the maximum x value, as well as the preview value.
        We also render in the number of the option, and take that into account for our shortening.
        """

        # Get type name here:

        type_name = self._get_type_name(opt)

        # Calculate stopping distance for the name

        stop = self.max_x - len(type_name) - (7 if num > 0 else 4) - (len(str(num)) if num > 0 else 0)

        # Returning shortened name:

        return ('[{}]:'.format(num) if num > 0 else '') + opt['name'][:stop] + \
               ('...' if stop < len(opt['name']) else '')

    def _render(self):

        """
        Renders the selected content to the screen.
        """

        # Iterate over every relevant option and render it to the screen:

        self.win.erase()

        off = 0  # Offset to render numbers:

        for num, opt in enumerate(self.options[self.scroll_position * self.max_y:
        (self.scroll_position + 1) * self.max_y]):

            # Get shortened name(If necessary):

            if opt['type'] == OptionWindow.NULL_OPTION:
                # Don't render an option number, it is a null option!

                off = off + 1

            name = self._get_shortened_name(opt, num + 1 + (self.max_y * self.scroll_position) - off
            if opt['type'] != OptionWindow.NULL_OPTION else -1)

            # Get type name:

            type_name = self._get_type_name(opt)

            # Render option name to screen:

            self.addstr(name, num, 0, attrib=([curses.A_STANDOUT] if num == self.option_position else None))

            # Render Type Name to screen:
            # We render with some special tricks to ensure that the window does not scroll

            self.addstr(type_name, num, self.max_x - len(type_name) - 1)
            self.win.insstr(num, self.max_x - len(type_name) - 1, " ")

        # Refresh the screen, as we are done rendering.

        self.refresh()

    def _handle_selection(self):

        """
        User selected the option we are currently on, handle it and make any changes.
        We edit the options list directly.
        :return:
        """

        # Clearing window:

        self.clear()

        # Get index of option:

        index = self._calc_position()

        # Handel option:

        self.options[index] = self._handle_option(self.options[index])

        return

    def _handle_option(self, opt):

        """
        Handles the option selected, and does any actions necessary
        :return: Altered option list
        """

        opt_type = opt['type']

        if OptionWindow.NULL_OPTION == opt_type:
            # This is a null option, do nothing

            return opt

        if OptionWindow.EXIT_OPTION == opt_type:

            # This is exit option, exit.
            # If simple selection, select the first option

            self._stop()

            if self.simple:
                return self.options[0]['name']

            return opt

        if OptionWindow.SIMPLE_SELECT == opt_type:
            # Simple selection, return value selected:

            self.run = False

            self.selected = opt['name']

            return opt

        if OptionWindow.TOGGLE_SELECT == opt_type:
            # Toggle the option on/off, return opposite

            opt['value'] = not opt['value']

            return opt

        if OptionWindow.VALUE_SELECT == opt_type:
            # Have the user choose from a list of options:

            # Create a new Option Menu, should be overlayed on top of ours:

            new = OptionWindow.create_subwin_at_pos(self.win, self.max_y, self.max_x)

            new.add_options(opt['value'][0])

            opt['value'][1] = new.display(title=opt['name'])

            return opt

        if OptionWindow.MANUAL_SELECT == opt_type:

            # Have the user manually enter an option:

            # Create an input window:

            input_win = InputWindow.create_subwin_at_pos(self.win, self.max_y, self.max_x,
                                                         position=BaseWindow.CENTERED)

            # Create a border for viewing enjoyment:

            input_win.border(header_len=1, sub_len=1)

            input_win.header.addstr("Enter/Edit Value Below:")

            input_win.refresh()

            inp = input_win.input(add=opt['value'])

            if inp is None:
                return opt

            opt['value'] = inp

            return opt

        if OptionWindow.SUB_MENU == opt_type:
            # Open up the OptionWindow associated with the sub menu.
            # Don't return the content, we leave that to the converter.

            # Clear our header:

            self.header.clear()

            opt['value'].display(no_return=True, title=opt['name'])

            # Clear options window's header

            opt['value'].header.clear()

            self.header.addstr(self.title)

            return opt

        if OptionWindow.RUN_OPTION == opt_type:
            opt['value']()

            return opt

    def _stop(self):

        """
        Stops the OptionWindow.
        :return:
        """

        self.run = False


class Color:

    def __init__(self, colorNumber, colorPairNumber, name, r, g, b):

        curses.init_color(colorNumber, r, g, b)
        curses.init_pair(colorPairNumber, colorNumber, curses.COLOR_BLACK)

        self.colorPairNumber = colorPairNumber
        self.resolvedColor = curses.color_pair(colorPairNumber)
