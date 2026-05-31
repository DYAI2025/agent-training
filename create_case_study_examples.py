#!/usr/bin/env python3
"""
Erstellung neuer Pitch-Deck Beispiele basierend auf Fallstudien
Airbnb: "Clarity beats Cleverness"
LinkedIn: "Netzwerkeffekt + Transformation"
Coinbase: "Radikale Vereinfachung"
"""

import json
from pathlib import Path

# Output Pfad
output_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_case_study_examples.jsonl")

# Fallstudien-Beispiele
case_study_examples = []

# Airbnb-Prinzip: "Clarity beats Cleverness" - Radikale Vereinfachung
airbnb_examples = [
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "ai_ml",
        "input": "Erstelle Problem-Slide für AI-Code-Generation (Airbnb-Prinzip: Clarity beats Cleverness)",
        "output": "Problem: Entwickler schreiben 80% Boilerplate-Code statt Business-Logic. Code-Generation ist komplex und erfordert Prompt-Engineering. Teams verbringen Tage mit Setup statt Features. 60% der Entwickler-Zeit geht für repetitive Aufgaben verloren.",
        "dataset_source": "Case Study - Airbnb Principle",
        "principle": "Clarity beats Cleverness",
        "enhancement_type": "radical_simplification"
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "ai_ml",
        "input": "Erstelle Solution-Slide für AI-Code-Generation (Airbnb-Prinzip: Clarity beats Cleverness)",
        "output": "Solution: AI schreibt Boilerplate-Code automatisch. Entwickler fokussieren auf Business-Logic. 10x schnellere Feature-Entwicklung. Kein Prompt-Engineering erforderlich.",
        "dataset_source": "Case Study - Airbnb Principle",
        "principle": "Clarity beats Cleverness",
        "enhancement_type": "radical_simplification"
    },
    {
        "role": "content",
        "slide_type": "market",
        "industry": "ai_ml",
        "input": "Erstelle Market-Slide für AI-Code-Generation (Airbnb-Prinzip: Clarity beats Cleverness)",
        "output": "Market: Global Developer Tools Market €15B/year. DACH Market €1.5B/year. Serviceable Addressable Market €750M/year (SMEs mit 10+ Entwicklern). Serviceable Obtainable Market €75M/year (10% market share). Growth Rate: 25% CAGR driven by Developer Shortage.",
        "dataset_source": "Case Study - Airbnb Principle",
        "principle": "Clarity beats Cleverness",
        "enhancement_type": "clear_segmentation"
    }
]

# LinkedIn-Prinzip: "Netzwerkeffekt + Transformation"
linkedin_examples = [
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "developer_tools",
        "input": "Erstelle Problem-Slide für Developer-Networking-Platform (LinkedIn-Prinzip: Netzwerkeffekt + Transformation)",
        "output": "Problem: Entwickler arbeiten isoliert ohne Wissensaustausch. Lösungen werden neu erfunden statt geteilt. Knowledge-Silos verlangsamen Innovation. 70% der Entwickler haben keinen Zugang zu Peer-Insights. Lernkurven sind unnötig steil.",
        "dataset_source": "Case Study - LinkedIn Principle",
        "principle": "Network Effect + Transformation",
        "enhancement_type": "network_problem"
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "developer_tools",
        "input": "Erstelle Solution-Slide für Developer-Networking-Platform (LinkedIn-Prinzip: Netzwerkeffekt + Transformation)",
        "output": "Solution: Developer-Networking-Platform für Wissensaustausch. Von isolierten Entwicklern zu kollaborativem Ökosystem. Vertrauensbasierte Code-Sharing und Peer-Reviews. Netzwerkeffekt: Mehr Nutzer = mehr Wissen = mehr Wert.",
        "dataset_source": "Case Study - LinkedIn Principle",
        "principle": "Network Effect + Transformation",
        "enhancement_type": "network_transformation"
    },
    {
        "role": "content",
        "slide_type": "traction",
        "industry": "developer_tools",
        "input": "Erstelle Traction-Slide für Developer-Networking-Platform (LinkedIn-Prinzip: Netzwerkeffekt + Transformation)",
        "output": "Traction: 12 Monate seit Launch. 50K+ Active Developers, 100K+ Code-Snippets geteilt. Netzwerkeffekt: 40% Wachstum durch virale Weiterempfehlung. 30% der Nutzer teilen aktiv Wissen. Revenue €150K MRR, +50% QoQ durch Netzwerk-Skalierung.",
        "dataset_source": "Case Study - LinkedIn Principle",
        "principle": "Network Effect + Transformation",
        "enhancement_type": "network_traction"
    }
]

