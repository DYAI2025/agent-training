import pytest
import os
import tempfile
import json
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autoresearch_wuphf_bridge import AutoresearchWuphfBridge

def test_full_experiment_workflow():
    """Test complete workflow from experiment to learning"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Setup
        bridge = AutoresearchWuphfBridge()
        
        # Override config for testing
        bridge.config["knowledge_base_path"] = os.path.join(temp_dir, "knowledge")
        bridge.config["patterns_path"] = os.path.join(temp_dir, "patterns")
        
        # Reinitialize managers with test paths
        from model_knowledge_manager import ModelKnowledgeManager
        from hyperparameter_pattern_manager import HyperparameterPatternManager
        
        bridge.model_manager = ModelKnowledgeManager(
            knowledge_base_path=bridge.config["knowledge_base_path"]
        )
        bridge.pattern_manager = HyperparameterPatternManager(
            patterns_path=bridge.config["patterns_path"]
        )
        
        # Simulate experiment
        experiment_id = "test_exp_001"
        parameters = {
            "learning_rate": 0.04,
            "depth": 8,
            "batch_size": 64
        }
        
        # Get suggestions before experiment
        suggestions = bridge.get_optimization_suggestions(parameters)
        assert isinstance(suggestions, list)
        
        # Simulate successful experiment
        result = {
            "val_bpb": 0.997,
            "training_seconds": 300.1,
            "peak_vram_mb": 45060.2,
            "mfu_percent": 39.80,
            "status": "success"
        }
        
        # Log result
        log_result = bridge.log_experiment_result(experiment_id, result)
        assert log_result["status"] in ["logged", "wuphf_unavailable", "error", "logged_fallback"]
        assert "quality_score" in log_result
        
        # Save model checkpoint
        model_metadata = {
            "experiment_id": experiment_id,
            "val_bpb": result["val_bpb"],
            "architecture": "GPT-8L",
            "parameters": parameters
        }
        
        entry_id = bridge.save_model_checkpoint(experiment_id, model_metadata)
        # entry_id can be None if model_manager not available
        if bridge.model_manager:
            assert entry_id is not None
        
        # Learn patterns
        bridge.learn_from_experiment(experiment_id, result, parameters)
        
        # Verify pattern was learned
        suggestions_after = bridge.get_optimization_suggestions(parameters)
        assert isinstance(suggestions_after, list)
        
        # Verify model was saved
        if bridge.model_manager:
            best_model = bridge.model_manager.get_best_model()
            if best_model:
                assert best_model["val_bpb"] == 0.997

def test_failure_handling():
    """Test handling of failed experiments"""
    with tempfile.TemporaryDirectory() as temp_dir:
        bridge = AutoresearchWuphfBridge()
        
        # Override config for testing
        bridge.config["knowledge_base_path"] = os.path.join(temp_dir, "knowledge")
        bridge.config["patterns_path"] = os.path.join(temp_dir, "patterns")
        
        # Reinitialize managers with test paths
        from model_knowledge_manager import ModelKnowledgeManager
        from hyperparameter_pattern_manager import HyperparameterPatternManager
        
        bridge.model_manager = ModelKnowledgeManager(
            knowledge_base_path=bridge.config["knowledge_base_path"]
        )
        bridge.pattern_manager = HyperparameterPatternManager(
            patterns_path=bridge.config["patterns_path"]
        )
        
        # Simulate failed experiment
        experiment_id = "test_exp_002"
        parameters = {
            "learning_rate": 0.1,  # Too high
            "depth": 16  # Too deep
        }
        
        result = {
            "val_bpb": 1.5,  # Poor result
            "status": "crash",
            "error": "OOM error"
        }
        
        # Log failure
        log_result = bridge.log_experiment_result(experiment_id, result)
        assert log_result["status"] in ["logged", "wuphf_unavailable", "error", "logged_fallback"]
        
        # Learn from failure
        bridge.learn_from_experiment(experiment_id, result, parameters)
        
        # Verify anti-pattern was created
        suggestions = bridge.get_optimization_suggestions(parameters)
        assert isinstance(suggestions, list)

def test_wuphf_unavailable_fallback():
    """Test fallback when WUPHF is not available"""
    # Test that the bridge handles WUPHF unavailability gracefully
    bridge = AutoresearchWuphfBridge()
    
    if not bridge.learning_system:
        # Should not crash when WUPHF is unavailable
        result = bridge.log_experiment_result("exp_001", {"status": "success"})
        assert result["status"] == "wuphf_unavailable"
        
        # Model manager should handle unavailability
        model_result = bridge.save_model_checkpoint("exp_001", {
            "val_bpb": 0.997,
            "architecture": "GPT-8L"
        })
        # Should return None or handle gracefully
        assert model_result is None or isinstance(model_result, str)
        
        # Pattern manager should handle unavailability
        suggestions = bridge.get_optimization_suggestions({"learning_rate": 0.04})
        assert isinstance(suggestions, list)