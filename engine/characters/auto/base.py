"""
Character AutoRun base classes.

This file contains the base components for character autoruns.
(TODO: Is this a bad name?)

An autorun is something that gets invoked upon each cycle of the display loop,
i.e each time our frontend asks for content to draw and the entities are refreshed.
The autorun framework is meant to be ambiguous, so anything can be ran upon each event loop automatically.

This allows you to attach functionality to entities instead of manually specifying it,
and it eliminates the need to make custom character classes for a specific functionality.

Autoruns are particularly useful for movement,
as one could configure an autorun and attach it to the desired class.

Autoruns do not inhibit the normal 'move()' function,
meaning that your character could have an autorun attached,
and custom code in the move method.
Both methods will be executed, with the autoruns being invoked first.

For example, to have your entity track a certain character,
you could attach a Tracker autorun that will move the character in the direction of the target.
"""


class BaseAutoRun(object):

    """
    TODO: Improve this description!
    BaseAutoRun - Base class all autoruns will inherit!

    We contain useful functionality, 
    and define a framework for all autorun implementations.

    Autoruns have access to the character they are attached to,
    and all autoruns can safely assume that the characters they are attached to
    are entities.
    """

    def __init__(self) -> None:
        
        self.char = None  # Character we are bound to
        self.tilemap = None # Tilemap we are bound to
        self.name = ''  # Name of this Autorun
        self.priority = 20  # Ordering priority of the autorun

    def run(self):

        """
        Function invoked when it is our turn to run.

        Your relevant code should be kept here.
        i.e - The code that moves the character around.
        """

        raise NotImplementedError("Should be overridden in child class!")


class AutoRunHandler:

    """
    AutorunHandler - Handler that manages addition, removal, and running of autoruns.

    We keep the autoruns stored and sorted in a list,
    and the order of the list determines which are invoked first
    (autoruns are invoked from left to right).

    We support iteration operations like '__len__()' and '__getitem__()'
    to emulate python lists.

    TODO: Figure this out:
    This class is somewhat barebones and might be redundant.
    If we want to add stuff like start() methods for each autorun,
    although this may be unnecessary.

    For now lets keep it like this, but we might add more to this class if
    our framework gets more complicated,
    or remove this class if it is redundant or unnecessary.
    """

    def __init__(self, char) -> None:
        
        self._runs = []  # List of autoruns attached to the Handler
        self.char = char  # Instance of the character we are bound to

    def _get_priority(self, run):

        """
        Gets the priority of the autorun and returns it.

        :param run: Autorun to get priority from
        :type run: BaseAutoRun
        :return: Priority of the autorun
        :rtype: int
        """

        return run.priority

    def add(self, run):

        """
        Adds the given autorun to the collection.

        We first make sure it is an autorun instance,
        and then we add it to the list and sort it.

        :param run: Autorun instance to add
        :type run: BaseAutoRun
        """

        # Check if the item is an autorun:

        assert isinstance(run, BaseAutoRun), "Autorun MUST inherit BaseAutoRun!"

        # Add the char to the autorun:

        run.char = self.char

        run.tilemap = self.char.tilemap

        # Add it to the list:

        self._runs.append(run)

        # Sort the list:

        self._runs.sort(key=self._get_priority)

    def run(self):

        """
        Runs through each autorun and invokes it's 'run()' method.

        Called each event loop.
        """

        # Iterate over the autoruns:

        for run in self._runs:

            # Invoke the autorun:

            run.run()

