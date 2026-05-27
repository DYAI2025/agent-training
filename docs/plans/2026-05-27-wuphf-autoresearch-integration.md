# WUPHF Learning System + autoresearch Integration Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Integriere autoresearch als spezialisierte Experiment-Engine in das WUPHF Learning System für zwei-Ebenen autonomes Lernen (Mikro: Modelloptimierung, Makro: Prozessoptimierung).

**Architecture:** WUPHF Learning System als Orchestrierer und Lern-Engine, autoresearch als Experiment-Engine, WUPHF Knowledge Base als Modellspeicher, WUPHF Pattern Library als Hyperparameter-Optimierer.

**Tech Stack:** Python 3.10+, WUPHF Learning System (agent_learning_system.py), autoresearch (train.py, prepare.py), PyTorch, JSON-based Knowledge Base.

---

## Task 1: Autoresearch-WUPHF Bridge Component

**Files:**
- Create: `autoresearch_wuphf_bridge.py` (main integration layer)
- Create: `autoresearch_wuphf_config.py` (configuration management)
- Test: `tests/test_autoresearch_wuphf_bridge.py`

**Step 1: Write the failing test**

```python
# tests/test_autoresearch_wuphf_bridge.py
import pytest
import json
import os
from autoresearch_wuphf_bridge import AutoresearchWuphfBridge

def test_bridge_initialization():
    """Test that bridge initializes with WUPHF learning system"""
    bridge = AutoresearchWuphfBridge()
    assert bridge.learning_system is not None
    assert bridge.knowledge_manager is not None

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
    
    # Mock the learning system for testing
    bridge.learning_system.start_task = lambda x, y: None
    bridge.learning_system.log_tool_usage = lambda x: None
    bridge.learning_system.complete_task = lambda **kwargs: {"quality_score": 0.85}
    
    result = bridge.log_experiment_result("exp_001", experiment_result)
    
    assert result["quality_score"] >= 0.0
    assert result["quality_score"] <= 1.0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_autoresearch_wuphf_bridge.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'autoresearch_wuphf_bridge'"

**Step 3: Write minimal implementation**

```python
# autoresearch_wuphf_bridge.py
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
                self.knowledge_manager = self.learning_system.knowledge_manager
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
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_autoresearch_wuphf_bridge.py -v`
Expected: PASS (some tests may skip if WUPHF not available)

**Step 5: Commit**

```bash
git add autoresearch_wuphf_bridge.py tests/test_autoresearch_wuphf_bridge.py
git commit -m "feat: add WUPHF learning system bridge component"
```

---

## Task 2: Configuration Management

**Files:**
- Create: `autoresearch_wuphf_config.py`
- Modify: `autoresearch_wuphf_bridge.py` (add config loading)
- Test: `tests/test_autoresearch_wuphf_config.py`

**Step 1: Write the failing test**

```python
# tests/test_autoresearch_wuphf_config.py
import pytest
import json
import os
import tempfile
from autoresearch_wuphf_config import AutoresearchWuphfConfig

def test_default_config():
    """Test that default configuration is loaded correctly"""
    config = AutoresearchWuphfConfig()
    assert config.task_type == "llm_training_experiment"
    assert config.expected_duration == 300
    assert config.target_metric == "val_bpb"

def test_custom_config_loading():
    """Test loading custom configuration from file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        custom_config = {
            "task_type": "custom_experiment",
            "expected_duration": 600,
            "quality_threshold": 0.8
        }
        json.dump(custom_config, f)
        temp_path = f.name
    
    try:
        config = AutoresearchWuphfConfig(config_path=temp_path)
        assert config.task_type == "custom_experiment"
        assert config.expected_duration == 600
        assert config.quality_threshold == 0.8
    finally:
        os.unlink(temp_path)

def test_config_validation():
    """Test that invalid configuration raises errors"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        invalid_config = {
            "expected_duration": -100,  # Invalid: negative duration
            "quality_threshold": 1.5   # Invalid: > 1.0
        }
        json.dump(invalid_config, f)
        temp_path = f.name
    
    try:
        with pytest.raises(ValueError):
            config = AutoresearchWuphfConfig(config_path=temp_path)
    finally:
        os.unlink(temp_path)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_autoresearch_wuphf_config.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'autoresearch_wuphf_config'"

**Step 3: Write minimal implementation**

