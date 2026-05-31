#!/bin/bash
# Training Script für llama3.2 mit Pitch-Deck 2026 Dataset

echo "🎯 Starte Training für llama3.2..."
echo "📊 Dataset: /home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_final_2026_dataset.jsonl"
echo "📁 Output: /home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/training_output/llama3_pitchdeck_2026"
echo "⏰ Startzeit: $(date)"

# Ollama Fine-tuning
ollama fine-tune llama3.2 \
  --dataset /home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/training_output/pitchdeck_2026_ollama.jsonl \
  --output /home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/training_output/llama3_pitchdeck_2026 \
  --epochs 3 \
  --batch-size 4 \
  --learning-rate 2e-05 \
  --max-seq-length 2048 \
  --fp16

echo "✅ Training abgeschlossen!"
echo "⏰ Endzeit: $(date)"
