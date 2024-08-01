#!/usr/bin/env python3
"""Module providing a function to zoom an array by repeating its elements."""

from typing import Tuple, List


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """
    Create a new list with each element of the input tuple repeated.

    Args:
        lst (Tuple): The input tuple of elements to be zoomed.
        factor (int, optional): The number of times each element should be
                                repeated. Defaults to 2.

    Returns:
        List: A new list with the elements of the input tuple repeated
              based on the factor.
    """
    zoomed_in: List = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in


array = [12, 72, 91]

zoom_2x = zoom_array(tuple(array))

zoom_3x = zoom_array(tuple(array), 3)
