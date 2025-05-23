from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api.organizations import loadDirections, loadRegions, loadServices
from typing import List

REGION_CALLBACK_PREFIX = "user_region_"
SERVICE_CALLBACK_PREFIX = "user_service_"
DIRECTION_CALLBACK_PREFIX = "user_direction_"

REGION_CALLBACK_PREFIX_ANONYMOUS = "anonymous_region_"
SERVICE_CALLBACK_PREFIX_ANONYMOUS = "anonymous_service_"
DIRECTION_CALLBACK_PREFIX_ANONYMOUS = "anonymous_direction_"

async def region_inline_keyboard() -> InlineKeyboardMarkup:
    try:
        regions: List[dict] = await loadRegions()
    except Exception as e:
        raise RuntimeError(f"Regionni o\'qishda xatolik yuz berdi: {e}") from e

    if not regions:
        raise ValueError("Region topilmadi")

    keyboard: List[List[InlineKeyboardButton]] = []

    for region in regions:
        name = region.get("name")
        region_id = region.get("id")

        if not name or region_id is None:
            continue  

        button = InlineKeyboardButton(
            text=name,
            callback_data=f"{REGION_CALLBACK_PREFIX}{region_id}"
        )
        keyboard.append([button])  

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
async def service_inline_keyboard() -> InlineKeyboardMarkup:
    try:
        services: List[dict] = await loadServices()
    except Exception as e:
        raise RuntimeError(f"Sohaviy xizmatlarni o\'qishda xatolik yuz berdi: {e}") from e

    if not services:
        raise ValueError("Sohaviy xizmatlar topilmadi")

    keyboard: List[List[InlineKeyboardButton]] = []

    for service in services:
        name = service.get("name")
        service_id = service.get("id")

        if not name or service_id is None:
            continue  

        button = InlineKeyboardButton(
            text=name,
            callback_data=f"{SERVICE_CALLBACK_PREFIX}{service_id}"
        )
        keyboard.append([button])  

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def direction_inline_keyboard() -> InlineKeyboardMarkup:
    try:
        directions: List[dict] = await loadDirections()
    except Exception as e:
        raise RuntimeError(f"Yo'nalish ma'lumotlarni o\'qishda xatolik yuz berdi: {e}") from e

    if not directions:
        raise ValueError("Yo\'nalish ma\'lumotlari topilmadi")

    keyboard: List[List[InlineKeyboardButton]] = []

    for direction in directions:
        name = direction.get("name")
        direction_id = direction.get("id")

        if not name or direction_id is None:
            continue  

        button = InlineKeyboardButton(
            text=name,
            callback_data=f"{DIRECTION_CALLBACK_PREFIX}{direction_id}"
        )
        keyboard.append([button])  

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def region_inline_keyboard_anonymous() -> InlineKeyboardMarkup:
    try:
        regions: List[dict] = await loadRegions()
    except Exception as e:
        raise RuntimeError(f"Regionni o\'qishda xatolik yuz berdi: {e}") from e

    if not regions:
        raise ValueError("Region topilmadi")

    keyboard: List[List[InlineKeyboardButton]] = []

    for region in regions:
        name = region.get("name")
        region_id = region.get("id")

        if not name or region_id is None:
            continue  

        button = InlineKeyboardButton(
            text=name,
            callback_data=f"{REGION_CALLBACK_PREFIX_ANONYMOUS}{region_id}"
        )
        keyboard.append([button])  

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
async def service_inline_keyboard_anonymous() -> InlineKeyboardMarkup:
    try:
        services: List[dict] = await loadServices()
    except Exception as e:
        raise RuntimeError(f"Sohaviy xizmatlarni o\'qishda xatolik yuz berdi: {e}") from e

    if not services:
        raise ValueError("Sohaviy xizmatlar topilmadi")

    keyboard: List[List[InlineKeyboardButton]] = []

    for service in services:
        name = service.get("name")
        service_id = service.get("id")

        if not name or service_id is None:
            continue  

        button = InlineKeyboardButton(
            text=name,
            callback_data=f"{SERVICE_CALLBACK_PREFIX_ANONYMOUS}{service_id}"
        )
        keyboard.append([button])  

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def direction_inline_keyboard_anonymous() -> InlineKeyboardMarkup:
    try:
        directions: List[dict] = await loadDirections()
    except Exception as e:
        raise RuntimeError(f"Yo'nalish ma'lumotlarni o\'qishda xatolik yuz berdi: {e}") from e

    if not directions:
        raise ValueError("Yo\'nalish ma\'lumotlari topilmadi")

    keyboard: List[List[InlineKeyboardButton]] = []

    for direction in directions:
        name = direction.get("name")
        direction_id = direction.get("id")

        if not name or direction_id is None:
            continue  

        button = InlineKeyboardButton(
            text=name,
            callback_data=f"{DIRECTION_CALLBACK_PREFIX_ANONYMOUS}{direction_id}"
        )
        keyboard.append([button])  

    return InlineKeyboardMarkup(inline_keyboard=keyboard)