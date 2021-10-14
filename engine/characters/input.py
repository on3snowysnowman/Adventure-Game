"""
Characters tha are effected by input.

This is usually the player character that is controlled via the keyboard,
or some other method.

We aim to make this class inheritable and ambiguous,
so once could change the specifics and logic
without affecting the overall concept of reacting via a keyboard.
"""

import logging
import random

from engine.characters.base import EntityCharacter
from engine.characters.items import *
from engine.characters.tiles import *

logging

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

        inp = self.get_input()

        logging.info("Got input from queue: {}".format(inp))

        # Get our coordinates:

        playerTile = self.tilemap.find_object(self)

        if inp == 'w':

            # Move up:

            if self.check_tile(playerTile.x, playerTile.y - 1):
                self.tilemap.move(self, playerTile.x, playerTile.y - 1)

        elif inp == 'a':

            # Move left

            if self.check_tile(playerTile.x - 1, playerTile.y):
                self.tilemap.move(self, playerTile.x - 1, playerTile.y)

        elif inp == 's':

            # Move down

            if self.check_tile(playerTile.x, playerTile.y + 1):
                self.tilemap.move(self, playerTile.x, playerTile.y + 1)

        elif inp == 'd':

            # Move right

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
