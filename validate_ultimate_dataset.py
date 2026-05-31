#!/usr/bin/env python3
"""
Validierung der Ultimate Trainingsdaten
Erstellt lesbare Formate für Überprüfung und Quality-Check
"""

import json
from pathlib import Path
from collections import Counter

# Ultimate Dataset Pfad
ultimate_dataset_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_ultimate_dataset.jsonl")
validation_output_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/ultimate_dataset_validation.md")

# Dataset laden
examples = []
with open(ultimate_dataset_path, 'r', encoding='utf-8') as f:
    for line in f:
        examples.append(json.loads(line))

print(f"📊 {len(examples)} Beispiele für Validierung geladen")

# Quality Checks
quality_checks = {
    'total_examples': len(examples),
    'missing_fields': [],
    'invalid_json': [],
    'duplicate_inputs': [],
    'empty_outputs': [],
    'role_distribution': Counter(),
    'slide_type_distribution': Counter(),
    'enhancement_coverage': 0
}

# Validierung
input_set = set()
for i, example in enumerate(examples):
    # Pflichtfelder checken
    required_fields = ['role', 'input', 'output']
    for field in required_fields:
        if field not in example or not example[field]:
            quality_checks['missing_fields'].append(f"Example {i}: Missing {field}")
    
    # Leere Outputs checken
    if example.get('output', '').strip() == '':
        quality_checks['empty_outputs'].append(f"Example {i}: Empty output")
    
    # Duplicate Inputs checken (nur für Content-Role, da Task Understanding absichtlich duplicates hat)
    input_text = example.get('input', '')
    if example.get('role') == 'content':  # Nur bei Content-Role auf duplicates prüfen
        if input_text in input_set:
            quality_checks['duplicate_inputs'].append(f"Example {i}: Duplicate input")
        input_set.add(input_text)
    
    # Verteilungen tracken
    quality_checks['role_distribution'][example.get('role', 'unknown')] += 1
    if 'slide_type' in example:
        quality_checks['slide_type_distribution'][example.get('slide_type', 'unknown')] += 1
    
    # Enhancement Coverage
    if 'enhancement_type' in example or 'principle' in example or 'region' in example or 'sector' in example:
        quality_checks['enhancement_coverage'] += 1

# Validierungs-Report erstellen
validation_report = f"""# Ultimate Dataset Validation Report

## 📊 Dataset-Übersicht

- **Gesamt Beispiele:** {quality_checks['total_examples']}
- **Enhancement Coverage:** {quality_checks['enhancement_coverage']}/{quality_checks['total_examples']} ({quality_checks['enhancement_coverage']/quality_checks['total_examples']*100:.1f}%)
- **Validierungs-Datum:** 2026-05-27

## ✅ Quality Checks

### Pflichtfelder
- **Missing Fields:** {len(quality_checks['missing_fields'])}
"""
if quality_checks['missing_fields']:
    validation_report += f"\n⚠️ **Probleme:**\n"
    for issue in quality_checks['missing_fields'][:5]:  # Nur erste 5 zeigen
        validation_report += f"  - {issue}\n"
else:
    validation_report += f"\n✅ **Alle Pflichtfelder vorhanden**\n"

validation_report += f"""
### Datenqualität
- **Empty Outputs:** {len(quality_checks['empty_outputs'])}
"""
if quality_checks['empty_outputs']:
    validation_report += f"\n⚠️ **Probleme:**\n"
    for issue in quality_checks['empty_outputs'][:5]:
        validation_report += f"  - {issue}\n"
else:
    validation_report += f"\n✅ **Keine leeren Outputs**\n"

validation_report += f"""
### Duplicate Inputs
- **Duplicate Inputs:** {len(quality_checks['duplicate_inputs'])}
"""
if quality_checks['duplicate_inputs']:
    validation_report += f"\n⚠️ **Probleme:**\n"
    for issue in quality_checks['duplicate_inputs'][:5]:
        validation_report += f"  - {issue}\n"
else:
    validation_report += f"\n✅ **Keine Duplicate Inputs**\n"

validation_report += f"""
## 📋 Verteilung

### Rollen
"""
for role, count in quality_checks['role_distribution'].most_common():
    validation_report += f"- **{role}:** {count}\n"

validation_report += f"""
### Slide Types
"""
for slide_type, count in quality_checks['slide_type_distribution'].most_common():
    validation_report += f"- **{slide_type}:** {count}\n"

validation_report += f"""
## 🎯 Enhancement Coverage

- **Enhanced Examples:** {quality_checks['enhancement_coverage']}
- **Coverage Rate:** {quality_checks['enhancement_coverage']/quality_checks['total_examples']*100:.1f}%

## 📋 Beispiel-Kategorien

### Task Understanding
{sum(1 for ex in examples if ex.get('role') in ['ceo', 'research', 'analyst', 'coordination', 'task_claiming', 'error_handling'])} Beispiele

### Enhanced Pitch Deck
{sum(1 for ex in examples if 'enhanced' in ex)} Beispiele

### Case Studies
{sum(1 for ex in examples if 'principle' in ex)} Beispiele

### Regional Adaptations
{sum(1 for ex in examples if 'region' in ex)} Beispiele

### Sectoral Adaptations
{sum(1 for ex in examples if 'sector' in ex)} Beispiele

## 🎯 Best Practices Integration

### Psychologische Trigger
{sum(1 for ex in examples if ex.get('enhancement_type') == 'psychological_triggers')} Beispiele

### Klarheits-Struktur
{sum(1 for ex in examples if ex.get('enhancement_type') == 'clarity_structure')} Beispiele

### Bottom-Up Market
{sum(1 for ex in examples if ex.get('enhancement_type') == 'bottom_up_market')} Beispiele

### Social Proof/FOMO
{sum(1 for ex in examples if ex.get('enhancement_type') == 'social_proof_fomo')} Beispiele

## ✅ Validierungs-Ergebnis

"""

# Gesamt-Validierung
total_issues = len(quality_checks['missing_fields']) + len(quality_checks['empty_outputs']) + len(quality_checks['duplicate_inputs'])
if total_issues == 0:
    validation_report += f"**✅ BESTANDEN** - Dataset ist qualitativ hochwertig und bereit für Training.\n\n"
    validation_report += f"**Empfehlung:** Dataset kann für WUPHF Training verwendet werden.\n"
else:
    validation_report += f"⚠️ **{total_issues} Probleme gefunden** - Dataset sollte überprüft werden.\n\n"
    validation_report += f"**Empfehlung:** Probleme beheben vor Training.\n"

# Speichern
with open(validation_output_path, 'w', encoding='utf-8') as f:
    f.write(validation_report)

print(f"✅ Validierungs-Report erstellt: {validation_output_path}")
print(f"📊 Quality Check Ergebnisse:")
print(f"   - Gesamt Beispiele: {quality_checks['total_examples']}")
print(f"   - Missing Fields: {len(quality_checks['missing_fields'])}")
print(f"   - Empty Outputs: {len(quality_checks['empty_outputs'])}")
print(f"   - Duplicate Inputs: {len(quality_checks['duplicate_inputs'])}")
print(f"   - Enhancement Coverage: {quality_checks['enhancement_coverage']}/{quality_checks['total_examples']} ({quality_checks['enhancement_coverage']/quality_checks['total_examples']*100:.1f}%)")

if total_issues == 0:
    print(f"\n✅ Dataset ist qualitativ hochwertig und bereit für Training!")
else:
    print(f"\n⚠️ {total_issues} Probleme gefunden - bitte überprüfen")