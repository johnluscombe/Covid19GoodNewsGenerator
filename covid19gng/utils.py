"""
Utils
=====

Utilities used throughout the app.
"""

import numpy as np

OPTIONS = "options"

DEFAULT_INPUT_ERROR = "Invalid input."


def list_to_lower_case(lst):
    """
    Converts the strings in the given list to lower-case.

    Args:
        lst (list): List to convert to lower-case.

    Returns:
        list
    """

    if lst is None:
        return None

    new_lst = []

    for i in range(len(lst)):
        if type(lst[i]) == str:
            new_lst.append(lst[i].lower())

    return new_lst


def unique(lst):
    """
    Returns the unique items in the given list.

    Args:
        lst (lst): List to get the unique items from.

    Returns:
        list
    """

    return list(dict.fromkeys(lst))


def input_with_prompt(prompt=None):
    """
    Gets input from a user, using a consistent prompt.

    Args:
        prompt (str): Prompt for the user.

    Returns:
        str
    """

    if prompt is not None:
        print(prompt)

    i = input(">>> ")

    if i == "exit" or i == "quit":
        exit()

    return i.strip()


def input_and_validate(prompt=None, options=None, ignore=None):
    """
    Gets input from a user, using a consistent prompt, and validates it.

    Args:
        prompt (str): Prompt for the user.
        options (list): Valid options.
        ignore (list): Valid options that should not appear in the options
            menu.

    Returns:
        str
    """

    i = input_with_prompt(prompt)
    i_lower = i.lower()

    # Remove nans, get unique values, and sort them
    options = sorted(unique(filter(lambda o: o is not np.nan, options)))

    if i_lower == OPTIONS:
        for option in options:
            print(option)

    lower_options = list_to_lower_case(options)
    lower_ignore = list_to_lower_case(ignore) or []

    while i_lower not in lower_options and i_lower not in lower_ignore:
        if i_lower != OPTIONS:
            print(DEFAULT_INPUT_ERROR)

        i = input_with_prompt(prompt)
        i_lower = i.lower()

        if i_lower == OPTIONS:
            for option in options:
                print(option)

    if i == "":
        return ""
    elif i_lower in lower_ignore:
        return i

    return options[lower_options.index(i_lower)]
