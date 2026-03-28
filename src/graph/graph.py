from langgraph.graph import StateGraph, END
from src.graph.state import AgentState
from src.graph.router import router_node
from src.graph.nodes import annual_report_node, news_node

def build_graph():

    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("router", router_node)
    graph.add_node("annual_report", annual_report_node)
    graph.add_node("news", news_node)

    # Entry point
    graph.set_entry_point("router")

    # Conditional routing
    def route_decision(state):
        return state["route"]

    graph.add_conditional_edges(
        "router",
        route_decision,
        {
            "annual_report": "annual_report",
            "news": "news"
        }
    )

    # End after agent response
    graph.add_edge("annual_report", END)
    graph.add_edge("news", END)

    return graph.compile()

app = build_graph()