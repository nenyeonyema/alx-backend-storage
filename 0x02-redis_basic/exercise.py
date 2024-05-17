#!/usr/bin/python3
""" Web """
import requests
import redis
import functools
from typing import Callable

# Initialize Redis client
r = redis.Redis()


def cache_page(method: Callable) -> Callable:
    """ Callable function """
    @functools.wraps(method)
    def wrapper(url: str) -> str:
        """ wrapper function """
        # Check if the result is cached
        cached_result = r.get(url)
        if cached_result:
            return cached_result.decode('utf-8')

        # If not cached, call the method and cache the result
        result = method(url)
        r.setex(url, 10, result)  # Set cache with expiration time of 10 seconds

        # Track the number of times the URL was accessed
        r.incr(f"count:{url}")

        return result
    return wrapper

@cache_page
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a particular URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"

    # Fetch the page and print the content
    print(get_page(url))

    # Print the number of times the URL was accessed
    print(f"Access count for {url}: {r.get(f'count:{url}').decode('utf-8')}")
