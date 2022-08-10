from typing import Optional

import aiohttp


async def get_session(base_url: Optional[str] = None):
    """Get an aiohttp session helper

    Args:
        base_url (Optional[str], optional): Base request URL. Defaults to None.

    Yields:
        ClientSession: Session
    """
    session = None
    try:
        session = aiohttp.ClientSession(base_url=base_url)
        yield session
    finally:
        if session:
            await session.close()
