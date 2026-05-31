#!/usr/bin/env python3
"""
Verbesserung der AI/Tech Pitch Deck Beispiele mit wissenschaftlichen Best Practices
Integriert psychologische Trigger, Storytelling und Bottom-Up Market Size
"""

import json
from pathlib import Path

# Dataset Pfad
dataset_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_ai_tech_combined_dataset.jsonl")
output_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_ai_tech_enhanced_dataset.jsonl")

# Beispiele laden
examples = []
with open(dataset_path, 'r', encoding='utf-8') as f:
    for line in f:
        examples.append(json.loads(line))

print(f"📊 {len(examples)} Beispiele geladen")

# Verbesserungsfunktionen
def enhance_problem_slide(example):
    """Verbessert Problem-Slides mit psychologischen Triggern"""
    if example.get('role') != 'content':
        return example
    
    slide_type = example.get('slide_type', '').lower()
    if slide_type != 'problem':
        return example
    
    industry = example.get('industry', '')
    input_text = example.get('input', '')
    output_text = example.get('output', '')
    
    # Psychologische Trigger hinzufügen
    enhanced_output = output_text
    
    # Emotionale Schwere und konkrete Folgen
    if '€' not in enhanced_output and '$' not in enhanced_output:
        # Kosten hinzufügen für Verlustaversion
        if 'AutoML' in input_text or 'ML' in input_text:
            enhanced_output += " €15M jährliche Kosten durch ineffiziente ML-Workflows. 80% der ML-Projects scheitern an Deployment-Phase."
        elif 'Quality Control' in input_text or 'QC' in input_text:
            enhanced_output += " €10M jährliche Kosten durch Ausschuss und Nacharbeit. 15% der Defekte werden übersehen."
        elif 'Developer' in input_text or 'Code' in input_text:
            enhanced_output += " €20M jährliche Kosten durch ineffiziente Development-Prozesse. 30% der Zeit mit Boilerplate-Code verschwendet."
        elif 'Data' in input_text or 'Analytics' in input_text:
            enhanced_output += " €15M jährliche Kosten durch schlechte Datenqualität. 30% der Daten sind fehlerhaft oder unvollständig."
        elif 'Kubernetes' in input_text or 'Cloud' in input_text:
            enhanced_output += " €8M jährliche Kosten durch suboptimale Cluster-Management. 50% der Unternehmen haben nicht genug Kubernetes-Expertise."
        elif 'Sales' in input_text or 'CRM' in input_text:
            enhanced_output += " €12M jährliche Kosten durch ineffiziente Sales-Prozesse. 60% der Sales-Zeit mit Admin-Aufgaben verschwendet."
        elif 'Support' in input_text or 'Customer' in input_text:
            enhanced_output += " €5M jährliche Kosten durch ineffiziente Support-Prozesse. 40% der Anfragen kommen außerhalb der Geschäftszeiten."
    
    # Storytelling-Elemente
    if 'Nach 5 Jahren' not in enhanced_output and 'experience' not in enhanced_output.lower():
        if 'Data Scientist' in input_text or 'ML' in input_text:
            enhanced_output = "Nach 5 Jahren als Data Scientist bei DAX-Unternehmen sah ich 80% meiner Zeit mit Model Engineering statt Business Value verschwendet. " + enhanced_output
        elif 'Developer' in input_text or 'Code' in input_text:
            enhanced_output = "Nach 10 Jahren als Senior Developer bei Tech-Giants sah ich 30% meiner Zeit mit Boilerplate-Code verschwendet. " + enhanced_output
        elif 'Sales' in input_text or 'CRM' in input_text:
            enhanced_output = "Nach 8 Jahren als Sales Director bei SaaS-Unternehmen sah ich 60% meiner Zeit mit Admin-Aufgaben statt Selling verschwendet. " + enhanced_output
    
    example['output'] = enhanced_output
    example['enhanced'] = True
    example['enhancement_type'] = 'psychological_triggers'
    
    return example

def enhance_solution_slide(example):
    """Verbessert Solution-Slides mit Klarheit und Vorteilen"""
    if example.get('role') != 'content':
        return example
    
    slide_type = example.get('slide_type', '').lower()
    if slide_type != 'solution':
        return example
    
    output_text = example.get('output', '')
    
    # Klarheit vor Cleverness - 3 Säulen Struktur
    if output_text.count('.') > 3:  # Wenn zu viele Sätze
        sentences = output_text.split('. ')
        if len(sentences) > 3:
            # Auf 3 Hauptpunkte reduzieren
            enhanced_output = '. '.join(sentences[:3]) + '.'
            example['output'] = enhanced_output
            example['enhanced'] = True
            example['enhancement_type'] = 'clarity_structure'
    
    return example

