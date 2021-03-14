"""
Classes representing certain tilemaps.

tielmaps contain characters drawn at certain positions on the screen.
tilemaps handle the logic of entity movement, and keeps everything organised.
"""

from character_classes import EntityCharacter, Player, TrackerEnemy, Fog
import math


class BaseTileMap(object):

    """
    BaseTileMap object, all child tilemaps MUST inherit this class!

    We offer some useful functionality, and offer some use cases.

    We utilise 3D arrays to represent the screen Here is an explanation of that logic:

        * 1st Degree - Line of the character(Y cordnet)
        * 2nd Degree - Collum of the character(X cordnet)
        * 3rd Degree - List of characters located at that position(Z cordnet). Ordered by relevance.

    Top left hand corner is (0, 0), bottom right hand corner is (width - 1, height -1).
    We use (X, Y) corndets to locate, and identify, characters on the screen.
    """

    def __init__(self, height, width, win):

        self.height = height  # Height of the tilemap
        self.width = width  # Width of the tilemap
        self.win = win  # DisplayWindow in use
        self.scrollWin = None

        self.tilemap = None  # 3D array representing the screen

        # Create out tilemap:

        self._init_tilemap()

    def _init_tilemap(self):

        """
        We create the underlying 3D array representing the screen.
        """

        final = []

        # Iterate over the lines(Y)

        for line in range(self.height):

            # Iterate over the columns(X):

            final.append([])

            for col in range(self.width):

                final[line].append([])

                # Create sublist at this position:

                final[line][col] = []

        # We are done, set our tilemap:

        self.tilemap = final

    def fill(self, obj):

        """
        Adds the given object to each position in the tilemap.

        :param obj: Object to add to each position
        """

        for y, lines in enumerate(self.tilemap):

            for x, columns in enumerate(lines):

                self.add(obj(), x, y)

    def get(self, x, y, z=None):

        """
        Gets the list of objects in the tilemap at cordents.

        Or, if Z is specified, gets the object at those cordnets.

        We return a 'Tile' object representing that position.

        :param x: X Cordnet to get
        :type x: int
        :param y: Y Cordnet to get
        :type y: int
        :param z: Z Cordnet to get
        :type z: int
        :return: Object at tht position
        :rtype: list, BaseCharacter
        """

        # Check boundaries

        self._bound_check(x, y, -1 if z is None else z)

        if z is not None:

            # Get character at Z

            return Tile(x, y, z, self.tilemap[y][x][z], self.tilemap[y][x])

        # Convert list of characters to tiles:

        final = []

        for z, cord in enumerate(self.tilemap[y][x]):

            final.append(Tile(x, y, z, cord, self.tilemap[y][x]))

        return final

    def get_all(self):

        """
        Returns all of the tiles as a 3d array.
        """

        tiles = []

        for x, y, z, obj in self._iterate():

            tiles.append(Tile(x, y, z, obj, self.tilemap[y][x]))

        return tiles

    def get_width(self, y=0):

        """
        Gets the width of the list in the tilemap of the passed y value

        :param y: List index to be evaluated
        :return Width of list indexed from y value
        """

        return len(self.tilemap[y])

    def get_height(self):

        """
        Gets the height of the list in the tilemap

        :return Height of tilemap list
        """

        return len(self.tilemap)

    def find_object(self, obj, findall=False):

        """
        Finds an object in the tilemap.

        We check by comparison, so the instance of the object should be passed to work correctly.

        If the object could not be found, then None will be returned for each cordnet.

        :param obj: Object to find
        :type obj: BaseCharacter
        :param findall: Boolean determining if we should find all matching objects
        :return: Tile object, or list of them, representing the positions(s)
        :rtype: Tile, list
        """

        final = []

        # Iterate though the lines:

        for x, y, z, fobj in self._iterate():

            # Check if the object is a match

            if obj == fobj:

                # Found our object! Return the cords:

                final.append(self.get(x, y, z))

                if not findall:

                    # Return just the one we found:

                    return final[0]

        if final:

            return final

        # Did not find the object! Return None

        return None

    def find_object_type(self, obj, findall=False):

        """
        Same as find_object, but instead we compare by types of objects.

        :param obj: Object type to find
        :type obj: BaseCharacter
        :param findall: Boolean determining if we return cornets of all matching objects
        :type findall: bool
        :return: Tile object, or list of them, representing those positions
        :rtype: Tile, list
        """

        final = []

        # Iterate through the list:

        for x, y, z, fobj in self._iterate():

            # Compare the types of the objects
            if isinstance(fobj, obj):

                # Add the cords to the final list:

                final.append(self.get(x, y, z))

                # Matching type found! Return our cordnets:

                if not findall:

                    return final[0]

        if final:

            return final

        # Nothing found, return None.

        return None

    def move(self, obj, x, y):

        """
        Moves the given object to a position in the list.

        First we find the object in the list,
        then we move it to it's new position.

        :param obj: Object to move
        :type obj: BaseCharacter
        :param x: X cordnet to move it to
        :type x: int
        :param y: Y cordnet to move it to
        :type y: int
        """

        tile = self.find_object(obj)

        # Check if movement is valid:

        self._bound_check(x, y, -1)

        # Remove the object from it's original position:

        self.tilemap[tile.y][tile.x].remove(obj)

        # Add the object to it's new position:

        self.tilemap[y][x].append(obj)

        # Sort the list at that position:

        self.tilemap[y][x].sort(key=self._get_priority)

    def get_around(self, x, y, radius=1, getSelf=False):

        """
        Gets all positions around the X and Y cordnets given.

        :param x: X cordnet to start at
        :type x : int
        :param y: Y corndet to start at
        :type y: int
        :param radius: Radius of objects around corndets
        :param getSelf: Determining if we return the self character in the list
        :type getSelf: Boolean
        :return: List of Tiles around the
        """

        if not self._bound_check(x, y):

            # Not a valid cordnet!

            return False

        # Calculate cords:

        start_x = x - radius if x - radius >= 0 else 0
        stop_x = x + radius if x + radius < len(self.tilemap[0]) else len(self.tilemap[0]) - 1

        start_y = y - radius if y - radius >= 0 else 0
        stop_y = y + radius if y + radius < len(self.tilemap) else len(self.tilemap) - 1

        final = []

        # Iterate over each value:

        for cur_y in range(start_y, stop_y + 1):

            for cur_x in range(start_x, stop_x + 1):

                if (cur_y == y and cur_x == x) and not getSelf:

                    # Ignore this tile, it is us!

                    continue

                # Get the Tile at this position:
                tile = self.get(cur_x, cur_y)

                final.append(tile)

        return final

    def add(self, obj, x, y, bind=True):

        """
        Adds an object to the tilemap.

        :param obj: Object to add
        :type obj: BaseCharacter
        :param x: X cordnet
        :type x: int
        :param y: Y cordnet
        :type y: int
        :param bind: Boolean determining if we bind data to the object
        """

        # Binding relevant data to the character:

        if bind:

            obj._bind(self.win, self)

        # Check if the object is expecting any keys:

        try:

            if obj.keys:

                # Iterate over the keys and add them

                for key in obj.keys:

                    self.win.add_callback(key, self.win._add_key, args=[key if type(key) == int else ord(key), obj])

        except AttributeError:

            pass

        # Adding object at coordinate:

        self.tilemap[y][x].append(obj)

        # Sort the objects at that position
        self.tilemap[y][x].sort(key=self._get_priority)

    def remove_obj(self, obj, findall=False):

        """
        Removes the object(s) from the tilemap
        :param obj: Object to be removed
        :type obj: BaseCharacter
        :param findall: Boolean determining if we should find all matching objects
        """

        if not findall:

            objTile = self.find_object(obj)
            self.tilemap[objTile.y][objTile.x].remove(obj)

        else:

            for tile in self.tilemap.find_object(obj, True):

                self.tilemap[tile.y][tile.x].remove(obj)

    def remove_obj_by_type(self, obj, findall=False):

        """
        Removes a type of object(s) from the tilemap
        :param obj: Object to be removed
        :type obj: BaseCharacter
        :param findall: Boolean determining if we should find all matching objects
        """

        if not findall:

            objTile = self.find_object_type(obj)
            self.tilemap[objTile.y][objTile.x].remove(obj)

        else:

            for tile in self.tilemap.find_object_type(obj, True):
                self.tilemap[tile.y][tile.x].remove(obj)

    def remove_fog(self):

        self.remove_obj_by_type(Fog, findall=True)

    def remove_obj_by_coords(self, x, y, z=0):

        if isinstance(self.tilemap[y][x][z], Player):

            z += 1

        del self.tilemap[y][x][z]

    def update(self):

        """
        Calls the 'move' method on all entities and refreshes our collection.
        """

        cords = self.find_object_type(EntityCharacter, findall=True)

        # Sort them in order of priority:

        cords.sort(key=self._get_move_priority)

        for cord in cords:

            # Call the 'move' method if the entity is alive:
            if cord.obj.is_alive:

                cord.obj.move()

            else:

                # If the entity is dead, remove it from the tilemap
                self.remove_obj(cord.obj)

    def _iterate(self):

        """
        Generator function that iterates through every character in the list.

        :return: x, y, z, character at position
        :rtype: tuple
        """

        # Iterate over lines:

        for y, line in enumerate(self.tilemap):

            # Iterate over columns

            for x, col in enumerate(line):

                # Iterate over objects:

                for z, objs in enumerate(col):

                    yield x, y, z, objs

    def _bound_check(self, x, y, z=None):

        """
        Checks if any of the coordinates are too big.

        We raise an exception if the coordinates are out of bounds.

        :param x: X cordnet
        :type x: int
        :param y: Y cordnet
        :type y: int
        :param z: Z cordnet
        :type z: int
        """

        if z is not None:

            if len(self.tilemap) > y >= 0 and len(self.tilemap[y]) > x >= 0 and len(self.tilemap[y][x]) > z:

                # We are valid, return True

                return True

        else:

            if len(self.tilemap) > y >= 0 and len(self.tilemap[y]) > x >= 0:

                # We are valid, return True

                return True


        # TODO: More verbose error handling?

        return False

    def _get_priority(self, obj):

        """
        Gets and returns the priority of the given object.

        Used for sorting purposes.

        :param obj: Object to get priority
        :type obj: BaseCharacter
        :return: Priority of the character
        :rtype: int
        """

        return obj.priority

    def _get_move_priority(self, tile):

        """
        Returns the move priority from the object list.

        :param tile: Tile object representing that location
        :type tile: Tile
        :return: Move priority
        :rtype: int
        """

        return tile.obj.move_priority

    def toggle_enemy_movement(self):

        for tile in self.get_all():

            if isinstance(tile.obj, TrackerEnemy):

                tile.obj.debug_move_toggle()

    def set_scroll_win(self, scrollWin):

        self.scrollWin = scrollWin

    def traverse_function(self, start_x, start_y, func, num_steps=None, step_size=1, args=None, ignore_bounds=False,
                          par=False, discrete=True):

        """
        Generator function that traverses the tilemap based on a given function,
        where an x cordnet is entered into said function,
        and the returned y cordnet will be used to determine the tile to return.

        First, the user must specify a starting position, via x and y cordnets.
        This will act as the origin of the function.
        The function will be traversed as if it had started at this point.

        For example, if the function simply returns x+1 and the origin is (5, 5),
        then the tiles returned will look like this:

        x | y
        -----
        6 | 7
        7 | 8
        8 | 9
        9 | 10

        And so on. You can use any algebraic concepts in your function.
        We leave it up to the given function to compute this,
        so if python can calculate it, it's fair game!

        By default, we operate in discrete mode,
        meaning that the function ONLY sees the steps away from the origin,
        and is unaware of our actual position on the board.
        After the operations is complete, we add the starting x and starting y values
        to get the true calculated items from the board.

        If your implementation requires the true cordnets, and not the discrete ones,
        then you can enable the option by setting 'discrete' to false.
        This will send the true X cordnet to the function, and we will expect the true y corndet in return.
        If we are in parametric mode, we will still pass the true x cordnet to the function, acting as the step.

        The function MUST have at least one argument, that being the X value inputted.
        We can optionally pass arguments to the function.
        You can define these using the 'args' parameter. Arguments must be in a list!

        We also offer a step size,
        which is how much the X value increases after each calculation.
        You can also specify the number of steps to take while traversing.
        If not specified, then we will continue until either the X or Y cordents go out of bounds.
        Which ever comes first.

        If the user does not care about Y bound checks, then we can ignore them.
        If the Y value returned is out of bounds, then we can optionally skip them.
        Essentially, we will continue until our X value is invalid.

        Optionally, the user can specify a parametric function,
        meaning that the function returns the X and Y value of the position.
        If this is the case, then the function MUST return two values,
        te first being the X cordnet, and the second being the Y cordnet.

        Because tilemaps only work with ints,
        we will automatically convert the returned value into an integer.

        :param start_x: X cordnet to start at
        :type start_x: int
        :param start_y: Y cordnet to start at
        :param func: Function to use when evaluating the Y value
        :type func: function
        :param num_steps: Number of steps to take
        :type num_steps: int, None
        :param step_size: How much the X value will increase by after each step
        :type step_size: int
        :param args: Arguments to pass to the function
        :type args: list, None
        :param ignore_bounds: Determines if we should skip returning invalid Y cordnets instead of exiting
        :type ignore_bounds: bool
        :param par: Determines if we should operate in parametric mode, where the function determines the X an dY value
        :type par: bool
        :param discrete: Determines if we should operate in discrete mode
        :type discrete: bool
        """

        if args is None:

            args = []

        # Determine the starting value:

        start = 0

        if not discrete:

            # Function wants absolute cordnet, lets give it to them:

            start = start_x

        steps = 0

        for step in count(start, step=step_size):

            # Check if we are done taking steps:

            if steps == num_steps:

                # Taken out maximum number of steps! Lets return:

                return

            # Check if we are advanced:

            if par:

                # Parametric mode, get X and Y values:

                x, y = func(step, *args)
                x = int(x)
                y = int(y)

            else:

                # Calculate our Y value:

                y = int(func(step, *args))
                x = int(step)

            if discrete:

                # Lets add the starting values to the results:

                y = y + start_y
                x = x + start_x

            if x >= self.width or x < 0:

                # Invalid X cordnet! Return and exit

                return

            # Check if Y value is out of bounds, and if we even care:

            if y >= self.height or y < 0:

                # Out of bounds! Whats next?

                if ignore_bounds:

                    # Lets continue on:

                    continue

                # Lets exit:

                return

            # Increment our steps value:

            steps += 1

            # Get the item at that position and return it:

            #print("In function: X: {} ; Y: {}".format(x, y))

            yield self.get(x, y)


