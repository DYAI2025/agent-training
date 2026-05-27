#!/usr/bin/env python3
"""
Merge aller Datasets: Enhanced + Case Studies + Task Understanding
Erstellt das finale comprehensive Dataset für WUPHF Training
"""

import json
from pathlib import Path
from collections import Counter

# Pfade
enhanced_dataset_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_ai_tech_enhanced_dataset.jsonl")
case_study_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_case_study_examples.jsonl")
task_dataset_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_task_dataset.jsonl")
output_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_final_comprehensive_dataset.jsonl")

# Alle Beispiele laden
all_examples = []

# Enhanced Dataset laden
with open(enhanced_dataset_path, 'r', encoding='utf-8') as f:
    for line in f:
        all_examples.append(json.loads(line))

# Case Study Examples laden
with open(case_study_path, 'r', encoding='utf-8') as f:
    for line in f:
        all_examples.append(json.loads(line))

# Task Understanding Dataset laden
with open(task_dataset_path, 'r', encoding='utf-8') as f:
    for line in f:
        all_examples.append(json.loads(line))

print(f"📊 Dataset-Statistiken:")
print(f"   - Enhanced Dataset: {sum(1 for ex in all_examples if 'enhanced' in ex)} Beispiele")
print(f"   - Case Study Examples: {sum(1 for ex in all_examples if 'principle' in ex)} Beispiele")
print(f"   - Task Understanding: {sum(1 for ex in all_examples if ex.get('dataset_source') == 'Task Understanding')} Beispiele")
print(f"   - Gesamt: {len(all_examples)} Beispiele")

# Analyse der Verteilung
role_distribution = Counter(ex.get('role', 'unknown') for ex in all_examples)
slide_type_distribution = Counter(ex.get('slide_type', 'unknown') for ex in all_examples if ex.get('slide_type'))
industry_distribution = Counter(ex.get('industry', 'unknown') for ex in all_examples if ex.get('industry'))
enhancement_distribution = Counter(ex.get('enhancement_type', 'not_enhanced') for ex in all_examples if 'enhancement_type' in ex)

print(f"\n📋 Verteilung:")
print(f"   - Rollen: {dict(role_distribution)}")
print(f"   - Slide Types: {dict(slide_type_distribution)}")
print(f"   - Industries: {dict(industry_distribution)}")
print(f"   - Enhancement Types: {dict(enhancement_distribution)}")

# Final Dataset speichern
with open(output_path, 'w', encoding='utf-8') as f:
    for example in all_examples:
        f.write(json.dumps(example, ensure_ascii=False) + '\n')

print(f"\n✅ Final Comprehensive Dataset erstellt: {output_path}")
print(f"🎯 Dataset-Zusammensetzung:")
print(f"   - Task Understanding: {role_distribution.get('ceo', 0) + role_distribution.get('research', 0) + role_distribution.get('analyst', 0) + role_distribution.get('coordination', 0) + role_distribution.get('task_claiming', 0) + role_distribution.get('error_handling', 0)} Beispiele")
print(f"   - AI/Tech Pitch Deck (Enhanced): {sum(1 for ex in all_examples if ex.get('role') == 'content' and 'enhanced' in ex)} Beispiele")
print(f"   - Case Study Examples: {sum(1 for ex in all_examples if 'principle' in ex)} Beispiele")

print(f"\n📋 Nächste Schritte:")
print(f"   1. WUPHF Config mit final Dataset aktualisieren")
print(f"   2. Regionale Unterschiede (USA vs. DACH) in zukünftige Beispiele integrieren")
print(f"   3. Deep Tech vs. SaaS spezifische Beispiele erstellen")
print(f"   4. Training mit comprehensive Dataset starten")