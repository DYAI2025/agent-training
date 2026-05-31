#!/usr/bin/env python3
"""
Training von gemma4:e4b und llama3.2 mit Final 2026 Pitch-Deck Dataset
Intensive Fine-tuning auf Pitch-Deck Expertise und Best Practices
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime

# Dataset Pfad
dataset_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_final_2026_dataset.jsonl")
output_dir = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/training_output")

# Output Directory erstellen
output_dir.mkdir(exist_ok=True)

print(f"🎯 Training Setup für Pitch-Deck Expertise")
print(f"📊 Dataset: {dataset_path}")
print(f"📁 Output Directory: {output_dir}")

# Dataset Analyse
examples = []
with open(dataset_path, 'r', encoding='utf-8') as f:
    for line in f:
        examples.append(json.loads(line))

print(f"📊 Dataset Statistiken:")
print(f"   - Gesamt Beispiele: {len(examples)}")
print(f"   - Content Beispiele: {sum(1 for ex in examples if ex.get('role') == 'content')}")
print(f"   - Task Understanding: {sum(1 for ex in examples if ex.get('role') != 'content')}")

# Training Konfiguration für gemma4:e4b
gemma4_config = {
    "model": "gemma4:e4b",
    "dataset": str(dataset_path),
    "output_dir": str(output_dir / "gemma4_pitchdeck_2026"),
    "epochs": 3,
    "batch_size": 4,
    "learning_rate": 2e-5,
    "warmup_steps": 100,
    "logging_steps": 10,
    "save_steps": 500,
    "max_seq_length": 2048,
    "gradient_accumulation_steps": 4,
    "fp16": True,
    "description": "gemma4:e4b fine-tuned on 2026 Pitch-Deck Best Practices with 120 examples including real structures, Berlin VC scene, and 2026 benchmarks"
}

# Training Konfiguration für llama3.2
llama3_config = {
    "model": "llama3.2:latest",
    "dataset": str(dataset_path),
    "output_dir": str(output_dir / "llama3_pitchdeck_2026"),
    "epochs": 3,
    "batch_size": 4,
    "learning_rate": 2e-5,
    "warmup_steps": 100,
    "logging_steps": 10,
    "save_steps": 500,
    "max_seq_length": 2048,
    "gradient_accumulation_steps": 4,
    "fp16": True,
    "description": "llama3.2 fine-tuned on 2026 Pitch-Deck Best Practices with 120 examples including real structures, Berlin VC scene, and 2026 benchmarks"
}

print(f"\n🎯 Training Konfigurationen:")
print(f"   - gemma4:e4b: {gemma4_config['epochs']} epochs, batch_size {gemma4_config['batch_size']}")
print(f"   - llama3.2: {llama3_config['epochs']} epochs, batch_size {llama3_config['batch_size']}")

print(f"\n📋 Nächste Schritte:")
print(f"   1. Dataset in JSONL-Format für Ollama Fine-tuning konvertieren")
print(f"   2. Training für gemma4:e4b starten")
print(f"   3. Training für llama3.2 starten (optional)")
print(f"   4. Modelle validieren und testen")

# Dataset für Ollama Fine-tuning vorbereiten
ollama_dataset_path = output_dir / "pitchdeck_2026_ollama.jsonl"

with open(ollama_dataset_path, 'w', encoding='utf-8') as f:
    for example in examples:
        # Format für Ollama Fine-tuning
        if example.get('role') == 'content':
            training_example = {
                "system": "Du bist ein Pitch-Deck Experte für AI/Tech-Startups mit 2026 Best Practices, VC-Frameworks (Sequoia, a16z, YC), und Berliner VC-Szene Kenntnissen.",
                "user": example.get('input', ''),
                "assistant": example.get('output', '')
            }
            f.write(json.dumps(training_example, ensure_ascii=False) + '\n')

print(f"✅ Ollama Training Dataset erstellt: {ollama_dataset_path}")

# Trainingsskript für gemma4:e4b erstellen
gemma4_training_script = f"""#!/bin/bash
# Training Script für gemma4:e4b mit Pitch-Deck 2026 Dataset

echo "🎯 Starte Training für gemma4:e4b..."
echo "📊 Dataset: {dataset_path}"
echo "📁 Output: {gemma4_config['output_dir']}"
echo "⏰ Startzeit: $(date)"

# Ollama Fine-tuning
ollama fine-tune gemma4:e4b \\
  --dataset {ollama_dataset_path} \\
  --output {gemma4_config['output_dir']} \\
  --epochs {gemma4_config['epochs']} \\
  --batch-size {gemma4_config['batch_size']} \\
  --learning-rate {gemma4_config['learning_rate']} \\
  --max-seq-length {gemma4_config['max_seq_length']} \\
  --fp16

echo "✅ Training abgeschlossen!"
echo "⏰ Endzeit: $(date)"
"""

gemma4_script_path = output_dir / "train_gemma4_pitchdeck.sh"
with open(gemma4_script_path, 'w', encoding='utf-8') as f:
    f.write(gemma4_training_script)

# Trainingsskript ausführbar machen
gemma4_script_path.chmod(0o755)

print(f"✅ Training Script erstellt: {gemma4_script_path}")

# Trainingsskript für llama3.2 erstellen
llama3_training_script = f"""#!/bin/bash
# Training Script für llama3.2 mit Pitch-Deck 2026 Dataset

echo "🎯 Starte Training für llama3.2..."
echo "📊 Dataset: {dataset_path}"
echo "📁 Output: {llama3_config['output_dir']}"
echo "⏰ Startzeit: $(date)"

# Ollama Fine-tuning
ollama fine-tune llama3.2 \\
  --dataset {ollama_dataset_path} \\
  --output {llama3_config['output_dir']} \\
  --epochs {llama3_config['epochs']} \\
  --batch-size {llama3_config['batch_size']} \\
  --learning-rate {llama3_config['learning_rate']} \\
  --max-seq-length {llama3_config['max_seq_length']} \\
  --fp16

echo "✅ Training abgeschlossen!"
echo "⏰ Endzeit: $(date)"
"""

llama3_script_path = output_dir / "train_llama3_pitchdeck.sh"
with open(llama3_script_path, 'w', encoding='utf-8') as f:
    f.write(llama3_training_script)

# Trainingsskript ausführbar machen
llama3_script_path.chmod(0o755)

print(f"✅ Training Script erstellt: {llama3_script_path}")

print(f"\n🎯 Training bereit!")
print(f"📋 Verfügbare Training Scripts:")
print(f"   1. {gemma4_script_path} (gemma4:e4b)")
print(f"   2. {llama3_script_path} (llama3.2)")
print(f"\n🚀 Starte Training mit:")
print(f"   bash {gemma4_script_path}")
print(f"   # oder")
print(f"   bash {llama3_script_path}")