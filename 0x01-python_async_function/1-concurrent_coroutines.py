#!/usr/bin/env python3
"""Module for task 1 - Multiple coroutines"""

import asyncio
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Spawn wait_random n times with the specified max_delay.

    Args:
        n (int): Number of times to spawn wait_random.
        max_delay (int): The maximum delay for each wait_random call.

    Returns:
        List[float]: List of all the delays in ascending order.
    """
    delays = await asyncio.gather(
        *[wait_random(max_delay) for _ in range(n)]
    )
    return sorted(delays)
