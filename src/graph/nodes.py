from src.tools.annual_report_agent import annual_report_agent
from src.tools.news_agent import news_agent

def annual_report_node(state):
    query = state["query"]
    answer = annual_report_agent(query)

    return {"answer": answer}

def news_node(state):
    query = state["query"]
    answer = news_agent(query)

    return {"answer": answer}