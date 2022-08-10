import time
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class CacheEntry:
    data: Any
    last_update: float


class LocalCache:
    """Local Cache Class

    Performs time caching of data.
    """

    def __init__(self) -> None:
        self._cache: Dict[str, CacheEntry] = {}

    def get(self, route: str, ttl: float) -> Optional[Any]:
        """Get cached data if available

        Args:
            route (str): Route of request(key)
            ttl (float): Cache time to live in seconds

        Returns:
            Optional[Any]: Cached data or None
        """
        if entry := self._cache.get(route):
            if entry.last_update + ttl >= time.time():
                return entry.data
        return None

    def set(self, route: str, data: Any) -> None:
        """Set cache data

        Args:
            route (str): Route of request(key)
            data (Any): Data to cache
        """
        if self._cache.get(route):
            del self._cache[route]
        entry = CacheEntry(data=data, last_update=time.time())
        self._cache[route] = entry
