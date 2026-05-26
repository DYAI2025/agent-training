import sys
import os
import json
from typing import Dict, Any, Optional
from datetime import datetime

# Add WUPHF providers to path
WUPHF_PATH = os.path.expanduser("~/.wuphf")
sys.path.insert(0, os.path.join(WUPHF_PATH, "providers"))

try:
    from agent_learning_system import get_learning_system
    WUPHF_AVAILABLE = True
except ImportError:
    WUPHF_AVAILABLE = False
    print("Warning: WUPHF Learning System not available, running in standalone mode")


class AutoresearchWuphfBridge:
    """Bridge between autoresearch experiments and WUPHF learning system"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the bridge with WUPHF learning system"""
        self.config = self._load_config(config_path)
        self.learning_system = None
        self.knowledge_manager = None
        
        if WUPHF_AVAILABLE:
            try:
                self.learning_system = get_learning_system()
                self.knowledge_manager = getattr(self.learning_system, 'knowledge_manager', None)
                print("✓ WUPHF Learning System connected")
            except Exception as e:
                print(f"Warning: Could not initialize WUPHF Learning System: {e}")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        default_config = {
            "task_type": "llm_training_experiment",
            "expected_duration": 300,  # 5 minutes
            "target_metric": "val_bpb",
            "quality_threshold": 0.7,
            "enable_pattern_learning": True,
            "enable_knowledge_consolidation": True
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def experiment_to_task_context(self, experiment_config: Dict[str, Any]) -> Dict[str, Any]:
        """Convert autoresearch experiment to WUPHF task context"""
        return {
            "task_type": self.config["task_type"],
            "expected_duration": self.config["expected_duration"],
            "target_metric": self.config["target_metric"],
            "experiment_description": experiment_config.get("description", ""),
            "modifications": experiment_config.get("train_py_modifications", {}),
            "timestamp": datetime.now().isoformat()
        }
    
    def log_experiment_result(self, experiment_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Log experiment result to WUPHF learning system"""
        if not self.learning_system:
            return {"quality_score": 0.5, "status": "wuphf_unavailable"}
        
        try:
            # Calculate quality score based on metrics
            quality_score = self._calculate_quality_score(result)
            
            # Complete the task with self-reflection
            assessment = self.learning_system.complete_task(
                success=result.get("status") == "success",
                context={
                    "experiment_id": experiment_id,
                    "val_bpb": result.get("val_bpb"),
                    "memory_gb": result.get("peak_vram_mb", 0) / 1024,
                    "training_time": result.get("training_seconds", 0),
                    "quality_score": quality_score
                }
            )
            
            return {
                "quality_score": quality_score,
                "assessment": assessment,
                "status": "logged"
            }
        except Exception as e:
            print(f"Error logging to WUPHF: {e}")
            return {"quality_score": 0.5, "status": "error", "error": str(e)}
    
    def _calculate_quality_score(self, result: Dict[str, Any]) -> float:
        """Calculate quality score from experiment metrics"""
        # Base score from val_bpb (lower is better, normalize around 1.0)
        val_bpb = result.get("val_bpb", 1.0)
        bpb_score = max(0.0, 1.0 - (val_bpb - 0.9))  # 0.9 is excellent, >1.9 is poor
        
        # Memory efficiency (prefer lower memory usage)
        memory_gb = result.get("peak_vram_mb", 0) / 1024
        memory_score = max(0.0, 1.0 - (memory_gb / 80.0))  # 80GB is poor
        
        # Training efficiency (MFU - Model FLOPs Utilization)
        mfu = result.get("mfu_percent", 0) / 100
        efficiency_score = mfu
        
        # Weighted average
        weights = {"bpb": 0.5, "memory": 0.3, "efficiency": 0.2}
        quality_score = (
            weights["bpb"] * bpb_score +
            weights["memory"] * memory_score +
            weights["efficiency"] * efficiency_score
        )
        
        return max(0.0, min(1.0, quality_score))
