import httpx


async def get(url: str, headers: dict):
    async with httpx.AsyncClient() as client:
        return await client.get(
            url=url, headers=headers
        )


async def post(url: str, params: dict, headers: dict):
    async with httpx.AsyncClient() as client:
        return await client.post(
            url=url, json=params, headers=headers
        )


async def put(url: str, params: dict, headers: dict):
    async with httpx.AsyncClient() as client:
        return await client.put(
            url=url, json=params, headers=headers
        )


async def delete(url: str, headers: dict):
    async with httpx.AsyncClient() as client:
        return await client.delete(
            url=url, headers=headers
        )
