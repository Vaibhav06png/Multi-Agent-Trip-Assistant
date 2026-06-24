import requests
import os
from dotenv import load_dotenv
 
load_dotenv()
 
def get_attractions(city: str) -> list:
    api_key = os.getenv("OPENTRIPMAP_API_KEY")
    
    print(f"[Destination Service] Fetching attractions for: {city}")
    
    try:
        # Step 1: Get city coordinates
        geo_url = "https://api.opentripmap.com/0.1/en/places/geoname"
        geo_params = {
            "name": city,
            "country": "IN",
            "apikey": api_key
        }
        
        geo_response = requests.get(geo_url, params=geo_params, timeout=10)
        geo_data = geo_response.json()
        
        if "lat" not in geo_data:
            print(f"[Destination Service] City not found: {city}")
            return []
        
        lat = geo_data["lat"]
        lon = geo_data["lon"]
        
        print(f"[Destination Service] Coordinates: {lat}, {lon}")
        
        # Step 2: Get attractions around those coordinates
        places_url = "https://api.opentripmap.com/0.1/en/places/radius"
        places_params = {
            "radius": 15000,       # 15km radius
            "lon": lon,
            "lat": lat,
            "kinds": "interesting_places,cultural,natural,architecture,religion,museums",
            "rate": "3",           # minimum rating 3 (out of 3)
            "format": "json",
            "limit": 15,           # top 15 places
            "apikey": api_key
        }
        
        places_response = requests.get(
            places_url, params=places_params, timeout=10
        )
        places_data = places_response.json()
        
        attractions = []
        for place in places_data:
            name = place.get("name", "").strip()
            if name:  # only add if has a name
                attractions.append({
                    "name": name,
                    "kind": place.get("kinds", "").replace(",", ", "),
                    "rating": place.get("rate", "N/A")
                })
        
        print(f"[Destination Service] Found {len(attractions)} attractions")
        return attractions
    
    except requests.exceptions.Timeout:
        print("[Destination Service] Request timed out")
        return []
    except Exception as e:
        print(f"[Destination Service] Error: {e}")
        return []
 