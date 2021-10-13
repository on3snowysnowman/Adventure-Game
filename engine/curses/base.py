"""
Base - Base curses features.

This file will contain the base curses features 
that all other components will utilise,
such as BaseWindow and MasterWindow.

Other more advanced curses features such as input, 
display, and drawing features will be found in other files in this directory. 
"""

import curses
import threading

from math import ceil
from queue import Queue

# TEMPORARY IMPORT:

import logging
import traceback as tb



class Color:

    """
    A class representing a color, which can easily integrate with BaseWindow.

    This class aims to simplify color developmen,
    and to make the process of displaying colors and attributes much easier.

    # TODO: This method might need some changes
    """

    def __init__(self, colorNumber, colorPairNumber, name, r, g, b):
        curses.init_color(colorNumber, r, g, b)
        curses.init_pair(colorPairNumber, colorNumber, curses.COLOR_BLACK)

        self.name = name
        self.colorPairNumber = colorPairNumber
        self.resolvedColor = curses.color_pair(colorPairNumber)


class BaseWindow:

    """
    Custom CURSES wrappings.

    We try to make curses development as simple as possible,
    while emulating the normal curses options as much as possible.

    We also offer some handy ways to integrate with the MasterWindow,
    such as optimized refreshing, handled input, and resizing(?)
    BaseWindow automatically identifies these changes and applies them automatically,
    so the developer/application should see no difference in a managed BaseWindow.

    Handles the following actions:
    1. Writing content to a window
    2. Creating subwindows
    3. Handling borders/headers/subheaders - (N/A)
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
        self.done = False  # Value determining if we are done displaying info

        self.managed = False  # Value  determining if our input is handled
        self.input_queue = None  # Queue to store inputs - only relevant if we are managed!
        self.master: MasterWindow  # Instance of MasterWindow controlling us - only relevant if we are managed!

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

        curses.cbreak()

        # Start Keypad handling

        self.win.keypad(True)

        # Allowing scrolling

        self.win.scrollok(True)

        # Allow hardware line editing facilities

        self.win.idlok(True)

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

    def stop(self):

        """
        Makes it clear that we are done displaying and working in the terminal.

        We clear the screen and set our done attribute to True.
        This is very useful for MasterWindow, which needs this information to determine when to exit.
        """

        # Set our 'done' attribute:

        self.done = False

        # CLear the screen

        self.clear()

        # Check if we are managed:

        if self.managed:

            # Tell the MasterWindow we are done:

            self.master.mark_done(self)

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

    def add_key(self, key, call=None, pass_self=False, args=None):

        """
        Adds a key that we are interested in to the window.
        While not very helpful on it's own,
        this tells MasterWindow what keys we require, if this window ever becomes managed.

        Optionally, you can specify a callback.
        When BaseWindow encounters the given key(s),
        then it will call the callback specified when 'get_input()' is called.
        You can specify a list of arguments to send to the callback,
        and BaseWindow can optionally pass itself to this function if necessary
        (self will the the first argument, if a list of arguments is specified).

        The 'wildcard' is None.
        If 'None' is specified, then ALL input will be directed to the specified callback.
        MasterWindow will interpret 'None' similarly,
        all input will be directed to this window if their are no other windows focused.

        :param key: Key to be pressed, can be string or list, special characters included
        :param call: Function to be called, leave 'None' for no function call
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

                self._register_keybind(val, call, args)

                return

        # Working with a single string here

        elif type(key) == str:
            # Convert string into ascii value

            key = ord(key)

        # Add key/function/args to dictionary of keys to handle

        self._register_keybind(key, call, args)

        if key is None:

            # This node requires ALL inputs, add a callback for the MasterWindow

            self._calls[None] = {'call': None, 'args': []}

            if self.managed:

                # Attach ourselves to the master window:

                self.master.bind_key(self, None)

        return

    def handle_key(self, key):

        """
        Handles a specified key.

        :param key: Key to be handled
        """

        if key in self._calls and self._calls[key]['call'] is not None:

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

            # We are managed, update the virtual screen:

            self.win.noutrefresh()

            # Mark the master window for refresh:

            self.master.need_refresh()

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

        # TODO: Look at this method!

        As of now, this method and the methods used are not compatable with MasterWindow!
        Subheaders and Headers might be better off in their own function?
        We should also fix the sub-windows created, as they do not integrate with the MasterWindow.

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

        # Refresh the parent - Should be the only time we will have to:

        self.parent.refresh()

    def clear(self):

        """
        Clears all content from the curses window.

        :return: Standard curses returncodes
        """

        return self.win.erase()

    def manage(self, master):

        """
        Sets the window mode to 'managed'. This does a few things:

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

        We offer the ability to automatically decode input characters to their ascii values.
        We also offer the ability to ignore special characters, returning False in their place.

        If the user does not want keys passed though the callbacks,
        then they can optionally disable this feature for this call only.

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
            # TODO: BETTER ERROR HANDLING!!!!!

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
        light_blue = Color(14, 6, "light_blue", 0, 900, 1000)
        brown = Color(15, 7, "brown", 550, 350, 0)
        light_brown = Color(16, 8, "light_brown", 527, 492, 425)
        white = Color(17, 9, "white", 1000, 1000, 1000)
        gray_blue_one = Color(18, 10, "gray_blue_one", 250, 350, 758)
        gray_blue_two = Color(19, 20, "gray_blue_two", 110, 280, 600)

        self.register_color("blue", blue)
        self.register_color("green", green)
        self.register_color("yellow", yellow)
        self.register_color("red", red)
        self.register_color("orange", orange)
        self.register_color("light_blue", light_blue)
        self.register_color("brown", brown)
        self.register_color("light_brown", light_brown)
        self.register_color("white", white)
        self.register_color("gray_blue_one", gray_blue_one)
        self.register_color("gray_blue_two", gray_blue_two)

    def _register_keybind(self, key, call, args):
        """
        Registers the given key to this object.

        We determine if a callback is necessary to add.
        We also check if we are managed,
        and if this is the case then we update the MasterWindow we are attached to.

        :param key: Key to register
        :type key: int
        :param call: Callback to register, if any
        :type call: None, func
        :param args: Arguments to pass to the callback at runtime
        """

        # Add the key:

        self._calls[key] = {'call': call if call is not None else None, 'args': args}

        # Check if we are managed:

        if self.managed:

            # Add this callback to the MasterWindow:

            self.master.bind_key(self, key)

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
    A window can request certain keys by providing them in the 'add_keys' method.
    They can optionally provide a callback, this makes no difference to MasterWindow
    as we only care about the keys.

    We also handle the process of refreshing windows,
    specifically physically updating the entire screen when a sub-window requests it.
    This removes a lot of drawing latency, and greatly reduces screen flicker.

    We have a thread dedicated to getting input information from curses and sending it to the sub-windows,
    This ensures that no input "overflows" into the display,
    and that our input content is handled quickly and sent to where it is excpected.

    At some later date, a more robust focusing method would be nice,
    as well as 'window-commands', which will simplify the method of focusing windows.
    We should also implement better 'window to window communication',
    so managed windows can interact with other managed windows.
    """

    def __init__(self, win):

        super(MasterWindow, self).__init__(win)

        self.win = win  # Master window to do our operations on

        self.thread = None  # Threading object
        self.event_queue = Queue()  # Event queue
        self._win_calls = {None: []}  # Mapping inputs to windows

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

        If a callback is specified as 'None', then all input will be directed to that window.
        Great if multiple windows need multiple input sources.

        :param subwin: Subwidow to extract callbacks from
        :type subwin: BaseWindow
        """

        for key in subwin._calls:

            # Bind the key:

            self.bind_key(subwin, key)

    def bind_key(self, subwin, key):
        """
        Method used to bind a key to a window.

        THIS METHOD DOES NOT ALTER THE CALLBACKS/KEYBINDS OF THE SUBWINDOW!

        Instead, we only alter our understanding of the keybindings.
        This means that we will put the relevant key into the event queue
        of the relevant sub-window when encountered.

        :param subwin: Subwindow to bind the key to
        :type subwin: BaseWindow
        :param key: Key to bind
        :type key: int
        """

        if key in self._win_calls.keys():

            # Key is present in window callbacks already, lets add it:

            self._win_calls[key].append(subwin)

        else:

            # Key is NOT present, lets make a new entry:

            self._win_calls[key] = [subwin]

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

    def need_refresh(self):

        """
        Add a 'refresh' event to the MasterWindow event queue.

        The 'refresh' event is a None value.
        When the event loop comes across a refresh value,
        then it does a physical screen refresh.
        """

        self.event_queue.put(None)

    def mark_done(self, win):

        """
        Removes the given window from the sub-list.

        If the sub-list is empty, then MasterWindow stops the event loop
        (If it is still running).
        """

        # Remove the window from the sublist

        self.subwins.remove(win)

        # Remove window from focus list, if present:

        if win in self.focus:

            self.focus.remove(win)

        # Check if we are done:

        if not self.subwins:

            # No more subwindows, let's exit:

            self.stop()

    def start(self):

        """
        Starts the MasterWindow input thread,
        and starts handling operations on sub-windows.

        We redirect input to relevant windows,
        as well as handle physical screen refreshes.
        """

        # Start the input thread:

        self._start_thread()

        # Iterate over our event loop:

        while self.run:

            # Get input from our input queue:

            inp = self.event_queue.get()

            # Check if we have to refresh the windows:

            if inp is None:

                # Refresh the physical screen:

                curses.doupdate()

                # Mark task as complete:

                self.event_queue.task_done()

                continue

            # Send input to focused window(If any):

            if self.focus:

                # Focused windows, iterate over them and send input:

                for win in self.focus:

                    win.add_input(inp)

            else:

                # Send the input to relevant window only:

                black = []  # Key blacklist - Used for adding window that we have already handled

                if inp in self._win_calls.keys():

                    # Key is present, lets send it over:

                    for win in self._win_calls[inp]:

                        # Append window to blacklist:

                        black.append(win)

                        # Add the input to the specified window:

                        win.add_input(inp)

                        logging.info("Sent input {} to window: {}".format(inp, win))

                # Iterate over the 'wildcard' windows:

                for win in self._win_calls[None]:

                    # Check if the window is blacklisted:

                    if win not in black:

                        # Add input to the window:

                        win.add_input(inp)

            # Mark task as complete:

            self.event_queue.task_done()

    def stop(self):

        """
        Stops all MasterWindow components,
        specifically the input loop and event loop.

        We also stop all child windows,
        so we can be absolutely sure that CURSES will be done upon exiting.

        We also request a refresh, so any changes made will carry over.
        """

        # Stop all sub-windows:

        for win in self.subwins:

            # Stop the window:

            win.stop()

        # Request a refresh:

        self.need_refresh()

        # Stop the window:

        self.run = False

    def _run(self):

        """
        Input event loop, continuously pulls values from CURSES and adds it to the input queue.
        """

        while self.run:

            try:

                logging.info("Master waiting for input...")

                inp = self.get_input(return_ascii=True, no_calls=True)

                self.event_queue.put(inp)

                logging.info("Master input: {}".format(inp))

            except Exception as e:

                logging.info("Encountered exception: {}".format(e))
                logging.info("Traceback: {}".format(tb.format_exception(None, e, e.__traceback__)))
