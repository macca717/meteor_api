from typing import Any, Dict

from aiohttp import ClientSession

__all__ = ["fetch_json", "fetch_bytes"]


async def fetch_json(url: str, session: ClientSession) -> Dict[Any, Any]:
    """Fetch JSON to Python dict helper

    Args:
        url (str): URL of data
        session (ClientSession): Session

    Returns:
        Dict[Any, Any]: Dict of retrieved data
    """
    async with session.get(url) as resp:
        return await resp.json(content_type=None)


async def fetch_bytes(url: str, session: ClientSession) -> bytes:
    """Fetch Bytes Helper

    Args:
        url (str): URL of data
        session (ClientSession): Session

    Returns:
        bytes: Data as bytes
    """
    async with session.get(url) as resp:
        return await resp.read()
