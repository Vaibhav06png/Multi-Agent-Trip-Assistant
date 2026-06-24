from services.llm import call_gemini
from services.destination_service import get_attractions
from prompts.destination_prompt import get_destination_prompt
 
def destination_agent(state: dict) -> dict:
    
    place = state.get("trip_place", "")
    style = state.get("trip_style", "general")
    days  = state.get("trip_days", 3)
    
    attractions = get_attractions(place)
    
    # Step 2: Format for prompt
    if attractions:
        attractions_text = "\n".join([
            f"- {a['name']} (Type: {a['kind']})"
            for a in attractions
        ])
    else:
        attractions_text = "Live attraction data unavailable"
    
    # Step 3: Gemini filters and interprets
    prompt = f"""
You are a travel destination expert for India.
 
DESTINATION: {place}
TRAVEL STYLE: {style}
NUMBER OF DAYS: {days}
WEATHER CONDITION: {state.get('weather_info', 'Not available')}
 
REAL ATTRACTIONS IN {place.upper()} (from OpenTripMap):
{attractions_text}
 
Using the REAL attractions listed above:
1. Select the best 6-8 attractions suitable for {style} travelers
2. Explain why each is suitable given the weather condition
3. Suggest what to AVOID based on weather
4. Group them by area/zone to minimize travel time
 
Do NOT invent attractions not listed above.
Only use the real places provided.
Keep it practical and specific.
"""
    
    place_summary = call_gemini(prompt)
    state["place_info"] = place_summary
    
    
    print(f"\n{'='*50}")
    print(f"DESTINATION AGENT OUTPUT")
    print(f"Place Info:\n{state.get('place_info')}")
    print(f"{'='*50}\n")
    return state
 