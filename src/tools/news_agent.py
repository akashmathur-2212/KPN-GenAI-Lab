import os
from src.models.llm import setup_models
from src.vectorstores.faiss import get_or_create_vector_store
from src.utils.web_scraper import create_documents_from_urls

web_documents = create_documents_from_urls()

llm, embeddings = setup_models()

news_vector_store = get_or_create_vector_store(
    document_name="KPN-news-articles",
    embeddings=embeddings,
    documents=web_documents,
    number_of_documents=5
)

def news_agent(query, vector_store=news_vector_store, top_k=5):
    docs = vector_store.similarity_search(query, k=top_k)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
    You are an assistant specialized in KPN News and announcements.

    Your task is to answer the user's question ONLY using the provided news context.

    ---------------------
    CONTEXT:
    {context}
    ---------------------

    QUESTION:
    {query}

    INSTRUCTIONS:
    - Use ONLY the information from the context above
    - Do NOT use prior knowledge
    - Focus on recent events, announcements, partnerships, or updates
    - If the answer is not in the context, say: "I could not find this information in KPN news."
    - Be clear, concise, and factual
    - If multiple news items are relevant, summarize them clearly

    SOURCE ATTRIBUTION:
    - Always end your answer with: source = kpn_news

    OUTPUT FORMAT:
    - Provide a clean, well-structured answer
    - Do NOT mention "context" or "provided text"
    - Do NOT hallucinate or guess

    EXAMPLES:

    Q: What are the latest announcements from KPN?
    A: KPN recently announced [event/announcement details], highlighting [key point]. source = kpn_news

    Q: Has KPN announced any partnerships?
    A: KPN announced a partnership with [partner name], focusing on [purpose]. source = kpn_news

    Q: What is KPN’s revenue?
    A: I could not find this information in KPN news. source = kpn_news

    Now answer the question.

    ANSWER:
    """
    response = llm.invoke(prompt)

    return response.content