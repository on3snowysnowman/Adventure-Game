"""
Base classes for NPC characters.

We offer ambiguous, inheritable classes for implementing NPC functionality
of all types.

#TODO: Create a standard for NPCs and fix this description
"""

import random

from engine.characters.base import EntityCharacter
from engine.characters.input import Player


class NPC(EntityCharacter):

    def start(self):

        self.name = "NPC"
        self.char = "C"
        self.attrib.append("light_blue")
        self.priority = 18

    def move(self):

        """
        Moves across the screen randomly.
        """

        shouldMove = random.choice([True, False, False, False])

        if shouldMove:

            # Get objects all around us:

            tile = self.tilemap.find_object(self)

            x = tile.x
            y = tile.y

            cords = [[x - 1, y], [x + 1, y], [x, y + 1], [x, y - 1], [x - 1, y - 1], [x + 1, y - 1], [x - 1, y + 1],
                     [x + 1, y + 1]]
            choices = []

            for targ in cords:

                if self.check_tile(targ[0], targ[1]):
                    choices.append(targ)

            if len(choices) > 0:
                # Now, select a random choice from the options and move their:

                choice = random.choice(choices)

                self.tilemap.move(self, choice[0], choice[1])


class Traveler(NPC):

    def start(self):

        super().start()
        self.name = "Traveler"

    def interact(self, char):

        if isinstance(char, Player):

            self.tilemap.scrollWin.add_content("Hello Player!")

