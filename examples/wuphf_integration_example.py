"""
Example script showing how to use WUPHF integration with autoresearch.
"""

from autoresearch_wuphf_bridge import AutoresearchWuphfBridge
from autoresearch_wuphf_config import load_config
import json

def main():
    # Initialize bridge with custom config
    config = load_config()
    config["quality_threshold"] = 0.75
    config["enable_pattern_learning"] = True
    
    bridge = AutoresearchWuphfBridge()
    
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
    print(f"  Status: {log_result.get('status', 'N/A')}")
    
    # Save model checkpoint
    entry_id = bridge.save_model_checkpoint(experiment_id, {
        "val_bpb": result["val_bpb"],
        "architecture": "GPT-8L",
        "parameters": parameters
    })
    if entry_id:
        print(f"  Model saved: {entry_id}")
    else:
        print("  Model saving skipped (manager not available)")
    
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
        else:
            print("  No models saved yet")
    else:
        print("  Model manager not available")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()