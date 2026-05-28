"""Tests for Main Application Entry Point"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
import json


@pytest.fixture
def temp_config_dir():
    """Create temporary directory for config"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_config(temp_config_dir):
    """Create sample config file"""
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
                "quality_threshold": 0.8
            }
        }
    }
    
    config_path = Path(temp_config_dir) / "config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f)
    
    return config_path


@pytest.fixture
def temp_memory_dir():
    """Create temporary directory for memory"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_network_initialization(sample_config, temp_memory_dir):
    """Test network initialization with config"""
    from main_agile_network import WUPHFAgileNetwork
    
    # Mock the memory directory in config
    with open(sample_config, 'r') as f:
        config = json.load(f)
    config["memory_dir"] = temp_memory_dir
    with open(sample_config, 'w') as f:
        json.dump(config, f)
    
    network = WUPHFAgileNetwork(config_path=str(sample_config))
    
    assert network.config is not None
    assert network.agents is not None
    assert "ceo" in network.agents
    assert "content" in network.agents
    assert "research" in network.agents
    assert "analyst" in network.agents
    assert "design" in network.agents
    assert network.orchestrator is not None
    assert network.memory is not None


def test_network_initialization_missing_config():
    """Test network initialization with missing config"""
    from main_agile_network import WUPHFAgileNetwork
    
    with pytest.raises(FileNotFoundError):
        WUPHFAgileNetwork(config_path="nonexistent_config.json")


def test_process_customer_request(sample_config, temp_memory_dir):
    """Test processing a customer request"""
    from main_agile_network import WUPHFAgileNetwork
    from workflow.agile_orchestrator import WorkflowResult
    
    # Mock the memory directory in config
    with open(sample_config, 'r') as f:
        config = json.load(f)
    config["memory_dir"] = temp_memory_dir
    with open(sample_config, 'w') as f:
        json.dump(config, f)
    
    network = WUPHFAgileNetwork(config_path=str(sample_config))
    
    # Mock the orchestrator to return a successful result
    mock_result = WorkflowResult(
        success=True,
        final_pitch_deck={"title": "Test Pitch", "slides": []},
        design=None,
        research_data=None,
        quality_score=0.85,
        iterations=1,
        total_duration=120.0
    )
    
    with patch.object(network.orchestrator, 'execute_full_workflow', return_value=mock_result):
        customer_request = {
            "customer_id": "test_123",
            "request_type": "pitch_deck",
            "topic": "AI startup",
            "target_audience": "investors"
        }
        
        result = network.process_customer_request(customer_request)
        
        assert result["success"] is True
        assert result["final_pitch_deck"] is not None
        assert result["quality_score"] == 0.85


def test_process_customer_request_failure(sample_config, temp_memory_dir):
    """Test processing a customer request that fails"""
    from main_agile_network import WUPHFAgileNetwork
    
    # Mock the memory directory in config
    with open(sample_config, 'r') as f:
        config = json.load(f)
    config["memory_dir"] = temp_memory_dir
    with open(sample_config, 'w') as f:
        json.dump(config, f)
    
    network = WUPHFAgileNetwork(config_path=str(sample_config))
    
    # Mock the orchestrator to raise an exception
    with patch.object(network.orchestrator, 'execute_full_workflow', side_effect=Exception("Test error")):
        customer_request = {
            "customer_id": "test_123",
            "request_type": "pitch_deck",
            "topic": "AI startup"
        }
        
        result = network.process_customer_request(customer_request)
        
        assert result["success"] is False
        assert "error" in result
        assert len(result["errors"]) > 0


def test_get_network_status(sample_config, temp_memory_dir):
    """Test getting network status"""
    from main_agile_network import WUPHFAgileNetwork
    
    # Mock the memory directory in config
    with open(sample_config, 'r') as f:
        config = json.load(f)
    config["memory_dir"] = temp_memory_dir
    with open(sample_config, 'w') as f:
        json.dump(config, f)
    
    network = WUPHFAgileNetwork(config_path=str(sample_config))
    
    status = network.get_network_status()
    
    assert "workflow_status" in status
    assert "agent_performance" in status
    assert "learning_insights" in status
    assert "config" in status
    assert status["config"]["network_name"] == "WUPHF Agile Agent Network"


def test_custom_quality_threshold(sample_config, temp_memory_dir):
    """Test processing with custom quality threshold"""
    from main_agile_network import WUPHFAgileNetwork
    from workflow.agile_orchestrator import WorkflowResult
    
    # Mock the memory directory in config
    with open(sample_config, 'r') as f:
        config = json.load(f)
    config["memory_dir"] = temp_memory_dir
    with open(sample_config, 'w') as f:
        json.dump(config, f)
    
    network = WUPHFAgileNetwork(config_path=str(sample_config))
    
    # Mock the orchestrator
    mock_result = WorkflowResult(
        success=True,
        final_pitch_deck={"title": "Test", "slides": []},
        design=None,
        research_data=None,
        quality_score=0.9,
        iterations=1,
        total_duration=100.0
    )
    
    with patch.object(network.orchestrator, 'execute_full_workflow', return_value=mock_result) as mock_execute:
        customer_request = {
            "customer_id": "test_123",
            "request_type": "pitch_deck",
            "topic": "AI startup"
        }
        
        # Process with custom threshold
        network.process_customer_request(customer_request, quality_threshold=0.9)
        
        # Verify the custom threshold was used
        mock_execute.assert_called_once()
        call_args = mock_execute.call_args
        assert call_args[1]["quality_threshold"] == 0.9


def test_agent_initialization(sample_config, temp_memory_dir):
    """Test that all agents are properly initialized"""
    from main_agile_network import WUPHFAgileNetwork
    
    # Mock the memory directory in config
    with open(sample_config, 'r') as f:
        config = json.load(f)
    config["memory_dir"] = temp_memory_dir
    with open(sample_config, 'w') as f:
        json.dump(config, f)
    
    network = WUPHFAgileNetwork(config_path=str(sample_config))
    
    # Check CEO agent
    assert network.agents["ceo"] is not None
    assert hasattr(network.agents["ceo"], "analyze_customer_request")
    
    # Check specialized agents
    assert hasattr(network.agents["content"], "create_pitch_deck")
    assert hasattr(network.agents["research"], "conduct_market_research")
    assert hasattr(network.agents["analyst"], "analyze_pitch_deck_quality")
    assert hasattr(network.agents["design"], "create_visual_design")


def test_memory_integration(sample_config, temp_memory_dir):
    """Test that memory is properly integrated"""
    from main_agile_network import WUPHFAgileNetwork
    from workflow.agile_orchestrator import WorkflowResult
    
    # Mock the memory directory in config
    with open(sample_config, 'r') as f:
        config = json.load(f)
    config["memory_dir"] = temp_memory_dir
    with open(sample_config, 'w') as f:
        json.dump(config, f)
    
    network = WUPHFAgileNetwork(config_path=str(sample_config))
    
    # Mock successful workflow
    mock_result = WorkflowResult(
        success=True,
        final_pitch_deck={"title": "Test", "slides": []},
        design=None,
        research_data=None,
        quality_score=0.85,
        iterations=1,
        total_duration=100.0
    )
    
    with patch.object(network.orchestrator, 'execute_full_workflow', return_value=mock_result):
        customer_request = {
            "customer_id": "test_123",
            "request_type": "pitch_deck",
            "topic": "AI startup"
        }
        
        # Process request
        network.process_customer_request(customer_request)
        
        # Check that memory entries were created
        all_entries = network.memory._load_all_entries()
        assert len(all_entries) >= 2  # Request log + result log


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
