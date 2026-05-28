"""Tests for Agile Workflow Orchestrator - coordinates agent workflow"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from workflow.agile_orchestrator import (
    AgileOrchestrator, 
    WorkflowState, 
    WorkflowPhase, 
    AgentTask,
    WorkflowResult
)


@pytest.fixture
def mock_agents():
    """Create mock agents"""
    return {
        "ceo": Mock(),
        "content": Mock(),
        "analyst": Mock(),
        "research": Mock(),
        "design": Mock()
    }


@pytest.fixture
def agile_orchestrator(mock_agents):
    """Create AgileOrchestrator instance with mock agents"""
    orchestrator = AgileOrchestrator(agents=mock_agents)
    return orchestrator


@pytest.fixture
def sample_customer_request():
    """Sample customer request"""
    return {
        "customer_id": "cust_123",
        "request_type": "pitch_deck",
        "topic": "AI-powered productivity tool",
        "target_audience": "investors",
        "requirements": {
            "style": "modern minimalist",
            "length": "10-12 slides",
            "focus": ["problem", "solution", "market", "team"]
        }
    }


def test_agile_orchestrator_initialization(mock_agents):
    """Test AgileOrchestrator initialization"""
    orchestrator = AgileOrchestrator(agents=mock_agents)
    assert orchestrator.agents == mock_agents
    assert orchestrator.state == WorkflowState.IDLE
    assert orchestrator.current_phase == WorkflowPhase.INITIALIZATION


def test_initialize_workflow(agile_orchestrator, sample_customer_request):
    """Test workflow initialization"""
    result = agile_orchestrator.initialize_workflow(sample_customer_request)
    
    assert result["success"] is True
    assert agile_orchestrator.state == WorkflowState.RUNNING
    assert agile_orchestrator.current_request == sample_customer_request


def test_execute_research_phase(agile_orchestrator, mock_agents):
    """Test research phase execution"""
    # Initialize workflow first
    agile_orchestrator.initialize_workflow({
        "customer_id": "test",
        "request_type": "pitch_deck",
        "topic": "AI tool",
        "target_audience": "investors"
    })
    
    # Mock research agent response
    from agents.research_agent import ResearchResult
    mock_agents["research"].conduct_market_research.return_value = ResearchResult(
        market_size={"tam": "$50B"},
        competitors=[],
        trends=[],
        insights=["Market growing"],
        sources=["Report 2024"]
    )
    
    result = agile_orchestrator.execute_research_phase(
        query="AI productivity tools",
        focus_areas=["market", "competitors"]
    )
    
    assert result["success"] is True
    assert "research_data" in result
    assert agile_orchestrator.current_phase == WorkflowPhase.RESEARCH
    mock_agents["research"].conduct_market_research.assert_called_once()


def test_execute_content_phase(agile_orchestrator, mock_agents):
    """Test content phase execution"""
    # Initialize workflow first
    agile_orchestrator.initialize_workflow({
        "customer_id": "test",
        "request_type": "pitch_deck",
        "topic": "AI tool",
        "target_audience": "investors"
    })
    
    # Mock content agent response
    mock_agents["content"].create_pitch_deck.return_value = {
        "title": "AI Productivity Tool",
        "slides": [{"title": "Problem", "content": "Current tools are slow"}]
    }
    
    research_data = {
        "market_size": {"tam": "$50B"},
        "insights": ["Market growing"]
    }
    
    result = agile_orchestrator.execute_content_phase(
        research_data=research_data,
        requirements={"style": "modern"}
    )
    
    assert result["success"] is True
    assert "pitch_deck" in result
    assert agile_orchestrator.current_phase == WorkflowPhase.CONTENT_CREATION
    mock_agents["content"].create_pitch_deck.assert_called_once()


def test_execute_analysis_phase(agile_orchestrator, mock_agents):
    """Test analysis phase execution"""
    # Initialize workflow first
    agile_orchestrator.initialize_workflow({
        "customer_id": "test",
        "request_type": "pitch_deck",
        "topic": "AI tool",
        "target_audience": "investors"
    })
    
    # Mock analyst agent response
    from agents.analyst_agent import AnalysisResult
    mock_analysis_result = AnalysisResult(
        overall_score=0.85,
        criteria_scores=[],
        strengths=["Clear problem"],
        weaknesses=["Weak market data"],
        improvement_suggestions=["Add more data"]
    )
    mock_agents["analyst"].analyze_pitch_deck_quality.return_value = mock_analysis_result
    
    pitch_deck = {"title": "Test", "slides": []}
    checklist = {"criteria": []}
    
    result = agile_orchestrator.execute_analysis_phase(
        pitch_deck=pitch_deck,
        checklist=checklist,
        threshold=0.8
    )
    
    assert result["success"] is True
    assert "analysis_result" in result
    assert result["passes_threshold"] is True
    assert agile_orchestrator.current_phase == WorkflowPhase.ANALYSIS
    mock_agents["analyst"].analyze_pitch_deck_quality.assert_called_once()


def test_execute_design_phase(agile_orchestrator, mock_agents):
    """Test design phase execution"""
    # Initialize workflow first
    agile_orchestrator.initialize_workflow({
        "customer_id": "test",
        "request_type": "pitch_deck",
        "topic": "AI tool",
        "target_audience": "investors"
    })
    
    # Mock design agent response
    from agents.design_agent import DesignResult
    mock_design_result = DesignResult(
        design_system={"primary_color": "#0066CC"},
        slide_layouts=[],
        visual_elements=["icons"],
        design_recommendations=["Use consistent spacing"]
    )
    mock_agents["design"].create_visual_design.return_value = mock_design_result
    
    pitch_deck = {"title": "Test", "slides": []}
    requirements = {"style": "modern"}
    
    result = agile_orchestrator.execute_design_phase(
        pitch_deck=pitch_deck,
        requirements=requirements
    )
    
    assert result["success"] is True
    assert "design_result" in result
    assert agile_orchestrator.current_phase == WorkflowPhase.DESIGN
    mock_agents["design"].create_visual_design.assert_called_once()


def test_execute_iteration_cycle(agile_orchestrator, mock_agents):
    """Test iteration cycle for improvements"""
    # Initialize workflow first
    agile_orchestrator.initialize_workflow({
        "customer_id": "test",
        "request_type": "pitch_deck",
        "topic": "AI tool",
        "target_audience": "investors"
    })
    
    # Mock content agent improvement
    mock_agents["content"].improve_pitch_deck.return_value = {
        "title": "Improved Pitch",
        "slides": [{"title": "Problem", "content": "Enhanced content"}]
    }
    
    # Mock analyst re-analysis
    from agents.analyst_agent import AnalysisResult
    mock_analysis_result = AnalysisResult(
        overall_score=0.90,
        criteria_scores=[],
        strengths=["Enhanced content"],
        weaknesses=[],
        improvement_suggestions=[]
    )
    mock_agents["analyst"].analyze_pitch_deck_quality.return_value = mock_analysis_result
    
    pitch_deck = {"title": "Test", "slides": []}
    feedback = ["Add more data", "Improve flow"]
    checklist = {"criteria": []}
    
    result = agile_orchestrator.execute_iteration_cycle(
        pitch_deck=pitch_deck,
        feedback=feedback,
        checklist=checklist,
        threshold=0.85
    )
    
    assert result["success"] is True
    assert "improved_pitch_deck" in result
    assert result["new_score"] == 0.90
    mock_agents["content"].improve_pitch_deck.assert_called_once()


def test_execute_full_workflow(agile_orchestrator, mock_agents, sample_customer_request):
    """Test full workflow execution"""
    # Mock CEO analysis
    mock_agents["ceo"].analyze_customer_request.return_value = {
        "task_type": "pitch_deck",
        "priority": "high",
        "requirements": {"style": "modern"}
    }
    
    # Mock research
    from agents.research_agent import ResearchResult
    mock_agents["research"].conduct_market_research.return_value = ResearchResult(
        market_size={"tam": "$50B"},
        competitors=[],
        trends=[],
        insights=["Market growing"],
        sources=["Report 2024"]
    )
    
    # Mock content creation
    mock_agents["content"].create_pitch_deck.return_value = {
        "title": "AI Productivity Tool",
        "slides": [{"title": "Problem", "content": "Current tools are slow"}]
    }
    
    # Mock analysis
    from agents.analyst_agent import AnalysisResult
    mock_analysis_result = AnalysisResult(
        overall_score=0.85,
        criteria_scores=[],
        strengths=["Clear problem"],
        weaknesses=[],
        improvement_suggestions=[]
    )
    mock_agents["analyst"].analyze_pitch_deck_quality.return_value = mock_analysis_result
    
    # Mock design
    from agents.design_agent import DesignResult
    mock_design_result = DesignResult(
        design_system={"primary_color": "#0066CC"},
        slide_layouts=[],
        visual_elements=["icons"],
        design_recommendations=[]
    )
    mock_agents["design"].create_visual_design.return_value = mock_design_result
    
    # Mock CEO evaluation
    mock_agents["ceo"].evaluate_true_north_compliance.return_value = {
        "compliant": True,
        "score": 0.85,
        "gaps": []
    }
    
    result = agile_orchestrator.execute_full_workflow(
        customer_request=sample_customer_request,
        checklist={"criteria": []},
        quality_threshold=0.8
    )
    
    assert result.success is True
    assert result.final_pitch_deck is not None
    assert result.design is not None
    assert result.quality_score is not None
    assert agile_orchestrator.state == WorkflowState.COMPLETED


def test_workflow_state_transitions(agile_orchestrator):
    """Test workflow state transitions"""
    assert agile_orchestrator.state == WorkflowState.IDLE
    
    agile_orchestrator.state = WorkflowState.RUNNING
    assert agile_orchestrator.state == WorkflowState.RUNNING
    
    agile_orchestrator.state = WorkflowState.PAUSED
    assert agile_orchestrator.state == WorkflowState.PAUSED
    
    agile_orchestrator.state = WorkflowState.COMPLETED
    assert agile_orchestrator.state == WorkflowState.COMPLETED
    
    agile_orchestrator.state = WorkflowState.FAILED
    assert agile_orchestrator.state == WorkflowState.FAILED


def test_get_workflow_status(agile_orchestrator):
    """Test workflow status retrieval"""
    agile_orchestrator.state = WorkflowState.RUNNING
    agile_orchestrator.current_phase = WorkflowPhase.CONTENT_CREATION
    
    status = agile_orchestrator.get_workflow_status()
    
    assert status["state"] == "running"
    assert status["current_phase"] == "content_creation"
    assert "progress" in status


def test_pause_and_resume_workflow(agile_orchestrator):
    """Test workflow pause and resume"""
    agile_orchestrator.state = WorkflowState.RUNNING
    
    agile_orchestrator.pause_workflow()
    assert agile_orchestrator.state == WorkflowState.PAUSED
    
    agile_orchestrator.resume_workflow()
    assert agile_orchestrator.state == WorkflowState.RUNNING


def test_reset_workflow(agile_orchestrator):
    """Test workflow reset"""
    agile_orchestrator.state = WorkflowState.COMPLETED
    agile_orchestrator.current_phase = WorkflowPhase.DESIGN
    
    agile_orchestrator.reset_workflow()
    
    assert agile_orchestrator.state == WorkflowState.IDLE
    assert agile_orchestrator.current_phase == WorkflowPhase.INITIALIZATION
    assert agile_orchestrator.current_request is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
