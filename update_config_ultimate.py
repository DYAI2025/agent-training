#!/usr/bin/env python3
"""
Aktualisierung der WUPHF Config mit dem Ultimate Dataset
"""

import json
from pathlib import Path

# WUPHF Config Pfad
config_path = Path.home() / ".wuphf-spaces/main/.wuphf/config.json"
ultimate_dataset_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_ultimate_dataset.jsonl")

# Config laden
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Training-Datasets Sektion aktualisieren
if 'training_datasets' not in config:
    config['training_datasets'] = {}

config['training_datasets']['ultimate'] = {
    "path": str(ultimate_dataset_path),
    "description": "Ultimate WUPHF Training Dataset with Scientific Best Practices (Task Understanding + Enhanced AI/Tech Pitch Deck + Case Studies + Regional/Sectoral Adaptations)",
    "examples": 95,
    "last_updated": "2026-05-27",
    "focus": "AI/ML, Developer Tools, Data/Analytics, Cloud/Infrastructure, AI SaaS with Scientific Best Practices and Regional/Sectoral Adaptations",
    "composition": {
        "task_understanding": 24,
        "enhanced_pitch_deck": 36,
        "case_studies": 9,
        "regional_adaptations": 6,
        "sectoral_adaptations": 6
    },
    "enhancement_types": {
        "psychological_triggers": 10,
        "clarity_structure": 10,
        "bottom_up_market": 10,
        "social_proof_fomo": 6,
        "radical_simplification": 2,
        "network_transformation": 3,
        "regional_adaptations": 6,
        "sectoral_adaptations": 6
    },
    "regional_coverage": {
        "DACH": 3,
        "USA": 3
    },
    "sectoral_coverage": {
        "deep_tech": 3,
        "saas": 3
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
        "Absolute No-Gos vermeiden",
        "Kulturelle Adaptationen (formal vs. narrativ)",
        "Branchenspezifische Metriken (Labordaten vs. User Metrics)"
    ]
}

# Backup erstellen
backup_path = config_path.with_suffix('.json.backup_before_ultimate_dataset')
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

# Config speichern
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"✅ WUPHF Config mit Ultimate Dataset aktualisiert")
print(f"📋 Backup erstellt: {backup_path}")
print(f"🎯 Dataset-Details:")
print(f"   - Pfad: {ultimate_dataset_path}")
print(f"   - Gesamt Beispiele: 95")
print(f"   - Task Understanding: 24")
print(f"   - Enhanced Pitch Deck: 36")
print(f"   - Case Studies: 9")
print(f"   - Regional Adaptations: 6")
print(f"   - Sectoral Adaptations: 6")

print(f"\n🎯 Regionale Abdeckung:")
print(f"   - DACH: 3 Beispiele (formal, detailliert, risikoavers)")
print(f"   - USA: 3 Beispiele (informell, narrativ, risikotolerant)")

print(f"\n🎯 Sektorale Abdeckung:")
print(f"   - Deep Tech: 3 Beispiele (Labordaten, Patente, Lighthouse-Kunden)")
print(f"   - SaaS: 3 Beispiele (User Metrics, Engagement, MRR, Churn)")

print(f"\n🎯 Integrierte Best Practices: 12")
print(f"   - Psychologische Mechanismen")
print(f"   - Strukturelle Paradigmen")
print(f"   - Quantitative Exzellenz")
print(f"   - Design-Prinzipien")
print(f"   - Regionale und sektorale Unterschiede")
print(f"   - Absolute No-Gos")
print(f"   - Fallstudien-Prinzipien")
print(f"   - Kulturelle Adaptationen")
print(f"   - Branchenspezifische Metriken")

print(f"\n📋 System bereit für Training mit:")
print(f"   1. WUPHF neu starten")
print(f"   2. Training mit Ultimate Dataset (95 Beispiele)")
print(f"   3. Agent-Verhalten mit wissenschaftlichen Best Practices validieren")