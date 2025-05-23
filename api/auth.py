import aiohttp
from config.settings import BASE_URL, BACK_PASSWORD, BACK_USERNAME

#Tizimga kirish
async def Login():
    payload = {
        "username": BACK_USERNAME,
        "password": BACK_PASSWORD
    }
    headers = {
        'Content-Type': 'application/json'
    }
    
    url = BASE_URL + "/api/v1/user/login/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data['access']
            else:
                error = await response.text()
                raise Exception(f'Tizimga kirishda xatolik yuz berdi: {error}')