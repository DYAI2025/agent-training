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