from services.weather_service import get_weather
from services.llm import call_gemini
from prompts.weather_prompt import get_weather_prompt


def format_weather_data(weather_data: dict, place: str) -> str:
    """
    Convert weather API response into readable text.
    """

    if not weather_data:
        return ""

    # Common possible keys from different weather APIs
    temperature = (
        weather_data.get("temperature")
        or weather_data.get("temp")
        or weather_data.get("current_temp")
    )

    condition = (
        weather_data.get("condition")
        or weather_data.get("description")
        or weather_data.get("weather")
    )

    humidity = weather_data.get("humidity")

    wind_speed = (
        weather_data.get("wind_speed")
        or weather_data.get("wind")
        or weather_data.get("windspeed")
    )

    summary = f"Live weather for {place}:\n"

    if temperature is not None:
        summary += f"- Temperature: {temperature}°C\n"

    if condition:
        summary += f"- Condition: {condition}\n"

    if humidity is not None:
        summary += f"- Humidity: {humidity}%\n"

    if wind_speed is not None:
        summary += f"- Wind Speed: {wind_speed} km/h\n"

    # If no useful field was found, show raw API data
    if summary.strip() == f"Live weather for {place}:":
        summary += f"- Weather Data: {weather_data}\n"

    return summary


def weather_agent(state: dict) -> dict:
    """
    Weather agent:
    1. Fetches weather using weather API.
    2. If API data is available, uses it directly.
    3. If API fails, calls Gemini as fallback.
    """

    place = state.get("trip_place", "")
    warnings = state.get("warnings", [])

    weather_data = get_weather(place)

    print(f"\nFetched Weather Data for {place}:")
    print(weather_data)

    # Case 1: API failed or returned invalid data
    if not weather_data or "error" in weather_data:
        warnings.append(
            f"Could not fetch live weather for {place}. Using LLM fallback."
        )

        prompt = get_weather_prompt(state, weather_data)
        weather_summary = call_gemini(prompt)

    # Case 2: API returned valid weather data
    else:
        weather_summary = format_weather_data(weather_data, place)

    state["weather_info"] = weather_summary
    state["warnings"] = warnings

    print(f"\n{'=' * 50}")
    print("WEATHER AGENT OUTPUT")
    print(f"Weather Info:\n{state.get('weather_info')}")
    print(f"Warnings: {state.get('warnings')}")
    print(f"{'=' * 50}\n")

    return state