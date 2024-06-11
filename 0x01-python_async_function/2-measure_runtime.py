#!/usr/bin/env python3
"""
2-measure_runtime.py
"""
import time
import asyncio
from 1_concurrent_coroutines import wait_n


async def measure_time(n: int, max_delay: int) -> float:
    """measure time"""
    start_time = time.perf_counter()
    await wait_n(n, max_delay)
    end_time = time.perf_counter()
    total_time = end_time - start_time
    return total_time / n
