#!/usr/bin/env python3
"""
Final Merge: Ultimate + Real Pitch Deck + Berlin/2026 Examples
Erstellt das abschließende comprehensive Dataset für WUPHF Training 2026
"""

import json
from pathlib import Path
from collections import Counter

# Pfade
ultimate_dataset_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_ultimate_dataset.jsonl")
real_pitch_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_real_pitch_deck_examples.jsonl")
berlin_2026_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_berlin_2026_examples.jsonl")
final_output_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_final_2026_dataset.jsonl")

# Alle Beispiele laden
all_examples = []

# Ultimate Dataset laden
with open(ultimate_dataset_path, 'r', encoding='utf-8') as f:
    for line in f:
        all_examples.append(json.loads(line))

# Real Pitch Deck Examples laden
with open(real_pitch_path, 'r', encoding='utf-8') as f:
    for line in f:
        all_examples.append(json.loads(line))

# Berlin/2026 Examples laden
with open(berlin_2026_path, 'r', encoding='utf-8') as f:
    for line in f:
        all_examples.append(json.loads(line))

print(f"📊 Final 2026 Dataset-Statistiken:")
print(f"   - Ultimate Dataset: {len([ex for ex in all_examples if 'dataset_source' in ex and 'Case Study' not in ex.get('dataset_source', '') and 'Regional' not in ex.get('dataset_source', '') and 'Real' not in ex.get('source', '')])} Beispiele")
print(f"   - Real Pitch Deck Structures: {len([ex for ex in all_examples if 'structure_source' in ex])} Beispiele")
print(f"   - Berlin VC-Szene: {len([ex for ex in all_examples if 'region' in ex and ex.get('region') == 'Berlin'])} Beispiele")
print(f"   - 2026 Benchmarks: {len([ex for ex in all_examples if 'benchmark_year' in ex or 'structure_version' in ex])} Beispiele")
print(f"   - Gesamt: {len(all_examples)} Beispiele")

# Detaillierte Analyse
role_distribution = Counter(ex.get('role', 'unknown') for ex in all_examples)
slide_type_distribution = Counter(ex.get('slide_type', 'unknown') for ex in all_examples if ex.get('slide_type'))
industry_distribution = Counter(ex.get('industry', 'unknown') for ex in all_examples if ex.get('industry'))
enhancement_distribution = Counter(ex.get('enhancement_type', 'not_enhanced') for ex in all_examples if 'enhancement_type' in ex)
structure_source_distribution = Counter(ex.get('structure_source', 'not_structured') for ex in all_examples if 'structure_source' in ex)
regional_distribution = Counter(ex.get('region', 'not_regional') for ex in all_examples if 'region' in ex)
benchmark_distribution = Counter(ex.get('benchmark_year', 'not_benchmark') for ex in all_examples if 'benchmark_year' in ex)

print(f"\n📋 Verteilung:")
print(f"   - Rollen: {dict(role_distribution)}")
print(f"   - Slide Types: {dict(slide_type_distribution)}")
print(f"   - Industries: {dict(industry_distribution)}")
print(f"   - Enhancement Types: {dict(enhancement_distribution)}")
print(f"   - Structure Sources: {dict(structure_source_distribution)}")
print(f"   - Regionen: {dict(regional_distribution)}")
print(f"   - Benchmark Years: {dict(benchmark_distribution)}")

# Final Dataset speichern
with open(final_output_path, 'w', encoding='utf-8') as f:
    for example in all_examples:
        f.write(json.dumps(example, ensure_ascii=False) + '\n')

print(f"\n✅ Final 2026 Dataset erstellt: {final_output_path}")
print(f"🎯 Dataset-Zusammensetzung:")
print(f"   - Task Understanding: {role_distribution.get('ceo', 0) + role_distribution.get('research', 0) + role_distribution.get('analyst', 0) + role_distribution.get('coordination', 0) + role_distribution.get('task_claiming', 0) + role_distribution.get('error_handling', 0)} Beispiele")
print(f"   - Enhanced Pitch Deck: {sum(1 for ex in all_examples if ex.get('role') == 'content' and 'enhanced' in ex)} Beispiele")
print(f"   - Case Studies: {sum(1 for ex in all_examples if 'principle' in ex)} Beispiele")
print(f"   - Real Pitch Deck Structures: {sum(1 for ex in all_examples if 'structure_source' in ex)} Beispiele")
print(f"   - Berlin VC-Szene: {sum(1 for ex in all_examples if 'region' in ex)} Beispiele")
print(f"   - 2026 Benchmarks: {sum(1 for ex in all_examples if 'benchmark_year' in ex or 'structure_version' in ex)} Beispiele")

print(f"\n🎯 2026 Exklusiv-Elemente:")
print(f"   - Real Pitch Deck Structures: {sum(structure_source_distribution.values())} Beispiele")
print(f"   - Berlin VC-Szene Integration: {sum(regional_distribution.values())} Beispiele")
print(f"   - 2026 Benchmarks: {sum(benchmark_distribution.values())} Beispiele")
print(f"   - 11-Slide-Struktur 2026: {sum(1 for ex in all_examples if 'structure_version' in ex)} Beispiele")

print(f"\n🎯 Integrierte Best Practices 2026:")
print(f"   - 30-Sekunden-Regel: {sum(1 for ex in all_examples if '30_second_hook' in ex.get('enhancement_type', ''))} Beispiele")
print(f"   - VC-Frameworks: {sum(structure_source_distribution.values())} Beispiele")
print(f"   - Quantitative Benchmarks: {sum(benchmark_distribution.values())} Beispiele")
print(f"   - Operation AI: {sum(1 for ex in all_examples if 'operation_ai' in ex.get('enhancement_type', ''))} Beispiele")
print(f"   - Berliner VC-Szene: {sum(regional_distribution.values())} Beispiele")

print(f"\n📋 Nächste Schritte:")
print(f"   1. WUPHF Config mit Final 2026 Dataset aktualisieren")
print(f"   2. Validierung der finalen Trainingsdaten")
print(f"   3. Training mit Final 2026 Dataset starten")