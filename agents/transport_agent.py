from services.llm import call_gemini
 
def transport_agent(state: dict) -> dict:
    prompt = f"""
You are a transport planning expert for Indian travel.
 
Destination: {state['trip_place']}
Number of days: {state['trip_days']}
Travel style: {state['trip_style']}
Budget level: INR {state['trip_budget']}
 
Your job:
1. Suggest how to reach {state['trip_place']} from major cities (flight/train/bus)
2. Suggest local transport options within {state['trip_place']}
3. Estimate rough transport costs
4. Give tips to avoid wasting travel time during the trip
 
Keep it short, practical, India-specific.
"""
    transport_summary = call_gemini(prompt)
    state["transport_info"] = transport_summary
    
    print(f"\n{'='*50}")
    print(f"TRANSPORT AGENT OUTPUT")
    print(f"Transport Info:\n{state.get('transport_info')}")
    print(f"{'='*50}\n")
    return state
 