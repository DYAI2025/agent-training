"""
Configuration management for Autoresearch-WUPHF Bridge

This module provides configuration utilities for the bridge component,
including default settings and validation.
"""
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


DEFAULT_CONFIG = {
    "task_type": "llm_training_experiment",
    "expected_duration": 300,  # 5 minutes in seconds
    "target_metric": "val_bpb",
    "quality_threshold": 0.7,
    "enable_pattern_learning": True,
    "enable_knowledge_consolidation": True,
    "wuphf_path": "~/.wuphf",
    "knowledge_retention_days": 30,
    "max_experiment_history": 1000
}


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from file or use defaults.
    
    Args:
        config_path: Path to custom configuration file (JSON format)
        
    Returns:
        Configuration dictionary
    """
    config = DEFAULT_CONFIG.copy()
    
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            user_config = json.load(f)
            config.update(user_config)
    
    return config


def save_config(config: Dict[str, Any], config_path: str) -> None:
    """
    Save configuration to file.
    
    Args:
        config: Configuration dictionary to save
        config_path: Path where to save the configuration
    """
    config_dir = os.path.dirname(config_path)
    if config_dir:
        os.makedirs(config_dir, exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


def get_default_config_path() -> str:
    """
    Get the default configuration file path.
    
    Returns:
        Path to default configuration file
    """
    config_dir = os.path.expanduser("~/.config/autoresearch")
    return os.path.join(config_dir, "wuphf_bridge_config.json")


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration values.
    
    Args:
        config: Configuration dictionary to validate
        
    Returns:
        True if configuration is valid, False otherwise
    """
    required_keys = [
        "task_type",
        "expected_duration",
        "target_metric",
        "quality_threshold"
    ]
    
    for key in required_keys:
        if key not in config:
            return False
    
    # Validate ranges
    if not (0 <= config["quality_threshold"] <= 1):
        return False
    
    if config["expected_duration"] <= 0:
        return False
    
    return True
