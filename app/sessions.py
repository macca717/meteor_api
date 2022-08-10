from typing import Optional

import aiohttp


async def get_session(base_url: Optional[str] = None):
    session = None
    try:
        session = aiohttp.ClientSession(base_url=base_url)
        yield session
    finally:
        if session:
            await session.close()
