from typing import Any, Dict

from aiohttp import ClientSession

__all__ = ["fetch_json", "fetch_bytes"]


async def fetch_json(url: str, session: ClientSession) -> Dict[Any, Any]:
    async with session.get(url) as resp:
        return await resp.json(content_type=None)


async def fetch_bytes(url: str, session: ClientSession) -> bytes:
    async with session.get(url) as resp:
        return await resp.read()