```python
# autoresearch_wuphf_config.py
import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class AutoresearchWuphfConfig:
    """Configuration for autoresearch-WUPHF integration"""
    
    # Task configuration
    task_type: str = "llm_training_experiment"
    expected_duration: int = 300  # seconds
    target_metric: str = "val_bpb"
    
    # Quality thresholds
    quality_threshold: float = 0.7
    min_success_rate: float = 0.6
    
    # Learning features
    enable_pattern_learning: bool = True
    enable_knowledge_consolidation: bool = True
    enable_failure_analysis: bool = True
    
    # WUPHF paths
    wuphf_path: str = os.path.expanduser("~/.wuphf")
    knowledge_base_path: str = None
    patterns_path: str = None
    
    def __post_init__(self):
        """Set default paths and validate configuration"""
        if self.knowledge_base_path is None:
            self.knowledge_base_path = os.path.join(self.wuphf_path, "knowledge_base")
        if self.patterns_path is None:
            self.patterns_path = os.path.join(self.wuphf_path, "patterns")
        
        self._validate_config()
    
    def _validate_config(self):
        """Validate configuration values"""
        if self.expected_duration <= 0:
            raise ValueError(f"expected_duration must be positive, got {self.expected_duration}")
        
        if not 0.0 <= self.quality_threshold <= 1.0:
            raise ValueError(f"quality_threshold must be between 0.0 and 1.0, got {self.quality_threshold}")
        
        if not 0.0 <= self.min_success_rate <= 1.0:
            raise ValueError(f"min_success_rate must be between 0.0 and 1.0, got {self.min_success_rate}")
    
    @classmethod
    def from_file(cls, config_path: str) -> 'AutoresearchWuphfConfig':
        """Load configuration from JSON file"""
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        return cls(**config_data)
    
    def to_file(self, config_path: str):
        """Save configuration to JSON file"""
        config_dict = {
            "task_type": self.task_type,
            "expected_duration": self.expected_duration,
            "target_metric": self.target_metric,
            "quality_threshold": self.quality_threshold,
            "min_success_rate": self.min_success_rate,
            "enable_pattern_learning": self.enable_pattern_learning,
            "enable_knowledge_consolidation": self.enable_knowledge_consolidation,
            "enable_failure_analysis": self.enable_failure_analysis,
            "wuphf_path": self.wuphf_path,
            "knowledge_base_path": self.knowledge_base_path,
            "patterns_path": self.patterns_path
        }
        
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "task_type": self.task_type,
            "expected_duration": self.expected_duration,
            "target_metric": self.target_metric,
            "quality_threshold": self.quality_threshold,
            "min_success_rate": self.min_success_rate,
            "enable_pattern_learning": self.enable_pattern_learning,
            "enable_knowledge_consolidation": self.enable_knowledge_consolidation,
            "enable_failure_analysis": self.enable_failure_analysis
        }
```

**Step 4: Update bridge to use config**

```python
# Modify autoresearch_wuphf_bridge.py
from autoresearch_wuphf_config import AutoresearchWuphfConfig

class AutoresearchWuphfBridge:
    def __init__(self, config: Optional[AutoresearchWuphfConfig] = None):
        """Initialize the bridge with WUPHF learning system"""
        self.config = config or AutoresearchWuphfConfig()
        # ... rest of initialization
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_autoresearch_wuphf_config.py -v`
Expected: PASS

**Step 6: Commit**

```bash
git add autoresearch_wuphf_config.py tests/test_autoresearch_wuphf_config.py autoresearch_wuphf_bridge.py
git commit -m "feat: add configuration management for WUPHF integration"
```

---

## Task 3: Knowledge Base Integration for Model Checkpoints

**Files:**
- Create: `model_knowledge_manager.py`
- Modify: `autoresearch_wuphf_bridge.py` (add model saving)
- Test: `tests/test_model_knowledge_manager.py`

**Step 1: Write the failing test**

```python
# tests/test_model_knowledge_manager.py
import pytest
import json
import os
import tempfile
import shutil
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
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_model_knowledge_manager.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'model_knowledge_manager'"

**Step 3: Write minimal implementation**

```python
# model_knowledge_manager.py
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
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_model_knowledge_manager.py -v`
Expected: PASS

**Step 5: Integrate into bridge**

```python
# Modify autoresearch_wuphf_bridge.py
from model_knowledge_manager import ModelKnowledgeManager

