import pytest
import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autoresearch_wuphf_bridge import AutoresearchWuphfBridge, WUPHF_AVAILABLE

def test_bridge_initialization():
    """Test that bridge initializes with WUPHF learning system"""
    bridge = AutoresearchWuphfBridge()
    
    if WUPHF_AVAILABLE:
        assert bridge.learning_system is not None
        # knowledge_manager may or may not be available depending on WUPHF version
        assert bridge.config is not None
    else:
        # When WUPHF is not available, bridge should still initialize
        assert bridge is not None
        assert bridge.config is not None

def test_experiment_to_task_conversion():
    """Test converting autoresearch experiment to WUPHF task"""
    bridge = AutoresearchWuphfBridge()
    
    experiment_config = {
        "description": "Increase learning rate to 0.04",
        "train_py_modifications": {
            "LEARNING_RATE": 0.04
        }
    }
    
    task_context = bridge.experiment_to_task_context(experiment_config)
    
    assert task_context["task_type"] == "llm_training_experiment"
    assert "expected_duration" in task_context
    assert "target_metric" in task_context

def test_result_logging():
    """Test logging experiment results to WUPHF learning system"""
    bridge = AutoresearchWuphfBridge()
    
    experiment_result = {
        "val_bpb": 0.997,
        "training_seconds": 300.1,
        "peak_vram_mb": 45060.2,
        "mfu_percent": 39.80,
        "status": "success"
    }
    
    if WUPHF_AVAILABLE:
        # Mock the learning system for testing
        bridge.learning_system.start_task = lambda x, y: None
        bridge.learning_system.log_tool_usage = lambda x: None
        bridge.learning_system.complete_task = lambda **kwargs: {"quality_score": 0.85}
        
        result = bridge.log_experiment_result("exp_001", experiment_result)
        
        assert result["quality_score"] >= 0.0
        assert result["quality_score"] <= 1.0
    else:
        # When WUPHF is not available, should return default score
        result = bridge.log_experiment_result("exp_001", experiment_result)
        
        assert result["quality_score"] >= 0.0
        assert result["quality_score"] <= 1.0
        assert result["status"] == "wuphf_unavailable"
