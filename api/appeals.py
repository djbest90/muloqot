import aiohttp
from config.settings import BASE_URL
from .auth import Login

async def createAppeal(data):
    headers = {
        # 'Content-Type': 'application/json'
    }

    access_token = await Login()
    headers['Authorization'] = f'Bearer {access_token}'

    url = BASE_URL + '/api/v1/appeals/create/'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as response:
            print(await response.text())
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return response.status
