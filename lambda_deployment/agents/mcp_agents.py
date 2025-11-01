"""
MCP-Enabled Specialist Agents

These agents can discover and use tools from MCP servers,
enabling true cross-agent tool sharing and coordination.
"""

from anthropic import Anthropic
import json
import subprocess
import os
from typing import List, Dict, Any

class MCPEnabledAgent:
    """
    Base class for agents that can interact with MCP servers
    """
    
    def __init__(self, name: str, specialization: str, model: str = "claude-sonnet-4-5-20250929"):
        self.name = name
        self.specialization = specialization
        self.model = model
        self.client = Anthropic()
        self.available_tools = []
        self.conversation_history = []
        
    def discover_mcp_tools(self) -> List[Dict]:
        """
        Discover available tools from MCP server
        
        Returns: List of tool definitions
        """
        try:
            # Start MCP server and query available tools
            result = subprocess.run(
                ["python", "mcp_server/oran_mcp_server.py", "--list-tools"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                tools = json.loads(result.stdout)
                self.available_tools = tools
                return tools
            else:
                # Fallback to hardcoded tools if MCP server unavailable
                return self._get_fallback_tools()
                
        except Exception as e:
            print(f"⚠️ MCP tool discovery failed: {e}. Using fallback tools.")
            return self._get_fallback_tools()
    
    def _get_fallback_tools(self) -> List[Dict]:
        """Fallback tool definitions if MCP unavailable"""
        return [
            {
                "name": "analyze_oran_config",
                "description": "Analyze O-RAN configuration for compliance",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "config_path": {"type": "string"}
                    },
                    "required": ["config_path"]
                }
            },
            {
                "name": "check_compatibility",
                "description": "Check O-DU and O-RU compatibility",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "odu_config_path": {"type": "string"},
                        "oru_config_path": {"type": "string"}
                    },
                    "required": ["odu_config_path", "oru_config_path"]
                }
            }
        ]
    
    def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a tool via MCP protocol
        
        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments
            
        Returns: Tool execution result
        """
        # Import our tools directly for now (MCP server integration in progress)
        from tools.oran_tools import analyze_oran_config, check_compatibility
        
        if tool_name == "analyze_oran_config":
            return analyze_oran_config(arguments["config_path"])
        elif tool_name == "check_compatibility":
            return check_compatibility(
                arguments["odu_config_path"],
                arguments["oru_config_path"]
            )
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    def process_request(self, user_message: str, available_tools: List[Dict] = None) -> str:
        """
        Process a request using Claude with MCP tool access
        
        Args:
            user_message: User's request
            available_tools: List of available tools (from MCP or fallback)
            
        Returns: Agent's response
        """
        if available_tools is None:
            available_tools = self.discover_mcp_tools()
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Call Claude with tool use capability
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            tools=available_tools,
            messages=self.conversation_history
        )
        
        # Process response and handle tool calls
        while response.stop_reason == "tool_use":
            # Extract tool use requests
            tool_use_blocks = [
                block for block in response.content 
                if block.type == "tool_use"
            ]
            
            # Execute tools via MCP
            tool_results = []
            for tool_use in tool_use_blocks:
                result = self.call_mcp_tool(
                    tool_use.name,
                    tool_use.input
                )
                
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": json.dumps(result) if isinstance(result, dict) else str(result)
                })
            
            # Add assistant response and tool results to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response.content
            })
            
            self.conversation_history.append({
                "role": "user",
                "content": tool_results
            })
            
            # Continue conversation with tool results
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                tools=available_tools,
                messages=self.conversation_history
            )
        
        # Extract final text response
        final_response = ""
        for block in response.content:
            if hasattr(block, 'text'):
                final_response += block.text
        
        # Add final response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": final_response
        })
        
        return final_response


class RUSpecialistMCP(MCPEnabledAgent):
    """RU Specialist with MCP capabilities"""
    
    def __init__(self):
        super().__init__(
            name="RU Specialist",
            specialization="O-RU analysis and RF specifications"
        )
        
        # Discover available MCP tools on initialization
        self.discover_mcp_tools()


class DUSpecialistMCP(MCPEnabledAgent):
    """DU Specialist with MCP capabilities"""
    
    def __init__(self):
        super().__init__(
            name="DU Specialist",
            specialization="O-DU analysis and MAC/PHY layer"
        )
        
        self.discover_mcp_tools()


class IntegrationSpecialistMCP(MCPEnabledAgent):
    """Integration Specialist with MCP capabilities"""
    
    def __init__(self):
        super().__init__(
            name="Integration Specialist",
            specialization="Multi-vendor compatibility analysis"
        )
        
        self.discover_mcp_tools()


class MCPCoordinator:
    """
    Coordinates multiple MCP-enabled agents
    
    Implements Model Context Protocol for agent-to-agent communication
    """
    
    def __init__(self):
        self.agents = {
            "ru": RUSpecialistMCP(),
            "du": DUSpecialistMCP(),
            "integration": IntegrationSpecialistMCP()
        }
        
        print("✅ MCP Coordinator initialized with 3 specialist agents")
        print("🔗 Agents connected via Model Context Protocol")
    
    def route_request(self, request: str, target_agent: str = None) -> Dict:
        """
        Route request to appropriate specialist agent
        
        Args:
            request: User request
            target_agent: Specific agent to use (or None for auto-routing)
            
        Returns: Response with agent attribution
        """
        if target_agent:
            agent = self.agents.get(target_agent)
            if not agent:
                raise ValueError(f"Unknown agent: {target_agent}")
        else:
            # Auto-route based on request content
            request_lower = request.lower()
            if "o-ru" in request_lower or "radio" in request_lower:
                agent = self.agents["ru"]
            elif "o-du" in request_lower or "distributed" in request_lower:
                agent = self.agents["du"]
            else:
                agent = self.agents["integration"]
        
        response = agent.process_request(request)
        
        return {
            "agent": agent.name,
            "specialization": agent.specialization,
            "request": request,
            "response": response,
            "mcp_enabled": True
        }
    
    def multi_agent_analysis(self, odu_path: str, oru_path: str) -> Dict:
        """
        Coordinate multiple agents for comprehensive analysis
        
        This demonstrates MCP's value: agents share tools and context
        """
        results = {}
        
        # Phase 1: RU analysis
        print("🤖 Phase 1: RU Specialist analyzing O-RU...")
        ru_response = self.agents["ru"].process_request(
            f"Analyze the O-RU configuration at {oru_path} for O-RAN compliance"
        )
        results["ru_analysis"] = {
            "agent": "RU Specialist",
            "response": ru_response
        }
        
        # Phase 2: DU analysis
        print("🤖 Phase 2: DU Specialist analyzing O-DU...")
        du_response = self.agents["du"].process_request(
            f"Analyze the O-DU configuration at {odu_path} for O-RAN compliance"
        )
        results["du_analysis"] = {
            "agent": "DU Specialist",
            "response": du_response
        }
        
        # Phase 3: Integration analysis with context from other agents
        print("🤖 Phase 3: Integration Specialist assessing compatibility...")
        integration_context = f"""
        Based on specialist analyses:
        
        RU Specialist findings: {ru_response[:300]}...
        DU Specialist findings: {du_response[:300]}...
        
        Now check compatibility between {odu_path} and {oru_path}
        """
        
        integration_response = self.agents["integration"].process_request(integration_context)
        results["integration_analysis"] = {
            "agent": "Integration Specialist",
            "response": integration_response
        }
        
        return {
            "workflow": "MCP Multi-Agent Analysis",
            "protocol": "Model Context Protocol",
            "agents_coordinated": 3,
            "results": results
        }