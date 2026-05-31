#!/usr/bin/env python3
"""
Merge WUPHF Datasets für umfassendes Training
Kombiniert Task-Understanding + Pitch Deck Content
"""

import json
import shutil

def merge_datasets(output_path="wuphf_combined_dataset.jsonl"):
    """Merge alle WUPHF Datasets"""
    
    datasets = [
        ("wuphf_task_dataset.jsonl", "Task Understanding"),
        ("pitch_deck_dataset.jsonl", "Pitch Deck Content")
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
    
    print(f"\n✅ Kombiniertes Dataset erstellt: {output_path}")
    print(f"📊 Gesamt Beispiele: {len(combined_data)}")
    
    # Statistiken
    sources = {}
    roles = {}
    for item in combined_data:
        source = item.get('dataset_source', 'unknown')
        role = item.get('role', 'unknown')
        sources[source] = sources.get(source, 0) + 1
        roles[role] = roles.get(role, 0) + 1
    
    print(f"\n📊 Dataset Sources: {sources}")
    print(f"🎯 Rollen: {roles}")
    
    return output_path

def update_wuphf_config_with_dataset(dataset_path):
    """Aktualisiere WUPHF Config mit neuem Dataset"""
    import json
    
    config_path = "/home/dyai/.wuphf-spaces/main/.wuphf/config.json"
    
    # Config laden
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Dataset Pfad hinzufügen
    if "training_datasets" not in config:
        config["training_datasets"] = {}
    
    config["training_datasets"]["combined"] = {
        "path": dataset_path,
        "description": "Combined WUPHF Training Dataset (Task Understanding + Pitch Deck)",
        "examples": len(open(dataset_path).readlines()),
        "last_updated": "2026-05-27"
    }
    
    # Config speichern
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ WUPHF Config aktualisiert mit Dataset: {dataset_path}")
    return config

def create_training_recommendation():
    """Erstelle Empfehlung für Training"""
    recommendation = """
# WUPHF Training Empfehlung

## Dataset Zusammenfassung
- Task Understanding: 12 Beispiele (CEO, Research, Analyst, Coordination, Task Claiming, Error Handling)
- Pitch Deck Content: 50 Beispiele (Problem, Solution, Market, Business Model, Traction)
- Gesamt: 62 Beispiele

## Training Strategie

### Option 1: System Prompt Engineering (Sofort wirksam)
- Nutze die Beispiele als Few-Shot Context
- Kein Training nötig
- Sofort spürbare Verbesserung

### Option 2: Fine-tuning (Größere Verbesserung)
- LoRA Fine-tuning auf kombiniertem Dataset
- 3-5 Epochs, Learning Rate 2e-4
- Bessere Rollen-spezifische Antworten

### Option 3: Hybrid (Beste Ergebnisse)
- System Prompts für Basis-Verhalten
- Fine-tuning für Pitch Deck Content
- Kombinierte Vorteile

## Empfohlene Vorgehensweise
1. Starte mit System Prompts (bereits installiert)
2. Teste Agent-Verhalten in WUPHF
3. Wenn nötig: Fine-tuning mit Pitch Deck Dataset
4. Kontinuierliche Verbesserung mit mehr Daten

## Nächste Schritte
1. WUPHF neu starten
2. Pitch Deck Aufgaben testen
3. Content-Agent Verhalten beobachten
4. Bei Bedarf Fine-tuning durchführen
"""
    
    with open("wuphf_training_recommendation.md", 'w') as f:
        f.write(recommendation)
    
    print("✅ Training Empfehlung erstellt: wuphf_training_recommendation.md")

def main():
    """Hauptfunktion"""
    print("🎯 WUPHF Dataset Merge und Integration")
    print("=" * 50)
    
    # Datasets mergen
    combined_path = merge_datasets()
    
    # WUPHF Config aktualisieren
    update_wuphf_config_with_dataset(combined_path)
    
    # Training Empfehlung erstellen
    create_training_recommendation()
    
    print("\n" + "=" * 50)
    print("🎉 WUPHF Dataset Integration abgeschlossen!")
    print("\n📋 Nächste Schritte:")
    print("1. WUPHF neu starten")
    print("2. Pitch Deck Content testen")
    print("3. Agent-Verhalten beobachten")
    print("4. Bei Bedarf Fine-tuning durchführen")
    
    print("\n💡 Vorteil: 62 hochwertige Beispiele für bessere Agent-Leistung!")

if __name__ == "__main__":
    main()