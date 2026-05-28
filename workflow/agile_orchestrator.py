"""Agile Workflow Orchestrator - coordinates agent workflow in agile fashion"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class WorkflowState(Enum):
    """Workflow states"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkflowPhase(Enum):
    """Workflow phases"""
    INITIALIZATION = "initialization"
    RESEARCH = "research"
    CONTENT_CREATION = "content_creation"
    ANALYSIS = "analysis"
    DESIGN = "design"
    ITERATION = "iteration"
    FINALIZATION = "finalization"


@dataclass
class AgentTask:
    """Task assigned to an agent"""
    agent_type: str
    task_description: str
    input_data: Dict[str, Any]
    priority: str = "medium"
    status: str = "pending"
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class WorkflowResult:
    """Result from workflow execution"""
    success: bool
    final_pitch_deck: Optional[Dict[str, Any]] = None
    design: Optional[Dict[str, Any]] = None
    research_data: Optional[Dict[str, Any]] = None
    quality_score: Optional[float] = None
    iterations: int = 0
    total_duration: Optional[float] = None
    errors: List[str] = field(default_factory=list)


class AgileOrchestrator:
    """Orchestrates agile workflow across multiple agents"""
    
    def __init__(self, agents: Dict[str, Any]):
        self.agents = agents
        self.state = WorkflowState.IDLE
        self.current_phase = WorkflowPhase.INITIALIZATION
        self.current_request: Optional[Dict[str, Any]] = None
        self.workflow_history: List[Dict[str, Any]] = []
        self.task_queue: List[AgentTask] = []
        self.iteration_count = 0
        self.max_iterations = 3
        self.workflow_start_time: Optional[datetime] = None
        
    def initialize_workflow(self, customer_request: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize workflow with customer request"""
        try:
            self.current_request = customer_request
            self.state = WorkflowState.RUNNING
            self.current_phase = WorkflowPhase.INITIALIZATION
            self.workflow_start_time = datetime.now()
            self.iteration_count = 0
            
            # Log initialization
            self._log_workflow_event("workflow_initialized", {
                "customer_id": customer_request.get("customer_id"),
                "request_type": customer_request.get("request_type")
            })
            
            return {
                "success": True,
                "message": "Workflow initialized successfully",
                "workflow_id": self._generate_workflow_id()
            }
        except Exception as e:
            self.state = WorkflowState.FAILED
            return {
                "success": False,
                "error": str(e)
            }
    
    def execute_research_phase(
        self,
        query: str,
        focus_areas: List[str]
    ) -> Dict[str, Any]:
        """Execute research phase using Research Agent"""
        try:
            self.current_phase = WorkflowPhase.RESEARCH
            
            research_agent = self.agents.get("research")
            if not research_agent:
                raise ValueError("Research agent not available")
            
            research_data = research_agent.conduct_market_research(
                query=query,
                focus_areas=focus_areas,
                target_audience=self.current_request.get("target_audience", "general")
            )
            
            self._log_workflow_event("research_completed", {
                "query": query,
                "focus_areas": focus_areas
            })
            
            return {
                "success": True,
                "research_data": research_data,
                "phase": "research"
            }
        except Exception as e:
            self._log_workflow_event("research_failed", {"error": str(e)})
            return {
                "success": False,
                "error": str(e),
                "phase": "research"
            }
    
    def execute_content_phase(
        self,
        research_data: Dict[str, Any],
        requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute content creation phase using Content Agent"""
        try:
            self.current_phase = WorkflowPhase.CONTENT_CREATION
            
            content_agent = self.agents.get("content")
            if not content_agent:
                raise ValueError("Content agent not available")
            
            pitch_deck = content_agent.create_pitch_deck(
                topic=self.current_request.get("topic"),
                research_data=research_data,
                requirements=requirements
            )
            
            self._log_workflow_event("content_created", {
                "topic": self.current_request.get("topic"),
                "slide_count": len(pitch_deck.get("slides", []))
            })
            
            return {
                "success": True,
                "pitch_deck": pitch_deck,
                "phase": "content_creation"
            }
        except Exception as e:
            self._log_workflow_event("content_creation_failed", {"error": str(e)})
            return {
                "success": False,
                "error": str(e),
                "phase": "content_creation"
            }
    
    def execute_analysis_phase(
        self,
        pitch_deck: Dict[str, Any],
        checklist: Dict[str, Any],
        threshold: float = 0.8
    ) -> Dict[str, Any]:
        """Execute analysis phase using Analyst Agent"""
        try:
            self.current_phase = WorkflowPhase.ANALYSIS
            
            analyst_agent = self.agents.get("analyst")
            if not analyst_agent:
                raise ValueError("Analyst agent not available")
            
            analysis_result = analyst_agent.analyze_pitch_deck_quality(
                pitch_deck=pitch_deck,
                checklist=checklist
            )
            
            passes_threshold = analysis_result.passes_threshold(threshold)
            
            self._log_workflow_event("analysis_completed", {
                "overall_score": analysis_result.overall_score,
                "passes_threshold": passes_threshold
            })
            
            return {
                "success": True,
                "analysis_result": analysis_result,
                "passes_threshold": passes_threshold,
                "phase": "analysis"
            }
        except Exception as e:
            self._log_workflow_event("analysis_failed", {"error": str(e)})
            return {
                "success": False,
                "error": str(e),
                "phase": "analysis"
            }
    
    def execute_design_phase(
        self,
        pitch_deck: Dict[str, Any],
        requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute design phase using Design Agent"""
        try:
            self.current_phase = WorkflowPhase.DESIGN
            
            design_agent = self.agents.get("design")
            if not design_agent:
                raise ValueError("Design agent not available")
            
            design_result = design_agent.create_visual_design(
                pitch_deck=pitch_deck,
                requirements=requirements
            )
            
            self._log_workflow_event("design_completed", {
                "design_system": design_result.design_system
            })
            
            return {
                "success": True,
                "design_result": design_result,
                "phase": "design"
            }
        except Exception as e:
            self._log_workflow_event("design_failed", {"error": str(e)})
            return {
                "success": False,
                "error": str(e),
                "phase": "design"
            }
    
    def execute_iteration_cycle(
        self,
        pitch_deck: Dict[str, Any],
        feedback: List[str],
        checklist: Dict[str, Any],
        threshold: float = 0.85
    ) -> Dict[str, Any]:
        """Execute iteration cycle for improvements"""
        try:
            if self.iteration_count >= self.max_iterations:
                return {
                    "success": False,
                    "error": "Max iterations reached",
                    "iteration_count": self.iteration_count
                }
            
            self.current_phase = WorkflowPhase.ITERATION
            self.iteration_count += 1
            
            # Improve content based on feedback
            content_agent = self.agents.get("content")
            if not content_agent:
                raise ValueError("Content agent not available")
            
            improved_pitch_deck = content_agent.improve_pitch_deck(
                pitch_deck=pitch_deck,
                feedback=feedback
            )
            
            # Re-analyze improved version
            analyst_agent = self.agents.get("analyst")
            if not analyst_agent:
                raise ValueError("Analyst agent not available")
            
            new_analysis = analyst_agent.analyze_pitch_deck_quality(
                pitch_deck=improved_pitch_deck,
                checklist=checklist
            )
            
            self._log_workflow_event("iteration_completed", {
                "iteration": self.iteration_count,
                "new_score": new_analysis.overall_score
            })
            
            return {
                "success": True,
                "improved_pitch_deck": improved_pitch_deck,
                "new_score": new_analysis.overall_score,
                "passes_threshold": new_analysis.passes_threshold(threshold),
                "iteration_count": self.iteration_count,
                "phase": "iteration"
            }
        except Exception as e:
            self._log_workflow_event("iteration_failed", {
                "error": str(e),
                "iteration": self.iteration_count
            })
            return {
                "success": False,
                "error": str(e),
                "iteration_count": self.iteration_count,
                "phase": "iteration"
            }
    
    def execute_full_workflow(
        self,
        customer_request: Dict[str, Any],
        checklist: Dict[str, Any],
        quality_threshold: float = 0.8
    ) -> WorkflowResult:
        """Execute complete agile workflow"""
        try:
            # Initialize
            init_result = self.initialize_workflow(customer_request)
            if not init_result["success"]:
                return WorkflowResult(success=False, errors=[init_result["error"]])
            
            # CEO analysis
            ceo_agent = self.agents.get("ceo")
            if ceo_agent:
                ceo_analysis = ceo_agent.analyze_customer_request(customer_request)
                customer_request.update(ceo_analysis.get("requirements", {}))
            
            # Research phase
            research_result = self.execute_research_phase(
                query=customer_request.get("topic", ""),
                focus_areas=customer_request.get("requirements", {}).get("focus", ["market", "competitors"])
            )
            if not research_result["success"]:
                return WorkflowResult(success=False, errors=[research_result["error"]])
            
            # Content creation
            content_result = self.execute_content_phase(
                research_data=research_result["research_data"],
                requirements=customer_request.get("requirements", {})
            )
            if not content_result["success"]:
                return WorkflowResult(success=False, errors=[content_result["error"]])
            
            current_pitch_deck = content_result["pitch_deck"]
            
            # Analysis and iteration loop
            for iteration in range(self.max_iterations + 1):
                analysis_result = self.execute_analysis_phase(
                    pitch_deck=current_pitch_deck,
                    checklist=checklist,
                    threshold=quality_threshold
                )
                
                if not analysis_result["success"]:
                    return WorkflowResult(success=False, errors=[analysis_result["error"]])
                
                if analysis_result["passes_threshold"]:
                    break
                
                if iteration < self.max_iterations:
                    feedback = analysis_result["analysis_result"].improvement_suggestions
                    iteration_result = self.execute_iteration_cycle(
                        pitch_deck=current_pitch_deck,
                        feedback=feedback,
                        checklist=checklist,
                        threshold=quality_threshold
                    )
                    
                    if iteration_result["success"]:
                        current_pitch_deck = iteration_result["improved_pitch_deck"]
                    else:
                        break
            
            # Design phase
            design_result = self.execute_design_phase(
                pitch_deck=current_pitch_deck,
                requirements=customer_request.get("requirements", {})
            )
            
            # Final CEO evaluation
            final_score = 0.0
            if ceo_agent:
                ceo_evaluation = ceo_agent.evaluate_true_north_compliance(
                    content=current_pitch_deck,
                    checklist=checklist
                )
                final_score = ceo_evaluation.get("score", 0.0)
            
            # Complete workflow
            self.state = WorkflowState.COMPLETED
            self.current_phase = WorkflowPhase.FINALIZATION
            
            duration = (datetime.now() - self.workflow_start_time).total_seconds() if self.workflow_start_time else None
            
            self._log_workflow_event("workflow_completed", {
                "duration": duration,
                "iterations": self.iteration_count,
                "final_score": final_score
            })
            
            return WorkflowResult(
                success=True,
                final_pitch_deck=current_pitch_deck,
                design=design_result.get("design_result") if design_result["success"] else None,
                research_data=research_result["research_data"],
                quality_score=final_score,
                iterations=self.iteration_count,
                total_duration=duration
            )
            
        except Exception as e:
            self.state = WorkflowState.FAILED
            return WorkflowResult(success=False, errors=[str(e)])
    
    def pause_workflow(self) -> Dict[str, Any]:
        """Pause workflow execution"""
        if self.state == WorkflowState.RUNNING:
            self.state = WorkflowState.PAUSED
            self._log_workflow_event("workflow_paused", {})
            return {"success": True, "message": "Workflow paused"}
        return {"success": False, "error": "Workflow not running"}
    
    def resume_workflow(self) -> Dict[str, Any]:
        """Resume paused workflow"""
        if self.state == WorkflowState.PAUSED:
            self.state = WorkflowState.RUNNING
            self._log_workflow_event("workflow_resumed", {})
            return {"success": True, "message": "Workflow resumed"}
        return {"success": False, "error": "Workflow not paused"}
    
    def reset_workflow(self) -> Dict[str, Any]:
        """Reset workflow to initial state"""
        self.state = WorkflowState.IDLE
        self.current_phase = WorkflowPhase.INITIALIZATION
        self.current_request = None
        self.iteration_count = 0
        self.task_queue = []
        self.workflow_start_time = None
        
        self._log_workflow_event("workflow_reset", {})
        return {"success": True, "message": "Workflow reset"}
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status"""
        progress = 0.0
        if self.state == WorkflowState.COMPLETED:
            progress = 1.0
        elif self.state == WorkflowState.RUNNING:
            phase_order = [
                WorkflowPhase.INITIALIZATION,
                WorkflowPhase.RESEARCH,
                WorkflowPhase.CONTENT_CREATION,
                WorkflowPhase.ANALYSIS,
                WorkflowPhase.DESIGN,
                WorkflowPhase.FINALIZATION
            ]
            try:
                current_index = phase_order.index(self.current_phase)
                progress = (current_index + 1) / len(phase_order)
            except ValueError:
                progress = 0.0
        
        return {
            "state": self.state.value,
            "current_phase": self.current_phase.value,
            "progress": progress,
            "iteration_count": self.iteration_count,
            "workflow_id": self._generate_workflow_id(),
            "start_time": self.workflow_start_time.isoformat() if self.workflow_start_time else None
        }
    
    def _generate_workflow_id(self) -> str:
        """Generate unique workflow ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"workflow_{timestamp}"
    
    def _log_workflow_event(self, event_type: str, data: Dict[str, Any]):
        """Log workflow event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "phase": self.current_phase.value,
            "state": self.state.value,
            "data": data
        }
        self.workflow_history.append(event)


if __name__ == "__main__":
    # Quick test
    from agents.ceo_orchestrator_agent import CEOOrchestratorAgent
    from agents.content_agent import ContentAgent
    from agents.analyst_agent import AnalystAgent
    from agents.research_agent import ResearchAgent
    from agents.design_agent import DesignAgent
    
    # Create mock agents
    mock_agents = {
        "ceo": CEOOrchestratorAgent(),
        "content": ContentAgent(),
        "analyst": AnalystAgent(),
        "research": ResearchAgent(),
        "design": DesignAgent()
    }
    
    orchestrator = AgileOrchestrator(agents=mock_agents)
    
    test_request = {
        "customer_id": "test_123",
        "request_type": "pitch_deck",
        "topic": "AI productivity tool",
        "target_audience": "investors"
    }
    
    status = orchestrator.get_workflow_status()
    print(f"Workflow status: {status}")
