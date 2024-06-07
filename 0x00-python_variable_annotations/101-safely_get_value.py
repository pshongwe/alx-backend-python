#!/usr/bin/env python3
"""
101-safely_get_value.py
"""
from typing import Any, Mapping, TypeVar, Union


T = TypeVar('T')


def safely_get_value(dct: Mapping[Any, Any],
                     key: Any,
                     default: Union[T, None] = None) -> Union[Any, T]:
    """Return the value from the dictionary for the given key if it exists,
    otherwise return the default value."""
    if key in dct:
        return dct[key]
    else:
        return default
