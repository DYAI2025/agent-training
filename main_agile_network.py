"""Main Application Entry Point for WUPHF Agile Agent Network

This module provides the main entry point for the WUPHF Agile Agent Network,
coordinating all agents, workflow orchestration, and learning memory.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import os

# Import agents
from agents.ceo_orchestrator_agent import CEOOrchestratorAgent, Task
from agents.content_agent import ContentAgent
from agents.analyst_agent import AnalystAgent
from agents.research_agent import ResearchAgent
from agents.design_agent import DesignAgent

# Import workflow
from workflow.agile_orchestrator import AgileOrchestrator

# Import memory
from memory.learning_memory import LearningMemory, MemoryEntry, MemoryType


class WUPHFAgileNetwork:
    """Main WUPHF Agile Agent Network application"""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize the WUPHF Agile Agent Network
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
        # Initialize agents
        self.agents = self._initialize_agents()
        
        # Initialize workflow orchestrator
        self.orchestrator = AgileOrchestrator(agents=self.agents)
        
        # Initialize learning memory
        memory_dir = self.config.get("memory_dir", "memory/storage")
        self.memory = LearningMemory(memory_dir=memory_dir)
        
        # Load True North checklist
        self.true_north_checklist = self._load_true_north_checklist()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all agents based on configuration"""
        agents = {}
        
        # Initialize CEO/Orchestrator Agent
        ceo_config = self.config.get("ceo_agent", {})
        
        # Get API key from environment or config
        openrouter_api_key = os.environ.get(
            "OPENROUTER_API_KEY",
            ceo_config.get("environment_variables", {}).get("openrouter_api_key", "")
        )
        
        # Only initialize CEO agent if API key is available and not empty
        if openrouter_api_key and openrouter_api_key.strip():
            print(f"=== DIAGNOSTIC: Using real CEO agent with OpenRouter API ===")
            agents["ceo"] = CEOOrchestratorAgent(
                openrouter_api_key=openrouter_api_key,
                model=ceo_config.get("model", "nvidia/nemotron-120b"),
                api_url=ceo_config.get("api_url", "https://openrouter.ai/api/v1/chat/completions")
            )
        else:
            print(f"=== DIAGNOSTIC: Using Mock CEO agent (no API key) ===")
            # Create a mock CEO agent for testing without API key
            agents["ceo"] = MockCEOAgent()
        
        # Initialize specialized agents
        specialized_config = self.config.get("specialized_agents", {})
        
        # Content Agent
        if "content_agent" in specialized_config:
            content_config = specialized_config["content_agent"]
            agents["content"] = ContentAgent(
                model=content_config.get("model", "pitchdeck-2026:latest")
            )
        
        # Research Agent
        if "research_agent" in specialized_config:
            research_config = specialized_config["research_agent"]
            agents["research"] = ResearchAgent(
                model=research_config.get("model", "qwen2.5:7b")
            )
        
        # Analyst Agent
        if "analyst_agent" in specialized_config:
            analyst_config = specialized_config["analyst_agent"]
            agents["analyst"] = AnalystAgent(
                model=analyst_config.get("model", "gemma4:e4b")
            )
        
        # Design Agent
        if "design_agent" in specialized_config:
            design_config = specialized_config["design_agent"]
            agents["design"] = DesignAgent(
                model=design_config.get("model", "llama3.2:latest")
            )
        
        return agents
    
    def _load_true_north_checklist(self) -> Dict[str, Any]:
        """Load True North checklist for quality assurance"""
        checklist_path = Path(".wuphf/knowledge_base/semantic/true_north_pitch_deck_checklist.md")
        
        if checklist_path.exists():
            # For now, return a basic structure
            # In production, this would parse the markdown file
            return {
                "criteria": [
                    {
                        "id": "structure",
                        "category": "Structure",
                        "description": "Clear problem statement and solution",
                        "weight": 0.3
                    },
                    {
                        "id": "content",
                        "category": "Content",
                        "description": "Quantified market size and traction",
                        "weight": 0.4
                    },
                    {
                        "id": "design",
                        "category": "Design",
                        "description": "Visual consistency and professionalism",
                        "weight": 0.3
                    }
                ]
            }
        else:
            return {"criteria": []}
    
    def process_customer_request(
        self,
        customer_request: Dict[str, Any],
        quality_threshold: Optional[float] = None
    ) -> Dict[str, Any]:
        """Process a customer request through the agile agent network
        
        Args:
            customer_request: Customer request details
            quality_threshold: Quality threshold for QA (default from config)
            
        Returns:
            Dictionary containing workflow results
        """
        print(f"=== DIAGNOSTIC [main_agile_network]: process_customer_request called ===")
        print(f"Input customer_request type: {type(customer_request)}")
        print(f"Input customer_request: {customer_request}")
        print(f"Input quality_threshold: {quality_threshold}")
        
        # Get quality threshold from config if not provided
        if quality_threshold is None:
            workflow_config = self.config.get("workflow", {})
            agile_config = workflow_config.get("agile_orchestrator", {})
            quality_threshold = agile_config.get("quality_threshold", 0.8)
            print(f"=== DIAGNOSTIC: Quality threshold from config: {quality_threshold} ===")
        
        # Log the request to memory
        self._log_request(customer_request)
        
        try:
            print(f"=== DIAGNOSTIC: Calling orchestrator.execute_full_workflow ===")
            # Execute full workflow
            result = self.orchestrator.execute_full_workflow(
                customer_request=customer_request,
                checklist=self.true_north_checklist,
                quality_threshold=quality_threshold
            )
            
            print(f"=== DIAGNOSTIC: Workflow result received ===")
            print(f"Result type: {type(result)}")
            print(f"Result success: {result.success}")
            print(f"Result errors: {result.errors}")
            
            # Log the result to memory
            self._log_result(customer_request, result)
            
            # Apply learning from this execution
            self._apply_learning()
            
            return {
                "success": result.success,
                "final_pitch_deck": result.final_pitch_deck,
                "design": result.design,
                "research_data": result.research_data,
                "quality_score": result.quality_score,
                "iterations": result.iterations,
                "total_duration": result.total_duration,
                "errors": result.errors
            }
            
        except Exception as e:
            print(f"=== DIAGNOSTIC [main_agile_network]: Exception in process_customer_request ===")
            print(f"Error type: {type(e)}")
            print(f"Error message: {str(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            
            # Log failure to memory
            self._log_failure(customer_request, str(e))
            
            return {
                "success": False,
                "error": str(e),
                "errors": [str(e)]
            }
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get current status of the agent network"""
        workflow_status = self.orchestrator.get_workflow_status()
        
        # Get agent performance summaries
        agent_performance = {}
        for agent_name, agent in self.agents.items():
            if agent_name != "ceo":  # Skip CEO for performance tracking
                performance = self.memory.get_agent_performance_summary(agent_name)
                agent_performance[agent_name] = performance
        
        # Get learning insights
        insights = self.memory.get_learning_insights()
        
        return {
            "workflow_status": workflow_status,
            "agent_performance": agent_performance,
            "learning_insights": [
                {
                    "type": insight.insight_type,
                    "description": insight.description,
                    "recommendation": insight.actionable_recommendation,
                    "confidence": insight.confidence
                }
                for insight in insights
            ],
            "config": {
                "network_name": self.config.get("agent_network", {}).get("name"),
                "version": self.config.get("agent_network", {}).get("version")
            }
        }
    
    def _log_request(self, customer_request: Dict[str, Any]):
        """Log customer request to memory"""
        entry = MemoryEntry(
            entry_type=MemoryType.SUCCESS,
            agent_type="network",
            task_description=f"Process request: {customer_request.get('request_type', 'unknown')}",
            outcome="Request received",
            quality_score=0.0,
            metadata={"customer_request": customer_request}
        )
        self.memory.store_entry(entry)
    
    def _log_result(self, customer_request: Dict[str, Any], result):
        """Log workflow result to memory"""
        entry_type = MemoryType.SUCCESS if result.success else MemoryType.FAILURE
        
        entry = MemoryEntry(
            entry_type=entry_type,
            agent_type="network",
            task_description=f"Completed request: {customer_request.get('request_type', 'unknown')}",
            outcome="Success" if result.success else "Failed",
            quality_score=result.quality_score if result.success else 0.0,
            metadata={
                "iterations": result.iterations,
                "duration": result.total_duration,
                "customer_request": customer_request
            }
        )
        self.memory.store_entry(entry)
    
    def _log_failure(self, customer_request: Dict[str, Any], error: str):
        """Log workflow failure to memory"""
        entry = MemoryEntry(
            entry_type=MemoryType.FAILURE,
            agent_type="network",
            task_description=f"Failed request: {customer_request.get('request_type', 'unknown')}",
            outcome="Error",
            quality_score=0.0,
            metadata={
                "error": error,
                "customer_request": customer_request
            }
        )
        self.memory.store_entry(entry)
    
    def _apply_learning(self):
        """Apply learning from recent executions"""
        # Detect patterns
        patterns = self.memory.detect_patterns()
        
        # Get insights
        insights = self.memory.get_learning_insights()
        
        # In a full implementation, this would adjust agent behavior
        # based on patterns and insights
        pass


class MockCEOAgent:
    """Mock CEO Agent for testing without API key"""
    
    def __init__(self):
        self.model = "mock_ceo"
    
    def analyze_customer_request(self, request: Dict[str, Any], context: str = None) -> Dict[str, Any]:
        """Mock customer request analysis"""
        # Handle both string and dict inputs
        if isinstance(request, str):
            request_type = "pitch_deck"
        else:
            request_type = request.get("request_type", "pitch_deck")
        
        return {
            "task_type": request_type,
            "priority": "medium",
            "requirements": {
                "style": "modern",
                "focus": ["problem", "solution", "market"]
            }
        }
    
    def delegate_task(self, task: Task, agent_type: str) -> Dict[str, Any]:
        """Mock task delegation"""
        return {
            "success": True,
            "assigned_agent": agent_type,
            "task_id": task.id
        }
    
    def evaluate_true_north_compliance(
        self,
        content: Dict[str, Any],
        checklist: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Mock True North compliance evaluation"""
        return {
            "compliant": True,
            "score": 0.85,
            "gaps": []
        }
    
    def integrate_learning(self, insights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Mock learning integration"""
        return {
            "success": True,
            "integrated_insights": len(insights)
        }


def main():
    """Main entry point for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="WUPHF Agile Agent Network - Multi-agent orchestration system"
    )
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show network status"
    )
    parser.add_argument(
        "--request",
        help="Process a customer request (JSON string)"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize network
        network = WUPHFAgileNetwork(config_path=args.config)
        
        if args.status:
            # Show network status
            status = network.get_network_status()
            print(json.dumps(status, indent=2))
        elif args.request:
            # Process customer request
            try:
                customer_request = json.loads(args.request)
                result = network.process_customer_request(customer_request)
                print(json.dumps(result, indent=2))
            except json.JSONDecodeError:
                print("Error: Invalid JSON in request", file=sys.stderr)
                sys.exit(1)
        else:
            # Show help
            parser.print_help()
            sys.exit(0)
            
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
