import streamlit as st
from graph.workflow import build_graph
 
st.set_page_config(page_title="Smart Trip Planner", page_icon="✈️", layout="wide")
st.title("✈️ Smart Trip Planning Assistant")
st.caption("Powered by Multi-Agent AI | Gemini + LangGraph")
 
# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "trip_state" not in st.session_state:
    st.session_state.trip_state = {
        "user_input": "",
        "chat_history": [],
        "trip_place": "",
        "trip_dates": "",
        "trip_days": 0,
        "trip_style": "",
        "trip_budget": 0.0,
        "weather_info": "",
        "place_info": "",
        "transport_info": "",
        "budget_info": "",
        "final_itinerary": "",
        "warnings": [],
        "agents_to_run": [],
        "routing_reason": "",
        "replan_needed": False
    }
 
# ─── SIDEBAR ───────────────────────────────────────────
with st.sidebar:
    st.header("🔍 Agent Execution Tracker")
    st.divider()
 
    # Show which agents ran
    if st.session_state.trip_state.get("agents_to_run"):
        agents = st.session_state.trip_state["agents_to_run"]
        st.write("**Agents that ran this turn:**")
        for i, agent in enumerate(agents, 1):
            st.success(f"Step {i} → {agent} ✓")
    else:
        st.info("No query run yet")
 
    st.divider()
 
    # Show planner reasoning
    if st.session_state.trip_state.get("routing_reason"):
        st.write("**Planner's reasoning:**")
        st.info(st.session_state.trip_state["routing_reason"])
 
    st.divider()
 
    # Show current trip state
    if st.session_state.trip_state.get("trip_place"):
        st.write("**Current Trip Info:**")
        st.write(f"📍 Place: {st.session_state.trip_state['trip_place']}")
        st.write(f"📅 Dates: {st.session_state.trip_state['trip_dates']}")
        st.write(f"🌙 Days: {st.session_state.trip_state['trip_days']}")
        st.write(f"👥 Style: {st.session_state.trip_state['trip_style']}")
        st.write(f"💰 Budget: ₹{st.session_state.trip_state['trip_budget']}")
    else:
        st.write("**Current Trip Info:**")
        st.write("No trip info yet")
 
    st.divider()
 
    # Show warnings if any
    if st.session_state.trip_state.get("warnings"):
        st.write("**Warnings:**")
        for w in st.session_state.trip_state["warnings"]:
            st.warning(w)
 
    # Reset button
    st.divider()
    if st.button("🔄 Reset Conversation"):
        st.session_state.chat_history = []
        st.session_state.trip_state = {
            "user_input": "",
            "chat_history": [],
            "trip_place": "",
            "trip_dates": "",
            "trip_days": 0,
            "trip_style": "",
            "trip_budget": 0.0,
            "weather_info": "",
            "place_info": "",
            "transport_info": "",
            "budget_info": "",
            "final_itinerary": "",
            "warnings": [],
            "agents_to_run": [],
            "routing_reason": "",
            "replan_needed": False
        }
        st.rerun()
 
# ─── MAIN CHAT AREA ────────────────────────────────────
 
# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
 
# Chat input
user_input = st.chat_input("Tell me about your trip... (e.g. I want to go to Goa in first week of June)")
 
if user_input:
    # Show user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
 
    with st.chat_message("assistant"):
        with st.spinner("🤖 Agents working on your plan..."):
 
            # Update state with new input
            current_state = st.session_state.trip_state.copy()
            current_state["user_input"] = user_input
            current_state["chat_history"] = [
                m["content"] for m in st.session_state.chat_history
                if m["role"] == "user"
            ]
 
            # Run the graph
            graph = build_graph()
            result = graph.invoke(current_state)
 
            # Save updated state
            st.session_state.trip_state = result
 
            # Build response
            response_parts = []
 
            if result.get("warnings"):
                for w in result["warnings"]:
                    response_parts.append(f"⚠️ **Warning:** {w}")
 
            if result.get("final_itinerary"):
                response_parts.append(result["final_itinerary"])
            else:
                response_parts.append(
                    "I need a bit more information. "
                    "Please tell me your destination, dates, and budget."
                )
 
            full_response = "\n\n".join(response_parts)
            st.markdown(full_response)
 
            # Show planner decision below response
            if result.get("routing_reason"):
                st.caption(f"🤖 Planner decided: {result['routing_reason']}")
 
            # Show agents that ran
            if result.get("agents_to_run"):
                agents = result["agents_to_run"]
                st.caption(f"✅ Agents ran: {' → '.join(agents)}")
 
    # Save to chat history
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": full_response
    })
 
    # Rerun to refresh sidebar immediately
    st.rerun()