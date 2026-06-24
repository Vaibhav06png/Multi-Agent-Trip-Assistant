import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_hotels(city: str) -> list:
    api_key = os.getenv("FOURSQUARE_API_KEY")
    
    url = "https://api.foursquare.com/v3places/search"
    headers = {"Authorization": api_key}
    params = {
        "query":"hotel",
        "near": f"{city},India",
        "limit": 5
    }
    
    try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            hotels = []
            for result in data.get("results", []):
                hotels.append({
                    "name": result["name"],
                    "address": result["location"].get("formatted_address", "")
                })
            
            return hotels
    except Exception as e:
        print(f"[Hotels Service] Error: {e}")
        return []
        