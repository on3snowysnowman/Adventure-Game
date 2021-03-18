"""
Characters tha are effected by input.

This is usually the player character that is controlled via the keyboard,
or some other method.

We aim to make this class inheritable and ambiguous,
so once could change the specifics and logic
without affecting the overall concept of reacting via a keyboard.
"""

import random

from engine.characters.base import EntityCharacter
from engine.characters.items import *
from engine.characters.tiles import *


class Player(EntityCharacter):
    
    """
    Player class, moves and gets controlled by the user.
    """

    def __init__(self):

        super().__init__()

        self.inventory = []
        self.inventory_space = 0
        self.inventory_space_max = 30

        self.char = 'C'
        self.name = 'Player'
        self.attrib.append("green")
        self.priority = 0
        self.move_priority = 18

        self.hp = 100
        self.active_weapon = None

        self.radius = 3

        self.keys = ['w', 'a', 's', 'd', 'q', 'e', 'z', 'c', 'p', 'i', 'l', 'o', 'y', ",", "."]

    def move(self):

        """
        Moves the character across the screen, or executes choices the player wants to make

        We accept input from the DisplayWindow here.
        """

        # Get input from the DisplayWindow

        # time.sleep(3)

        inp = self.get_input()

        # Get our coordinates:

        playerTile = self.tilemap.find_object(self)

        if inp == 'w':

            # Move up:

            # Checks if the player is moving into a tile with a chest. If so, open it
            self.check_chest(playerTile.x, playerTile.y - 1)

            # Checks if the player is moving into a tile with an entity. If so, interact with it
            self.check_entity(playerTile.x, playerTile.y - 1)

            if self.check_tile(playerTile.x, playerTile.y - 1):
                self.tilemap.move(self, playerTile.x, playerTile.y - 1)

        elif inp == 'a':

            # Move left

            # Checks if the player is moving into a tile with a chest. If so, open it
            self.check_chest(playerTile.x - 1, playerTile.y)

            # Checks if the player is moving into a tile with an entity. If so, interact with it
            self.check_entity(playerTile.x - 1, playerTile.y)

            if self.check_tile(playerTile.x - 1, playerTile.y):
                self.tilemap.move(self, playerTile.x - 1, playerTile.y)

        elif inp == 's':

            # Move down

            # Checks if the player is moving into a tile with a chest. If so, open it
            self.check_chest(playerTile.x, playerTile.y + 1)

            # Checks if the player is moving into a tile with an entity. If so, interact with it
            self.check_entity(playerTile.x, playerTile.y + 1)

            if self.check_tile(playerTile.x, playerTile.y + 1):
                self.tilemap.move(self, playerTile.x, playerTile.y + 1)

        elif inp == 'd':

            # Move right

            # Checks if the player is moving into a tile with a chest. If so, open it
            self.check_chest(playerTile.x + 1, playerTile.y)

            # Checks if the player is moving into a tile with an entity. If so, interact with it
            self.check_entity(playerTile.x + 1, playerTile.y)

            if self.check_tile(playerTile.x + 1, playerTile.y):
                self.tilemap.move(self, playerTile.x + 1, playerTile.y)

        elif inp == 'q':

            # Move diagonal up left

            if self.check_tile(playerTile.x - 1, playerTile.y - 1):
                self.tilemap.move(self, playerTile.x - 1, playerTile.y - 1)

        elif inp == 'e':

            # Move diagonal up right

            if self.check_tile(playerTile.x + 1, playerTile.y - 1):
                self.tilemap.move(self, playerTile.x + 1, playerTile.y - 1)

        elif inp == 'z':

            # Move diagonal down left

            if self.check_tile(playerTile.x - 1, playerTile.y + 1):
                self.tilemap.move(self, playerTile.x - 1, playerTile.y + 1)

        elif inp == 'c':

            # Move diagonal down right

            if self.check_tile(playerTile.x + 1, playerTile.y + 1):
                self.tilemap.move(self, playerTile.x + 1, playerTile.y + 1)

        elif inp == 'p':
            self.pickup_first_item()

        elif inp == 'i':

            if len(self.inventory) == 0:
                self.tilemap.scrollWin.add_content("Your inventory is empty", attrib="white")

            else:

                self.tilemap.scrollWin.add_content("Inventory: ", attrib="white")

                for x in self.inventory:

                    if isinstance(x, Item):
                        self.tilemap.scrollWin.add_content(x.name)

                self.tilemap.scrollWin.add_content("\n" * 0)

        elif inp == 'l':

            self.look(100)

            # self.tilemap.scrollWin.add_content("You don't see any objects in this room", "white")

        elif inp == 'o':

            groundContents = []

            for x in self.tilemap.get(playerTile.x, playerTile.y):

                if not isinstance(x.obj, Player) and not isinstance(x.obj, Floor):

                    groundContents.append(x)

            if len(groundContents) > 0:

                self.tilemap.scrollWin.add_content("Things on the ground: ", "white")

                for x in groundContents:

                    if not isinstance(x.obj, Player):
                        self.tilemap.scrollWin.add_content(x.obj.name)

                self.tilemap.scrollWin.add_content("\n" * 0)

        elif inp == 'y':

            self.tilemap.toggle_enemy_movement()

        elif inp == ',':

            if self.radius - 1 >= 0:

                self.radius -= 1

        elif inp == '.':

            if self.radius + 1 >= int(self.win.max_y / 2) - 1 or self.radius + 1 >= int(self.win.max_x / 2) - 1:

                if int(self.win.max_x / 2) - 1 < int(self.win.max_y / 2) - 1:

                    self.radius = int(self.win.max_x / 2) - 1

                else:

                    self.radius = int(self.win.max_y / 2) - 1

            elif self.radius + 1 >= int(self.tilemap.height / 2) and self.radius + 1 >= int(self.tilemap.width / 2):

                if int(self.tilemap.width / 2) < int(self.tilemap.height / 2):

                    self.radius = int(self.tilemap.height / 2)

                else:

                    self.radius = int(self.tilemap.width / 2)

            else:

                self.radius += 1

    def attack(self, targ):

        amountDamage = random.randrange(self.active_weapon.damage_min, self.active_weapon.damage_max + 1)

        if self.active_weapon.damage_type == "physical":

            self.tilemap.scrollWin.add_content("You strike the " + targ.name + " dealing, " + str(amountDamage) + " damage")

        targ.hp -= amountDamage

        if targ.hp < 0:

            targ.death()

    def check_inventory_bounds(self, obj):

        if self.inventory_space + obj.size > self.inventory_space_max:
            return False

        return True

    def pickup_first_item(self):

        """
        Adds the first item in the tile list to player inventory if there is enough space
        :return:
        """

        playerObj = self.tilemap.find_object_type(Player)
        targObj = self.tilemap.get(playerObj.x, playerObj.y, 1).obj

        # Checks if the item is of Class Item

        if isinstance(targObj, Item):

            # Checks if the object is allowed to be picked up

            if targObj.can_player_pickup:

                if self.check_inventory_bounds(targObj):
                    self.inventory.append(targObj)
                    self.inventory_space += targObj.size
                    self.tilemap.removeObj(targObj)
                    self.tilemap.scrollWin.add_content(targObj.name + " added to inventory")

    def pickup_item(self, targObj):

        if isinstance(targObj, Item):

            # Checks if the object is allowed to be picked up

            if targObj.can_player_pickup:

                if self.check_inventory_bounds(targObj):
                    self.inventory.append(targObj)
                    self.inventory_space += targObj.size
                    self.tilemap.scrollWin.add_content(targObj.name + " added to inventory")

    def get_item(self, targObj):

        if isinstance(targObj, Item):

            if not self.check_inventory_bounds(targObj):

                playerPos = self.tilemap.get(self)
                self.tilemap.add(targObj, playerPos.x, playerPos.y)
                self.tilemap.scrollWin.add_content(f"You don't have enough space for the {targObj.name}")

            else:

                self.inventory.append(targObj)
                self.inventory_space += targObj.size
                self.tilemap.scrollWin.add_content(targObj.name + " added to inventory")

    def check_chest(self, xPos, yPos):

        if self.tilemap._bound_check(xPos, yPos):

            for i in self.tilemap.get(xPos, yPos):

                if isinstance(i.obj, Chest):

                    item = i.obj.open_chest()

                    if isinstance(item, Item):
                        self.tilemap.scrollWin.add_content(f"You found a {item.name} in a chest! ")
                        self.pickup_item(item)
                        self.tilemap.removeObj_by_coords(xPos, yPos)
                        self.tilemap.add(OpenedChest(), xPos, yPos)

    def check_entity(self, xPos, yPos):

        if self.tilemap._bound_check(xPos, yPos):

            for tile in self.tilemap.get(xPos, yPos):

                if isinstance(tile.obj, EntityCharacter):

                    tile.obj.interact(self)