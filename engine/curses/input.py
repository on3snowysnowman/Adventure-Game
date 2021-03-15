"""
Curses windows that manage input from the user.

We have the following components:

    > InputWindow - Receives text info from the user and offers some basic line editing
    > OptionWindow - Displays options for the user to select

These windows should be used used with a MasterWindow,
as they will always request input from curses, 
which could cause trouble with other windows and components!

Other types of input windows might be added at a later date. 
"""

import curses

from math import floor, ceil
from inspect import isfunction

from engine.curses.base import BaseWindow


class InputWindow(BaseWindow):

    """
    Curses text input window

    We receive input from the user until a return character is encountered,
    which we will then return the inputted content to whatever invoked us.

    We offer some basic editing features,
    such as changing the cursor position and scrolling.  
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


class OptionWindow(BaseWindow):

    """
    Displays a list of options to the user.
    Support simple selection, boolean selection, and value selection.  

    #TODO Fix documentation for OptionWindow!
    This window needs to be explained better,
    and it needs some improvements and bug checks.
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