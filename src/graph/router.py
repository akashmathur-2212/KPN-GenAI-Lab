from src.models.llm import setup_models

llm, _ = setup_models()

def router_node(state):
    query = state["query"]

    prompt = f"""
    You are a strict routing agent for a multi-agent system.

    Your task is to decide which specialized agent should answer the user's query.

    Agents available:
    1. annual_report - financial data, KPIs, revenue, strategy, yearly performance, official reports
    2. news - recent events, announcements, updates

    Routing Rules:
    - If the query is about financials, metrics, performance, or official reports, route to annual_report
    - If the query is about recent events, announcements, or latest updates, route to news
    - If the query mentions a specific year (e.g., 2024 report), route to annual_report
    - If the query contains words like "latest", "recent", "news", "announcement", route to news
    - If unsure, prefer news

    Output Rules:
    - Respond with ONLY one word
    - Allowed outputs: annual_report OR news
    - Do NOT explain your answer
    - Do NOT include punctuation or extra text

    Examples:
    Query: What was KPN's revenue in 2024?
    Answer: annual_report

    Query: What are the latest announcements from KPN?
    Answer: news

    Query: Tell me about KPN strategy
    Answer: annual_report

    Query: Any recent partnerships?
    Answer: news

    Now classify:

    Query: {query}
    """
    
    response = llm.invoke(prompt)

    decision = response.content.strip().lower()

    return {"route": decision}