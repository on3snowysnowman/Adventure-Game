
class Item(object):

    """
    Item class all sub-characters must inherit.

    Instanciates basic variables of every Item
    """

    def __init__(self):

        self.char = 'I'  # Character to draw
        self.contains_color = True
        self.attrib = ["orange"]
        self.name = 'Item'  # Name of the character
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

        self.res = 0 # Amount of damage this piece of armor resists, divided by 10 for a percentage
        self.durability = 0 # Amount of durability
        self.max_durability = 0 # Maximum amount of durability
        self.part = "" # What part of the body this covers

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


class Sword(Weapon):

    def _start(self):

        self.damage_min = 4
        self.damage_max = 8
        self.damage_type = "physical"
        self.value = 150
        self.size = 2