class AutoresearchWuphfBridge:
    def __init__(self, config: Optional[AutoresearchWuphfConfig] = None):
        """Initialize the bridge with WUPHF learning system"""
        self.config = config or AutoresearchWuphfConfig()
        self.learning_system = None
        self.knowledge_manager = None
        self.model_manager = None
        
        if WUPHF_AVAILABLE:
            try:
                self.learning_system = get_learning_system()
                self.knowledge_manager = self.learning_system.knowledge_manager
                self.model_manager = ModelKnowledgeManager(
                    knowledge_base_path=self.config.knowledge_base_path
                )
                print("✓ WUPHF Learning System connected")
            except Exception as e:
                print(f"Warning: Could not initialize WUPHF Learning System: {e}")
    
    def save_model_checkpoint(self, experiment_id: str, model_metadata: Dict[str, Any]) -> str:
        """Save model checkpoint metadata to knowledge base"""
        if not self.model_manager:
            print("Warning: Model manager not available")
            return None
        
        try:
            entry_id = self.model_manager.save_model_metadata(model_metadata)
            print(f"✓ Model checkpoint saved: {entry_id}")
            return entry_id
        except Exception as e:
            print(f"Error saving model checkpoint: {e}")
            return None
```

**Step 6: Commit**

```bash
git add model_knowledge_manager.py tests/test_model_knowledge_manager.py autoresearch_wuphf_bridge.py
git commit -m "feat: add model knowledge base integration"
```

---

## Task 4: Pattern Library for Hyperparameter Optimization

**Files:**
- Create: `hyperparameter_pattern_manager.py`
- Modify: `autoresearch_wuphf_bridge.py` (add pattern learning)
- Test: `tests/test_hyperparameter_pattern_manager.py`

**Step 1: Write the failing test**

```python
# tests/test_hyperparameter_pattern_manager.py
import pytest
import json
import os
import tempfile
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
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_hyperparameter_pattern_manager.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'hyperparameter_pattern_manager'"

**Step 3: Write minimal implementation**

```python
# hyperparameter_pattern_manager.py
import json
import os
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import defaultdict

class HyperparameterPatternManager:
    """Manager for hyperparameter patterns in WUPHF pattern library"""
    
    def __init__(self, patterns_path: Optional[str] = None):
        """Initialize pattern manager"""
        self.patterns_path = patterns_path or os.path.expanduser("~/.wuphf/patterns")
        self.success_patterns_file = os.path.join(self.patterns_path, "success_patterns.json")
        self.anti_patterns_file = os.path.join(self.patterns_path, "anti_patterns.json")
        
        # Ensure directory exists
        os.makedirs(self.patterns_path, exist_ok=True)
        
        # Load existing patterns
        self.success_patterns = self._load_patterns(self.success_patterns_file)
        self.anti_patterns = self._load_patterns(self.anti_patterns_file)
    
    def _load_patterns(self, file_path: str) -> List[Dict[str, Any]]:
        """Load patterns from file"""
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return []
    
    def _save_patterns(self, patterns: List[Dict[str, Any]], file_path: str):
        """Save patterns to file"""
        with open(file_path, 'w') as f:
            json.dump(patterns, f, indent=2)
    
    def create_success_pattern(self, experiment_result: Dict[str, Any], experiment_id: str) -> Dict[str, Any]:
        """Create a success pattern from a successful experiment"""
        parameters = experiment_result.get("parameters", {})
        
        pattern = {
            "pattern_id": str(uuid.uuid4())[:8],
            "pattern_type": "success",
            "experiment_id": experiment_id,
            "timestamp": datetime.now().isoformat(),
            "parameters": parameters,
            "quality_score": experiment_result.get("quality_score", 0.5),
            "val_bpb": experiment_result.get("val_bpb"),
            "usage_count": 0,
            "success_rate": 1.0  # Will be updated with more data
        }
        
        return pattern
    
    def create_anti_pattern(self, experiment_result: Dict[str, Any], experiment_id: str) -> Dict[str, Any]:
        """Create an anti-pattern from a failed experiment"""
        parameters = experiment_result.get("parameters", {})
        error = experiment_result.get("error", "Unknown error")
        
        pattern = {
            "pattern_id": str(uuid.uuid4())[:8],
            "pattern_type": "anti",
            "experiment_id": experiment_id,
            "timestamp": datetime.now().isoformat(),
            "parameters": parameters,
            "symptoms": [error] if isinstance(error, str) else error,
            "mitigation": self._generate_mitigation(parameters, error),
            "usage_count": 0
        }
        
        return pattern
    
    def _generate_mitigation(self, parameters: Dict[str, Any], error: str) -> str:
        """Generate mitigation strategy for anti-pattern"""
        mitigations = {
            "OOM error": "Reduce model depth or batch size",
            "NaN loss": "Lower learning rate or add gradient clipping",
            "Training too slow": "Increase batch size or reduce model complexity",
            "Poor convergence": "Adjust learning rate or use different optimizer"
        }
        
        for symptom, mitigation in mitigations.items():
            if symptom.lower() in error.lower():
                return mitigation
        
        return "Review hyperparameters and model architecture"
    
    def save_success_pattern(self, pattern: Dict[str, Any]):
        """Save success pattern to library"""
        self.success_patterns.append(pattern)
        self._save_patterns(self.success_patterns, self.success_patterns_file)
    
    def save_anti_pattern(self, pattern: Dict[str, Any]):
        """Save anti-pattern to library"""
        self.anti_patterns.append(pattern)
        self._save_patterns(self.anti_patterns, self.anti_patterns_file)
    
    def get_optimization_suggestions(self, current_parameters: Dict[str, Any]) -> List[str]:
        """Get optimization suggestions based on patterns"""
        suggestions = []
        
        # Check against anti-patterns
        for anti_pattern in self.anti_patterns:
            if self._parameters_match(current_parameters, anti_pattern["parameters"]):
                suggestions.append(f"⚠️ AVOID: {anti_pattern['mitigation']}")
        
        # Check success patterns for improvements
        for success_pattern in self.success_patterns:
            if success_pattern.get("quality_score", 0) > 0.8:
                for param, value in success_pattern["parameters"].items():
                    if param in current_parameters:
                        if current_parameters[param] != value:
                            suggestions.append(
                                f"💡 CONSIDER: Set {param} to {value} "
                                f"(quality: {success_pattern['quality_score']:.2f})"
                            )
        
        return suggestions
    
    def _parameters_match(self, params1: Dict[str, Any], params2: Dict[str, Any], tolerance: float = 0.1) -> bool:
        """Check if parameters match within tolerance"""
        for key, value1 in params1.items():
            if key not in params2:
                continue
            
            value2 = params2[key]
            
            if isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
                if abs(value1 - value2) > tolerance * max(abs(value1), abs(value2)):
                    return False
            elif value1 != value2:
                return False
        
        return True
    
    def get_best_parameters(self, param_name: str) -> Optional[Any]:
        """Get best value for a specific parameter from success patterns"""
        if not self.success_patterns:
            return None
        
        # Extract values for the parameter
        param_values = []
        for pattern in self.success_patterns:
            if param_name in pattern["parameters"]:
                param_values.append((
                    pattern["parameters"][param_name],
                    pattern.get("quality_score", 0)
                ))
        
        if not param_values:
            return None
        
        # Return value with highest quality score
        param_values.sort(key=lambda x: x[1], reverse=True)
        return param_values[0][0]
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_hyperparameter_pattern_manager.py -v`
Expected: PASS

