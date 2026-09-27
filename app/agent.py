from dotenv import load_dotenv

load_dotenv()


# ============================================================
# LANGCHAIN IMPORTS
# ============================================================

from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import create_agent


# ============================================================
# MCP CLIENT
# ============================================================

from app.mcp_client import call_mcp_tool_sync


# ============================================================
# MCP-BACKED TOOL 1
# ============================================================

@tool
def lookup_claim_via_mcp(claim_id: int):
    """
    Look up an insurance claim through
    the MCP server.
    """

    return call_mcp_tool_sync(
        "lookup_claim",
        {
            "claim_id": claim_id
        }
    )


# ============================================================
# MCP-BACKED TOOL 2
# ============================================================

@tool
def high_priority_claims_via_mcp():
    """
    Retrieve all high-priority insurance claims
    through the MCP server.
    """

    return call_mcp_tool_sync(
        "high_priority_claims",
        {}
    )


# ============================================================
# MCP-BACKED TOOL 3
# ============================================================

@tool
def search_insurance_policy_via_mcp(question: str):
    """
    Search the insurance policy knowledge base
    through the MCP server.
    """

    return call_mcp_tool_sync(
        "search_insurance_policy",
        {
            "question": question
        }
    )


# ============================================================
# MCP-BACKED TOOL 4
# ============================================================

@tool
def claim_analytics_via_mcp():
    """
    Calculate insurance claim analytics
    through the MCP server.
    """

    return call_mcp_tool_sync(
        "claim_analytics",
        {}
    )


# ============================================================
# LOCAL LLM
# ============================================================

model = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
    base_url="http://host.docker.internal:11434"
)


# ============================================================
# AGENT
# ============================================================

agent = create_agent(
    model=model,

    tools=[
        lookup_claim_via_mcp,
        high_priority_claims_via_mcp,
        search_insurance_policy_via_mcp,
        claim_analytics_via_mcp
    ],

    system_prompt=(
        "You are an insurance operations assistant. "

        "Use lookup_claim_via_mcp when the user asks "
        "about a specific insurance claim. "

        "Use high_priority_claims_via_mcp when the user "
        "asks for high-priority claims. "

        "Use search_insurance_policy_via_mcp when the user "
        "asks about insurance policies, claim rules, "
        "claim approval, rejection, appeals, deductibles, "
        "reporting, or other policy-related information. "

        "Use claim_analytics_via_mcp when the user asks "
        "for claim statistics, totals, averages, counts, "
        "pending claim counts, high-priority claim counts, "
        "or estimated damage calculations. "

        "Never invent claim or policy information. "

        "For policy questions, only use information returned "
        "by the MCP policy search tool. "

        "For claim questions, only use information returned "
        "by the MCP claim tools. "

        "For analytics questions, only use values returned "
        "by the MCP analytics tool. "

        "If the available MCP tools do not contain the answer, "
        "clearly say that the information is not available. "

        "Give concise and professional answers."
    )
)


# ============================================================
# FUNCTION USED BY FASTAPI
# ============================================================

def ask_agent(question: str):
    """
    Send a user question to the AI agent
    and return the final response.
    """

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    return result["messages"][-1].content