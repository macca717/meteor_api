import aiohttp

_session = None


async def get_session():
    global _session
    if not _session:
        _session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15.0))
    return _session


async def close_session():
    if _session:
        await _session.close()