**Step 5: Integrate into bridge**

```python
# Modify autoresearch_wuphf_bridge.py
from hyperparameter_pattern_manager import HyperparameterPatternManager

class AutoresearchWuphfBridge:
    def __init__(self, config: Optional[AutoresearchWuphfConfig] = None):
        """Initialize the bridge with WUPHF learning system"""
        self.config = config or AutoresearchWuphfConfig()
        self.learning_system = None
        self.knowledge_manager = None
        self.model_manager = None
        self.pattern_manager = None
        
        if WUPHF_AVAILABLE:
            try:
                self.learning_system = get_learning_system()
                self.knowledge_manager = self.learning_system.knowledge_manager
                self.model_manager = ModelKnowledgeManager(
                    knowledge_base_path=self.config.knowledge_base_path
                )
                self.pattern_manager = HyperparameterPatternManager(
                    patterns_path=self.config.patterns_path
                )
                print("✓ WUPHF Learning System connected")
            except Exception as e:
                print(f"Warning: Could not initialize WUPHF Learning System: {e}")
    
    def learn_from_experiment(self, experiment_id: str, result: Dict[str, Any], parameters: Dict[str, Any]):
        """Learn from experiment result using pattern library"""
        if not self.pattern_manager or not self.config.enable_pattern_learning:
            return
        
        try:
            experiment_data = {
                "val_bpb": result.get("val_bpb"),
                "parameters": parameters,
                "quality_score": result.get("quality_score", 0.5)
            }
            
            if result.get("status") == "success":
                pattern = self.pattern_manager.create_success_pattern(experiment_data, experiment_id)
                self.pattern_manager.save_success_pattern(pattern)
                print(f"✓ Success pattern learned from {experiment_id}")
            else:
                experiment_data["error"] = result.get("error", "Unknown error")
                pattern = self.pattern_manager.create_anti_pattern(experiment_data, experiment_id)
                self.pattern_manager.save_anti_pattern(pattern)
                print(f"✓ Anti-pattern learned from {experiment_id}")
        except Exception as e:
            print(f"Error learning from experiment: {e}")
    
    def get_optimization_suggestions(self, current_parameters: Dict[str, Any]) -> List[str]:
        """Get hyperparameter optimization suggestions"""
        if not self.pattern_manager:
            return []
        
        return self.pattern_manager.get_optimization_suggestions(current_parameters)
```

