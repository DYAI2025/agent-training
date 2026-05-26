import pytest
import json
import os
import sys
import tempfile

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hyperparameter_pattern_manager import HyperparameterPatternManager

def test_success_pattern_creation():
    """Test creating success pattern from successful experiment"""
    manager = HyperparameterPatternManager()
    
    experiment_result = {
        "val_bpb": 0.997,
        "parameters": {
            "learning_rate": 0.04,
            "depth": 8,
            "batch_size": 64
        },
        "quality_score": 0.85
    }
    
    pattern = manager.create_success_pattern(experiment_result, "exp_001")
    
    assert pattern["pattern_type"] == "success"
    assert pattern["learning_rate"] == 0.04
    assert pattern["quality_score"] == 0.85

def test_anti_pattern_creation():
    """Test creating anti-pattern from failed experiment"""
    manager = HyperparameterPatternManager()
    
    experiment_result = {
        "val_bpb": 1.5,  # Poor result
        "parameters": {
            "learning_rate": 0.1,  # Too high
            "depth": 16  # Too deep for hardware
        },
        "error": "OOM error"
    }
    
    pattern = manager.create_anti_pattern(experiment_result, "exp_002")
    
    assert pattern["pattern_type"] == "anti"
    assert pattern["symptoms"] == ["OOM error"]
    assert "mitigation" in pattern

def test_pattern_retrieval_for_optimization():
    """Test retrieving patterns for hyperparameter optimization"""
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = HyperparameterPatternManager(patterns_path=temp_dir)
        
        # Add some patterns
        manager.save_success_pattern({
            "learning_rate": 0.04,
            "depth": 8,
            "quality_score": 0.85
        })
        
        manager.save_anti_pattern({
            "learning_rate": 0.1,
            "depth": 16,
            "symptoms": ["OOM error"]
        })
        
        # Get optimization suggestions
        suggestions = manager.get_optimization_suggestions({
            "learning_rate": 0.03,
            "depth": 8
        })
        
        assert len(suggestions) > 0
        assert any("learning_rate" in s for s in suggestions)
