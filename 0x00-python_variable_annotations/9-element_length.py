#!/usr/bin/env python3
"""
9-element_length.py
"""
from typing import List, Tuple, Iterable, Sequence


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Return a list of tuples, each containing a sequence and its length."""
    return [(i, len(i)) for i in lst]

