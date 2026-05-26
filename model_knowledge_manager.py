import json
import os
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

class ModelKnowledgeManager:
    """Manager for storing and retrieving model checkpoints in WUPHF knowledge base"""
    
    def __init__(self, knowledge_base_path: Optional[str] = None):
        """Initialize model knowledge manager"""
        self.knowledge_base_path = knowledge_base_path or os.path.expanduser("~/.wuphf/knowledge_base")
        self.episodic_path = os.path.join(self.knowledge_base_path, "episodic")
        self.semantic_path = os.path.join(self.knowledge_base_path, "semantic")
        
        # Ensure directories exist
        os.makedirs(self.episodic_path, exist_ok=True)
        os.makedirs(self.semantic_path, exist_ok=True)
    
    def create_model_entry(self, model_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create a knowledge base entry for a model checkpoint"""
        entry_id = str(uuid.uuid4())[:8]
        
        entry = {
            "entry_id": entry_id,
            "entry_type": "model_checkpoint",
            "timestamp": datetime.now().isoformat(),
            "experiment_id": model_metadata.get("experiment_id", "unknown"),
            "val_bpb": model_metadata.get("val_bpb"),
            "architecture": model_metadata.get("architecture", "unknown"),
            "parameters": model_metadata.get("parameters", {}),
            "metrics": {
                "training_seconds": model_metadata.get("training_seconds"),
                "peak_vram_mb": model_metadata.get("peak_vram_mb"),
                "mfu_percent": model_metadata.get("mfu_percent")
            },
            "quality_score": model_metadata.get("quality_score")
        }
        
        return entry
    
    def save_model_metadata(self, model_metadata: Dict[str, Any]) -> str:
        """Save model metadata to episodic memory"""
        entry = self.create_model_entry(model_metadata)
        entry_id = entry["entry_id"]
        
        file_path = os.path.join(self.episodic_path, f"model_{entry_id}.json")
        
        with open(file_path, 'w') as f:
            json.dump(entry, f, indent=2)
        
        # Update index
        self._update_index(entry_id, entry)
        
        return entry_id
    
    def _update_index(self, entry_id: str, entry: Dict[str, Any]):
        """Update the episodic memory index"""
        index_path = os.path.join(self.episodic_path, "index.json")
        
        index = {}
        if os.path.exists(index_path):
            with open(index_path, 'r') as f:
                index = json.load(f)
        
        index[entry_id] = {
            "entry_type": entry["entry_type"],
            "timestamp": entry["timestamp"],
            "val_bpb": entry["val_bpb"],
            "experiment_id": entry["experiment_id"]
        }
        
        with open(index_path, 'w') as f:
            json.dump(index, f, indent=2)
    
    def get_best_model(self, top_n: int = 1) -> Optional[Dict[str, Any]]:
        """Retrieve the best model(s) from knowledge base"""
        index_path = os.path.join(self.episodic_path, "index.json")
        
        if not os.path.exists(index_path):
            return None
        
        with open(index_path, 'r') as f:
            index = json.load(f)
        
        # Filter model checkpoints and sort by val_bpb
        models = [
            (entry_id, data) 
            for entry_id, data in index.items() 
            if data.get("entry_type") == "model_checkpoint"
        ]
        
        if not models:
            return None
        
        # Sort by val_bpb (lower is better)
        models.sort(key=lambda x: x[1]["val_bpb"])
        
        if top_n == 1:
            best_entry_id = models[0][0]
            return self._load_entry(best_entry_id)
        else:
            return [self._load_entry(entry_id) for entry_id, _ in models[:top_n]]
    
    def _load_entry(self, entry_id: str) -> Dict[str, Any]:
        """Load a specific entry from episodic memory"""
        file_path = os.path.join(self.episodic_path, f"model_{entry_id}.json")
        
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def search_models(self, query: str, min_quality: float = 0.0) -> List[Dict[str, Any]]:
        """Search models by description or parameters"""
        index_path = os.path.join(self.episodic_path, "index.json")
        
        if not os.path.exists(index_path):
            return []
        
        with open(index_path, 'r') as f:
            index = json.load(f)
        
        results = []
        query_lower = query.lower()
        
        for entry_id, data in index.items():
            if data.get("entry_type") != "model_checkpoint":
                continue
            
            # Load full entry for detailed search
            entry = self._load_entry(entry_id)
            
            # Quality filter
            if entry.get("quality_score", 0) < min_quality:
                continue
            
            # Text search
            searchable_text = f"{entry.get('architecture', '')} {entry.get('experiment_id', '')}"
            if query_lower in searchable_text.lower():
                results.append(entry)
        
        return results
