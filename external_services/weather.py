from fastapi import Depends
from core.htppx_client import get_httpx_client
from core.config import get_settings, Settings
import httpx

async def fetch_weather_data(
        city_name: str,
        settings: Settings = Depends(get_settings),
        client: httpx.AsyncClient = Depends(get_httpx_client)
):
    Base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.52,  # Example static coordinates for demonstration
        "longitude": 13.41,
        "current_weather": True
    }

    # Headers are usually not needed for Open-Meteo but included for best practice
    headers = {
        "X-API-Key": settings.API_AUTH_KEY, # Use the injected settings
        "User-Agent": "FastAPI-WeatherApp/1.0"
    }

    response = await client.get(Base_url, params=params, headers=headers)
    response.raise_for_status() # Raise an exception for bad status codes

    # The return value is what gets cached
    return response.json()