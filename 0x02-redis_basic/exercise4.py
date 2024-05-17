#!/usr/bin/env python3
""" List """
import redis
import uuid
from typing import Union, Callable, Optional
import functools


def call_history(method: Callable) -> Callable:
    """ Define the call_history decorator """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapps input and stores them """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store the input arguments
        self._redis.rpush(input_key, str(args))

        # Execute the original method
        result = method(self, *args, **kwargs)

        # Store the output result
        self._redis.rpush(output_key, str(result))

        return result
    return wrapper

class Cache:
    """ Cache class """
    def __init__(self):
        """Initialize the Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data in Redis and return the key.

        Args:
            data: The data to store, which can be of type str, bytes, int, or float.

        Returns:
            str: The generated key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and optionally apply a conversion function.

        Args:
            key (str): The key to retrieve.
            fn (Callable, optional): The function to convert the data back to the desired format.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved and possibly converted data.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string from Redis.

        Args:
            key (str): The key to retrieve.

        Returns:
            Optional[str]: The retrieved string or None if the key does not exist.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis.

        Args:
            key (str): The key to retrieve.

        Returns:
            Optional[int]: The retrieved integer or None if the key does not exist.
        """
        return self.get(key, lambda d: int(d))


if __name__ == "__main__":
    cache = Cache()

    s1 = cache.store("first")
    print(s1)
    s2 = cache.store("second")
    print(s2)
    s3 = cache.store("third")
    print(s3)

    inputs = cache._redis.lrange("{}:inputs".format(cache.store.__qualname__), 0, -1)
    outputs = cache._redis.lrange("{}:outputs".format(cache.store.__qualname__), 0, -1)

    print("inputs: {}".format(inputs))
    print("outputs: {}".format(outputs))
