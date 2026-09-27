import asyncio

from mcp_server import mcp


async def main():
    print("MCP server loaded successfully")

    tools = await mcp.list_tools()

    print("Registered MCP tools:")

    for tool in tools:
        print(f"- {tool.name}")


if __name__ == "__main__":
    asyncio.run(main())