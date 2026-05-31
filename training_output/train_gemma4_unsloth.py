#!/usr/bin/env python3
"""
Training Script für gemma4:e4b mit Pitch-Deck 2026 Dataset
Verwendet lokales Ollama-Modell und Fine-tuning über API
"""

import json
import requests
from pathlib import Path

# Konfiguration
OLLAMA_MODEL = "gemma4:e4b"
DATASET_PATH = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/training_output/pitchdeck_2026_unsloth.json")
OUTPUT_DIR = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/training_output/gemma4_pitchdeck_2026")

# Dataset laden
with open(DATASET_PATH, 'r', encoding='utf-8') as f:
    training_data = json.load(f)

print(f"📊 Dataset geladen: {len(training_data)} Beispiele")
print(f"🎯 Modell: {OLLAMA_MODEL}")

# Output-Verzeichnis erstellen
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
print(f"📁 Output-Verzeichnis erstellt: {OUTPUT_DIR}")

# Ollama API für Fine-tuning (falls verfügbar)
def check_ollama_finetuning():
    """Prüft ob Ollama Fine-tuning unterstützt"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Ollama läuft, verfügbare Modelle: {list(models.get('models', {}).keys())}")
            return True
    except Exception as e:
        print(f"⚠️ Ollama nicht erreichbar: {e}")
        return False

# Alternative: Few-Shot Learning mit System Prompt
def create_fewshot_examples():
    """Erstellt Few-Shot Beispiele für System-Prompt-Integration"""
    examples = []
    for i, example in enumerate(training_data[:10]):  # Top 10 Beispiele
        examples.append({
            "user": example['instruction'],
            "assistant": example['output']
        })
    return examples

# System-Prompt mit Pitch-Deck Expertise erweitern
pitchdeck_system_prompt = """Du bist ein Pitch-Deck Experte für AI/Tech-Startups mit 2026 Best Practices.

DEINE EXPERTISE:
- 30-Sekunden-Regel (Hook in 30 Sekunden)
- 11-Slide-Struktur (Intro, Problem, Solution, Warum jetzt, Markt, Wettbewerb, Produkt, Traktion, Business Model, Team, Ask)
- VC-Frameworks (Sequoia Capital, Andreessen Horowitz, Y Combinator)
- Quantitative Benchmarks 2024/2025 (SaaS Funding Napkin, Unit Economics)
- Operation AI (Deep Integration vs. oberflächliche Features)
- Berliner VC-Szene (KfW Capital, Deutschlandfonds, Climate Tech Hub)
- Echte Pitch-Deck-Strukturen (Airbnb, Uber, Coinbase, LinkedIn, Square, Shopify)

DEIN VERHALTEN:
1. Nutze 30-Sekunden-Hook für sofortige Aufmerksamkeit
2. Folge 11-Slide-Struktur für 2026 VC-Erwartungen
3. Integriere VC-Frameworks (Sequoia: Klarheit, a16z: Founder-Market Fit, YC: 2-Satz-Test)
4. Nutze quantitative Benchmarks (Seed ARR 0.25-1.5M, Series A 1.5-5M, LTV:CAC ≥ 3:1)
5. Berücksichtige Berliner VC-Szene und staatliche Förderung
6. Vermeide No-Gos (NDA vor Erstkontakt, "Keine Konkurrenz", unrealistische Projektionen)
7. Fokuss auf "Clarity beats Cleverness" (Airbnb-Prinzip)
8. Erzeuge FOMO und Verlustaversion durch psychologische Trigger
9. Nutze Bottom-Up Market Size Approach statt Fantasy Math
10. Zeige echte Traktion mit Trends statt statischen Daten

BEISPIEL-ANTWORT:
"Erstelle Problem-Slide für AI-Startup" → 
"Problem: Data Scientists verbringen 80% ihrer Zeit mit Model Engineering statt Business Value. AutoML Tools sind komplex und erfordern ML-Expertise. Kleinere Unternehmen haben keine Ressourcen für ML-Teams. 70% der ML-Projects scheitern an der Deployment-Phase. Zeit-to-Market für AI-Features ist zu lang."

"""

# Few-Shot Beispiele erstellen
fewshot_examples = create_fewshot_examples()

print(f"✅ Few-Shot Beispiele erstellt: {len(fewshot_examples)}")

# System-Prompt mit Few-Shot Beispielen speichern
system_prompt_path = OUTPUT_DIR / "pitchdeck_system_prompt.txt"
with open(system_prompt_path, 'w', encoding='utf-8') as f:
    f.write(pitchdeck_system_prompt)
    f.write("\n\n### FEW-SHOT BEISPIE:\n\n")
    for i, example in enumerate(fewshot_examples):
        f.write(f"### Beispiel {i+1}:\n")
        f.write(f"User: {example['user']}\n")
        f.write(f"Assistant: {example['assistant']}\n\n")

print(f"✅ System-Prompt mit Few-Shot Beispielen gespeichert: {system_prompt_path}")

# Ollama Modelfile erstellen (Custom Modelfile)
modelfile_content = f"""FROM {OLLAMA_MODEL}
PARAMETER temperature 0.7
PARAMETER top_p 0.9
SYSTEM Du bist ein Pitch-Deck Experte fuer AI/Tech-Startups mit 2026 Best Practices. 30-Sekunden-Regel, 11-Slide-Struktur, VC-Frameworks (Sequoia, a16z, YC), Quantitative Benchmarks 2024/2025, Operation AI, Berliner VC-Szene, Echte Pitch-Deck-Strukturen (Airbnb, Uber, Coinbase, LinkedIn, Square, Shopify).
"""

modelfile_path = OUTPUT_DIR / "Modelfile"
with open(modelfile_path, 'w', encoding='utf-8') as f:
    f.write(modelfile_content)

print(f"✅ Ollama Modelfile erstellt: {modelfile_path}")

# Anweisungen für Ollama Custom Model
print(f"\n🎯 Pitch-Deck Training Setup abgeschlossen!")
print(f"📋 Nächste Schritte:")
print(f"   1. Ollama Custom Model erstellen:")
print(f"      ollama create pitchdeck-2026 -f {modelfile_path}")
print(f"   2. Custom Model testen:")
print(f"      ollama run pitchdeck-2026")
print(f"   3. WUPHF Config auf neues Model updaten:")
print(f"      content agent → pitchdeck-2026")
print(f"\n💡 Alternative: Few-Shot Learning")
print(f"   - System-Prompt mit Expertise erweitert")
print(f"   - Few-Shot Beispiele für kontextuelle Lernung")
print(f"   - Kein Fine-tuning erforderlich, sofort einsatzbereit")
