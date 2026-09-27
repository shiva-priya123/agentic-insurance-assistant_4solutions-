import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import TextContent


server_params = StdioServerParameters(
    command="python",
    args=["mcp_server.py"]
)


async def call_mcp_tool(tool_name: str, arguments: dict):
    """
    Connect to the MCP server and call a specific tool.
    """

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                tool_name,
                arguments=arguments
            )

            if result.is_error:
                return {
                    "error": True,
                    "content": [
                        block.text
                        for block in result.content
                        if isinstance(block, TextContent)
                    ]
                }

            if result.structured_content:
                return result.structured_content

            return {
                "content": [
                    block.text
                    for block in result.content
                    if isinstance(block, TextContent)
                ]
            }


async def main():

    print("Calling MCP tool...")

    result = await call_mcp_tool(
        "lookup_claim",
        {
            "claim_id": 1001
        }
    )

    print("\nMCP tool result:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())