

class Item(object):

    """
    Item class all sub-characters must inherit.

    Instanciates basic variables of every Item
    """

    def __init__(self):

        self.char = 'I'  # Character to draw
        self.contains_color = True
        self.attrib = ["orange"]
        self.name = ''  # Name of the character
        self.can_traverse = True  # Boolean determining if things can walk their
        self.can_player_pickup = True # Boolean determining if the player can pickup
        self.can_entity_pickup = False #Boolean determining if any other than player can pickup
        self.priority = 20  # Value determining object stacking priority
        self.can_move = False

        self.size = 0 # Amount of space this takes in player inventory
        self.value = 0 # In game currency value

        self.tilemap = None  # Tilemap instance
        self.win = None  # DisplayWindow instance

    def _bind(self, win, tilemap):
        """
        Binds the DisplayWindow and Tilemap
        objects to this character.

        :param win: DisplayWindow instance
        :type win: DisplayWindow
        :param tilemap: tilemap instance
        :type tilemap: BaseTileMap
        """

        self.win = win
        self.tilemap = tilemap

    def _start(self):

        """
        Meta start method, used by child characters.
        """

        pass


class Armor(Item):

    def __init__(self):

        super().__init__()

        self.res = 0 # Amount of damage this piece of armor resists, divided by 100 for a percentage
        self.durability = 0 # Amount of durability
        self.max_durability = 0 # Maximum amount of durability
        self.part = "" # What part of the body this covers
        self.priority = 19

        # Calling meta start method:

        self._start()

    def block(self, amount):

        """
        Returns the resulting damage to wearer after they have been attacked
        :param amount: Initial amount of damage dealt to wearer
        :return: Integer resulting in the reduced, blocked damage
        """

        pass

    def repair(self):
        """
        Resets the durability to the maximum durability
        :return:
        """

        self.durability = self.max_durability

        pass


class Weapon(Item):

    def __init__(self):

        super().__init__()

        self.damage_min = 0 # Minimum amount of damage this weapon can deal
        self.damage_max = 0 # Maximum amount of damage this weapon can deal
        self.damage_type = "" #Type of damage dealt when attacking
        self.durability = 0  # Amount of durability
        self.max_durability = 0  # Maximum amount of durability
        self.priority = 19

        # Calling meta start method:

        self._start()

    def attack(self, targObj):

        """
        Called when the wearer attacks a target
        :param targObj: Target object the wearer is attacking
        :return:
        """

        pass

    def repair(self):
        """
        Resets the durability to the maximum durability
        :return:
        """

        self.durability = self.max_durability

        pass


# Custom Item Classes - probably wont live here

class Sword(Weapon):

    def _start(self):

        self.name = "Sword"
        self.damage_min = 4
        self.damage_max = 8
        self.damage_type = "physical"
        self.durability = 100
        self.max_durability = 100
        self.value = 150
        self.size = 2


class Helmet(Armor):

    def _start(self):

        self.name = "Helmet"
        self.res = 5
        self.durability = 200
        self.max_durability = 200
        self.part = "head"
        self.size = 3
        self.value = 200


class Chestplate(Armor):

    def _start(self):

        self.name = "Chestplate"
        self.res = 10
        self.durability = 500
        self.max_durability = 500
        self.part = "chest"
        self.size = 5
        self.value = 400


class Chausses(Armor):

    def _start(self):

        self.name = "Chausses"
        self.res = 5
        self.durability = 250
        self.max_durability = 250
        self.part = "legs"
        self.size = 4
        self.value = 250


class Boots(Armor):

    def _start(self):

        self.name = "Boots"
        self.res = 4
        self.durability = 200
        self.max_durability = 200
        self.part = "boots"
        self.size = 3
        self.value = 200

