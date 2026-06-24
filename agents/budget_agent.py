from services.llm import call_gemini
from prompts.budget_prompt import get_budget_prompt
 
def budget_agent(state: dict) -> dict:
    prompt = get_budget_prompt(state)
    budget_summary = call_gemini(prompt)
    
    warnings = state.get("warnings", [])
    if state.get("trip_budget", 0) > 0 and state.get("trip_days", 1) > 0:
        per_day = state["trip_budget"] / state["trip_days"]
        if per_day < 2000:
            warnings.append("Budget seems very tight. Consider increasing or adjusting expectations.")
    
    state["budget_info"] = budget_summary
    state["warnings"] = warnings
    
    print(f"\n{'='*50}")
    print(f"BUDGET AGENT OUTPUT")
    print(f"Budget Info:\n{state.get('budget_info')}")
    print(f"Warnings : {state.get('warnings')}")
    print(f"{'='*50}\n")
    return state
 