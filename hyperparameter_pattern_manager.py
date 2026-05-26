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
        
        # Flatten parameters to top level for easy access
        pattern.update(parameters)
        
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
        
        # Flatten parameters to top level for easy access
        pattern.update(parameters)
        
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
        # Ensure pattern has parameters field if not present
        if "parameters" not in pattern:
            # Extract parameters from top-level keys (excluding metadata)
            metadata_keys = {"pattern_id", "pattern_type", "experiment_id", "timestamp", 
                           "quality_score", "val_bpb", "usage_count", "success_rate"}
            parameters = {k: v for k, v in pattern.items() if k not in metadata_keys}
            pattern["parameters"] = parameters
        
        self.success_patterns.append(pattern)
        self._save_patterns(self.success_patterns, self.success_patterns_file)
    
    def save_anti_pattern(self, pattern: Dict[str, Any]):
        """Save anti-pattern to library"""
        # Ensure pattern has parameters field if not present
        if "parameters" not in pattern:
            # Extract parameters from top-level keys (excluding metadata)
            metadata_keys = {"pattern_id", "pattern_type", "experiment_id", "timestamp", 
                           "symptoms", "mitigation", "usage_count"}
            parameters = {k: v for k, v in pattern.items() if k not in metadata_keys}
            pattern["parameters"] = parameters
        
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
