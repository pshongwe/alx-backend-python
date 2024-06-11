#!/usr/bin/env python3
"""
1-concurrent_coroutines.py
"""
from typing import List
import asyncio


wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """wait n times"""
    delays = []
    for _ in range(n):
        delays.append(await wait_random(max_delay))

    for i in range(1, len(delays)):
        key = delays[i]
        j = i - 1
        while j >= 0 and key < delays[j]:
            delays[j + 1] = delays[j]
            j -= 1
        delays[j + 1] = key

    return sorted(delays)
