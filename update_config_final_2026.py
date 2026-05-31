#!/usr/bin/env python3
"""
Aktualisierung der WUPHF Config mit dem Final 2026 Dataset
"""

import json
from pathlib import Path

# WUPHF Config Pfad
config_path = Path.home() / ".wuphf-spaces/main/.wuphf/config.json"
final_2026_dataset_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_final_2026_dataset.jsonl")

# Config laden
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Training-Datasets Sektion aktualisieren
if 'training_datasets' not in config:
    config['training_datasets'] = {}

config['training_datasets']['final_2026'] = {
    "path": str(final_2026_dataset_path),
    "description": "Final 2026 WUPHF Training Dataset with Real Pitch Deck Structures, Berlin VC-Scene, and 2026 Benchmarks (Task Understanding + Enhanced AI/Tech Pitch Deck + Case Studies + Real Structures + Berlin/2026)",
    "examples": 120,
    "last_updated": "2026-05-27",
    "focus": "AI/ML, Developer Tools, Data/Analytics, Cloud/Infrastructure, AI SaaS with 2026 Best Practices, Real Pitch Deck Structures, and Berlin VC-Scene Integration",
    "composition": {
        "task_understanding": 24,
        "enhanced_pitch_deck": 36,
        "case_studies": 9,
        "real_pitch_deck_structures": 16,
        "berlin_vc_scene": 9,
        "regional_adaptations": 6,
        "sectoral_adaptations": 6,
        "benchmarks_2026": 6
    },
    "real_pitch_structures": {
        "airbnb": 3,
        "uber": 3,
        "coinbase": 3,
        "linkedin": 3,
        "square": 2,
        "shopify": 2
    },
    "berlin_integration": {
        "climate_tech": 1,
        "ai_talent": 1,
        "deep_tech_funding": 1,
        "government_support": 3
    },
    "benchmarks_2026": {
        "saas_funding_napkin": 2,
        "operation_ai": 1,
        "11_slide_structure": 3
    },
    "best_practices_integrated": [
        "30-Sekunden-Regel (Update von 40-Sekunden)",
        "11-Slide-Struktur (Update von 10-14)",
        "3-30-3-Prinzip (Visual Check, Core Message, Deep Dive)",
        "VC-Frameworks (Sequoia, a16z, YC)",
        "Quantitative Benchmarks 2024/2025 (SaaS Funding Napkin)",
        "Operation AI (Model Centricity, Defensibility, Usage Metrics)",
        "Berliner VC-Szene (KfW, Deutschlandfonds)",
        "Ladder of Proof (Risikominderungs-Signalen)",
        "Who-What-Where-Why-How Framework",
        "Passion-Studie (Visuelle Performance > Inhalt)",
        "Häufige Fehler 2026 (Send-Ahead vs. Presentation)",
        "Real Pitch Deck Structures (Airbnb, Uber, Coinbase, LinkedIn, Square, Shopify)",
        "Psychologische Trigger (FOMO, Verlustaversion)",
        "Storytelling-Struktur",
        "Bottom-Up Market Size Approach",
        "Unit Economics (LTV, CAC, Payback)",
        "Design-Prinzipien (Kognitive Ergonomie)",
        "Regionale Unterschiede (USA vs. DACH vs. Berlin)",
        "Sektorale Differenzen (SaaS vs. Deep Tech)",
        "Fallstudien-Prinzipien (Airbnb, LinkedIn, Coinbase)",
        "Absolute No-Gos vermeiden",
        "Kulturelle Adaptationen (formal vs. narrativ)",
        "Branchenspezifische Metriken (Labordaten vs. User Metrics)"
    ]
}

# Backup erstellen
backup_path = config_path.with_suffix('.json.backup_before_final_2026')
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

# Config speichern
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"✅ WUPHF Config mit Final 2026 Dataset aktualisiert")
print(f"📋 Backup erstellt: {backup_path}")
print(f"🎯 Dataset-Details:")
print(f"   - Pfad: {final_2026_dataset_path}")
print(f"   - Gesamt Beispiele: 120")
print(f"   - Task Understanding: 24")
print(f"   - Enhanced Pitch Deck: 36")
print(f"   - Case Studies: 9")
print(f"   - Real Pitch Deck Structures: 16")
print(f"   - Berlin VC-Szene: 9")
print(f"   - Regional Adaptations: 6")
print(f"   - Sectoral Adaptations: 6")
print(f"   - 2026 Benchmarks: 6")

print(f"\n🎯 Real Pitch Deck Structures:")
print(f"   - Airbnb: 3 Beispiele (Einfachheit)")
print(f"   - Uber: 3 Beispiele (Ineffizienz des aktuellen Systems)")
print(f"   - Coinbase: 3 Beispiele (Logische Evolution)")
print(f"   - LinkedIn: 3 Beispiele (Netzwerkeffekt + Transformation)")
print(f"   - Square: 2 Beispiele (Eleganz in der Komplexität)")
print(f"   - Shopify: 2 Beispiele (Demokratisierung)")

print(f"\n🎯 Berlin VC-Szene Integration:")
print(f"   - Climate Tech Hub (340+ Startups, 814M€ Investment)")
print(f"   - AI Talent Pool (9.000+ Spezialisten)")
print(f"   - Government Funding (KfW Capital, Deutschlandfonds)")
print(f"   - Scale-up Direct (Ko-Investor)")

print(f"\n🎯 2026 Benchmarks:")
print(f"   - SaaS Funding Napkin (Seed ARR 0.25-1.5M, 3x YoY)")
print(f"   - Operation AI (Deep Integration 2x Faster Growth)")
print(f"   - 11-Slide-Struktur (Vision in einem Satz, Timing-Dringlichkeit)")

print(f"\n🎯 Integrierte Best Practices: 22")
print(f"   - 2026 Updates: 30-Sekunden-Regel, 11-Slide-Struktur, 3-30-3-Prinzip")
print(f"   - VC-Frameworks: Sequoia, a16z, YC")
print(f"   - Quantitative Benchmarks 2024/2025")
print(f"   - Real Pitch Deck Structures (6 erfolgreiche Startups)")
print(f"   - Berliner VC-Szene und staatliche Förderung")
print(f"   - Operation AI und Ladder of Proof")

print(f"\n📋 System bereit für Training mit:")
print(f"   1. WUPHF neu starten")
print(f"   2. Training mit Final 2026 Dataset (120 Beispiele)")
print(f"   3. Agent-Verhalten mit 2026 Best Practices validieren")