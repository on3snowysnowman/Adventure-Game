"""
This file will contain built in autoruns managing entity movement.

We currently have the following:

    > RandomMove - Randomly moves the entity to a position around it
"""

import random

from engine.characters.auto.base import BaseAutoRun


class RandomMove(BaseAutoRun):

    """
    RandomMove - Randomly moves the character to a position around it.
    """

    def run(self):
        
        # Find ourselves:

        entity = self.char.tilemap.find_object(self.char)

        # Get the tiles around us:

        tiles = self.char.tilemap.get_around(entity.x, entity.y)

        # Choose a random tile from the list:

        choice = random.choice(tiles)

        # Move the character to the location:

        self.char.tilemap.move(self.char, choice[0].x, choice[0].y)
