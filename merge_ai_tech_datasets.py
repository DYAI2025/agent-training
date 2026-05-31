#!/usr/bin/env python3
"""
Merge AI/Tech Datasets für WUPHF Training
Ersetzt allgemeine Pitch Deck Beispiele mit AI/Tech-spezifischen
"""

import json
import shutil

def merge_ai_tech_datasets(output_path="wuphf_ai_tech_combined_dataset.jsonl"):
    """Merge AI/Tech Datasets"""
    
    datasets = [
        ("wuphf_task_dataset.jsonl", "Task Understanding"),
        ("ai_tech_pitch_dataset.jsonl", "AI/Tech Pitch Deck Content")
    ]
    
    combined_data = []
    
    for dataset_file, description in datasets:
        try:
            with open(dataset_file, 'r') as f:
                for line in f:
                    item = json.loads(line)
                    item['dataset_source'] = description
                    combined_data.append(item)
            print(f"✅ {description} geladen: {dataset_file}")
        except FileNotFoundError:
            print(f"⚠️ {description} nicht gefunden: {dataset_file}")
    
    # Speichern
    with open(output_path, 'w') as f:
        for item in combined_data:
            f.write(json.dumps(item) + '\n')
    
    print(f"\n✅ Kombiniertes AI/Tech Dataset erstellt: {output_path}")
    print(f"📊 Gesamt Beispiele: {len(combined_data)}")
    
    # Statistiken
    sources = {}
    roles = {}
    industries = {}
    for item in combined_data:
        source = item.get('dataset_source', 'unknown')
        role = item.get('role', 'unknown')
        industry = item.get('industry', 'unknown')
        sources[source] = sources.get(source, 0) + 1
        roles[role] = roles.get(role, 0) + 1
        if industry != 'unknown':
            industries[industry] = industries.get(industry, 0) + 1
    
    print(f"\n📊 Dataset Sources: {sources}")
    print(f"🎯 Rollen: {roles}")
    print(f"🏭 Industries: {industries}")
    
    return output_path

def update_wuphf_config_with_ai_tech_dataset(dataset_path):
    """Aktualisiere WUPHF Config mit AI/Tech Dataset"""
    import json
    
    config_path = "/home/dyai/.wuphf-spaces/main/.wuphf/config.json"
    
    # Config laden
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Dataset Pfad hinzufügen
    if "training_datasets" not in config:
        config["training_datasets"] = {}
    
    config["training_datasets"]["ai_tech_combined"] = {
        "path": dataset_path,
        "description": "AI/Tech WUPHF Training Dataset (Task Understanding + AI/Tech Pitch Deck)",
        "examples": len(open(dataset_path).readlines()),
        "last_updated": "2026-05-27",
        "focus": "AI/ML, Developer Tools, Data/Analytics, Cloud/Infrastructure, AI SaaS"
    }
    
    # Config speichern
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ WUPHF Config aktualisiert mit AI/Tech Dataset: {dataset_path}")
    return config

def create_ai_tech_training_recommendation():
    """Erstelle Empfehlung für AI/Tech Training"""
    recommendation = """
# AI/Tech WUPHF Training Empfehlung

## Dataset Zusammenfassung
- Task Understanding: 12 Beispiele (CEO, Research, Analyst, Coordination, Task Claiming, Error Handling)
- AI/Tech Pitch Deck Content: 50 Beispiele (Problem, Solution, Market, Business Model, Traction)
- Gesamt: 62 Beispiele

## AI/Tech Fokus
- AI/ML Startups: 15 Beispiele (AutoML, Computer Vision, LLM, Predictive Analytics, AI Infrastructure)
- Developer Tools: 10 Beispiele (CI/CD, Security Scanning, Developer Experience, Testing, IaC)
- Data/Analytics: 10 Beispiele (Real-time Analytics, Data Quality, BI, Data Engineering, Governance)
- Cloud/Infrastructure: 5 Beispiele (Kubernetes, Serverless, Edge Computing, Multi-Cloud, Monitoring)
- AI SaaS: 10 Beispiele (AI CRM, AI Marketing, AI HR Tech, AI Finance, AI Legal Tech)

## Training Strategie

### Option 1: System Prompt Engineering (Sofort wirksam)
- Nutze die AI/Tech Beispiele als Few-Shot Context
- Kein Training nötig
- Sofort spürbare Verbesserung für AI/Tech Pitch Decks

### Option 2: Fine-tuning (Größere Verbesserung)
- LoRA Fine-tuning auf AI/Tech kombiniertem Dataset
- 3-5 Epochs, Learning Rate 2e-4
- Bessere AI/Tech-spezifische Antworten

### Option 3: Hybrid (Beste Ergebnisse)
- System Prompts für Basis-Verhalten
- Fine-tuning für AI/Tech Pitch Deck Content
- Kombinierte Vorteile

## Empfohlene Vorgehensweise
1. Starte mit System Prompts (bereits installiert)
2. Teste AI/Tech Pitch Deck Aufgaben in WUPHF
3. Bei Bedarf Fine-tuning mit AI/Tech Dataset
4. Kontinuierliche Verbesserung mit mehr AI/Tech Daten

## Nächste Schritte
1. WUPHF neu starten
2. AI/Tech Pitch Deck Aufgaben testen
3. Content-Agent Verhalten beobachten
4. Bei Bedarf Fine-tuning durchführen

## Vorteil für dein Business
- Spezialisiert auf deine Zielgruppe (AI/Tech Startups)
- Bessere Relevanz für deine Kunden
- Höhere Conversion-Rate durch Branchenexpertise
- Differenzierung von generischen Pitch Deck Services
"""
    
    with open("ai_tech_training_recommendation.md", 'w') as f:
        f.write(recommendation)
    
    print("✅ AI/Tech Training Empfehlung erstellt: ai_tech_training_recommendation.md")

def main():
    """Hauptfunktion"""
    print("🎯 AI/Tech WUPHF Dataset Merge und Integration")
    print("=" * 50)
    
    # Datasets mergen
    combined_path = merge_ai_tech_datasets()
    
    # WUPHF Config aktualisieren
    update_wuphf_config_with_ai_tech_dataset(combined_path)
    
    # Training Empfehlung erstellen
    create_ai_tech_training_recommendation()
    
    print("\n" + "=" * 50)
    print("🎉 AI/Tech WUPHF Dataset Integration abgeschlossen!")
    print("\n📋 Nächste Schritte:")
    print("1. WUPHF neu starten")
    print("2. AI/Tech Pitch Deck Aufgaben testen")
    print("3. Agent-Verhalten beobachten")
    print("4. Bei Bedarf Fine-tuning durchführen")
    
    print("\n💡 Vorteil: 62 AI/Tech-spezifische Beispiele für bessere Agent-Leistung!")

if __name__ == "__main__":
    main()