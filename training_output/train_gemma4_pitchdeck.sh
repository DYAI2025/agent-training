#!/bin/bash
# Training Script für gemma4:e4b mit Pitch-Deck 2026 Dataset

echo "🎯 Starte Training für gemma4:e4b..."
echo "📊 Dataset: /home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_final_2026_dataset.jsonl"
echo "📁 Output: /home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/training_output/gemma4_pitchdeck_2026"
echo "⏰ Startzeit: $(date)"

# Ollama Fine-tuning
ollama fine-tune gemma4:e4b \
  --dataset /home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/training_output/pitchdeck_2026_ollama.jsonl \
  --output /home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/training_output/gemma4_pitchdeck_2026 \
  --epochs 3 \
  --batch-size 4 \
  --learning-rate 2e-05 \
  --max-seq-length 2048 \
  --fp16

echo "✅ Training abgeschlossen!"
echo "⏰ Endzeit: $(date)"
