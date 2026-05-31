#!/usr/bin/env python3
"""
Final Merge: Comprehensive + Regional/Sectoral Examples
Erstellt das ultimative Dataset für WUPHF Training mit allen Best Practices
"""

import json
from pathlib import Path
from collections import Counter

# Pfade
final_dataset_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_final_comprehensive_dataset.jsonl")
regional_sectoral_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_regional_sectoral_examples.jsonl")
ultimate_output_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_ultimate_dataset.jsonl")

# Alle Beispiele laden
all_examples = []

# Final Comprehensive Dataset laden
with open(final_dataset_path, 'r', encoding='utf-8') as f:
    for line in f:
        all_examples.append(json.loads(line))

# Regional/Sectoral Examples laden
with open(regional_sectoral_path, 'r', encoding='utf-8') as f:
    for line in f:
        all_examples.append(json.loads(line))

print(f"📊 Ultimate Dataset-Statistiken:")
print(f"   - Final Comprehensive: {len([ex for ex in all_examples if 'dataset_source' in ex and 'Case Study' not in ex.get('dataset_source', '') and 'Regional' not in ex.get('dataset_source', '')])} Beispiele")
print(f"   - Case Studies: {len([ex for ex in all_examples if 'principle' in ex])} Beispiele")
print(f"   - Regional/Sectoral: {len([ex for ex in all_examples if 'region' in ex or 'sector' in ex])} Beispiele")
print(f"   - Gesamt: {len(all_examples)} Beispiele")

# Detaillierte Analyse
role_distribution = Counter(ex.get('role', 'unknown') for ex in all_examples)
slide_type_distribution = Counter(ex.get('slide_type', 'unknown') for ex in all_examples if ex.get('slide_type'))
industry_distribution = Counter(ex.get('industry', 'unknown') for ex in all_examples if ex.get('industry'))
enhancement_distribution = Counter(ex.get('enhancement_type', 'not_enhanced') for ex in all_examples if 'enhancement_type' in ex)
regional_distribution = Counter(ex.get('region', 'not_regional') for ex in all_examples if 'region' in ex)
sectoral_distribution = Counter(ex.get('sector', 'not_sectoral') for ex in all_examples if 'sector' in ex)
cultural_distribution = Counter(ex.get('cultural_adaptation', 'not_cultural') for ex in all_examples if 'cultural_adaptation' in ex)

print(f"\n📋 Verteilung:")
print(f"   - Rollen: {dict(role_distribution)}")
print(f"   - Slide Types: {dict(slide_type_distribution)}")
print(f"   - Industries: {dict(industry_distribution)}")
print(f"   - Enhancement Types: {dict(enhancement_distribution)}")
print(f"   - Regionen: {dict(regional_distribution)}")
print(f"   - Sektoren: {dict(sectoral_distribution)}")
print(f"   - Kulturelle Adaptationen: {dict(cultural_distribution)}")

# Ultimate Dataset speichern
with open(ultimate_output_path, 'w', encoding='utf-8') as f:
    for example in all_examples:
        f.write(json.dumps(example, ensure_ascii=False) + '\n')

print(f"\n✅ Ultimate Dataset erstellt: {ultimate_output_path}")
print(f"🎯 Dataset-Zusammensetzung:")
print(f"   - Task Understanding: {role_distribution.get('ceo', 0) + role_distribution.get('research', 0) + role_distribution.get('analyst', 0) + role_distribution.get('coordination', 0) + role_distribution.get('task_claiming', 0) + role_distribution.get('error_handling', 0)} Beispiele")
print(f"   - AI/Tech Pitch Deck (Enhanced): {sum(1 for ex in all_examples if ex.get('role') == 'content' and 'enhanced' in ex)} Beispiele")
print(f"   - Case Studies: {sum(1 for ex in all_examples if 'principle' in ex)} Beispiele")
print(f"   - Regional (DACH/USA): {sum(1 for ex in all_examples if 'region' in ex)} Beispiele")
print(f"   - Sektoral (Deep Tech/SaaS): {sum(1 for ex in all_examples if 'sector' in ex)} Beispiele")

print(f"\n🎯 Integrierte Best Practices:")
print(f"   - Psychologische Trigger: {enhancement_distribution.get('psychological_triggers', 0)} Beispiele")
print(f"   - Klarheits-Struktur: {enhancement_distribution.get('clarity_structure', 0)} Beispiele")
print(f"   - Bottom-Up Market: {enhancement_distribution.get('bottom_up_market', 0)} Beispiele")
print(f"   - Social Proof/FOMO: {enhancement_distribution.get('social_proof_fomo', 0)} Beispiele")
print(f"   - Regionale Adaptationen: {sum(regional_distribution.values())} Beispiele")
print(f"   - Sektorale Adaptationen: {sum(sectoral_distribution.values())} Beispiele")

print(f"\n📋 Nächste Schritte:")
print(f"   1. WUPHF Config mit Ultimate Dataset aktualisieren")
print(f"   2. Validierung der neuen Trainingsdaten")
print(f"   3. Training mit Ultimate Dataset starten")