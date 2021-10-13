"""
Tools and components used for debugging purposes.
"""

import logging


def debug_log(name="engine_output.txt"):
    """
    Configures the logging module to work with the engine.

    We configure the logger to automatically
    output to an external file,
    and we disable printing to the terminal.

    This method of event logging can be desierable,
    as it will not work with the terminal.
    It allows for output to be viewed,
    even if CURSES crashes or does something strange.

    :param name: Name of log file, defaults to "engine_output.txt"
    :type name: str, optional
    """

    logging.basicConfig(filename=name, level=logging.INFO)


def clear_debug_log(name="engine_output.txt"):
    """
    Clears the debug log.

    This removes all content from the debug log.
    It might be useful to put this function at the start
    of engine activity,
    so you can have a clean log while debuging.

    :param name: Name of log file, defaults to "engine_output.txt"
    :type name: str, optional
    """

    file = open(name, mode='w')

    file.write("")

    file.close()
