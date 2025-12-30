from typing import Any
from external_services.weather import fetch_weather_data
from fastapi import APIRouter, Depends
from core.config import get_settings, Settings
from core.htppx_client import get_httpx_client
import httpx
from fastapi_cache.decorator import cache


router = APIRouter()

@router.get("/{city_name}")
@cache(expire=300)
async def get_weather_data(
        city_name: str,
        settings: Settings = Depends(get_settings),
        client: httpx.AsyncClient = Depends(get_httpx_client)
):
    weather_data = await fetch_weather_data(city_name, settings, client)
    return weather_data