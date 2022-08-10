import time
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class CacheEntry:
    data: Any
    last_update: float


class LocalCache:
    def __init__(self) -> None:
        self._cache: Dict[str, CacheEntry] = {}

    def get(self, route: str, ttl: float) -> Optional[Any]:
        if entry := self._cache.get(route):
            if entry.last_update + ttl >= time.time():
                return entry.data
        return None

    def set(self, route: str, data: Any) -> None:
        if self._cache.get(route):
            del self._cache[route]
        entry = CacheEntry(data=data, last_update=time.time())
        self._cache[route] = entry
