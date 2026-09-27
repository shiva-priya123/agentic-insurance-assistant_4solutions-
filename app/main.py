from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.tools.claims_tool import (
    get_claim,
    get_high_priority_claims
)

from app.agent import ask_agent


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Agentic Insurance Operations Assistant",
    version="1.0.0"
)


# ============================================================
# CORS
# Allow React frontend to communicate with FastAPI
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Agentic Insurance Assistant is running!"
    }


# ============================================================
# HIGH-PRIORITY CLAIMS
# IMPORTANT: Keep this BEFORE /claims/{claim_id}
# ============================================================

@app.get("/claims/high-priority")
def high_priority_claims():
    return get_high_priority_claims()


# ============================================================
# INDIVIDUAL CLAIM LOOKUP
# ============================================================

@app.get("/claims/{claim_id}")
def claim_lookup(claim_id: int):
    return get_claim(claim_id)


# ============================================================
# AGENT REQUEST MODEL
# ============================================================

class AgentRequest(BaseModel):
    question: str


# ============================================================
# AI AGENT ENDPOINT
# ============================================================

@app.post("/agent")
def run_agent(request: AgentRequest):
    answer = ask_agent(request.question)

    return {
        "question": request.question,
        "answer": answer
    }