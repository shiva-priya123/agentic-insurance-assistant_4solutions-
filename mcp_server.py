from mcp.server import MCPServer

from app.tools.claims_tool import (
    get_claim,
    get_high_priority_claims
)

from app.tools.policy_tool import search_policy

from app.tools.analytics_tool import get_claim_analytics


# ============================================================
# CREATE MCP SERVER
# ============================================================

mcp = MCPServer(
    "Insurance Operations MCP Server"
)


# ============================================================
# MCP TOOL 1: CLAIM LOOKUP
# ============================================================

@mcp.tool()
def lookup_claim(claim_id: int):
    """
    Look up an insurance claim by claim ID.
    """
    return get_claim(claim_id)


# ============================================================
# MCP TOOL 2: HIGH-PRIORITY CLAIMS
# ============================================================

@mcp.tool()
def high_priority_claims():
    """
    Return all high-priority insurance claims.
    """
    return get_high_priority_claims()


# ============================================================
# MCP TOOL 3: POLICY SEARCH
# ============================================================

@mcp.tool()
def search_insurance_policy(question: str):
    """
    Search the insurance policy knowledge base.
    """
    return search_policy(question)


# ============================================================
# MCP TOOL 4: CLAIM ANALYTICS
# ============================================================

@mcp.tool()
def claim_analytics():
    """
    Calculate summary analytics across insurance claims.
    """
    return get_claim_analytics()


# ============================================================
# START MCP SERVER
# ============================================================

if __name__ == "__main__":
    mcp.run()