**Step 6: Commit**

```bash
git add hyperparameter_pattern_manager.py tests/test_hyperparameter_pattern_manager.py autoresearch_wuphf_bridge.py
git commit -m "feat: add hyperparameter pattern library integration"
```

---

## Task 5: Enhanced program.md for WUPHF Integration

**Files:**
- Modify: `program.md` (add WUPHF integration instructions)
- Create: `program_wuphf_enhanced.md` (standalone enhanced version)

**Step 1: Read current program.md**

```bash
cat program.md
```

**Step 2: Create enhanced version with WUPHF integration**

```markdown
# autoresearch with WUPHF Learning System Integration

This is an enhanced version of autoresearch that integrates with the WUPHF Learning System for two-level autonomous learning.

## Enhanced Setup

### WUPHF Integration Setup

1. **Install the bridge components:**
   ```bash
   pip install -e .
   ```

2. **Configure WUPHF integration:**
   ```bash
   # Create config file
   cat > autoresearch_wuphf_config.json << EOF
   {
     "task_type": "llm_training_experiment",
     "expected_duration": 300,
     "target_metric": "val_bpb",
     "quality_threshold": 0.7,
     "enable_pattern_learning": true,
     "enable_knowledge_consolidation": true
   }
   EOF
   ```

3. **Verify WUPHF connection:**
   ```bash
   python -c "from autoresearch_wuphf_bridge import AutoresearchWuphfBridge; bridge = AutoresearchWuphfBridge(); print('Connected' if bridge.learning_system else 'Not connected')"
   ```

## Enhanced Experimentation Loop

### Standard autoresearch loop (unchanged):
- Modify `train.py`
- Run experiment
- Log results to `results.tsv`
- Keep or discard based on val_bpb

### Enhanced loop with WUPHF integration:
- Modify `train.py`
- **Extract hyperparameters** for pattern learning
- Run experiment
- **Log to WUPHF learning system** with self-reflection
- **Save model checkpoint** to knowledge base
- **Learn patterns** from success/failure
- **Get optimization suggestions** for next experiment
- Log results to `results.tsv`
- Keep or discard based on val_bpb

## Experiment Flow with WUPHF

### Before Experiment:
```python
from autoresearch_wuphf_bridge import AutoresearchWuphfBridge

bridge = AutoresearchWuphfBridge()

# Get optimization suggestions
current_params = {
    "learning_rate": 0.03,
    "depth": 8,
    "batch_size": 64
}

suggestions = bridge.get_optimization_suggestions(current_params)
for suggestion in suggestions:
    print(suggestion)
```

### After Experiment:
```python
# Parse experiment results
result = {
    "val_bpb": 0.997,
    "training_seconds": 300.1,
    "peak_vram_mb": 45060.2,
    "status": "success"
}

# Extract parameters from train.py
parameters = {
    "learning_rate": 0.04,
    "depth": 8,
    "batch_size": 64
}

# Log to WUPHF
bridge.log_experiment_result("exp_001", result)

# Save model checkpoint
bridge.save_model_checkpoint("exp_001", {
    "val_bpb": 0.997,
    "architecture": "GPT-8L",
    "parameters": parameters
})

# Learn patterns
bridge.learn_from_experiment("exp_001", result, parameters)
```

## Quality Gates

The WUPHF integration adds automatic quality assessment:

- **Quality Score**: 0.0-1.0 based on val_bpb, memory usage, and efficiency
- **Quality Threshold**: Experiments below threshold are flagged for review
- **Kill Criteria**: Critical errors (OOM, data loss) trigger automatic investigation

## Pattern Learning

The system automatically learns:

### Success Patterns:
- Hyperparameter combinations that achieve good val_bpb
- Architecture configurations that work well
- Training strategies that converge efficiently

### Anti-Patterns:
- Configurations that cause OOM errors
- Learning rates that lead to NaN loss
- Architectures that train too slowly

## Knowledge Base

Successful model checkpoints are stored in WUPHF knowledge base:

- **Episodic Memory**: Individual experiment results
- **Semantic Memory**: Consolidated patterns across experiments
- **Retrieval**: Query for best models, similar configurations

## Monitoring

Check learning progress:

```python
from autoresearch_wuphf_bridge import AutoresearchWuphfBridge

bridge = AutoresearchWuphfBridge()

# Get best model
best_model = bridge.model_manager.get_best_model()
print(f"Best val_bpb: {best_model['val_bpb']}")

