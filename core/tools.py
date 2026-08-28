import json
import re
from typing import Optional, List
from mcp.types import CallToolResult, TextContent, Tool
from mcp_client import MCPClient
from google.genai import types


def _sanitize_tool_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", name)


class ToolManager:
    @classmethod
    async def get_all_tools(cls, clients: dict[str, MCPClient]) -> list[types.Tool]:
        """Gets all tools from the provided clients as Gemini function declarations."""
        tools = []
        for client in clients.values():
            tool_models = await client.list_tools()
            function_declarations = [
                types.FunctionDeclaration(
                    name=_sanitize_tool_name(t.name),
                    description=t.description,
                    parameters=t.inputSchema or {
                        "type": "object",
                        "properties": {},
                    },
                )
                for t in tool_models
            ]
            if function_declarations:
                tools.append(
                    types.Tool(function_declarations=function_declarations)
                )
        return tools

    @classmethod
    async def _find_client_with_tool(
        cls, clients: list[MCPClient], tool_name: str
    ) -> Optional[MCPClient]:
        """Finds the first client that has the specified tool."""
        for client in clients:
            tools = await client.list_tools()
            tool = next(
                (
                    t
                    for t in tools
                    if t.name == tool_name
                    or _sanitize_tool_name(t.name) == tool_name
                ),
                None,
            )
            if tool:
                return client
        return None

    @classmethod
    def _build_tool_result_part(
        cls,
        tool_use_id: str,
        tool_name: str,
        text: str,
        status: str,
    ) -> dict:
        """Builds a Gemini function_response part dictionary."""
        return {
            "function_response": {
                "id": tool_use_id,
                "name": tool_name,
                "response": {
                    "content": text,
                    "is_error": status == "error",
                },
            }
        }

    @classmethod
    async def execute_tool_requests(
        cls, clients: dict[str, MCPClient], message
    ) -> List[dict]:
        """Executes a list of tool requests against the provided clients."""
        tool_requests = [
            part.function_call
            for part in message.parts
            if part.function_call is not None
        ]
        tool_result_blocks: list[dict] = []
        for tool_request in tool_requests:
            tool_use_id = tool_request.id
            tool_name = tool_request.name
            tool_input = tool_request.args or {}

            client = await cls._find_client_with_tool(
                list(clients.values()), tool_name
            )

            if not client:
                tool_result_blocks.append(
                    cls._build_tool_result_part(
                        tool_use_id, tool_name, "Could not find that tool", "error"
                    )
                )
                continue

            try:
                tool_output: CallToolResult | None = await client.call_tool(
                    tool_name, tool_input
                )
                items = []
                if tool_output:
                    items = tool_output.content
                content_list = [
                    item.text for item in items if isinstance(item, TextContent)
                ]
                content_json = json.dumps(content_list)
                tool_result_blocks.append(
                    cls._build_tool_result_part(
                        tool_use_id,
                        tool_name,
                        content_json,
                        "error"
                        if tool_output and tool_output.isError
                        else "success",
                    )
                )
            except Exception as e:
                error_message = f"Error executing tool '{tool_name}': {e}"
                print(error_message)
                tool_result_blocks.append(
                    cls._build_tool_result_part(
                        tool_use_id,
                        tool_name,
                        json.dumps({"error": error_message}),
                        "error",
                    )
                )

        return tool_result_blocks