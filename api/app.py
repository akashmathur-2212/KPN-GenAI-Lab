from fastapi import FastAPI
from pydantic import BaseModel
from src.graph.graph import app

# Initialize FastAPI
api = FastAPI(
    title="KPN Multi-Agent AI System",
    description="Routes queries to Annual Report or News agents",
    version="1.0.0"
)

# Request schema
class QueryRequest(BaseModel):
    query: str

# Response schema
class QueryResponse(BaseModel):
    answer: str
    
# Health check
@api.get("/health")
def health():
    return {"status": "ok"}


# Main endpoint
@api.post("/query", response_model=QueryResponse)
def query_agent(request: QueryRequest):

    result = app.invoke({
        "query": request.query,
        "route": "",
        "answer": ""
    })

    return {
        "answer": result["answer"],
    }