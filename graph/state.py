from typing import TypedDict, List, Optional

class TripState(TypedDict):
    user_input : str
    chat_history : List[str]
    trip_place:str
    trip_dates: str
    trip_days:int
    trip_style: str
    trip_budget: float
    weather_info:str
    place_info: str
    transport_info: str
    budget_info: str
    final_itinerary: str
    warnings: List[str]
    replan_needed:bool
    agents_to_run: List[str]
    routing_reason: str
    
    