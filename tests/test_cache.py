from unittest.mock import patch

from app.local_cache import LocalCache


def test_cache_not_present():
    cache = LocalCache()
    assert cache.get("missing", 12) is None


def test_cache_present():
    cache = LocalCache()
    cache.set("test", 34)
    assert cache.get("test", 1000) == 34


def test_cache_invalidate():
    with patch("time.time", return_value=1000):
        cache = LocalCache()
        cache.set("test", 100)
    assert cache.get("test", 100) is None
