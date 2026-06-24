from langgraph.graph import StateGraph, END
from graph.state import TripState
from agents.planner import planner_agent
from agents.weather_agent import weather_agent
from agents.destination_agent import destination_agent
from agents.transport_agent import transport_agent
from agents.budget_agent import budget_agent
from agents.itinerary_agent import itinerary_agent
 
# Routing functions - each checks if this agent is in the list
def route_after_planner(state: dict) -> str:
    agents = state.get("agents_to_run", [])
    if "weather" in agents:
        return "weather"
    elif "destination" in agents:
        return "destination"
    elif "transport" in agents:
        return "transport"
    elif "budget" in agents:
        return "budget"
    else:
        return "itinerary"
 
def route_after_weather(state: dict) -> str:
    agents = state.get("agents_to_run", [])
    if "destination" in agents:
        return "destination"
    elif "transport" in agents:
        return "transport"
    elif "budget" in agents:
        return "budget"
    else:
        return "itinerary"
 
def route_after_destination(state: dict) -> str:
    agents = state.get("agents_to_run", [])
    if "transport" in agents:
        return "transport"
    elif "budget" in agents:
        return "budget"
    else:
        return "itinerary"
 
def route_after_transport(state: dict) -> str:
    agents = state.get("agents_to_run", [])
    if "budget" in agents:
        return "budget"
    else:
        return "itinerary"
 
def build_graph():
    graph = StateGraph(TripState)
 
    # Add all nodes
    graph.add_node("planner", planner_agent)
    graph.add_node("weather", weather_agent)
    graph.add_node("destination", destination_agent)
    graph.add_node("transport", transport_agent)
    graph.add_node("budget", budget_agent)
    graph.add_node("itinerary", itinerary_agent)
 
    # Entry point
    graph.set_entry_point("planner")
 
    # Planner decides first jump
    graph.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "weather": "weather",
            "destination": "destination",
            "transport": "transport",
            "budget": "budget",
            "itinerary": "itinerary"
        }
    )
 
    # Each agent conditionally routes to next
    graph.add_conditional_edges(
        "weather",
        route_after_weather,
        {
            "destination": "destination",
            "transport": "transport",
            "budget": "budget",
            "itinerary": "itinerary"
        }
    )
 
    graph.add_conditional_edges(
        "destination",
        route_after_destination,
        {
            "transport": "transport",
            "budget": "budget",
            "itinerary": "itinerary"
        }
    )
 
    graph.add_conditional_edges(
        "transport",
        route_after_transport,
        {
            "budget": "budget",
            "itinerary": "itinerary"
        }
    )
 
    # Budget always goes to itinerary
    graph.add_edge("budget", "itinerary")
    graph.add_edge("itinerary", END)
 
    return graph.compile()
 