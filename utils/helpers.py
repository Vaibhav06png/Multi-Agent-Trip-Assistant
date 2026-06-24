def extract_place_from_input(text: str) -> str:
    # Simple extraction - LLM handles complex cases
    common_places = [
        "Goa", "Kerala", "Rajasthan", "Manali", "Shimla",
        "Jaipur", "Mumbai", "Delhi", "Agra", "Ooty",
        "Coorg", "Rishikesh", "Leh", "Ladakh", "Darjeeling",
        "Andaman", "Mysore", "Pune", "Hyderabad", "Chennai"
    ]
    for place in common_places:
        if place.lower() in text.lower():
            return place
    return "Unknown"
 
def extract_days_from_input(text: str) -> int:
    import re
    # Look for patterns like "4 days", "4-day", "four days"
    word_to_num = {"one":1,"two":2,"three":3,"four":4,"five":5,
                   "six":6,"seven":7,"eight":8,"nine":9,"ten":10}
    
    match = re.search(r'(\d+)\s*[-\s]?\s*day', text.lower())
    if match:
        return int(match.group(1))
    
    for word, num in word_to_num.items():
        if word in text.lower():
            return num
    return 3  # default
 
def extract_budget_from_input(text: str) -> float:
    import re
    # Look for patterns like 40000, 40,000, 40k, INR 40000
    text = text.replace(",", "")
    
    match = re.search(r'(\d+)\s*k\b', text.lower())
    if match:
        return float(match.group(1)) * 1000
    
    match = re.search(r'(\d{4,6})', text)
    if match:
        return float(match.group(1))
    
    return 0.0  # unknown
 
def extract_style_from_input(text: str) -> str:
    text = text.lower()
    if "couple" in text or "honeymoon" in text or "romantic" in text:
        return "couple"
    elif "family" in text or "kids" in text or "children" in text:
        return "family"
    elif "solo" in text or "alone" in text or "myself" in text:
        return "solo"
    elif "friends" in text or "group" in text or "gang" in text:
        return "friends group"
    return "general"
 