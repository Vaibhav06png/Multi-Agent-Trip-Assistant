def get_weather_prompt(state: dict, weather_data: dict) -> str:
    return f"""
You are a travel weather advisor.
 
Destination: {state['trip_place']}
Travel dates: {state['trip_dates']}
Current weather data: {weather_data}
 
Your job:
1. Tell if this is a good time to visit based on season
2. Mention any weather risks (monsoon, extreme heat, cold)
3. Suggest how weather affects activity planning
4. Give 2-3 practical tips for this weather
 
Keep it short and practical.
"""