from services.llm import call_gemini
from services.hotels_service import get_hotels

def itinerary_agent(state: dict) -> dict:
    
    hotels = get_hotels(state.get("trip_place",""))
    
    if hotels:
        hotel_list = "\n".join([
            f"-{h['name']} ({h['address']})"
            for h in hotels
        ])
    else:
        hotel_list = "No Live hotel data is available"
        
    prompt = f"""
You are a professional travel itinerary planner for India.
 
Here is all the information gathered:
 
DESTINATION: {state['trip_place']}
DATES: {state['trip_dates']}
DAYS: {state['trip_days']}
TRAVEL STYLE: {state['trip_style']}
BUDGET: INR {state['trip_budget']}
 
WEATHER ADVISORY:
{state.get('weather_info', 'Not available')}
 
PLACES & ACTIVITIES:
{state.get('place_info', 'Not available')}
 
TRANSPORT PLAN:
{state.get('transport_info', 'Not available')}
 
BUDGET BREAKDOWN:
{state.get('budget_info', 'Not available')}

REAL HOTELS AVAILABLE IN {state['trip_place']}:
{hotel_list}
 
WARNINGS:
{', '.join(state.get('warnings', [])) or 'None'}
 
INSTRUCTIONS:
- Use the Real  Hotel names provided above for stay recommendations
- Match hotel to budget level
- Include estimated cost per night
- Always give COST RANGES (min - max) not exact fixed numbers for Daily and Total Est. Cost

Now create a clean day-wise itinerary for {state['trip_days']} days.
Format:
Day 1 - [Theme]
- Morning: ...
- Afternoon: ...
- Evening: ...
- Stay: [Real Hotel Name] (~INR XXXX/night)
- Est. Cost: INR XXXX - XXXX (range)
 
Day 2 - [Theme]
...and so on
 
At the end add a short "Why these choices?" section explaining key decisions.
Keep it practical and realistic for India.
"""
    
    itinerary = call_gemini(prompt)
    state["final_itinerary"] = itinerary
    
    print(f"\n{'='*50}")
    print(f"ITINERARY AGENT OUTPUT")
    print(f"Final Itinerary:\n{state.get('final_itinerary')}")
    print(f"{'='*50}\n")
    return state
 