# Get learning statistics
stats = bridge.learning_system.get_learning_statistics()
print(f"Total experiments: {stats['total_events']}")
```

## Fallback Mode

If WUPHF is not available, the system runs in standalone mode:

- All autoresearch functionality works normally
- Pattern learning and knowledge base features are disabled
- Graceful degradation with warning messages

## Original Instructions (Unchanged)

The original autoresearch instructions from program.md still apply:

[Include original program.md content here]
```

**Step 3: Commit**

```bash
git add program_wuphf_enhanced.md
git commit -m "docs: add enhanced program.md with WUPHF integration"
```

---

## Task 6: Integration Tests

**Files:**
- Create: `tests/test_integration_wuphf_autoresearch.py`
- Create: `tests/fixtures/sample_train.py` (sample training script)

**Step 1: Write the failing test**

```python
# tests/test_integration_wuphf_autoresearch.py
import pytest
import os
import tempfile
import json
from autoresearch_wuphf_bridge import AutoresearchWuphfBridge
from autoresearch_wuphf_config import AutoresearchWuphfConfig

def test_full_experiment_workflow():
    """Test complete workflow from experiment to learning"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Setup
        config = AutoresearchWuphfConfig(
            knowledge_base_path=os.path.join(temp_dir, "knowledge"),
            patterns_path=os.path.join(temp_dir, "patterns")
        )
        bridge = AutoresearchWuphfBridge(config=config)
        
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
        assert log_result["status"] == "logged"
        assert "quality_score" in log_result
        
        # Save model checkpoint
        model_metadata = {
            "experiment_id": experiment_id,
            "val_bpb": result["val_bpb"],
            "architecture": "GPT-8L",
            "parameters": parameters
        }
        
        entry_id = bridge.save_model_checkpoint(experiment_id, model_metadata)
        assert entry_id is not None
        
        # Learn patterns
        bridge.learn_from_experiment(experiment_id, result, parameters)
        
        # Verify pattern was learned
        suggestions_after = bridge.get_optimization_suggestions(parameters)
        assert len(suggestions_after) >= len(suggestions)
        
        # Verify model was saved
        best_model = bridge.model_manager.get_best_model()
        assert best_model is not None
        assert best_model["val_bpb"] == 0.997

def test_failure_handling():
    """Test handling of failed experiments"""
    with tempfile.TemporaryDirectory() as temp_dir:
        config = AutoresearchWuphfConfig(
            knowledge_base_path=os.path.join(temp_dir, "knowledge"),
            patterns_path=os.path.join(temp_dir, "patterns")
        )
        bridge = AutoresearchWuphfBridge(config=config)
        
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
        assert log_result["status"] in ["logged", "error"]
        
        # Learn from failure
        bridge.learn_from_experiment(experiment_id, result, parameters)
        
        # Verify anti-pattern was created
        suggestions = bridge.get_optimization_suggestions(parameters)
        assert any("AVOID" in s for s in suggestions)

def test_wuphf_unavailable_fallback():
    """Test fallback when WUPHF is not available"""
    # This test would need to mock WUPHF unavailability
    # For now, we test that the bridge handles it gracefully
    bridge = AutoresearchWuphfBridge()
    
    if not bridge.learning_system:
        # Should not crash when WUPHF is unavailable
        result = bridge.log_experiment_result("exp_001", {"status": "success"})
        assert result["status"] == "wuphf_unavailable"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_integration_wuphf_autoresearch.py -v`
Expected: May fail if WUPHF not available, but should handle gracefully

**Step 3: Run test to verify it passes**

Run: `pytest tests/test_integration_wuphf_autoresearch.py -v`
Expected: PASS (or skip if WUPHF unavailable)

**Step 4: Commit**

```bash
git add tests/test_integration_wuphf_autoresearch.py
git commit -m "test: add integration tests for WUPHF-autoresearch"
```

---

## Task 7: Documentation and Examples

**Files:**
- Create: `README_WUPHF_INTEGRATION.md`
- Create: `examples/wuphf_integration_example.py`
- Modify: `README.md` (add section about WUPHF integration)

**Step 1: Create integration documentation**

```markdown
# WUPHF Learning System Integration

This document describes the integration between autoresearch and the WUPHF Learning System.

## Overview

The integration enables two-level autonomous learning:

1. **Micro-level**: autoresearch optimizes individual models through hyperparameter experiments
2. **Macro-level**: WUPHF Learning System optimizes the research process itself through pattern recognition and knowledge consolidation

## Architecture

```
autoresearch (Experiment Engine)
    ↓ experiments/results
WUPHF Learning System (Orchestrator)
    ↓ pattern recognition
WUPHF Knowledge Base (Model Storage)
    ↓ best practices
WUPHF Pattern Library (Hyperparameter Optimizer)
    ↓ optimization suggestions
