"""
Classes representing certain tilemaps.

tielmaps contain characters drawn at certain positions on the screen.
tilemaps handle the logic of entity movement, and keeps everything organised.
"""


from character_classes import EntityCharacter
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

        self.tilemap = None  # 3D array representing the screen

        # Crete out tilemap:

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

        for y, lines in enumerate(self.tilemap):

            for x, columns in enumerate(lines):

                self.add(obj(), x, y)

    def get(self, x, y, z=None):

        """
        Gets the list of objects in the tilemap at cordents.

        Or, if Z is specified, gets the object at those cordnets.

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

    def get_all_positions(self, x, y):

        listObjects = []

        for j in range(8):

            listObjects.append([])

        #UP
        count = 0
        if self._bound_check(x, y - 1):

            for i in self.tilemap[y - 1][x]:

                listObjects[0].append(TileMap(x, y - 1, count, i))
                count += 1

        else:

            listObjects[0] = None

        #RIGHT UP
        if self._bound_check(x + 1, y - 1):

            count = 0
            for i in self.tilemap[y - 1][x + 1]:
                listObjects[1].append(TileMap(x + 1, y - 1, count, i))
                count += 1

        else:

            listObjects[1] = None

        #RIGHT
        if self._bound_check(x + 1, y):

            count = 0
            for i in self.tilemap[y][x + 1]:
                listObjects[2].append(TileMap(x + 1, y, count, i,))
                count += 1

        else:

            listObjects[2] = None

        #RIGHT DOWN
        if self._bound_check(x + 1, y + 1):

            count = 0
            for i in self.tilemap[y + 1][x + 1]:
                listObjects[3].append(TileMap(x + 1, y + 1, count, i))
                count += 1
        else:

            listObjects[3] = None

        #DOWN
        if self._bound_check(x, y + 1):

            count = 0
            for i in self.tilemap[y + 1][x]:
                listObjects[4].append(TileMap(x, y + 1, count, i))
                count += 1
        else:

            listObjects[4] = None

        #LEFT DOWN
        if self._bound_check(x - 1, y + 1):

            count = 0
            for i in self.tilemap[y + 1][x - 1]:
                listObjects[5].append(TileMap(x - 1, y + 1, count, i))
                count += 1
        else:

            listObjects[5] = None

        #LEFT
        if self._bound_check(x - 1, y):

            count = 0
            for i in self.tilemap[y][x - 1]:
                listObjects[6].append(TileMap(x - 1, y, count, i))
                count += 1
        else:

            listObjects[6] = None

        #LEFT UP
        if self._bound_check(x - 1, y - 1):

            count = 0
            for i in self.tilemap[y - 1][x - 1]:
                listObjects[7].append(TileMap(x - 1, y - 1, count, i))
                count += 1
        else:

            listObjects[7] = None

        return listObjects

    def add(self, obj, x, y):

        """
        Adds an object to the tilemap.

        :param obj: Object to add
        :type obj: BaseCharacter
        :param x: X cordnet
        :type x: int
        :param y: Y cordnet
        :type y: int
        """

        # Binding relevant data to the character:

        obj._bind(self.win, self)

        # Check if the object is expecting any keys:

        if obj.keys:

            # Iterate over the keys and add them

            for key in obj.keys:

                print("Adding key {} to obj {}".format(key, obj))

                self.win.add_callback(key, self.win._add_key, args=[key if type(key) == int else ord(key), obj])

        # Adding object at cordnet:

        self.tilemap[y][x].append(obj)

        # Sort the objects at that position

        self.tilemap[y][x].sort(key=self._get_priority)

    def update(self):

        """
        Calls the 'move' method on all entities and refreshes our collection.
        """

        cords = self.find_object_type(EntityCharacter, findall=True)

        # Sort them in order of priority:

        cords.sort(key=self._get_move_priority)

        print("Cords: {}".format(cords))

        for cord in cords:

            print("Spec. Cord: {}".format(cord))

            # Call the 'move' method:

            cord.obj.move()

            self.win._render()

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

    def _bound_check(self, x, y, z = None):

        """
        Checks if any of the coordinates are too big.

        We raise an exception if the thing is out of bounds.

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

    def _calc_fastest_route(self, targObj):

       pass

#tile = TileMap(12, 2, 0, "object")
#tile2 = TileMap(4, 10, 0, "object2")

#print(tile.calc_distance(tile, tile2))