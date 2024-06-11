#!/usr/bin/env python3
"""
3-tasks.py
"""
import asyncio
from 0_basic_async_syntax import wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """wait for random tasks"""
    return asyncio.create_task(wait_random(max_delay))
