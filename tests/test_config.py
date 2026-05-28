"""Tests for config.json loading and validation"""

import pytest
import json
from pathlib import Path


def test_config_file_exists():
    """Test that config.json exists"""
    config_path = Path("config.json")
    assert config_path.exists(), "config.json should exist"


def test_config_file_valid_json():
    """Test that config.json is valid JSON"""
    config_path = Path("config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    assert isinstance(config, dict)


def test_config_has_required_sections():
    """Test that config has all required sections"""
    config_path = Path("config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    required_sections = [
        "agent_network",
        "ceo_agent",
        "specialized_agents",
        "true_north_principles",
        "task_priorities",
        "task_statuses",
        "learning",
        "workflow",
        "ollama"
    ]
    
    for section in required_sections:
        assert section in config, f"Config should have {section} section"


def test_ceo_agent_config():
    """Test CEO agent configuration"""
    config_path = Path("config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    ceo_config = config["ceo_agent"]
    
    assert ceo_config["name"] == "CEO/Orchestrator Agent"
    assert ceo_config["class"] == "CEOOrchestratorAgent"
    assert ceo_config["module"] == "agents.ceo_orchestrator_agent"
    assert ceo_config["model"] == "nvidia/nemotron-120b"
    assert ceo_config["api_provider"] == "openrouter"
    assert "capabilities" in ceo_config
    assert len(ceo_config["capabilities"]) > 0


def test_specialized_agents_config():
    """Test specialized agents configuration"""
    config_path = Path("config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    specialized_agents = config["specialized_agents"]
    
    # Check that all specialized agents are implemented
    expected_agents = ["content_agent", "research_agent", "analyst_agent", "design_agent"]
    
    for agent_name in expected_agents:
        assert agent_name in specialized_agents, f"Config should have {agent_name}"
        agent_config = specialized_agents[agent_name]
        assert agent_config["status"] == "implemented", f"{agent_name} should be implemented"
        assert "class" in agent_config
        assert "module" in agent_config
        assert "model" in agent_config
        assert "capabilities" in agent_config


def test_content_agent_config():
    """Test Content Agent specific configuration"""
    config_path = Path("config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    content_config = config["specialized_agents"]["content_agent"]
    
    assert content_config["model"] == "pitchdeck-2026:latest"
    assert content_config["api_provider"] == "ollama"
    assert "pitch_deck_creation" in content_config["capabilities"]


def test_research_agent_config():
    """Test Research Agent specific configuration"""
    config_path = Path("config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    research_config = config["specialized_agents"]["research_agent"]
    
    assert research_config["model"] == "qwen2.5:7b"
    assert research_config["api_provider"] == "ollama"
    assert "market_research" in research_config["capabilities"]


def test_analyst_agent_config():
    """Test Analyst Agent specific configuration"""
    config_path = Path("config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    analyst_config = config["specialized_agents"]["analyst_agent"]
    
    assert analyst_config["model"] == "gemma4:e4b"
    assert analyst_config["api_provider"] == "ollama"
    assert "quality_analysis" in analyst_config["capabilities"]


def test_design_agent_config():
    """Test Design Agent specific configuration"""
    config_path = Path("config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    design_config = config["specialized_agents"]["design_agent"]
    
    assert design_config["model"] == "llama3.2:latest"
    assert design_config["api_provider"] == "ollama"
    assert "visual_design" in design_config["capabilities"]


def test_workflow_config():
    """Test workflow configuration"""
    config_path = Path("config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    workflow_config = config["workflow"]["agile_orchestrator"]
    
    assert workflow_config["class"] == "AgileOrchestrator"
    assert workflow_config["module"] == "workflow.agile_orchestrator"
    assert workflow_config["max_iterations"] == 3
    assert workflow_config["quality_threshold"] == 0.8
    assert len(workflow_config["phases"]) == 7
    assert "state_management" in workflow_config


def test_ollama_config():
    """Test Ollama configuration"""
    config_path = Path("config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    ollama_config = config["ollama"]
    
    assert ollama_config["base_url"] == "http://localhost:11434"
    assert ollama_config["timeout"] == 120
    assert len(ollama_config["allowed_local_models"]) == 4
    
    # Check that all our custom models are in the allowed list
    expected_models = ["pitchdeck-2026:latest", "qwen2.5:7b", "gemma4:e4b", "llama3.2:latest"]
    for model in expected_models:
        assert model in ollama_config["allowed_local_models"]


def test_true_north_principles():
    """Test True North principles configuration"""
    config_path = Path("config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    principles = config["true_north_principles"]
    
    assert "alignment_with_mission" in principles
    assert "customer_value_creation" in principles
    assert "quality_and_excellence" in principles
    assert "innovation_and_continuous_improvement" in principles


def test_learning_config():
    """Test learning configuration"""
    config_path = Path("config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    learning_config = config["learning"]
    
    assert "pattern_recognition" in learning_config
    assert "adaptive_delegation" in learning_config
    assert learning_config["pattern_recognition"]["enabled"] is True
    assert learning_config["adaptive_delegation"]["enabled"] is True


def test_task_priorities_config():
    """Test task priorities configuration"""
    config_path = Path("config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    priorities = config["task_priorities"]
    
    assert "high" in priorities
    assert "medium" in priorities
    assert "low" in priorities


def test_task_statuses_config():
    """Test task statuses configuration"""
    config_path = Path("config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    statuses = config["task_statuses"]
    
    assert "pending" in statuses
    assert "in_progress" in statuses
    assert "completed" in statuses
    assert "failed" in statuses


def test_agent_network_info():
    """Test agent network metadata"""
    config_path = Path("config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    network_info = config["agent_network"]
    
    assert network_info["name"] == "WUPHF Agile Agent Network"
    assert network_info["version"] == "1.0.0"
    assert "description" in network_info


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
