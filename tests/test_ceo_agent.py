# tests/test_ceo_agent.py
import pytest
from agents.ceo_orchestrator_agent import CEOOrchestratorAgent, Task

def test_ceo_agent_initialization():
    ceo = CEOOrchestratorAgent("test_api_key")
    assert ceo.model == "nvidia/nemotron-120b"
    assert ceo.temperature == 0.3
    assert ceo.max_tokens == 1000

def test_delegate_task():
    ceo = CEOOrchestratorAgent("test_api_key")
    task = ceo.delegate_task(
        description="Test Task",
        assigned_agent="content",
        priority="high"
    )
    assert task.assigned_agent == "content"
    assert task.priority == "high"
    assert task.status == "pending"
    assert task.id.startswith("task-")

def test_task_creation():
    task = Task(
        id="test-1",
        description="Test Description",
        assigned_agent="analyst",
        priority="medium",
        status="pending"
    )
    assert task.id == "test-1"
    assert task.description == "Test Description"
    assert task.assigned_agent == "analyst"
    assert task.priority == "medium"
    assert task.status == "pending"
    assert task.result is None
    assert task.true_north_score is None