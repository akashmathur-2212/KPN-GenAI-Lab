import os
from src.models.llm import setup_models
from src.vectorstores.faiss import get_or_create_vector_store
from src.utils.pdf_parser import load_or_parse_pdf

annual_report_name = "KPN-integrated-annual-report-2024_2025"
annual_report_documents = load_or_parse_pdf(annual_report_name)

llm, embeddings = setup_models()

pdf_vector_store = get_or_create_vector_store(
    document_name=annual_report_name,
    embeddings=embeddings,
    documents=annual_report_documents,
    number_of_documents=50
)

def annual_report_agent(query, vector_store=pdf_vector_store, top_k=5):
    docs = vector_store.similarity_search(query, k=top_k)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
    You are a financial analyst assistant specialized in KPN Annual Reports.

    Your role is to answer the user's question ONLY using the provided context.

    ---------------------
    CONTEXT:
    {context}
    ---------------------

    QUESTION:
    {query}

    INSTRUCTIONS:
    - Use ONLY the information from the context above
    - Do NOT use prior knowledge
    - If the answer is not in the context, say:"I could not find this information in the annual report."
    - Be precise, factual, and concise
    - Prefer numbers, dates, and exact figures when available
    - If multiple relevant points exist, summarize clearly

    SOURCE ATTRIBUTION:
    - Always end your answer with: source = annual_report

    OUTPUT FORMAT:
    - Provide a clear, well-structured answer
    - Do NOT mention "context" or "provided text"
    - Do NOT hallucinate or guess

    EXAMPLES:

    Q: What was KPN's revenue in 2024?
    A: KPN reported a revenue of €X billion in 2024. source = annual_report

    Q: What is the CEO's favorite color?
    A: I could not find this information in the annual report. source = annual_report

    Now answer the question.

    ANSWER:
    """
    response = llm.invoke(prompt)
    
    return response.content