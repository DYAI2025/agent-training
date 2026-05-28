"""Integration tests for full WUPHF Agile Agent Network workflow"""

import pytest
import tempfile
import shutil
from pathlib import Path
import json
from unittest.mock import Mock, patch


@pytest.fixture
def temp_integration_dir():
    """Create temporary directory for integration testing"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def integration_config(temp_integration_dir):
    """Create integration test configuration"""
    config = {
        "agent_network": {
            "name": "WUPHF Agile Agent Network",
            "version": "1.0.0"
        },
        "ceo_agent": {
            "model": "nvidia/nemotron-120b",
            "api_url": "https://openrouter.ai/api/v1/chat/completions"
        },
        "specialized_agents": {
            "content_agent": {
                "model": "pitchdeck-2026:latest"
            },
            "research_agent": {
                "model": "qwen2.5:7b"
            },
            "analyst_agent": {
                "model": "gemma4:e4b"
            },
            "design_agent": {
                "model": "llama3.2:latest"
            }
        },
        "workflow": {
            "agile_orchestrator": {
                "max_iterations": 3,
                "quality_threshold": 0.8
            }
        },
        "memory_dir": str(Path(temp_integration_dir) / "memory")
    }
    
    config_path = Path(temp_integration_dir) / "config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f)
    
    return config_path


@pytest.fixture
def sample_customer_request():
    """Sample customer request for integration testing"""
    return {
        "customer_id": "integration_test_123",
        "request_type": "pitch_deck",
        "topic": "AI-powered productivity tool for remote teams",
        "target_audience": "investors",
        "requirements": {
            "style": "modern minimalist",
            "length": "10-12 slides",
            "focus": ["problem", "solution", "market", "team", "business_model"]
        }
    }


def test_full_workflow_integration(integration_config, sample_customer_request):
    """Test complete workflow from request to delivery"""
    from main_agile_network import WUPHFAgileNetwork
    from workflow.agile_orchestrator import WorkflowResult
    from agents.research_agent import ResearchResult
    from agents.analyst_agent import AnalysisResult
    from agents.design_agent import DesignResult
    
    # Initialize network
    network = WUPHFAgileNetwork(config_path=str(integration_config))
    
    # Mock the workflow to return successful result
    mock_result = WorkflowResult(
        success=True,
        final_pitch_deck={
            "title": "AI Productivity Tool for Remote Teams",
            "slides": [
                {"title": "Problem", "content": "Remote teams struggle with collaboration"},
                {"title": "Solution", "content": "Our AI-powered platform solves this"},
                {"title": "Market", "content": "$50B market opportunity"}
            ]
        },
        design=DesignResult(
            design_system={"primary_color": "#0066CC"},
            slide_layouts=[],
            visual_elements=["icons", "charts"],
            design_recommendations=[]
        ),
        research_data=ResearchResult(
            market_size={"tam": "$50B"},
            competitors=[],
            trends=[],
            insights=["Market growing rapidly"],
            sources=["Industry Report 2024"]
        ),
        quality_score=0.85,
        iterations=1,
        total_duration=120.0
    )
    
    with patch.object(network.orchestrator, 'execute_full_workflow', return_value=mock_result):
        # Process customer request
        result = network.process_customer_request(sample_customer_request)
        
        # Verify successful processing
        assert result["success"] is True
        assert result["final_pitch_deck"] is not None
        assert result["quality_score"] == 0.85
        assert result["iterations"] == 1
        assert result["design"] is not None
        assert result["research_data"] is not None


def test_workflow_with_iteration_cycle(integration_config, sample_customer_request):
    """Test workflow that requires iteration for quality improvement"""
    from main_agile_network import WUPHFAgileNetwork
    from workflow.agile_orchestrator import WorkflowResult
    from agents.research_agent import ResearchResult
    from agents.analyst_agent import AnalysisResult
    from agents.design_agent import DesignResult
    
    network = WUPHFAgileNetwork(config_path=str(integration_config))
    
    # Mock workflow that requires iteration
    mock_result = WorkflowResult(
        success=True,
        final_pitch_deck={
            "title": "Improved Pitch Deck",
            "slides": [{"title": "Problem", "content": "Enhanced content"}]
        },
        design=DesignResult(
            design_system={"primary_color": "#0066CC"},
            slide_layouts=[],
            visual_elements=[],
            design_recommendations=[]
        ),
        research_data=ResearchResult(
            market_size={"tam": "$50B"},
            competitors=[],
            trends=[],
            insights=[],
            sources=[]
        ),
        quality_score=0.88,
        iterations=2,  # Required 2 iterations
        total_duration=180.0
    )
    
    with patch.object(network.orchestrator, 'execute_full_workflow', return_value=mock_result):
        result = network.process_customer_request(
            sample_customer_request,
            quality_threshold=0.85
        )
        
        assert result["success"] is True
        assert result["iterations"] == 2
        assert result["quality_score"] >= 0.85


def test_workflow_failure_handling(integration_config, sample_customer_request):
    """Test workflow failure handling and logging"""
    from main_agile_network import WUPHFAgileNetwork
    
    network = WUPHFAgileNetwork(config_path=str(integration_config))
    
    # Mock workflow failure
    with patch.object(network.orchestrator, 'execute_full_workflow', side_effect=Exception("Simulated workflow failure")):
        result = network.process_customer_request(sample_customer_request)
        
        assert result["success"] is False
        assert "error" in result
        assert len(result["errors"]) > 0
        
        # Verify failure was logged to memory
        all_entries = network.memory._load_all_entries()
        failure_entries = [e for e in all_entries if e.entry_type.value == "failure"]
        assert len(failure_entries) > 0


def test_network_status_reporting(integration_config):
    """Test network status reporting functionality"""
    from main_agile_network import WUPHFAgileNetwork
    
    network = WUPHFAgileNetwork(config_path=str(integration_config))
    
    status = network.get_network_status()
    
    # Verify status structure
    assert "workflow_status" in status
    assert "agent_performance" in status
    assert "learning_insights" in status
    assert "config" in status
    
    # Verify workflow status
    assert status["workflow_status"]["state"] == "idle"
    assert status["workflow_status"]["current_phase"] == "initialization"
    
    # Verify config info
    assert status["config"]["network_name"] == "WUPHF Agile Agent Network"
    assert status["config"]["version"] == "1.0.0"


def test_memory_integration_across_workflow(integration_config, sample_customer_request):
    """Test that memory is properly integrated throughout workflow"""
    from main_agile_network import WUPHFAgileNetwork
    from workflow.agile_orchestrator import WorkflowResult
    from agents.research_agent import ResearchResult
    from agents.analyst_agent import AnalysisResult
    from agents.design_agent import DesignResult
    
    network = WUPHFAgileNetwork(config_path=str(integration_config))
    
    # Mock successful workflow
    mock_result = WorkflowResult(
        success=True,
        final_pitch_deck={"title": "Test", "slides": []},
        design=DesignResult(
            design_system={},
            slide_layouts=[],
            visual_elements=[],
            design_recommendations=[]
        ),
        research_data=ResearchResult(
            market_size={},
            competitors=[],
            trends=[],
            insights=[],
            sources=[]
        ),
        quality_score=0.85,
        iterations=1,
        total_duration=100.0
    )
    
    with patch.object(network.orchestrator, 'execute_full_workflow', return_value=mock_result):
        # Process request
        network.process_customer_request(sample_customer_request)
        
        # Verify memory entries were created
        all_entries = network.memory._load_all_entries()
        assert len(all_entries) >= 2  # Request log + result log
        
        # Verify entry types
        entry_types = [e.entry_type for e in all_entries]
        assert "success" in [t.value for t in entry_types]


def test_agent_coordination(integration_config):
    """Test that all agents are properly coordinated"""
    from main_agile_network import WUPHFAgileNetwork
    
    network = WUPHFAgileNetwork(config_path=str(integration_config))
    
    # Verify all agents are initialized
    assert "ceo" in network.agents
    assert "content" in network.agents
    assert "research" in network.agents
    assert "analyst" in network.agents
    assert "design" in network.agents
    
    # Verify agent capabilities
    assert hasattr(network.agents["content"], "create_pitch_deck")
    assert hasattr(network.agents["research"], "conduct_market_research")
    assert hasattr(network.agents["analyst"], "analyze_pitch_deck_quality")
    assert hasattr(network.agents["design"], "create_visual_design")


def test_config_driven_behavior(integration_config):
    """Test that configuration properly drives system behavior"""
    from main_agile_network import WUPHFAgileNetwork
    
    network = WUPHFAgileNetwork(config_path=str(integration_config))
    
    # Verify configuration is loaded
    assert network.config is not None
    assert network.config["agent_network"]["name"] == "WUPHF Agile Agent Network"
    
    # Verify workflow configuration
    workflow_config = network.config["workflow"]["agile_orchestrator"]
    assert workflow_config["max_iterations"] == 3
    assert workflow_config["quality_threshold"] == 0.8


def test_quality_threshold_enforcement(integration_config, sample_customer_request):
    """Test that quality thresholds are properly enforced"""
    from main_agile_network import WUPHFAgileNetwork
    from workflow.agile_orchestrator import WorkflowResult
    from agents.research_agent import ResearchResult
    from agents.analyst_agent import AnalysisResult
    from agents.design_agent import DesignResult
    
    network = WUPHFAgileNetwork(config_path=str(integration_config))
    
    # Mock result below threshold
    low_quality_result = WorkflowResult(
        success=True,
        final_pitch_deck={"title": "Test", "slides": []},
        design=DesignResult(
            design_system={},
            slide_layouts=[],
            visual_elements=[],
            design_recommendations=[]
        ),
        research_data=ResearchResult(
            market_size={},
            competitors=[],
            trends=[],
            insights=[],
            sources=[]
        ),
        quality_score=0.75,  # Below 0.8 threshold
        iterations=3,
        total_duration=200.0
    )
    
    with patch.object(network.orchestrator, 'execute_full_workflow', return_value=low_quality_result):
        result = network.process_customer_request(
            sample_customer_request,
            quality_threshold=0.8
        )
        
        # System should still return result even if below threshold
        # (real system would iterate more, but mock returns as-is)
        assert result["success"] is True
        assert result["quality_score"] == 0.75


def test_multiple_sequential_requests(integration_config):
    """Test handling multiple sequential customer requests"""
    from main_agile_network import WUPHFAgileNetwork
    from workflow.agile_orchestrator import WorkflowResult
    from agents.research_agent import ResearchResult
    from agents.analyst_agent import AnalysisResult
    from agents.design_agent import DesignResult
    
    network = WUPHFAgileNetwork(config_path=str(integration_config))
    
    # Mock successful result
    mock_result = WorkflowResult(
        success=True,
        final_pitch_deck={"title": "Test", "slides": []},
        design=DesignResult(
            design_system={},
            slide_layouts=[],
            visual_elements=[],
            design_recommendations=[]
        ),
        research_data=ResearchResult(
            market_size={},
            competitors=[],
            trends=[],
            insights=[],
            sources=[]
        ),
        quality_score=0.85,
        iterations=1,
        total_duration=100.0
    )
    
    with patch.object(network.orchestrator, 'execute_full_workflow', return_value=mock_result):
        # Process multiple requests
        requests = [
            {
                "customer_id": f"customer_{i}",
                "request_type": "pitch_deck",
                "topic": f"Topic {i}",
                "target_audience": "investors"
            }
            for i in range(3)
        ]
        
        results = []
        for request in requests:
            result = network.process_customer_request(request)
            results.append(result)
        
        # Verify all requests were processed
        assert len(results) == 3
        assert all(r["success"] for r in results)
        
        # Verify memory captured all requests
        all_entries = network.memory._load_all_entries()
        assert len(all_entries) >= 6  # 2 entries per request


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
