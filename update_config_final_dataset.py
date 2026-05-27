#!/usr/bin/env python3
"""
Aktualisierung der WUPHF Config mit dem final comprehensive Dataset
"""

import json
from pathlib import Path

# WUPHF Config Pfad
config_path = Path.home() / ".wuphf-spaces/main/.wuphf/config.json"
final_dataset_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_final_comprehensive_dataset.jsonl")

# Config laden
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Training-Datasets Sektion aktualisieren
if 'training_datasets' not in config:
    config['training_datasets'] = {}

config['training_datasets']['final_comprehensive'] = {
    "path": str(final_dataset_path),
    "description": "Final Comprehensive WUPHF Training Dataset (Task Understanding + Enhanced AI/Tech Pitch Deck + Case Studies)",
    "examples": 83,
    "last_updated": "2026-05-27",
    "focus": "AI/ML, Developer Tools, Data/Analytics, Cloud/Infrastructure, AI SaaS with Scientific Best Practices",
    "composition": {
        "task_understanding": 24,
        "enhanced_pitch_deck": 36,
        "case_studies": 9,
        "enhancement_types": ["psychological_triggers", "clarity_structure", "bottom_up_market", "social_proof_fomo", "radical_simplification", "network_transformation"]
    },
    "best_practices_integrated": [
        "40-Sekunden-Regel (Hook)",
        "Psychologische Trigger (FOMO, Verlustaversion)",
        "Storytelling-Struktur",
        "Bottom-Up Market Size Approach",
        "Unit Economics (LTV, CAC, Payback)",
        "Design-Prinzipien (Kognitive Ergonomie)",
        "Regionale Unterschiede (USA vs. DACH)",
        "Sektorale Differenzen (SaaS vs. Deep Tech)",
        "Fallstudien-Prinzipien (Airbnb, LinkedIn, Coinbase)",
        "Absolute No-Gos vermeiden"
    ]
}

# Backup erstellen
backup_path = config_path.with_suffix('.json.backup_before_final_dataset')
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

# Config speichern
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"✅ WUPHF Config mit final comprehensive Dataset aktualisiert")
print(f"📋 Backup erstellt: {backup_path}")
print(f"🎯 Dataset-Details:")
print(f"   - Pfad: {final_dataset_path}")
print(f"   - Gesamt Beispiele: 83")
print(f"   - Task Understanding: 24")
print(f"   - Enhanced Pitch Deck: 36")
print(f"   - Case Studies: 9")
print(f"   - Integrated Best Practices: 10")

print(f"\n🎯 Content-System-Prompt bereits aktualisiert mit:")
print(f"   - Psychologische Mechanismen")
print(f"   - Strukturelle Paradigmen")
print(f"   - Quantitative Exzellenz")
print(f"   - Design-Prinzipien")
print(f"   - Regionale und sektorale Unterschiede")
print(f"   - Absolute No-Gos")
print(f"   - Fallstudien-Prinzipien")

print(f"\n📋 System bereit für Training mit:")
print(f"   1. WUPHF neu starten")
print(f"   2. Training mit comprehensive Dataset")
print(f"   3. Agent-Verhalten mit wissenschaftlichen Best Practices validieren")