class Camera(object):

    def __init__(self, tilemap, win):

        self.tilemap = tilemap  # Full tilemap
        self.win = win  # DisplayWindow in use
        self.displayArea = []  # Visual tilemap area will will display, based on full tilemap
        self.focusObject = None  # Object that the camera is focused on
        self.focusPoint = [0, 0]  # Coordinate point of the focused object
        self.radius = 0  # Amount of tiles that we will be rendering around the focus object

    def set_focus_object(self, obj):

        """
        Sets the focus point of the camera onto an object of Tile class in the tilemap

        :param obj: Object being set as the focus point
        :type obj : Tile
        """

        objTile = self.tilemap.find_object(obj)

        self.focusObject = objTile
        self.focusPoint = [objTile.x, objTile.y]

    def refresh_focus_position(self):

        """
        Finds the focus object position in the tilemap and resets the focus point to its position
        """

        self.focusObject = self.tilemap.find_object(self.focusObject.obj)
        self.focusPoint = [self.focusObject.x, self.focusObject.y]

        # print("Camera self.tilemap: " + str(self.tilemap))
        # print("Camera self.displayArea: " + str(self.displayArea))

    def set_radius(self, radius):

        """
        Sets the radius of the display area

        :param radius: New number of tiles to be displayed around the focus object
        :type radius: Int
        """

        self.radius = radius

    def update(self):

        """
        Fills the tilemap with fog to block the player's vision relative to walls
        """
        playerTile = self.tilemap.find_object_type(Player)
        # self.radius = playerTile.obj.radius

        self.refresh_focus_position()
        self.create_display()

        playerTile.obj.look(self.displayArea)

    def create_display(self):

        """
        Creates the display area based on the radius, using our tilemap
        """

        if (self.radius * 2) + 1 >= self.tilemap.height:

            height = self.tilemap.height

        else:

            height = (self.radius * 2) + 1

        if (self.radius * 2) + 1 >= self.tilemap.width:

            width = self.tilemap.width

        else:

            width = (self.radius * 2) + 1

        # Clearing our displayArea
        del self.displayArea
        self.displayArea = BaseTileMap(height, width, self.win)

        # Creating the starting x position of our display zone
        startX = self.focusPoint[0] - self.radius

        # Creating the ending x position of our display zone
        if self.focusPoint[0] + self.radius > len(self.tilemap.tilemap[self.focusPoint[1]]) - 1:

            endX = len(self.tilemap.tilemap[self.focusPoint[1]]) - 1
            startX -= ((self.focusPoint[0] + 1) + self.radius) - len(self.tilemap.tilemap[self.focusPoint[1]])

            if startX < 0:

                startX = 0

        else:

            endX = self.focusPoint[0] + self.radius

        if startX < 0:

            endX += abs(startX)
            if endX > len(self.tilemap.tilemap[self.focusPoint[1]]) - 1:

                endX = len(self.tilemap.tilemap[self.focusPoint[1]]) - 1

            startX = 0

        # Creating the starting y position of our display zone
        startY = self.focusPoint[1] - self.radius

        # Creating the ending y position of our display zone
        if self.focusPoint[1] + self.radius > len(self.tilemap.tilemap) - 1:

            endY = len(self.tilemap.tilemap) - 1
            startY -= ((self.focusPoint[1] + 1) + self.radius) - len(self.tilemap.tilemap)

            if startY < 0:

                startY = 0

        else:

            endY = self.focusPoint[1] + self.radius

        if startY < 0:

            endY += abs(startY)
            if endY > len(self.tilemap.tilemap) - 1:

                endY = len(self.tilemap.tilemap) - 1

            startY = 0

        yIndex = 0
        xIndex = 0

        # Adding Tiles to the displayArea tilemap from our main tilemap
        while yIndex + startY <= endY:

            while xIndex + startX <= endX:

                for obj in self.tilemap.tilemap[yIndex + startY][xIndex + startX]:

                    self.displayArea.add(obj, xIndex, yIndex, bind=False)

                xIndex += 1

            yIndex += 1
            xIndex = 0


