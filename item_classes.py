
class Item(object):

    def __init__(self):

        self.char = ''  # Character to draw
        self.contains_color = True
        self.color = ""
        self.attrib = []
        self.name = 'Item'  # Name of the character
        self.can_traverse = False  # Boolean determining if things can walk their
        self.priority = 20  # Value determining object stacking priority
        self.can_move = False

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

    def start(self):

        """
        Start method called when the object is instantiated.

        Allows child characters to set parameters to the way that they like.
        """

        pass


class Weapon(Item):

    def _start(self):

        self.damage_min = 0
        self.damage_max = 0
        self.damage_type = ""

    def attack(self):

        pass


class Sword(Weapon):

    def start(self):

        self.damage_min = 4
        self.damage_max = 8
        self.damage_type = "physical"
        self.value = 150


sword = Sword()

print(sword.damage_min)