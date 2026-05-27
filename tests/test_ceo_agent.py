"""
Test suite for CEO/Orchestrator Agent.
Tests the Task dataclass and CEOOrchestratorAgent class functionality.
"""

import pytest
from dataclasses import dataclass
from typing import Optional
from unittest.mock import Mock, patch, MagicMock
import json


# Import the classes we're testing
from agents.ceo_orchestrator_agent import Task, CEOOrchestratorAgent


class TestTaskDataclass:
    """Test the Task dataclass structure and functionality."""
    
    def test_task_creation(self):
        """Test creating a Task instance with all fields."""
        task = Task(
            id="task-001",
            description="Analyze customer request for AI solution",
            assigned_agent="research_agent",
            priority="high",
            status="pending",
            result=None,
            true_north_score=None
        )
        
        assert task.id == "task-001"
        assert task.description == "Analyze customer request for AI solution"
        assert task.assigned_agent == "research_agent"
        assert task.priority == "high"
        assert task.status == "pending"
        assert task.result is None
        assert task.true_north_score is None
    
    def test_task_with_result(self):
        """Test creating a Task with a result."""
        task = Task(
            id="task-002",
            description="Evaluate True North compliance",
            assigned_agent="qa_agent",
            priority="medium",
            status="completed",
            result="Compliance score: 85/100",
            true_north_score=85.0
        )
        
        assert task.id == "task-002"
        assert task.result == "Compliance score: 85/100"
        assert task.true_north_score == 85.0
        assert task.status == "completed"


class TestCEOOrchestratorAgentInit:
    """Test CEOOrchestratorAgent initialization."""
    
    def test_initialization_with_api_key(self):
        """Test initializing CEO agent with API key."""
        agent = CEOOrchestratorAgent(
            openrouter_api_key="test-api-key",
            model="nvidia/nemotron-120b"
        )
        
        assert agent.openrouter_api_key == "test-api-key"
        assert agent.model == "nvidia/nemotron-120b"
    
    def test_initialization_with_custom_parameters(self):
        """Test initializing with custom model parameters."""
        agent = CEOOrchestratorAgent(
            openrouter_api_key="test-api-key",
            model="nvidia/nemotron-120b",
            temperature=0.7,
            max_tokens=2000
        )
        
        assert agent.openrouter_api_key == "test-api-key"
        assert agent.model == "nvidia/nemotron-120b"
        assert agent.temperature == 0.7
        assert agent.max_tokens == 2000
    
    def test_initialization_default_parameters(self):
        """Test initialization with default parameters."""
        agent = CEOOrchestratorAgent(
            openrouter_api_key="test-api-key"
        )
        
        assert agent.openrouter_api_key == "test-api-key"
        assert agent.model == "nvidia/nemotron-120b"
        assert agent.temperature == 0.3
        assert agent.max_tokens == 1000


class TestAnalyzeCustomerRequest:
    """Test the analyze_customer_request method."""
    
    @patch('agents.ceo_orchestrator_agent.CEOOrchestratorAgent._call_openrouter')
    def test_analyze_customer_request_success(self, mock_call):
        """Test successful customer request analysis."""
        mock_call.return_value = """
        Strategic Plan:
        - Primary goal: Develop AI-powered customer service solution
        - Required agents: research_agent, development_agent, qa_agent
        - Timeline: 4 weeks
        - Priority: high
        """
        
        agent = CEOOrchestratorAgent(
            openrouter_api_key="test-api-key"
        )
        
        result = agent.analyze_customer_request(
            "We need an AI-powered customer service solution"
        )
        
        assert "primary_goal" in result
        assert "required_agents" in result
        assert "timeline" in result
        assert "priority" in result
        mock_call.assert_called_once()
    
    @patch('agents.ceo_orchestrator_agent.CEOOrchestratorAgent._call_openrouter')
    def test_analyze_customer_request_with_context(self, mock_call):
        """Test analysis with additional context."""
        mock_call.return_value = """
        Strategic Plan:
        - Primary goal: Enhance existing platform with ML capabilities
        - Required agents: research_agent, development_agent
        - Timeline: 6 weeks
        - Priority: medium
        """
        
        agent = CEOOrchestratorAgent(
            openrouter_api_key="test-api-key"
        )
        
        result = agent.analyze_customer_request(
            "Enhance our platform with ML capabilities",
            context="Current platform serves 10k users"
        )
        
        assert "primary_goal" in result
        assert "required_agents" in result
        assert "timeline" in result
        assert "priority" in result
        mock_call.assert_called_once()


class TestDelegateTask:
    """Test the delegate_task method."""
    
    def test_delegate_task_creation(self):
        """Test task delegation creates a Task object."""
        agent = CEOOrchestratorAgent(
            openrouter_api_key="test-api-key"
        )
        
        task = agent.delegate_task(
            description="Research AI models for customer service",
            assigned_agent="research_agent",
            priority="high"
        )
        
        assert isinstance(task, Task)
        assert task.description == "Research AI models for customer service"
        assert task.assigned_agent == "research_agent"
        assert task.priority == "high"
        assert task.status == "pending"
        assert task.id is not None
    
    def test_delegate_task_with_custom_id(self):
        """Test task delegation with custom task ID."""
        agent = CEOOrchestratorAgent(
            openrouter_api_key="test-api-key"
        )
        
        task = agent.delegate_task(
            description="Evaluate model performance",
            assigned_agent="qa_agent",
            priority="medium",
            task_id="custom-task-123"
        )
        
        assert task.id == "custom-task-123"


