#!/usr/bin/env python3
"""
1-async_comprehension.py
"""
from typing import List
from importlib import import_module


async_generator = import_module('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """
    Collects 10 random numbers using an asynchronous
    comprehension over async_generator.

    Returns:
        List[float]: A list of 10 random numbers.
    """
    return [number async for number in async_generator()]