# Coinbase-Prinzip: "Radikale Vereinfachung" - Nur 7 Folien, 3 Vorteile
coinbase_examples = [
    {
        "role": "content",
        "slide_type": "problem",
        "industry": "data_analytics",
        "input": "Erstelle Problem-Slide für Real-time Analytics (Coinbase-Prinzip: Radikale Vereinfachung - 3 Vorteile)",
        "output": "Problem: Real-time Analytics ist komplex und teuer. Unternehmen haben Daten-Latency von Stunden. Batch-Processing zu langsam für Customer Experience. 50% der Daten werden nie analysiert.",
        "dataset_source": "Case Study - Coinbase Principle",
        "principle": "Radical Simplification",
        "enhancement_type": "3_point_problem"
    },
    {
        "role": "content",
        "slide_type": "solution",
        "industry": "data_analytics",
        "input": "Erstelle Solution-Slide für Real-time Analytics (Coinbase-Prinzip: Radikale Vereinfachung - 3 Vorteile)",
        "output": "Solution: Real-time Analytics Platform mit 3 Vorteilen: 1) Einfach - Setup in 10 Minuten, 2) International - globale Daten-Verarbeitung, 3) Kostenlos - bis 1M events/month. Kein technischer Jargon.",
        "dataset_source": "Case Study - Coinbase Principle",
        "principle": "Radical Simplification",
        "enhancement_type": "3_point_solution"
    },
    {
        "role": "content",
        "slide_type": "business_model",
        "industry": "data_analytics",
        "input": "Erstelle Business Model-Slide für Real-time Analytics (Coinbase-Prinzip: Radikale Vereinfachung)",
        "output": "Business Model: Freemium mit transparentem Pricing. Free: bis 1M events/month. Pro: €999/Month bis 10M events. Enterprise: Custom. Keine versteckten Kosten. Transparente Unit Economics.",
        "dataset_source": "Case Study - Coinbase Principle",
        "principle": "Radical Simplification",
        "enhancement_type": "transparent_pricing"
    }
]

# Alle Beispiele sammeln
case_study_examples.extend(airbnb_examples)
case_study_examples.extend(linkedin_examples)
case_study_examples.extend(coinbase_examples)

# Speichern
with open(output_path, 'w', encoding='utf-8') as f:
    for example in case_study_examples:
        f.write(json.dumps(example, ensure_ascii=False) + '\n')

print(f"✅ Fallstudien-Beispiele erstellt: {output_path}")
print(f"📊 Statistiken:")
print(f"   - Gesamt Beispiele: {len(case_study_examples)}")
print(f"   - Airbnb-Prinzip (Clarity beats Cleverness): {len(airbnb_examples)}")
print(f"   - LinkedIn-Prinzip (Netzwerkeffekt + Transformation): {len(linkedin_examples)}")
print(f"   - Coinbase-Prinzip (Radikale Vereinfachung): {len(coinbase_examples)}")

print(f"\n🎯 Angewandte Prinzipien:")
print(f"   - Airbnb: Radikale Vereinfachung, klare Segmentierung")
print(f"   - LinkedIn: Netzwerkeffekt, Transformation von statisch zu dynamisch")
print(f"   - Coinbase: 3-Punkte-Struktur, keine technischen Details, transparentes Pricing")

print(f"\n📋 Nächste Schritte:")
print(f"   1. Fallstudien-Beispiele mit enhanced Dataset mergen")
print(f"   2. Regionale Unterschiede (USA vs. DACH) integrieren")
print(f"   3. Deep Tech vs. SaaS spezifische Beispiele erstellen")