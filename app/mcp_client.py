import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ============================================================
# MCP SERVER CONFIGURATION
# ============================================================

server_params = StdioServerParameters(
    command="python",
    args=["mcp_server.py"]
)


# ============================================================
# ASYNC MCP TOOL CALL
# ============================================================

async def call_mcp_tool(
    tool_name: str,
    arguments: dict
):
    """
    Connect to the MCP server,
    call an MCP tool,
    and return the result.
    """

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # Initialize MCP connection
            await session.initialize()

            # Call the requested MCP tool
            result = await session.call_tool(
                tool_name,
                arguments=arguments
            )

            # If the MCP tool returns structured data
            if result.structured_content:
                return result.structured_content

            # Otherwise return text content
            return {
                "content": [
                    item.text
                    for item in result.content
                    if hasattr(item, "text")
                ]
            }


# ============================================================
# SYNC WRAPPER
# ============================================================

def call_mcp_tool_sync(
    tool_name: str,
    arguments: dict
):
    """
    Synchronous wrapper around the
    asynchronous MCP client.

    This allows our LangChain agent
    to call MCP tools synchronously.
    """

    return asyncio.run(
        call_mcp_tool(
            tool_name,
            arguments
        )
    )