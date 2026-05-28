"""Learning Memory System - continuous improvement and pattern recognition"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from pathlib import Path
import uuid
from collections import defaultdict


class MemoryType(Enum):
    """Types of memory entries"""
    SUCCESS = "success"
    FAILURE = "failure"
    IMPROVEMENT = "improvement"
    INSIGHT = "insight"
    PATTERN = "pattern"


@dataclass
class MemoryEntry:
    """Single memory entry"""
    entry_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    entry_type: MemoryType = MemoryType.SUCCESS
    agent_type: str = ""
    task_description: str = ""
    outcome: str = ""
    quality_score: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "entry_id": self.entry_id,
            "entry_type": self.entry_type.value,
            "agent_type": self.agent_type,
            "task_description": self.task_description,
            "outcome": self.outcome,
            "quality_score": self.quality_score,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        """Create from dictionary"""
        return cls(
            entry_id=data.get("entry_id", str(uuid.uuid4())),
            entry_type=MemoryType(data.get("entry_type", "success")),
            agent_type=data.get("agent_type", ""),
            task_description=data.get("task_description", ""),
            outcome=data.get("outcome", ""),
            quality_score=data.get("quality_score", 0.0),
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            metadata=data.get("metadata", {})
        )


@dataclass
class Pattern:
    """Detected pattern in memory"""
    pattern_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    pattern_type: str = ""
    description: str = ""
    confidence: float = 0.0
    occurrences: int = 0
    discovered_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "pattern_id": self.pattern_id,
            "pattern_type": self.pattern_type,
            "description": self.description,
            "confidence": self.confidence,
            "occurrences": self.occurrences,
            "discovered_at": self.discovered_at.isoformat(),
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Pattern':
        """Create Pattern from dictionary"""
        return cls(
            pattern_id=data.get("pattern_id", str(uuid.uuid4())),
            pattern_type=data.get("pattern_type", ""),
            description=data.get("description", ""),
            confidence=data.get("confidence", 0.0),
            occurrences=data.get("occurrences", 0),
            discovered_at=datetime.fromisoformat(data.get("discovered_at", datetime.now().isoformat())),
            metadata=data.get("metadata", {})
        )


@dataclass
class LearningInsight:
    """Insight derived from memory analysis"""
    insight_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    insight_type: str = ""
    description: str = ""
    actionable_recommendation: str = ""
    confidence: float = 0.0
    generated_at: datetime = field(default_factory=datetime.now)
    related_patterns: List[str] = field(default_factory=list)


class LearningMemory:
    """Learning memory system for continuous improvement"""
    
    def __init__(
        self,
        memory_dir: str = "memory/storage",
        pattern_recognition_enabled: bool = True,
        min_history_size: int = 5
    ):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        self.pattern_recognition_enabled = pattern_recognition_enabled
        self.min_history_size = min_history_size
        
        self._memory_file = self.memory_dir / "memory_entries.jsonl"
        self._patterns_file = self.memory_dir / "patterns.json"
        
        # Initialize storage files
        if not self._memory_file.exists():
            self._memory_file.touch()
        if not self._patterns_file.exists():
            self._patterns_file.write_text("[]")
    
    def store_entry(self, entry: MemoryEntry) -> str:
        """Store a memory entry"""
        # Append to memory file
        with open(self._memory_file, 'a') as f:
            f.write(json.dumps(entry.to_dict()) + '\n')
        
        # Trigger pattern detection if enabled
        if self.pattern_recognition_enabled:
            self._update_patterns()
        
        return entry.entry_id
    
    def retrieve_entry(self, entry_id: str) -> Optional[MemoryEntry]:
        """Retrieve a specific memory entry"""
        for entry in self._load_all_entries():
            if entry.entry_id == entry_id:
                return entry
        return None
    
    def get_entries_by_agent(self, agent_type: str) -> List[MemoryEntry]:
        """Get all entries for a specific agent"""
        return [
            entry for entry in self._load_all_entries()
            if entry.agent_type == agent_type
        ]
    
    def get_entries_by_type(self, entry_type: MemoryType) -> List[MemoryEntry]:
        """Get all entries of a specific type"""
        return [
            entry for entry in self._load_all_entries()
            if entry.entry_type == entry_type
        ]
    
    def get_recent_entries(self, limit: int = 10) -> List[MemoryEntry]:
        """Get most recent entries"""
        all_entries = self._load_all_entries()
        # Sort by timestamp descending
        all_entries.sort(key=lambda x: x.timestamp, reverse=True)
        return all_entries[:limit]
    
    def detect_patterns(self) -> List[Pattern]:
        """Detect patterns in memory entries"""
        if not self.pattern_recognition_enabled:
            return []
        
        all_entries = self._load_all_entries()
        
        if len(all_entries) < self.min_history_size:
            return []
        
        patterns = []
        
        # Detect success patterns by agent
        agent_success_rates = self._calculate_agent_success_rates(all_entries)
        for agent_type, success_rate in agent_success_rates.items():
            if success_rate > 0.8:
                patterns.append(Pattern(
                    pattern_type="high_success_rate",
                    description=f"{agent_type} has high success rate ({success_rate:.1%})",
                    confidence=success_rate,
                    occurrences=len([e for e in all_entries if e.agent_type == agent_type]),
                    metadata={"agent_type": agent_type, "success_rate": success_rate}
                ))
        
        # Detect quality patterns
        high_quality_entries = [e for e in all_entries if e.quality_score > 0.85]
        if len(high_quality_entries) >= self.min_history_size:
            # Find common metadata in high-quality entries
            common_metadata = self._find_common_metadata(high_quality_entries)
            if common_metadata:
                patterns.append(Pattern(
                    pattern_type="high_quality_pattern",
                    description=f"Common factors in high-quality outcomes: {list(common_metadata.keys())}",
                    confidence=0.8,
                    occurrences=len(high_quality_entries),
                    metadata={"common_factors": common_metadata}
                ))
        
        # Detect failure patterns
        failure_entries = [e for e in all_entries if e.entry_type == MemoryType.FAILURE]
        if len(failure_entries) >= 3:
            failure_metadata = self._find_common_metadata(failure_entries)
            if failure_metadata:
                patterns.append(Pattern(
                    pattern_type="failure_pattern",
                    description=f"Common factors in failures: {list(failure_metadata.keys())}",
                    confidence=0.7,
                    occurrences=len(failure_entries),
                    metadata={"common_factors": failure_metadata}
                ))
        
        # Save patterns
        self._save_patterns(patterns)
        
        return patterns
    
    def get_learning_insights(self) -> List[LearningInsight]:
        """Generate learning insights from memory"""
        all_entries = self._load_all_entries()
        
        if len(all_entries) < self.min_history_size:
            return []
        
        insights = []
        patterns = self._load_patterns()
        
        # Generate insights from patterns
        for pattern in patterns:
            if pattern.pattern_type == "high_success_rate":
                insights.append(LearningInsight(
                    insight_type="agent_optimization",
                    description=f"{pattern.metadata.get('agent_type')} performs well",
                    actionable_recommendation=f"Consider delegating similar tasks to {pattern.metadata.get('agent_type')}",
                    confidence=pattern.confidence,
                    related_patterns=[pattern.pattern_id]
                ))
            elif pattern.pattern_type == "high_quality_pattern":
                insights.append(LearningInsight(
                    insight_type="quality_optimization",
                    description=f"High-quality outcomes share common factors",
                    actionable_recommendation=f"Incorporate factors: {list(pattern.metadata.get('common_factors', {}).keys())}",
                    confidence=pattern.confidence,
                    related_patterns=[pattern.pattern_id]
                ))
            elif pattern.pattern_type == "failure_pattern":
                insights.append(LearningInsight(
                    insight_type="risk_mitigation",
                    description=f"Common failure factors identified",
                    actionable_recommendation=f"Avoid factors: {list(pattern.metadata.get('common_factors', {}).keys())}",
                    confidence=pattern.confidence,
                    related_patterns=[pattern.pattern_id]
                ))
        
        return insights
    
    def get_agent_performance_summary(self, agent_type: str) -> Dict[str, Any]:
        """Get performance summary for an agent"""
        entries = self.get_entries_by_agent(agent_type)
        
        if not entries:
            return {
                "agent_type": agent_type,
                "total_entries": 0,
                "success_rate": 0.0,
                "average_quality_score": 0.0
            }
        
        successful_entries = [e for e in entries if e.entry_type == MemoryType.SUCCESS]
        success_rate = len(successful_entries) / len(entries)
        
        avg_quality = sum(e.quality_score for e in entries) / len(entries)
        
        return {
            "agent_type": agent_type,
            "total_entries": len(entries),
            "success_rate": success_rate,
            "average_quality_score": avg_quality,
            "recent_performance": self._get_recent_performance(entries)
        }
    
    def apply_learning_to_task(
        self,
        agent_type: str,
        task_description: str
    ) -> List[str]:
        """Apply learning to provide suggestions for a new task"""
        suggestions = []
        
        # Get patterns
        patterns = self._load_patterns()
        
        # Get agent performance
        performance = self.get_agent_performance_summary(agent_type)
        
        # Add performance-based suggestions
        if performance["success_rate"] > 0.8:
            suggestions.append(f"Agent has high success rate ({performance['success_rate']:.1%})")
        elif performance["success_rate"] < 0.5:
            suggestions.append(f"Agent has low success rate ({performance['success_rate']:.1%}) - consider alternative")
        
        # Add pattern-based suggestions
        for pattern in patterns:
            if pattern.pattern_type == "high_quality_pattern":
                common_factors = pattern.metadata.get("common_factors", {})
                if common_factors:
                    suggestions.append(f"Consider incorporating: {list(common_factors.keys())}")
        
        # Add historical suggestions
        similar_entries = [
            e for e in self.get_entries_by_agent(agent_type)
            if task_description.lower() in e.task_description.lower()
        ]
        
        if similar_entries:
            best_entry = max(similar_entries, key=lambda x: x.quality_score)
            suggestions.append(f"Similar task achieved {best_entry.quality_score:.1%} quality with: {best_entry.outcome}")
        
        return suggestions
    
    def prune_old_entries(self, max_entries: int = 100) -> int:
        """Prune old entries to keep memory size manageable"""
        all_entries = self._load_all_entries()
        
        if len(all_entries) <= max_entries:
            return 0
        
        # Sort by timestamp and keep most recent
        all_entries.sort(key=lambda x: x.timestamp, reverse=True)
        entries_to_keep = all_entries[:max_entries]
        entries_to_remove = len(all_entries) - max_entries
        
        # Rewrite memory file with pruned entries
        with open(self._memory_file, 'w') as f:
            for entry in entries_to_keep:
                f.write(json.dumps(entry.to_dict()) + '\n')
        
        return entries_to_remove
    
    def export_memory(self, export_path: Path):
        """Export memory to file"""
        all_entries = self._load_all_entries()
        patterns = self._load_patterns()
        
        export_data = {
            "entries": [entry.to_dict() for entry in all_entries],
            "patterns": [pattern.to_dict() for pattern in patterns],
            "exported_at": datetime.now().isoformat()
        }
        
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2)
    
    def import_memory(self, import_path: Path):
        """Import memory from file"""
        with open(import_path, 'r') as f:
            import_data = json.load(f)
        
        # Import entries
        for entry_data in import_data.get("entries", []):
            entry = MemoryEntry.from_dict(entry_data)
            self.store_entry(entry)
        
        # Import patterns
        patterns = [Pattern.from_dict(p) for p in import_data.get("patterns", [])]
        self._save_patterns(patterns)
    
    def _load_all_entries(self) -> List[MemoryEntry]:
        """Load all entries from memory file"""
        entries = []
        
        if not self._memory_file.exists():
            return entries
        
        with open(self._memory_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entry_data = json.loads(line)
                        entries.append(MemoryEntry.from_dict(entry_data))
                    except json.JSONDecodeError:
                        continue
        
        return entries
    
    def _load_patterns(self) -> List[Pattern]:
        """Load patterns from file"""
        if not self._patterns_file.exists():
            return []
        
        with open(self._patterns_file, 'r') as f:
            pattern_data = json.load(f)
        
        return [Pattern.from_dict(p) for p in pattern_data]
    
    def _save_patterns(self, patterns: List[Pattern]):
        """Save patterns to file"""
        with open(self._patterns_file, 'w') as f:
            json.dump([p.to_dict() for p in patterns], f, indent=2)
    
    def _update_patterns(self):
        """Update patterns based on current memory"""
        self.detect_patterns()
    
    def _calculate_agent_success_rates(self, entries: List[MemoryEntry]) -> Dict[str, float]:
        """Calculate success rates by agent"""
        agent_entries = defaultdict(list)
        
        for entry in entries:
            agent_entries[entry.agent_type].append(entry)
        
        success_rates = {}
        for agent_type, agent_entries_list in agent_entries.items():
            successful = [e for e in agent_entries_list if e.entry_type == MemoryType.SUCCESS]
            success_rates[agent_type] = len(successful) / len(agent_entries_list)
        
        return success_rates
    
    def _find_common_metadata(self, entries: List[MemoryEntry]) -> Dict[str, Any]:
        """Find common metadata factors across entries"""
        if not entries:
            return {}
        
        # Get all metadata keys
        all_keys = set()
        for entry in entries:
            all_keys.update(entry.metadata.keys())
        
        # Find keys with common values
        common_metadata = {}
        for key in all_keys:
            values = [entry.metadata.get(key) for entry in entries if key in entry.metadata]
            if values and len(set(values)) == 1:
                common_metadata[key] = values[0]
        
        return common_metadata
    
    def _get_recent_performance(self, entries: List[MemoryEntry], window: int = 5) -> Dict[str, Any]:
        """Get recent performance metrics"""
        recent_entries = sorted(entries, key=lambda x: x.timestamp, reverse=True)[:window]
        
        if not recent_entries:
            return {"average_quality": 0.0, "success_count": 0}
        
        avg_quality = sum(e.quality_score for e in recent_entries) / len(recent_entries)
        success_count = sum(1 for e in recent_entries if e.entry_type == MemoryType.SUCCESS)
        
        return {
            "average_quality": avg_quality,
            "success_count": success_count,
            "total_count": len(recent_entries)
        }


if __name__ == "__main__":
    # Quick test
    memory = LearningMemory()
    
    # Store some test entries
    entry = MemoryEntry(
        entry_type=MemoryType.SUCCESS,
        agent_type="content_agent",
        task_description="Create pitch deck for AI startup",
        outcome="Successfully created 12-slide pitch deck",
        quality_score=0.85,
        metadata={"topic": "AI startup", "slides": 12}
    )
    
    entry_id = memory.store_entry(entry)
    print(f"Stored entry: {entry_id}")
    
    # Retrieve entry
    retrieved = memory.retrieve_entry(entry_id)
    print(f"Retrieved: {retrieved.task_description}")