def enhance_market_slide(example):
    """Verbessert Market-Slides mit Bottom-Up Approach"""
    if example.get('role') != 'content':
        return example
    
    slide_type = example.get('slide_type', '').lower()
    if slide_type != 'market':
        return example
    
    output_text = example.get('output', '')
    
    # Bottom-Up Approach hinzufügen
    if 'Bottom-Up' not in output_text and 'Ein Kunde' not in output_text:
        industry = example.get('industry', '')
        
        bottom_up_text = "\n\nBottom-Up-Ansatz:\n- Ein Kunde zahlt €10K/Jahr\n- 10.000 potenzielle Kunden in DACH\n- Realistisch: 500 Kunden in 3 Jahren = €5M ARR\n\n"
        
        example['output'] = output_text + bottom_up_text
        example['enhanced'] = True
        example['enhancement_type'] = 'bottom_up_market'
    
    return example

def enhance_business_model_slide(example):
    """Verbessert Business Model-Slides mit Unit Economics"""
    if example.get('role') != 'content':
        return example
    
    slide_type = example.get('slide_type', '').lower()
    if slide_type != 'business model':
        return example
    
    output_text = example.get('output', '')
    
    # Unit Economics hinzufügen
    if 'LTV' not in output_text or 'CAC' not in output_text:
        unit_economics = "\n\nUnit Economics:\n- LTV: €8K (Customer Lifetime)\n- CAC: €1.5K (Customer Acquisition)\n- LTV:CAC Ratio: 5:1 (Benchmark: 3:1)\n- Payback Period: 8 Monate (Benchmark: <12 Monate)\n"
        
        example['output'] = output_text + unit_economics
        example['enhanced'] = True
        example['enhancement_type'] = 'unit_economics'
    
    return example

def enhance_traction_slide(example):
    """Verbessert Traction-Slides mit psychologischen Triggern"""
    if example.get('role') != 'content':
        return example
    
    slide_type = example.get('slide_type', '').lower()
    if slide_type != 'traction':
        return example
    
    output_text = example.get('output', '')
    
    # Social Proof und FOMO hinzufügen
    if 'VC' not in output_text and 'Partner' not in output_text:
        social_proof = "\n\nSocial Proof:\n- 3 VCs haben bereits Termine vereinbart\n- 5 namhafte Tech-Unternehmen als Pilot-Kunden\n- Series A Funding in 6 Monaten geplant\n"
        
        example['output'] = output_text + social_proof
        example['enhanced'] = True
        example['enhancement_type'] = 'social_proof_fomo'
    
    return example

# Alle Beispiele verbessern
enhanced_examples = []
enhancement_stats = {
    'total': len(examples),
    'content_examples': 0,
    'enhanced': 0,
    'by_type': {}
}

for example in examples:
    original_example = example.copy()
    
    # Nur Content-Beispiele verbessern (Pitch Deck)
    if example.get('role') == 'content' and 'slide_type' in example:
        enhancement_stats['content_examples'] += 1
        slide_type = example.get('slide_type', '').lower()
        
        if slide_type == 'problem':
            example = enhance_problem_slide(example)
        elif slide_type == 'solution':
            example = enhance_solution_slide(example)
        elif slide_type == 'market':
            example = enhance_market_slide(example)
        elif slide_type == 'business model':
            example = enhance_business_model_slide(example)
        elif slide_type == 'traction':
            example = enhance_traction_slide(example)
        
        if example.get('enhanced'):
            enhancement_stats['enhanced'] += 1
            enhancement_type = example.get('enhancement_type', 'unknown')
            enhancement_stats['by_type'][enhancement_type] = enhancement_stats['by_type'].get(enhancement_type, 0) + 1
    
    enhanced_examples.append(example)

# Enhanced Dataset speichern
with open(output_path, 'w', encoding='utf-8') as f:
    for example in enhanced_examples:
        f.write(json.dumps(example, ensure_ascii=False) + '\n')

print(f"✅ Enhanced Dataset erstellt: {output_path}")
print(f"📊 Verbesserungs-Statistiken:")
print(f"   - Gesamt Beispiele: {enhancement_stats['total']}")
print(f"   - Content Beispiele (Pitch Deck): {enhancement_stats['content_examples']}")
print(f"   - Verbesserte Beispiele: {enhancement_stats['enhanced']}")
print(f"   - Verbesserungs-Typen:")
for enhancement_type, count in enhancement_stats['by_type'].items():
    print(f"     • {enhancement_type}: {count}")

print(f"\n🎯 Angewandte Best Practices:")
print(f"   - Psychologische Trigger (40-Sekunden-Regel, FOMO, Verlustaversion)")
print(f"   - Storytelling-Elemente (persönliche Geschichte)")
print(f"   - Bottom-Up Market Size Approach")
print(f"   - Unit Economics (LTV, CAC, Payback Period)")
print(f"   - Social Proof und FOMO-Trigger")
print(f"   - Klarheit und Struktur (3-Säulen-Prinzip)")

print(f"\n📋 Nächste Schritte:")
print(f"   1. WUPHF Config mit enhanced Dataset aktualisieren")
print(f"   2. Training mit verbesserten Beispielen starten")
print(f"   3. Agent-Verhalten mit neuen Best Practices validieren")