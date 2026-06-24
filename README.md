# Multi-Agent-Trip-Assistant
Multi Agent Trip planner using LangGraph framework

SYSTEM ARCHITECTURE
User Input (Streamlit)
        │
        ▼
┌─────────────────┐
│  Planner Agent  │ ← Extracts intent, decides which agents to run
└────────┬────────┘
         │
    (Gemini decides routing)
         │
    ┌────┴──────────────────┐
    │                       │
    ▼                       ▼
Weather Agent        (skip if unchanged)
    │
    ▼
Destination Agent
    │
    ▼
Transport Agent
    │
    ▼
Budget Agent
    │
    ▼
Itinerary Agent ← Synthesizes everything into day-wise plan
    │
    ▼
Final Output (Streamlit Chat UI)**


FOLDER STRUCTURE
├── agents/
│   ├── planner.py
│   ├── weather_agent.py
│   ├── destination_agent.py
│   ├── transport_agent.py
│   ├── budget_agent.py
│   └── itinerary_agent.py
├── graph/
│   ├── state.py
│   └── workflow.py
├── prompts/
│   ├── weather_prompt.py
│   ├── destination_prompt.py
│   └── budget_prompt.py
├── services/
│   ├── llm.py
│   ├── weather_service.py
│   ├── destination_service.py
│   └── hotels_service.py
├── app.py
├── requirements.txt
└── .env

Agents:-
1. Planner Agent (Orchestrator)
Reads user message and full chat history
Uses Gemini to extract: destination, days, budget, style, dates
Uses Gemini to decide which agents need to run
Detects constraint changes for selective replanning

2. Weather Agent
Calls OpenWeatherMap API for live weather data
Uses Gemini to interpret seasonal risk for travelers
Flags monsoon, extreme heat, or unsuitable conditions
Falls back to Gemini seasonal knowledge if API unavailable

3. Destination Agent
Fetches real attractions from OpenTripMap API
Uses Gemini to filter by travel style and weather conditions
Suggests best zones, activities, and what to avoid

4. Transport Agent
Suggests how to reach the destination from major cities
Recommends local transport options within the destination
Estimates realistic transport costs for India

5. Budget Agent
Breaks down total budget into categories
Flags if budget is too tight
Suggests trade-offs and money-saving tips

6. Itinerary Composer Agent
Fetches real hotel names from Foursquare API
Synthesizes all agent outputs into a day-wise plan
Explains reasoning behind every key decision
 
