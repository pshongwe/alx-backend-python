#!/usr/bin/env python3
"""
7-to_kv.py
"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Return a tuple with the string k and the square of the int/float v."""
    return (k, float(v ** 2))
