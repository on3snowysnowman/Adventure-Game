"""
Curses windows that handle displaying content.

We have the following components:

    > ScrollWindow - Displaying and wrapping content to the screen, 
    allowing users to scroll through content bigger than the screen.
    > DisplayWindow - Handles the displaying of tilemaps to the screen

These windows do sometimes take input,
so they should be used with MasterWindow to prevent any conflicts.
"""

import curses
import threading

from queue import Queue
from math import ceil

from engine.curses.base import BaseWindow
from engine.tilemaps import BaseTileMap
from engine.characters.tiles import Fog


class DisplayWindow(BaseWindow):

    """
    New display window for testing.

    We handle displaying tilemaps to the screen,
    and displaying visual game information.
    Most likely, this is where the graphics of the game will be displayed.
    """

    def __init__(self, win):

        super(DisplayWindow, self).__init__(win)

        self.win = win  # CURSES window instance

        # We simply create a tilemap with our width and height,
        # as the DisplayWindow is not smart enough to handle anything different

        # self.tilemap = BaseTileMap(self.max_y, self.max_x, self)  # Tilemap storing game info
        self.tilemap = BaseTileMap(self.max_y, self.max_x, self)
        #self.camera = Camera(self.tilemap, self)
        self.run = True  # Value determining if we are running

        self.thread = None  # Treading instance of the input loop

    def _render(self):

        """
        Renders the tilemap content based on the display area of camera to our screen.
        """

        self.clear()

        for x, y, z, obj in self.tilemap._iterate():

            # Render the character at specified position. We don't care about secondary characters!

            self.tilemap.tilemap[y][x].sort(key=self.tilemap._get_priority)

            if z == 0:

                if isinstance(self.tilemap.tilemap[y][x][z], Fog):

                    continue

                self.addstr(obj.char, y, x, attrib=obj.attrib)

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

        while self.run:

            # Update the camera
            #self.camera.update()

            self._render()

            #self.tilemap.scrollWin._render_content()

            # Update the tilemap:
            self.tilemap.update()

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

        # Mark ourselves as done:

        super(DisplayWindow, self).stop()


class ScrollWindow(BaseWindow):

    """
    A curses window for handling content scrolling.

    #TODO: Fix scroll implementation!

    Is a threading model really necessary?
    See if we can re-write to be blocking instead,
    and still allow for on-the-fly content addition.
    """

    def __init__(self, win):

        # Constructs the BaseWindow

        super(ScrollWindow, self).__init__(win)

        self.pos = 0  # Scroll position we are at

        self.content = []  # Content to render
        self.running = False  # Value determining if we are running

        self.thread = None  # Threading instance for frontend

        self.keys = Queue()  # Queue for holding keypress

        # Adding callbacks:

        self.add_key(curses.KEY_DOWN, self._increment_scroll)
        self.add_key(curses.KEY_UP, self._decrement_scroll)
        self.add_key('r', self._render_content)
        self.add_key([curses.KEY_END, curses.KEY_EXIT, 'f'], self.stop)

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

        # Stops parent window:

        super(ScrollWindow, self).stop()

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
