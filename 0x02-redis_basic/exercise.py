#!/usr/bin/env python3
""" Exercise file """
import redis
import uuid
from typing import Union


class Cache:
    """ Cache the data """
    def __init__(self):
        """Initialize the Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data in Redis and return the key.

        Args:
            data: The data to store, which can be of type str, bytes, int, or float.

        Returns:
            str: The generated key.
        """
        # Generate a random key using uuid
        key = str(uuid.uuid4())
        # Store the data in Redis using the generated key
        self._redis.set(key, data)
        # Return the generated key
        return key


if __name__ == "__main__":
    # Main file for testing the Cache class
    cache = Cache()

    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))
