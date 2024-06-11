#!/usr/bin/env python3
"""
2-measure_runtime.py
"""
import asyncio
import time
from importlib import import_module as im


async_comprehension = im('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    Executes async_comprehension four times
    in parallel using asyncio.gather.

    Returns:
        float: The total runtime.
    """
    start_time = time.time()
    await asyncio.gather(async_comprehension(),
                         async_comprehension(),
                         async_comprehension(),
                         async_comprehension())
    end_time = time.time()
    total_time = end_time - start_time
    return total_time
