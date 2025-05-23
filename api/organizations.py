import aiohttp
from config.settings import BASE_URL
from .auth import Login
import json

#Murojaat yunalishi to'g'risidagi ma'lumotlarni o'qib olish
async def loadDirections():
    headers = {
        'Content-Type': 'application/json'
    }

    access_token = await Login()
    headers['Authorization'] = f'Bearer {access_token}'

    url = BASE_URL + '/api/v1/organizations/directions?limit=100'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data['results']
            else:
                error = await response.text()
                raise Exception(f'Yo\'nalish ma\'lumotlarni o\'qishda xatolik yuz berdi: {error}')

#Hudud ma'lumotlarni o'qib olish
async def loadRegions():
    headers = {
        'Content-Type': 'application/json'
    }
    access_token = await Login()
    headers['Authorization'] = f'Bearer {access_token}'

    url = BASE_URL + '/api/v1/organizations/regions?limit=100'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data['results']
            else:
                error = await response.text()
                raise Exception (f'Xudud ma\'lumotlarni o\'qishda xatolik yuz berdi: {error}')

#Sohaviy xizmatlar to'g'risidagi ma\'lumotlarni o'qib olish

async def loadServices():
    headers = {
        'Content-Type': 'application/json'
    }
    access_token = await Login()
    headers['Authorization'] = f'Bearer {access_token}'

    url = BASE_URL + '/api/v1/organizations/services?limit=100'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data['results']

            else:
                error = await response.text()
                raise Exception(f'Sohaviy xizmatlar ma\'lumotlarni o\'qishda xatolik yuz berdi: {error}') 
            
# Murojaatlar holatini tekshitish qismi
async def checkAppealStatus(user_id):
    headers = {
        'Content-Type': 'application/json'
    }
    access_token = await Login()
    headers['Authorization'] = f'Bearer {access_token}'

    data = {
        'telegram_id': user_id
    }
    url = BASE_URL + f'/api/v1/appeals/check/'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(data),  headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                error = await response.text()
                raise Exception(f'Murojaat holatini tekshirishda xatolik yuz berdi: {error}')




