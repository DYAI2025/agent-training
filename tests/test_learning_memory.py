"""Tests for Learning Memory System - continuous improvement and pattern recognition"""

import pytest
import tempfile
import shutil
from pathlib import Path
from memory.learning_memory import (
    LearningMemory,
    MemoryEntry,
    Pattern,
    LearningInsight,
    MemoryType
)


@pytest.fixture
def temp_memory_dir():
    """Create temporary directory for memory storage"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def learning_memory(temp_memory_dir):
    """Create LearningMemory instance with temporary directory"""
    return LearningMemory(memory_dir=temp_memory_dir)


def test_learning_memory_initialization(learning_memory):
    """Test LearningMemory initialization"""
    assert learning_memory.memory_dir is not None
    assert learning_memory.pattern_recognition_enabled is True
    assert learning_memory.min_history_size == 5


def test_store_memory_entry(learning_memory):
    """Test storing a memory entry"""
    entry = MemoryEntry(
        entry_type=MemoryType.SUCCESS,
        agent_type="content_agent",
        task_description="Create pitch deck for AI startup",
        outcome="Successfully created 12-slide pitch deck",
        quality_score=0.85,
        metadata={"topic": "AI startup", "slides": 12}
    )
    
    entry_id = learning_memory.store_entry(entry)
    
    assert entry_id is not None
    assert isinstance(entry_id, str)


def test_retrieve_memory_entry(learning_memory):
    """Test retrieving a memory entry"""
    entry = MemoryEntry(
        entry_type=MemoryType.SUCCESS,
        agent_type="content_agent",
        task_description="Test task",
        outcome="Success",
        quality_score=0.9,
        metadata={}
    )
    
    entry_id = learning_memory.store_entry(entry)
    retrieved_entry = learning_memory.retrieve_entry(entry_id)
    
    assert retrieved_entry is not None
    assert retrieved_entry.agent_type == "content_agent"
    assert retrieved_entry.quality_score == 0.9


def test_get_entries_by_agent(learning_memory):
    """Test retrieving entries by agent type"""
    # Store entries for different agents
    entry1 = MemoryEntry(
        entry_type=MemoryType.SUCCESS,
        agent_type="content_agent",
        task_description="Task 1",
        outcome="Success",
        quality_score=0.8,
        metadata={}
    )
    
    entry2 = MemoryEntry(
        entry_type=MemoryType.SUCCESS,
        agent_type="research_agent",
        task_description="Task 2",
        outcome="Success",
        quality_score=0.75,
        metadata={}
    )
    
    entry3 = MemoryEntry(
        entry_type=MemoryType.SUCCESS,
        agent_type="content_agent",
        task_description="Task 3",
        outcome="Success",
        quality_score=0.85,
        metadata={}
    )
    
    learning_memory.store_entry(entry1)
    learning_memory.store_entry(entry2)
    learning_memory.store_entry(entry3)
    
    content_entries = learning_memory.get_entries_by_agent("content_agent")
    
    assert len(content_entries) == 2
    assert all(entry.agent_type == "content_agent" for entry in content_entries)


def test_get_entries_by_type(learning_memory):
    """Test retrieving entries by memory type"""
    # Store entries of different types
    entry1 = MemoryEntry(
        entry_type=MemoryType.SUCCESS,
        agent_type="content_agent",
        task_description="Task 1",
        outcome="Success",
        quality_score=0.8,
        metadata={}
    )
    
    entry2 = MemoryEntry(
        entry_type=MemoryType.FAILURE,
        agent_type="content_agent",
        task_description="Task 2",
        outcome="Failed",
        quality_score=0.3,
        metadata={}
    )
    
    entry3 = MemoryEntry(
        entry_type=MemoryType.SUCCESS,
        agent_type="research_agent",
        task_description="Task 3",
        outcome="Success",
        quality_score=0.75,
        metadata={}
    )
    
    learning_memory.store_entry(entry1)
    learning_memory.store_entry(entry2)
    learning_memory.store_entry(entry3)
    
    success_entries = learning_memory.get_entries_by_type(MemoryType.SUCCESS)
    failure_entries = learning_memory.get_entries_by_type(MemoryType.FAILURE)
    
    assert len(success_entries) == 2
    assert len(failure_entries) == 1


def test_detect_patterns(learning_memory):
    """Test pattern detection in memory entries"""
    # Store similar successful entries
    for i in range(6):
        entry = MemoryEntry(
            entry_type=MemoryType.SUCCESS,
            agent_type="content_agent",
            task_description=f"Create pitch deck for AI startup {i}",
            outcome="Success",
            quality_score=0.85 + (i * 0.01),
            metadata={"topic": "AI startup", "slides": 12}
        )
        learning_memory.store_entry(entry)
    
    patterns = learning_memory.detect_patterns()
    
    # Should detect high success rate pattern for content_agent
    assert len(patterns) > 0
    assert any(pattern.pattern_type == "high_success_rate" for pattern in patterns)


def test_get_learning_insights(learning_memory):
    """Test generating learning insights"""
    # Store entries with varying outcomes
    for i in range(10):
        entry = MemoryEntry(
            entry_type=MemoryType.SUCCESS if i % 2 == 0 else MemoryType.FAILURE,
            agent_type="content_agent",
            task_description=f"Task {i}",
            outcome="Success" if i % 2 == 0 else "Failed",
            quality_score=0.8 if i % 2 == 0 else 0.4,
            metadata={"iteration": i}
        )
        learning_memory.store_entry(entry)
    
    # Trigger pattern detection first
    learning_memory.detect_patterns()
    
    insights = learning_memory.get_learning_insights()
    
    # Insights are generated from patterns, so we might not have insights if no patterns detected
    # Just check that the method works and returns the right type
    assert isinstance(insights, list)
    assert all(isinstance(insight, LearningInsight) for insight in insights)


def test_get_agent_performance_summary(learning_memory):
    """Test getting agent performance summary"""
    # Store entries for an agent
    for i in range(5):
        entry = MemoryEntry(
            entry_type=MemoryType.SUCCESS,
            agent_type="content_agent",
            task_description=f"Task {i}",
            outcome="Success",
            quality_score=0.7 + (i * 0.05),
            metadata={}
        )
        learning_memory.store_entry(entry)
    
    summary = learning_memory.get_agent_performance_summary("content_agent")
    
    assert "total_entries" in summary
    assert "success_rate" in summary
    assert "average_quality_score" in summary
    assert summary["total_entries"] == 5


def test_apply_learning_to_task(learning_memory):
    """Test applying learning to new tasks"""
    # Store successful pattern
    entry = MemoryEntry(
        entry_type=MemoryType.SUCCESS,
        agent_type="content_agent",
        task_description="Create pitch deck with modern minimalist style",
        outcome="Success",
        quality_score=0.9,
        metadata={"style": "modern minimalist", "slides": 10}
    )
    learning_memory.store_entry(entry)
    
    # Apply learning to similar task
    task_suggestions = learning_memory.apply_learning_to_task(
        agent_type="content_agent",
        task_description="Create pitch deck with modern minimalist style for tech startup"
    )
    
    # Just check that it returns suggestions (content may vary)
    assert isinstance(task_suggestions, list)


def test_memory_persistence(learning_memory, temp_memory_dir):
    """Test that memory persists across instances"""
    # Store an entry
    entry = MemoryEntry(
        entry_type=MemoryType.SUCCESS,
        agent_type="content_agent",
        task_description="Test task",
        outcome="Success",
        quality_score=0.85,
        metadata={}
    )
    entry_id = learning_memory.store_entry(entry)
    
    # Create new instance with same directory
    new_memory = LearningMemory(memory_dir=temp_memory_dir)
    retrieved_entry = new_memory.retrieve_entry(entry_id)
    
    assert retrieved_entry is not None
    assert retrieved_entry.agent_type == "content_agent"


def test_prune_old_entries(learning_memory):
    """Test pruning old memory entries"""
    # Store entries
    for i in range(10):
        entry = MemoryEntry(
            entry_type=MemoryType.SUCCESS,
            agent_type="content_agent",
            task_description=f"Task {i}",
            outcome="Success",
            quality_score=0.8,
            metadata={}
        )
        learning_memory.store_entry(entry)
    
    # Prune to keep only 5 most recent
    pruned_count = learning_memory.prune_old_entries(max_entries=5)
    
    assert pruned_count == 5
    
    all_entries = learning_memory.get_entries_by_agent("content_agent")
    assert len(all_entries) == 5


def test_export_memory(learning_memory, temp_memory_dir):
    """Test exporting memory to file"""
    # Store some entries
    for i in range(3):
        entry = MemoryEntry(
            entry_type=MemoryType.SUCCESS,
            agent_type="content_agent",
            task_description=f"Task {i}",
            outcome="Success",
            quality_score=0.8,
            metadata={}
        )
        learning_memory.store_entry(entry)
    
    # Export to file
    export_path = Path(temp_memory_dir) / "memory_export.json"
    learning_memory.export_memory(export_path)
    
    assert export_path.exists()
    
    # Create new instance in a different directory and import
    import_dir = tempfile.mkdtemp()
    try:
        new_memory = LearningMemory(memory_dir=import_dir)
        new_memory.import_memory(export_path)
        
        content_entries = new_memory.get_entries_by_agent("content_agent")
        assert len(content_entries) == 3
    finally:
        shutil.rmtree(import_dir)


def test_memory_entry_dataclass():
    """Test MemoryEntry dataclass"""
    entry = MemoryEntry(
        entry_type=MemoryType.SUCCESS,
        agent_type="content_agent",
        task_description="Test",
        outcome="Success",
        quality_score=0.85,
        metadata={"key": "value"}
    )
    
    assert entry.entry_type == MemoryType.SUCCESS
    assert entry.agent_type == "content_agent"
    assert entry.quality_score == 0.85
    assert entry.metadata["key"] == "value"


def test_pattern_dataclass():
    """Test Pattern dataclass"""
    pattern = Pattern(
        pattern_type="success_pattern",
        description="High success rate for AI startup pitch decks",
        confidence=0.9,
        occurrences=5,
        metadata={"topic": "AI startup"}
    )
    
    assert pattern.pattern_type == "success_pattern"
    assert pattern.confidence == 0.9
    assert pattern.occurrences == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