class Tile:

    """
    Creates a disposable object that stores the x and y coordinate, index of the list at the
    target coordinates, and stores the object itself for reference
    """

    def __init__(self, xPos, yPos, zPos, obj, pos_list):

        """

        :param xPos = X Coordinate of the object
        :param yPos: Y Coordinate of the object
        :param zPos: Index of the list of the object
        :param obj: The object itself
        :param pos_list: List of objects at that position
        """

        self.x = xPos
        self.y = yPos
        self.z = zPos
        self.obj = obj
        self.list = pos_list

    def return_obj(self):

        """

        :return: returns the object
        """

        return self.obj

    def get_x(self):

        """

        :return: returns the x coordinate of the object
        """

        return self.x

    def get_y(self):

        """

        :return: return sthe y coordinate of the object
        """

        return self.y

    def get_z(self):

        """

        :return: returns the index of the object in the list at the x and y coordinate
        """

        return self.z

    def calc_distance(self, targObj):

        return math.sqrt(math.pow(targObj.xPos - self.x, 2) + math.pow(targObj.yPos - self.y, 2))


class WalkingFunctions:

    """
    A collection of useful functions for traversing the tilemap.

    This class provides the the functionality for a few operations:

        - Vertical Lines
        - Horizontal lines
        - Lines with a given slope

    All the user has to do is determine which function they wish to call,
    and then pass the instance of this class onto the tilemap.

    All of these function require 'traverse_function' to be in discrete mode!
    This is the default operation, so be sure to not turn off discrete mode when using these functions!

    We also require 'traverse_function' to be in parametric mode when using our functions!
    """

    def __init__(self, func, slope):

        self.step = 0  # Number of steps we have taken
        self.selection = func  # Function to do our calculations with
        self.gen = None  # Generator function of the selection
        self.slope = slope  # Slope of the line

    @classmethod
    def from_slope(cls, slope):

        """
        Automatically creates and selects a function based on the slope.
        This is only relevant for linear equations!

        We will also determine if we need any special functions,
        such as 'vertical_line', or 'horizontal_line'.
        """

        if slope == 0:

            # we need a horizontal line, let's select it:

            return cls(cls.horizontal_line, 0)

        if slope == maxsize or slope == maxsize * -1:

            # Right above or below us, let's select vertical line:

            return cls(cls.vertical_line, 0)

        # Otherwise, return our value with the given slope:

        return cls(cls.line, slope)

    def __call__(self, *args):

        """
        We are being called, most likely by the 'traverse_function' method.

        Let's pass on the step to our selected function and return it!

        :param step: Step we are on
        :type step: int
        :return: Tuple containing X and Y values of the step
        :rtype: tuple
        """

        print(*args)

        return self.selection(self, *args)

    def vertical_line(self, step):

        """
        Vertical line function.

        We will generate a vertical line at the given X value!

        We use the given equation:

        X = 0
        Y = step

        Where:

        step = The step we are currently on

        If we are given the following input, we generate the following output:

        s | x | y
        ----------
        0 | 0 | 0
        1 | 0 | 1
        2 | 0 | 2
        3 | 0 | 3

        So on and so forth.

        :param step: Step we are currently on
        """

        return 0, step

    def horizontal_line(self, step):

        """
        Horizontal line function.

        We will generate a vertical line at the given X value.

        We use the following equation:

        X = step
        Y = 0

        If we are given the following input, we generate the following output:

        s | x | y
        ----------
        0 | 0 | 0
        1 | 1 | 0
        2 | 2 | 0
        3 | 3 | 0

        So on and so forth.

        :param step: Step we are currently on
        :type step: int
        :return: X and Y cordnets of the function at step
        :rtype: tuple
        """

        return step, 0

    def line(self, step):

        """
        Basic line function.

        We will generate a straight line using the given X value.

        We use the following equation:

        X = step
        Y = step * self.slope

        If we are given the following input, and we have a slope of 1, we generate the following output:

        s | x | y
        ----------
        0 | 0 | 0
        1 | 1 | 1
        2 | 2 | 2
        3 | 3 | 3

        So on and so forth.

        :param step: Step we are currently on
        :type step: int
        :return: X and Y cordnets of the function at step
        :rtype: tuple
        """

        return step, step * self.slope