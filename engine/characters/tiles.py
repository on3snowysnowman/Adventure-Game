"""
Simple tiles that represent items or terrain - usually don't move!

We provide floors and wallsfor map creation,
as well as a item system.

Developers can create their own tiles to represent these,
but we provide some default ones for convenience.

# TODO: Figure out items

These is probably a much better way to handle weapons that don't require a class to be made for each one.
This can get complicated, as we will have to get into how attributes, damage, health, status effects, ect.
will work, and this can get really complicated.

I think bottom line health and attribute information should NOT be kept
as character attributes. Character attributes should determine how they are interpreted by other characters and the tilemap.

Instead, I think we should create a whole new system for determining health and game attributes.
I have no idea what this will look like, but it should be focused on modularity and customizability,
as we can provide some pre-built configs if the user doesn't want to build their own.

This will require some deliberating and talk, and this can get very complicated very quickly.
"""

import random

from engine.characters.base import BaseCharacter, EntityCharacter
from engine.characters.items import *


class Wall(BaseCharacter):
    
    """
    Represents a wall. Player can't move past it.
    """

    def start(self):
        self.char = 'W'
        self.name = 'Wall'
        self.attrib.append("yellow")
        self.priority = 19

        # Disabling traversal mode:

        self.can_traverse = False


class Chest(BaseCharacter):

    def start(self):
        self.char = 'C'
        self.name = 'Chest'
        self.attrib.append("brown")
        self.priority = 19

        # Disabling traversal mode

        self.can_traverse = False

    def open_chest(self):
        posTile = self.tilemap.find_object(self)
        contents = [Sword(), Chestplate()]
        self.tilemap.add(EntityCharacter(), posTile.x, posTile.y)
        self.tilemap.removeObj(self)
        return random.choice(contents)


class OpenedChest(BaseCharacter):

    def start(self):
        self.char = "C"
        self.name = "Opened Chest"
        self.attrib.append("light_brown")
        self.priority = 19

        # Disabling traversal mode

        self.can_traverse = False


class Floor(BaseCharacter):
    """
    Represents a floor. Player can move over it.
    """

    def start(self):

        self.char = '0'
        self.name = 'Floor'
        self.attrib.append(random.choice(["gray_blue_one", "gray_blue_two"]))


class Fog(BaseCharacter):

    def start(self):

        self.char = ' '
        self.name = 'Fog'
        self.priority = 1

    def clear(self):

        self.tilemap.remove_obj(self, True)
