#!/usr/bin/env python3
"""
MCP Server for O-RAN Analysis Tools

This server exposes O-RAN configuration analysis tools via Model Context Protocol,
allowing multiple agents to discover and use these capabilities.
"""

import asyncio
import json
from typing import Any
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Import our existing tools
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.oran_tools import analyze_oran_config as _analyze_oran_config
from tools.oran_tools import check_compatibility as _check_compatibility

# Create MCP server
server = Server("oran-analysis-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available O-RAN analysis tools via MCP.
    
    Returns tools that agents can discover and invoke.
    """
    return [
        types.Tool(
            name="analyze_oran_config",
            description=(
                "Analyzes an O-RAN component configuration file (O-DU or O-RU) for "
                "O-RAN Alliance specification compliance. Returns compliance score, "
                "identified issues, warnings, and configuration summary. "
                "Checks: protocol versions, timing parameters, QoS settings, capabilities."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "config_path": {
                        "type": "string",
                        "description": "Path to the JSON configuration file (e.g., 'sample_configs/vendor_a_odu.json')"
                    }
                },
                "required": ["config_path"]
            }
        ),
        types.Tool(
            name="check_compatibility",
            description=(
                "Checks compatibility between O-DU and O-RU configurations from different vendors. "
                "Analyzes interface alignment, timing parameters, QoS settings, and capabilities. "
                "Returns compatibility score (0-100), status (COMPATIBLE/INCOMPATIBLE), "
                "specific issues, and integration recommendations."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "odu_config_path": {
                        "type": "string",
                        "description": "Path to O-DU configuration JSON file"
                    },
                    "oru_config_path": {
                        "type": "string",
                        "description": "Path to O-RU configuration JSON file"
                    }
                },
                "required": ["odu_config_path", "oru_config_path"]
            }
        ),
        types.Tool(
            name="search_oran_knowledge",
            description=(
                "Search O-RAN specifications and technical documentation in the knowledge base. "
                "Returns relevant excerpts from O-RAN Alliance specs with citations. "
                "Use for: timing requirements, protocol specifications, compliance rules, best practices."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language query about O-RAN specifications or requirements"
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Execute O-RAN analysis tools requested by agents via MCP.
    """
    
    if name == "analyze_oran_config":
        config_path = arguments.get("config_path")
        if not config_path:
            raise ValueError("config_path is required")
        
        # Call our existing tool
        result = _analyze_oran_config(config_path)
        
        return [
            types.TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]
    
    elif name == "check_compatibility":
        odu_path = arguments.get("odu_config_path")
        oru_path = arguments.get("oru_config_path")
        
        if not odu_path or not oru_path:
            raise ValueError("Both odu_config_path and oru_config_path are required")
        
        # Call our existing tool
        result = _check_compatibility(odu_path, oru_path)
        
        return [
            types.TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]
    
    elif name == "search_oran_knowledge":
        query = arguments.get("query")
        if not query:
            raise ValueError("query is required")
        
        # Import KB tool
        from tools.kb_tool import search_oran_specs
        result = search_oran_specs(query)
        
        return [
            types.TextContent(
                type="text",
                text=result
            )
        ]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    List available O-RAN configuration resources.
    
    Exposes sample configurations that agents can reference.
    """
    return [
        types.Resource(
            uri="config://vendor_a_odu",
            name="Vendor A O-DU Configuration",
            description="Sample O-DU configuration from Vendor A (Open Fronthaul 7.0)",
            mimeType="application/json"
        ),
        types.Resource(
            uri="config://vendor_b_oru",
            name="Vendor B O-RU Configuration",
            description="Sample O-RU configuration from Vendor B (Compatible with Vendor A)",
            mimeType="application/json"
        ),
        types.Resource(
            uri="config://vendor_c_oru",
            name="Vendor C O-RU Configuration",
            description="Sample O-RU configuration from Vendor C (Known compatibility issues)",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """
    Read O-RAN configuration resources.
    """
    resource_map = {
        "config://vendor_a_odu": "sample_configs/vendor_a_odu.json",
        "config://vendor_b_oru": "sample_configs/vendor_b_oru.json",
        "config://vendor_c_oru": "sample_configs/vendor_c_oru.json"
    }
    
    if uri not in resource_map:
        raise ValueError(f"Unknown resource: {uri}")
    
    file_path = resource_map[uri]
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        raise ValueError(f"Configuration file not found: {file_path}")

async def main():
    """Run the MCP server using stdio transport."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="oran-analysis-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())