autoresearch (next experiment)
```

## Installation

```bash
# Ensure WUPHF Learning System is available at ~/.wuphf/
# The bridge will automatically detect and connect to it

# Install additional dependencies (if needed)
pip install -e .
```

## Quick Start

```python
from autoresearch_wuphf_bridge import AutoresearchWuphfBridge

# Initialize bridge
bridge = AutoresearchWuphfBridge()

# Get optimization suggestions before experiment
suggestions = bridge.get_optimization_suggestions({
    "learning_rate": 0.03,
    "depth": 8
})

# Run experiment (standard autoresearch)
# uv run train.py

# Parse and log results
result = {
    "val_bpb": 0.997,
    "training_seconds": 300.1,
    "status": "success"
}

bridge.log_experiment_result("exp_001", result)

# Save model checkpoint
bridge.save_model_checkpoint("exp_001", {
    "val_bpb": 0.997,
    "parameters": {"learning_rate": 0.04, "depth": 8}
})

# Learn patterns
bridge.learn_from_experiment("exp_001", result, {
    "learning_rate": 0.04,
    "depth": 8
})
```

## Configuration

Create `autoresearch_wuphf_config.json`:

```json
{
  "task_type": "llm_training_experiment",
  "expected_duration": 300,
  "target_metric": "val_bpb",
  "quality_threshold": 0.7,
  "enable_pattern_learning": true,
  "enable_knowledge_consolidation": true
}
```

## Monitoring

Check learning progress:

```python
# Get best model
best_model = bridge.model_manager.get_best_model()
print(f"Best val_bpb: {best_model['val_bpb']}")

# Get optimization suggestions
suggestions = bridge.get_optimization_suggestions(current_params)

# Search for similar models
similar_models = bridge.model_manager.search_models("GPT-8L")
```

## Fallback Mode

If WUPHF is not available, the system runs in standalone mode with reduced functionality.

## Troubleshooting

**WUPHF not connected:**
- Verify WUPHF is installed at ~/.wuphf/
- Check that agent_learning_system.py exists in ~/.wuphf/providers/

**Patterns not being learned:**
- Check enable_pattern_learning in config
- Verify experiments have proper status field

**Models not being saved:**
- Check knowledge_base_path in config
- Verify write permissions
```

**Step 2: Create example script**

```python
# examples/wuphf_integration_example.py
"""
Example script showing how to use WUPHF integration with autoresearch.
"""

from autoresearch_wuphf_bridge import AutoresearchWuphfBridge
from autoresearch_wuphf_config import AutoresearchWuphfConfig
import json

def main():
    # Initialize bridge with custom config
    config = AutoresearchWuphfConfig(
        quality_threshold=0.75,
        enable_pattern_learning=True
    )
    bridge = AutoresearchWuphfBridge(config)
    
    print("=" * 60)
    print("WUPHF-autoresearch Integration Example")
    print("=" * 60)
    
    # Example 1: Get optimization suggestions
    print("\n1. Getting optimization suggestions...")
    current_params = {
        "learning_rate": 0.03,
        "depth": 8,
        "batch_size": 64
    }
    
    suggestions = bridge.get_optimization_suggestions(current_params)
    if suggestions:
        print("Suggestions:")
        for suggestion in suggestions:
            print(f"  - {suggestion}")
    else:
        print("  No suggestions yet (run more experiments)")
    
    # Example 2: Simulate experiment and log results
    print("\n2. Simulating experiment...")
    experiment_id = "example_exp_001"
    
    # These would normally come from actual train.py output
    result = {
        "val_bpb": 0.997,
        "training_seconds": 300.1,
        "peak_vram_mb": 45060.2,
        "mfu_percent": 39.80,
        "status": "success"
    }
    
    parameters = {
        "learning_rate": 0.04,
        "depth": 8,
        "batch_size": 64
    }
    
    # Log to WUPHF
    log_result = bridge.log_experiment_result(experiment_id, result)
    print(f"  Quality score: {log_result.get('quality_score', 'N/A')}")
    
    # Save model checkpoint
    entry_id = bridge.save_model_checkpoint(experiment_id, {
        "val_bpb": result["val_bpb"],
        "architecture": "GPT-8L",
        "parameters": parameters
    })
    print(f"  Model saved: {entry_id}")
    
    # Learn patterns
    bridge.learn_from_experiment(experiment_id, result, parameters)
    print("  Patterns learned")
    
    # Example 3: Retrieve best model
    print("\n3. Retrieving best model...")
    if bridge.model_manager:
        best_model = bridge.model_manager.get_best_model()
        if best_model:
            print(f"  Best val_bpb: {best_model['val_bpb']}")
            print(f"  Architecture: {best_model['architecture']}")
            print(f"  Parameters: {json.dumps(best_model['parameters'], indent=2)}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
```

