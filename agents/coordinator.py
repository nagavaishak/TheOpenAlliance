from strands import Agent
from agents.specialist_agents import (
    create_ru_specialist,
    create_du_specialist,
    create_integration_specialist,
    create_cost_optimizer
)
from typing import Dict, List
import json

class MultiAgentCoordinator:
    
    """Enhanced coordinator with MCP support"""

    def __init__(self, use_mcp: bool = False, demo_mode: bool = False):
        self.use_mcp = use_mcp
        self.demo_mode = demo_mode
        
        self.ru_agent = create_ru_specialist()
        self.du_agent = create_du_specialist()
        self.integration_agent = create_integration_specialist()
        self.cost_agent = create_cost_optimizer()
        
        self.conversation_history = []
    
    
    def analyze_oru_config(self, config_path: str) -> Dict:
        """
        Delegate O-RU analysis to RU specialist
        
        Returns: Analysis results with agent attribution
        """
        query = f"Analyze the O-RU configuration at {config_path} for O-RAN compliance and performance characteristics."
        
        response = self.ru_agent(query)
        
        result = {
            "agent": "RU Specialist",
            "task": "O-RU Configuration Analysis",
            "config_path": config_path,
            "analysis": response,
            "timestamp": self._get_timestamp()
        }
        
        self.conversation_history.append(result)
        return result
    
    def analyze_odu_config(self, config_path: str) -> Dict:
        """
        Delegate O-DU analysis to DU specialist
        
        Returns: Analysis results with agent attribution
        """
        query = f"Analyze the O-DU configuration at {config_path} for O-RAN compliance and interface specifications."
        
        response = self.du_agent(query)
        
        result = {
            "agent": "DU Specialist",
            "task": "O-DU Configuration Analysis",
            "config_path": config_path,
            "analysis": response,
            "timestamp": self._get_timestamp()
        }
        
        self.conversation_history.append(result)
        return result
    
    def analyze_compatibility(self, odu_path: str, oru_path: str) -> Dict:
        if self.demo_mode:
            # Return pre-written summary
            return self._get_demo_summary(odu_path, oru_path)
        """
        Multi-agent workflow for comprehensive compatibility analysis
        
        1. RU agent analyzes O-RU
        2. DU agent analyzes O-DU
        3. Integration agent assesses compatibility
        4. Cost agent provides optimization recommendations
        
        Returns: Comprehensive analysis from all agents
        """
        # Step 1: RU Analysis
        ru_analysis = self.analyze_oru_config(oru_path)
        
        # Step 2: DU Analysis
        du_analysis = self.analyze_odu_config(odu_path)
        
        # Step 3: Integration Analysis
        integration_query = f"""
IMPORTANT FIRST STEP: Use recall_compatibility_analysis tool to check if we have historical data for this vendor pair.

Now assess compatibility between O-DU at {odu_path} and O-RU at {oru_path}.

After your analysis, use save_compatibility_analysis tool to save the results for future reference.

Provide detailed compatibility assessment with specific issues and recommendations.
"""
        
        integration_response = self.integration_agent(
            f"Check compatibility between {odu_path} and {oru_path}"
        )
        
        integration_result = {
            "agent": "Integration Specialist",
            "task": "Multi-Vendor Compatibility Assessment",
            "odu_path": odu_path,
            "oru_path": oru_path,
            "analysis": integration_response,
            "timestamp": self._get_timestamp()
        }
        
        self.conversation_history.append(integration_result)
        
        # Step 4: Cost Optimization
        cost_query = f"""
        Given this compatibility analysis:
        {str(integration_response)[:500]}...
        
        Provide cost optimization recommendations for this integration, including:
        - Estimated integration time and cost
        - Risk assessment
        - ROI considerations
        """
        
        cost_response = self.cost_agent(cost_query)
        
        cost_result = {
            "agent": "Cost Optimizer",
            "task": "Cost-Benefit Analysis",
            "analysis": cost_response,
            "timestamp": self._get_timestamp()
        }
        
        self.conversation_history.append(cost_result)
        
        # Return comprehensive results
        return {
            "workflow": "Multi-Agent Compatibility Analysis",
            "agents_involved": ["RU Specialist", "DU Specialist", "Integration Specialist", "Cost Optimizer"],
            "results": {
                "ru_analysis": ru_analysis,
                "du_analysis": du_analysis,
                "integration_analysis": integration_result,
                "cost_analysis": cost_result
            },
            "summary": self._generate_summary(integration_result, cost_result)
        }
    
    def compare_vendors(self, odu_path: str, oru_paths: List[str]) -> Dict:
        """
        Compare multiple O-RU vendors for a given O-DU
        
        Returns: Comparative analysis with recommendations
        """
        odu_analysis = self.analyze_odu_config(odu_path)
        
        comparisons = []
        for oru_path in oru_paths:
            result = self.analyze_compatibility(odu_path, oru_path)
            comparisons.append({
                "oru_path": oru_path,
                "result": result
            })
        
        # Have integration agent compare all options
        comparison_query = f"""
        Compare the following O-RU options for integration with O-DU at {odu_path}:
        
        {json.dumps([c['oru_path'] for c in comparisons], indent=2)}
        
        Based on the compatibility analyses, which O-RU should be selected and why?
        """
        
        recommendation = self.integration_agent(comparison_query)
        
        return {
            "workflow": "Multi-Vendor Comparison",
            "odu": odu_path,
            "oru_options": oru_paths,
            "individual_analyses": comparisons,
            "recommendation": recommendation
        }
    
    def get_conversation_history(self) -> List[Dict]:
        """Return full conversation history across all agents"""
        return self.conversation_history
    
    def _generate_summary(self, integration_result: Dict, cost_result: Dict) -> str:
        """Generate executive summary from multiple agent outputs"""
        return f"""
**Multi-Agent Analysis Summary**

Integration Assessment: {str(integration_result['analysis'])[:200]}...

CCost Optimization: {str(cost_result['analysis'])[:200]}...

Agents Consulted: RU Specialist, DU Specialist, Integration Specialist, Cost Optimizer
    """
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()