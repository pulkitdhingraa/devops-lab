# Write an async function check_all_services(services: list[dict]) -> list[dict] where each service dict has "name" and "url". The function should:
# - Check all services concurrently using aiohttp
# - Return a list of dicts: {"name": ..., "status": "up"/"down", "latency_ms": ...}
# - Mark a service as "down" if it throws an exception or returns non-200
# - Use asyncio.gather with return_exceptions=True

import asyncio
import aiohttp
import time
import logging

log = logging.getLogger(__name__)

async def check_service_status(session: aiohttp.ClientSession, service: dict) -> dict:
    start = time.monotonic()
    try:
        async with session.get(service["url"]) as resp:
            resp.raise_for_status()
            latency_ms = (time.monotonic() - start)*1000
            return {
                "name": service["name"],
                "status": "up",
                "latency_ms": round(latency_ms,2)
            }
    except Exception as e:
        log.error("service not responding", extra={"error": str(e)})
        return {
            "name": service["name"],
            "status": "down",
            "latency_ms": 0
        }

async def check_all_services(services: list[dict]) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [check_service_status(session, s) for s in services]
        results = await asyncio.gather(*tasks)
        return results
    

# Key Learnings

# Async is for I/O-bound work, not CPU-bound.
# await — pause here, let others run
# asyncio.gather() — run all of these concurrently, wait for all to finish