**Step 3: Update main README**

```markdown
# Add to README.md

## WUPHF Learning System Integration

autoresearch can be integrated with the WUPHF Learning System for enhanced autonomous learning capabilities. This enables:

- **Pattern Learning**: Automatic learning of successful and unsuccessful hyperparameter combinations
- **Knowledge Base**: Storage and retrieval of model checkpoints
- **Quality Gates**: Automatic quality assessment of experiments
- **Optimization Suggestions**: Data-driven recommendations for future experiments

See [README_WUPHF_INTEGRATION.md](README_WUPHF_INTEGRATION.md) for details.
```

**Step 4: Commit**

```bash
git add README_WUPHF_INTEGRATION.md examples/wuphf_integration_example.py README.md
git commit -m "docs: add WUPHF integration documentation and examples"
```

---

## Task 8: Final Integration and Testing

**Files:**
- Create: `setup.py` (package installation)
- Create: `pyproject.toml` (modern Python packaging)
- Test: Full integration test suite

**Step 1: Create setup.py**

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="autoresearch-wuphf",
    version="0.1.0",
    description="Integration between autoresearch and WUPHF Learning System",
    packages=find_packages(),
    install_requires=[
        # Add dependencies if needed
    ],
    python_requires=">=3.10",
)
```

**Step 2: Create pyproject.toml**

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "autoresearch-wuphf"
version = "0.1.0"
description = "Integration between autoresearch and WUPHF Learning System"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

**Step 3: Run full test suite**

```bash
# Install in development mode
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v --cov=.

# Run specific test categories
pytest tests/test_autoresearch_wuphf_bridge.py -v
pytest tests/test_model_knowledge_manager.py -v
pytest tests/test_hyperparameter_pattern_manager.py -v
pytest tests/test_integration_wuphf_autoresearch.py -v
```

**Step 4: Test example script**

```bash
python examples/wuphf_integration_example.py
```

**Step 5: Commit**

```bash
git add setup.py pyproject.toml
git commit -m "build: add packaging configuration"
```

---

## Task 9: Cleanup and Final Verification

**Files:**
- Modify: `.gitignore` (add Python cache files)
- Verify: All tests pass
- Verify: Documentation complete

**Step 1: Update .gitignore**

```gitignore
# Add to .gitignore
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.pytest_cache/
.coverage
htmlcov/
```

**Step 2: Run final test suite**

```bash
pytest tests/ -v --cov=. --cov-report=html
```

**Step 3: Verify documentation**

```bash
# Check all documentation files exist
ls -la README_WUPHF_INTEGRATION.md
ls -la examples/wuphf_integration_example.py
ls -la program_wuphf_enhanced.md
```

**Step 4: Create summary document**

```markdown
# Integration Summary

## Completed Components

1. ✅ Autoresearch-WUPHF Bridge (`autoresearch_wuphf_bridge.py`)
2. ✅ Configuration Management (`autoresearch_wuphf_config.py`)
3. ✅ Model Knowledge Manager (`model_knowledge_manager.py`)
4. ✅ Hyperparameter Pattern Manager (`hyperparameter_pattern_manager.py`)
5. ✅ Enhanced program.md (`program_wuphf_enhanced.md`)
6. ✅ Integration Tests (`tests/test_integration_wuphf_autoresearch.py`)
7. ✅ Documentation (`README_WUPHF_INTEGRATION.md`)
8. ✅ Example Script (`examples/wuphf_integration_example.py`)
9. ✅ Packaging (`setup.py`, `pyproject.toml`)

## Test Results

All tests passing:
- Bridge component tests: ✅
- Configuration tests: ✅
- Model knowledge manager tests: ✅
- Pattern manager tests: ✅
- Integration tests: ✅

## Usage

```bash
# Install
pip install -e .

# Run example
python examples/wuphf_integration_example.py

# Use in autoresearch
python -c "from autoresearch_wuphf_bridge import AutoresearchWuphfBridge; bridge = AutoresearchWuphfBridge()"
```

## Next Steps

1. Run actual autoresearch experiments with WUPHF integration
2. Monitor pattern learning progress
3. Iterate on quality thresholds and configuration
4. Extend pattern library with more sophisticated patterns
```

**Step 5: Final commit**

```bash
git add .gitignore INTEGRATION_SUMMARY.md
git commit -m "docs: add integration summary and cleanup"
```

---

## Execution Instructions

This plan is complete and ready for implementation. Two execution options:

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?