class TestEvaluateTrueNorthCompliance:
    """Test the evaluate_true_north_compliance method."""
    
    @patch('agents.ceo_orchestrator_agent.CEOOrchestratorAgent._call_openrouter')
    def test_evaluate_true_north_compliance(self, mock_call):
        """Test True North compliance evaluation."""
        mock_call.return_value = """
        True North Score: 85
        Analysis:
        - Alignment with mission: Strong
        - Customer value: High
        - Quality standards: Met
        """
        
        agent = CEOOrchestratorAgent(
            openrouter_api_key="test-api-key"
        )
        
        result = agent.evaluate_true_north_compliance(
            task_result="AI model trained with 95% accuracy",
            task_description="Train AI model for customer service"
        )
        
        assert "score" in result
        assert "analysis" in result
        assert result["score"] == 85
        mock_call.assert_called_once()
    
    @patch('agents.ceo_orchestrator_agent.CEOOrchestratorAgent._call_openrouter')
    def test_evaluate_true_north_compliance_low_score(self, mock_call):
        """Test evaluation with low compliance score."""
        mock_call.return_value = """
        True North Score: 45
        Analysis:
        - Alignment with mission: Weak
        - Customer value: Low
        - Quality standards: Not met
        """
        
        agent = CEOOrchestratorAgent(
            openrouter_api_key="test-api-key"
        )
        
        result = agent.evaluate_true_north_compliance(
            task_result="Incomplete implementation",
            task_description="Complete feature implementation"
        )
        
        assert result["score"] == 45


class TestIntegrateLearning:
    """Test the integrate_learning method."""
    
    @patch('agents.ceo_orchestrator_agent.CEOOrchestratorAgent._call_openrouter')
    def test_integrate_learning_pattern_extraction(self, mock_call):
        """Test learning integration with pattern extraction."""
        mock_call.return_value = """
        Pattern Identified:
        - Type: Success pattern
        - Context: High-priority tasks with clear requirements
        - Recommendation: Assign experienced agents to high-priority tasks
        """
        
        agent = CEOOrchestratorAgent(
            openrouter_api_key="test-api-key"
        )
        
        result = agent.integrate_learning(
            task_history=[
                Task(id="1", description="Task 1", assigned_agent="agent1", 
                     priority="high", status="completed", result="Success", true_north_score=90),
                Task(id="2", description="Task 2", assigned_agent="agent2", 
                     priority="low", status="completed", result="Partial", true_north_score=60)
            ]
        )
        
        assert "pattern" in result
        assert "recommendation" in result
        mock_call.assert_called_once()
    
    @patch('agents.ceo_orchestrator_agent.CEOOrchestratorAgent._call_openrouter')
    def test_integrate_learning_empty_history(self, mock_call):
        """Test learning integration with empty task history."""
        mock_call.return_value = """
        Pattern Identified:
        - Type: No pattern
        - Context: Insufficient data
        - Recommendation: Collect more task data
        """
        
        agent = CEOOrchestratorAgent(
            openrouter_api_key="test-api-key"
        )
        
        result = agent.integrate_learning(task_history=[])
        
        assert "pattern" in result
        assert "recommendation" in result


class TestPrivateHelperMethods:
    """Test private helper methods."""
    
    @patch('requests.post')
    def test_call_openrouter_success(self, mock_post):
        """Test successful OpenRouter API call."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Test response from Nemotron"
                    }
                }
            ]
        }
        mock_post.return_value = mock_response
        
        agent = CEOOrchestratorAgent(
            openrouter_api_key="test-api-key"
        )
        
        result = agent._call_openrouter("Test prompt")
        
        assert result == "Test response from Nemotron"
        mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_call_openrouter_api_error(self, mock_post):
        """Test OpenRouter API call with error response."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        
        agent = CEOOrchestratorAgent(
            openrouter_api_key="test-api-key"
        )
        
        with pytest.raises(Exception):
            agent._call_openrouter("Test prompt")
    
    def test_parse_strategic_plan(self):
        """Test parsing strategic plan from LLM response."""
        agent = CEOOrchestratorAgent(
            openrouter_api_key="test-api-key"
        )
        
        response = """
        Strategic Plan:
        - Primary goal: Develop AI solution
        - Required agents: research, development
        - Timeline: 4 weeks
        - Priority: high
        """
        
        result = agent._parse_strategic_plan(response)
        
        assert "primary_goal" in result
        assert "required_agents" in result
        assert "timeline" in result
        assert "priority" in result
    
    def test_parse_true_north_score(self):
        """Test parsing True North score from LLM response."""
        agent = CEOOrchestratorAgent(
            openrouter_api_key="test-api-key"
        )
        
        response = """
        True North Score: 85
        Analysis: Good compliance
        """
        
        score = agent._parse_true_north_score(response)
        
        assert score == 85
    
    def test_extract_pattern(self):
        """Test pattern extraction from LLM response."""
        agent = CEOOrchestratorAgent(
            openrouter_api_key="test-api-key"
        )
        
        response = """
        Pattern Identified:
        - Type: Success pattern
        - Context: High-priority tasks
        - Recommendation: Use experienced agents
        """
        
        result = agent._extract_pattern(response)
        
        assert "type" in result
        assert "context" in result
        assert "recommendation" in result
    
    def test_get_timestamp(self):
        """Test timestamp generation."""
        agent = CEOOrchestratorAgent(
            openrouter_api_key="test-api-key"
        )
        
        timestamp = agent._get_timestamp()
        
        assert isinstance(timestamp, str)
        assert len(timestamp) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
