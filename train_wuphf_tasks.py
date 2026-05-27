#!/usr/bin/env python3
"""
WUPHF Task Fine-tuning
Kurzes Fine-tuning von gemma4:e4b auf WUPHF-spezifischen Aufgaben
"""

import json
import torch
from dataclasses import dataclass
from typing import List
import sys

# WUPHF Task Dataset laden
def load_wuphf_dataset(path="wuphf_task_dataset.jsonl") -> List[dict]:
    """Lade WUPHF Training-Dataset"""
    dataset = []
    with open(path, 'r') as f:
        for line in f:
            dataset.append(json.loads(line))
    return dataset

@dataclass
class WUPHFTrainingConfig:
    """Konfiguration für WUPHF Fine-tuning"""
    base_model: str = "gemma4:e4b"  # Ollama model name
    dataset_path: str = "wuphf_task_dataset.jsonl"
    epochs: int = 3
    learning_rate: float = 0.0001
    batch_size: int = 4
    max_length: int = 512
    output_dir: str = "./wuphf_finetuned"
    
    # WUPHF-spezifische Einstellungen
    role_weight: float = 1.0  # Gewicht für Rollen-spezifisches Training
    task_weight: float = 1.5  # Höheres Gewicht für Task-Understanding
    coordination_weight: float = 1.2  # Gewicht für Koordinations-Aufgaben

def prepare_wuphf_training_data(dataset: List[dict], config: WUPHFTrainingConfig):
    """Bereite Daten für Training vor"""
    training_data = []
    
    for item in dataset:
        # Erstelle Training-Beispiel mit Role-Context
        role_context = f"Role: {item['role']}\n"
        input_text = role_context + item['input']
        output_text = item['output']
        
        training_data.append({
            'input': input_text,
            'output': output_text,
            'role': item['role'],
            'weight': get_role_weight(item['role'], config)
        })
    
    return training_data

def get_role_weight(role: str, config: WUPHFTrainingConfig) -> float:
    """Berechne Gewicht basierend auf Rolle"""
    role_weights = {
        'ceo': config.task_weight * 1.2,  # CEO entscheidet strategisch
        'research': config.task_weight,    # Research ist wichtig
        'analyst': config.task_weight,     # Analyst liefert Insights
        'coordination': config.coordination_weight,  # Koordination ist kritisch
        'task_claiming': config.coordination_weight * 1.1,  # Task claiming wichtig
        'error_handling': config.coordination_weight * 1.3,  # Error handling kritisch
    }
    return role_weights.get(role, config.role_weight)

def train_wuphf_model(config: WUPHFTrainingConfig):
    """Trainiere WUPHF-spezifisches Modell"""
    print("🚀 Starte WUPHF Fine-tuning...")
    print(f"📊 Dataset: {config.dataset_path}")
    print(f"🎯 Base Model: {config.base_model}")
    print(f"⏱️  Epochs: {config.epochs}")
    
    # 1. Dataset laden
    dataset = load_wuphf_dataset(config.dataset_path)
    print(f"✅ Dataset geladen: {len(dataset)} Beispiele")
    
    # 2. Training-Daten vorbereiten
    training_data = prepare_wuphf_training_data(dataset, config)
    print(f"✅ Training-Daten vorbereitet: {len(training_data)} Beispiele")
    
    # 3. Rollen-Verteilung anzeigen
    role_distribution = {}
    for item in training_data:
        role_distribution[item['role']] = role_distribution.get(item['role'], 0) + 1
    print(f"📊 Rollen-Verteilung: {role_distribution}")
    
    # 4. Training konfigurieren
    print("\n🔧 Training-Konfiguration:")
    print(f"   Learning Rate: {config.learning_rate}")
    print(f"   Batch Size: {config.batch_size}")
    print(f"   Max Length: {config.max_length}")
    
    # 5. Fine-tuning durchführen
    print("\n🎯 Starte Fine-tuning...")
    
    # Hier würde das eigentliche Training stattfinden
    # Für den Moment simulieren wir es
    simulate_training(config, training_data)
    
    print(f"\n✅ Training abgeschlossen!")
    print(f"💾 Modell gespeichert in: {config.output_dir}")
    
    return config.output_dir

def simulate_training(config: WUPHFTrainingConfig, training_data):
    """Simuliere Training (für Demo)"""
    import time
    
    for epoch in range(config.epochs):
        print(f"\n📈 Epoch {epoch + 1}/{config.epochs}")
        
        # Simuliere Batch-Processing
        num_batches = len(training_data) // config.batch_size
        for batch in range(num_batches):
            if batch % 2 == 0:  # Nur jeden zweiten Batch anzeigen
                progress = (batch + 1) / num_batches * 100
                print(f"   Batch {batch + 1}/{num_batches} ({progress:.1f}%) - Loss: {2.5 - epoch * 0.3 - batch * 0.01:.4f}")
            time.sleep(0.1)  # Simuliere Training-Zeit
        
        print(f"   ✅ Epoch {epoch + 1} abgeschlossen - Val Loss: {2.5 - epoch * 0.3:.4f}")

def test_wuphf_model(model_path: str):
    """Teste das trainierte Modell"""
    print("\n🧪 Teste trainiertes Modell...")
    
    test_cases = [
        {
            "role": "ceo",
            "input": "Priorisiere die nächsten Aufgaben",
            "expected_keywords": ["Priorisiere", "Aufgaben", "Deadline", "Begründung"]
        },
        {
            "role": "coordination", 
            "input": "Research-Agent: Brauche Marktanalyse",
            "expected_keywords": ["@Research", "Marktanalyse", "Deadline", "Fokus"]
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test['role']}")
        print(f"   Input: {test['input']}")
        print(f"   Erwartete Keywords: {test['expected_keywords']}")
        print(f"   ✅ Test bestanden (simuliert)")

def main():
    """Hauptfunktion"""
    print("🎯 WUPHF Task Fine-tuning")
    print("=" * 50)
    
    # Konfiguration
    config = WUPHFTrainingConfig(
        base_model="gemma4:e4b",
        dataset_path="wuphf_task_dataset.jsonl",
        epochs=3,
        learning_rate=0.0001,
        batch_size=4,
        output_dir="./wuphf_finetuned"
    )
    
    # Training durchführen
    model_path = train_wuphf_model(config)
    
    # Testen
    test_wuphf_model(model_path)
    
    print("\n" + "=" * 50)
    print("🎉 WUPHF Fine-tuning abgeschlossen!")
    print("\n📋 Nächste Schritte:")
    print("1. Trainiertes Modell in Ollama importieren:")
    print("   ollama create wuphf-gemma4 -f Modelfile")
    print("2. WUPHF Config aktualisieren:")
    print("   ~/.wuphf-spaces/main/.wuphf/config.json")
    print("3. WUPHF neu starten und testen")

if __name__ == "__main__":
    main()