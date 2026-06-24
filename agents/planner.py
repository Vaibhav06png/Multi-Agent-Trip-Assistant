from services.llm import call_gemini
import json
 
def planner_agent(state: dict) -> dict:
    user_input = state.get("user_input", "")
    chat_history = state.get("chat_history", [])
    
    full_context = "\n".join(chat_history) + "\n" + user_input
 
    # Step 1: Extract trip details
    extract_prompt = f"""
You are a travel information extractor.
 
From the conversation below, extract the following details:
1. destination - the place they want to visit (just the city/place name)
2. days - number of days as an integer (default 3 if not mentioned)
3. budget - total budget in INR as a number only (default 5000-8000 if not mentioned)
4. style - travel style: solo / couple / family / friends group / general
5. dates - travel dates or month/week mentioned (e.g. "First week of June")
 
Conversation:
{full_context}
 
Reply ONLY in this exact JSON format, nothing else:
{{
  "destination": "...",
  "days": 3,
  "budget": 0,
  "style": "general",
  "dates": "Not specified"
}}
"""
 
    raw = call_gemini(extract_prompt)
 
    try:
        raw = raw.replace("```json", "").replace("```", "").strip()
        extracted = json.loads(raw)
    except:
        extracted = {
            "destination": "",
            "days": 3,
            "budget": 0,
            "style": "general",
            "dates": "Not specified"
        }
 
    place = extracted.get("destination") or state.get("trip_place", "")
    days = extracted.get("days") or state.get("trip_days", 3)
    budget = extracted.get("budget") or state.get("trip_budget", 0.0)
    style = extracted.get("style") or state.get("trip_style", "general")
    dates = extracted.get("dates") or state.get("trip_dates", "Not specified")
 
    # Step 2: Ask Gemini to decide which agents need to run
    previous_state_summary = f"""
Previous trip info:
- Destination: {state.get('trip_place', 'Not set')}
- Dates: {state.get('trip_dates', 'Not set')}
- Days: {state.get('trip_days', 'Not set')}
- Style: {state.get('trip_style', 'Not set')}
- Budget: {state.get('trip_budget', 'Not set')}
 
New trip info extracted:
- Destination: {place}
- Dates: {dates}
- Days: {days}
- Style: {style}
- Budget: {budget}
"""
 
    routing_prompt = f"""
You are an AI orchestrator for a travel planning system.
 
You have 5 specialized agents available:
1. weather   - checks seasonal risk for destination and dates
2. destination - suggests places and activities based on style and weather
3. transport - plans how to reach and move around the destination
4. budget    - breaks down cost and checks budget feasibility
5. itinerary - composes the final day-wise travel plan (ALWAYS runs last)
 
{previous_state_summary}
 
Based on what changed between previous and new trip info, decide which agents need to run.
 
Rules:
- If this is a FIRST REQUEST (previous info was empty/not set), run ALL agents
- If destination or dates changed, run: weather, destination, transport, budget, itinerary
- If style changed, run: destination, transport, budget, itinerary
- If days changed, run: transport, budget, itinerary
- If only budget changed, run: budget, itinerary
- itinerary ALWAYS runs last no matter what
- If nothing changed, still run: itinerary (to refresh output)
 
Reply ONLY in this exact JSON format, nothing else:
{{
  "agents_to_run": ["weather", "destination", "transport", "budget", "itinerary"],
  "reason": "one line explanation of why these agents were chosen"
}}
"""
 
    routing_raw = call_gemini(routing_prompt)
 
    try:
        routing_raw = routing_raw.replace("```json", "").replace("```", "").strip()
        routing_decision = json.loads(routing_raw)
        agents_to_run = routing_decision.get("agents_to_run", 
                        ["weather", "destination", "transport", "budget", "itinerary"])
        routing_reason = routing_decision.get("reason", "")
    except:
        # Safe fallback - run everything
        agents_to_run = ["weather", "destination", "transport", "budget", "itinerary"]
        routing_reason = "Fallback: running all agents due to parsing error"
 
    state.update({
        "trip_place": place,
        "trip_days": int(days),
        "trip_budget": float(budget),
        "trip_style": style,
        "trip_dates": dates,
        "agents_to_run": agents_to_run,
        "routing_reason": routing_reason,
        "warnings": []
    })
    
    print (f"\n{'='*50}")
    print(f"PLANNER AGENT DECISION")
    print(f"Gemini chose agents: {agents_to_run}")
    print(f"Reason: {routing_reason}")
    print(f"{'='*50}\n")
    
    
    
    print(f"\n{'='*50}")
    print(f"PLANNER AGENT OUTPUT")
    print(f"Place : {state.get('trip_place')}")
    print(f"Days : {state.get('trip_days')}")
    print(f"Budget : {state.get('trip_budget')}")
    print(f"Style : {state.get('trip_style')}")
    print(f"Dates : {state.get('trip_dates')}")
    print(f"Agents : {state.get('agents_to_run')}")
    print(f"Reason : {state.get('routing_reason')}")
    print(f"{'='*50}\n")
 
    return state