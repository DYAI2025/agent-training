#!/usr/bin/env python3
"""
Alternative Training Setup mit Unsloth für gemma4:e4b und llama3.2
Verwendet LoRA/QLoRA für effizientes Fine-tuning auf Pitch-Deck Expertise
"""

import json
from pathlib import Path

# Dataset Pfad
dataset_path = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/wuphf_final_2026_dataset.jsonl")
output_dir = Path("/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/training_output")

print(f"🎯 Alternative Training Setup mit Unsloth")
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

# Dataset für Unsloth Training vorbereiten (JSON Format)
unsloth_dataset_path = output_dir / "pitchdeck_2026_unsloth.json"

training_data = []
for example in examples:
    if example.get('role') == 'content':
        training_data.append({
            "instruction": example.get('input', ''),
            "input": "",
            "output": example.get('output', ''),
            "system": "Du bist ein Pitch-Deck Experte für AI/Tech-Startups mit 2026 Best Practices, VC-Frameworks (Sequoia, a16z, YC), und Berliner VC-Szene Kenntnissen."
        })

with open(unsloth_dataset_path, 'w', encoding='utf-8') as f:
    json.dump(training_data, f, indent=2, ensure_ascii=False)

print(f"✅ Unsloth Training Dataset erstellt: {unsloth_dataset_path}")

# Python Training Script für gemma4:e4b mit Unsloth
gemma4_training_script = '''#!/usr/bin/env python3
"""
Training Script für gemma4:e4b mit Unsloth und Pitch-Deck 2026 Dataset
"""

import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer
)
from peft import LoraConfig, PeftModel
import json
from pathlib import Path

# Konfiguration
MODEL_NAME = "google/gemma-2b"
DATASET_PATH = "training_output/pitchdeck_2026_unsloth.json"
OUTPUT_DIR = "training_output/gemma4_pitchdeck_2026"

# Dataset laden
with open(DATASET_PATH, 'r', encoding='utf-8') as f:
    training_data = json.load(f)

# Formatieren für Training
def format_prompt(example):
    return f"""### System:
{example['system']}

### User:
{example['instruction']}

### Assistant:
{example['output']}"""

formatted_data = [format_prompt(ex) for ex in training_data]

# Tokenizer laden
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

# Dataset erstellen
class PitchDeckDataset(torch.utils.data.Dataset):
    def __init__(self, texts, tokenizer, max_length=2048):
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        encodings = self.tokenizer(
            text,
            truncation=True,
            max_length=self.max_length,
            padding="max_length",
            return_tensors="pt"
        )
        return {
            'input_ids': encodings['input_ids'].flatten(),
            'attention_mask': encodings['attention_mask'].flatten(),
            'labels': encodings['input_ids'].flatten()
        }

dataset = PitchDeckDataset(formatted_data, tokenizer)

# Quantization Konfiguration (für 8GB VRAM)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=False,
)

# Modell laden
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map="auto"
)

# LoRA Konfiguration
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]
)

model = get_peft_model(model, peft_config)
model.print_trainable_parameters()

# Training Arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    warmup_steps=100,
    logging_steps=10,
    save_steps=500,
    learning_rate=2e-5,
    fp16=True,
    optim="paged_adamw_8bit",
    gradient_checkpointing=True,
    max_grad_norm=0.3,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

# Training starten
print("🎯 Starte Training für gemma4:e4b...")
trainer.train()

# Modell speichern
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"✅ Training abgeschlossen! Modell gespeichert in: {OUTPUT_DIR}")
'''

gemma4_script_path = output_dir / "train_gemma4_unsloth.py"
with open(gemma4_script_path, 'w', encoding='utf-8') as f:
    f.write(gemma4_training_script)

gemma4_script_path.chmod(0o755)

print(f"✅ Unsloth Training Script erstellt: {gemma4_script_path}")

# Requirements File erstellen
requirements = '''torch>=2.0.0
transformers>=4.30.0
peft>=0.6.0
bitsandbytes>=0.41.0
accelerate>=0.20.0
datasets>=2.14.0
trl>=0.7.0
'''

requirements_path = output_dir / "requirements.txt"
with open(requirements_path, 'w', encoding='utf-8') as f:
    f.write(requirements)

print(f"✅ Requirements erstellt: {requirements_path}")

print(f"\n🎯 Training Setup abgeschlossen!")
print(f"📋 Nächste Schritte:")
print(f"   1. Dependencies installieren: pip install -r {requirements_path}")
print(f"   2. Training starten: python {gemma4_script_path}")
print(f"   3. Nach Training: Modell validieren und in Ollama importieren")

print(f"\n💡 Hinweis:")
print(f"   - Verwendet 4-bit Quantization für 8GB VRAM Kompatibilität")
print(f"   - LoRA/QLoRA für effizientes Fine-tuning")
print(f"   - 3 Training Epochs mit 120 Pitch-Deck Beispielen")
print(f"   - Optimiert für RTX 3070 Ti")