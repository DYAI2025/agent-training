import pytest
import json
import os
import sys
import tempfile
import shutil

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model_knowledge_manager import ModelKnowledgeManager

def test_model_metadata_creation():
    """Test creating model metadata for knowledge base"""
    manager = ModelKnowledgeManager()
    
    model_metadata = {
        "experiment_id": "exp_001",
        "val_bpb": 0.997,
        "architecture": "GPT-8L",
        "parameters": {
            "depth": 8,
            "learning_rate": 0.04
        }
    }
    
    entry = manager.create_model_entry(model_metadata)
    
    assert entry["entry_type"] == "model_checkpoint"
    assert entry["val_bpb"] == 0.997
    assert "timestamp" in entry

def test_model_save_to_knowledge_base():
    """Test saving model metadata to WUPHF knowledge base"""
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = ModelKnowledgeManager(knowledge_base_path=temp_dir)
        
        model_metadata = {
            "experiment_id": "exp_001",
            "val_bpb": 0.997,
            "architecture": "GPT-8L"
        }
        
        entry_id = manager.save_model_metadata(model_metadata)
        
        # Verify file was created
        expected_path = os.path.join(temp_dir, "episodic", f"model_{entry_id}.json")
        assert os.path.exists(expected_path)
        
        # Verify content
        with open(expected_path, 'r') as f:
            saved_data = json.load(f)
        
        assert saved_data["val_bpb"] == 0.997

def test_best_model_retrieval():
    """Test retrieving best model from knowledge base"""
    with tempfile.TemporaryDirectory() as temp_dir:
        manager = ModelKnowledgeManager(knowledge_base_path=temp_dir)
        
        # Save multiple models
        for i, val_bpb in enumerate([1.2, 0.997, 1.1, 0.985]):
            manager.save_model_metadata({
                "experiment_id": f"exp_{i}",
                "val_bpb": val_bpb,
                "architecture": "GPT-8L"
            })
        
        best_model = manager.get_best_model()
        
        assert best_model["val_bpb"] == 0.985  # Lowest val_bpb
