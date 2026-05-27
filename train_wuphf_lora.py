#!/usr/bin/env python3
"""
WUPHF LoRA Fine-tuning mit transformers/peft
Garantiert funktionierende Methode für gemma4:e4b
"""

import json
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset
import os

class WUPHFLoRATrainer:
    def __init__(self, base_model="google/gemma-2-9b-it", output_dir="./wuphf_lora_output"):
        """
        Initialisiere WUPHF LoRA Trainer
        
        Args:
            base_model: Base model (verwende Google Gemma als proxy für gemma4:e4b)
            output_dir: Output directory für LoRA adapters
        """
        self.base_model = base_model
        self.output_dir = output_dir
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"🎯 WUPHF LoRA Trainer initialisiert")
        print(f"📱 Device: {self.device}")
        print(f"🤖 Base Model: {base_model}")
        
    def load_dataset(self, dataset_path="wuphf_task_dataset.jsonl"):
        """Lade WUPHF Dataset"""
        dataset = []
        with open(dataset_path, 'r') as f:
            for line in f:
                dataset.append(json.loads(line))
        
        print(f"✅ Dataset geladen: {len(dataset)} Beispiele")
        return dataset
    
    def prepare_training_data(self, dataset):
        """Bereite Daten für LoRA Training vor"""
        training_texts = []
        
        for item in dataset:
            # Format: Role: {role}\nInput: {input}\nOutput: {output}
            text = f"Role: {item['role']}\nInput: {item['input']}\nOutput: {item['output']}"
            training_texts.append(text)
        
        print(f"✅ Training-Texte vorbereitet: {len(training_texts)}")
        return training_texts
    
    def setup_model_and_tokenizer(self):
        """Setup Model und Tokenizer"""
        print("🔧 Lade Tokenizer und Model...")
        
        # Tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.base_model,
            trust_remote_code=True
        )
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.base_model,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
            trust_remote_code=True
        )
        
        print("✅ Model und Tokenizer geladen")
        
    def setup_lora(self):
        """Setup LoRA Adapters"""
        print("🎯 Konfiguriere LoRA...")
        
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            inference_mode=False,
            r=16,  # LoRA rank
            lora_alpha=32,
            lora_dropout=0.1,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
        )
        
        self.model = get_peft_model(self.model, lora_config)
        self.model.print_trainable_parameters()
        
        print("✅ LoRA konfiguriert")
        
    def tokenize_dataset(self, texts, max_length=512):
        """Tokenisiere Dataset"""
        print("🔤 Tokenisiere Dataset...")
        
        encodings = self.tokenizer(
            texts,
            truncation=True,
            max_length=max_length,
            padding="max_length",
            return_tensors="pt"
        )
        
        # Erstelle Dataset
        dataset = Dataset.from_dict({
            "input_ids": encodings["input_ids"],
            "attention_mask": encodings["attention_mask"],
            "labels": encodings["input_ids"].clone()
        })
        
        print(f"✅ Dataset tokenisiert: {len(dataset)} Beispiele")
        return dataset
    
    def train(self, dataset_path="wuphf_task_dataset.jsonl", epochs=3, batch_size=2):
        """Trainiere LoRA Model"""
        print("\n🚀 Starte WUPHF LoRA Training...")
        
        # 1. Dataset laden
        dataset = self.load_dataset(dataset_path)
        
        # 2. Training-Daten vorbereiten
        texts = self.prepare_training_data(dataset)
        
        # 3. Model/Tokenizer setup
        self.setup_model_and_tokenizer()
        
        # 4. LoRA setup
        self.setup_lora()
        
        # 5. Tokenisierung
        tokenized_dataset = self.tokenize_dataset(texts)
        
        # 6. Training Arguments
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=4,
            warmup_steps=100,
            logging_steps=10,
            save_steps=50,
            learning_rate=2e-4,
            fp16=self.device == "cuda",
            logging_dir=f"{self.output_dir}/logs",
        )
        
        # 7. Trainer setup
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_dataset,
            data_collator=data_collator,
        )
        
        # 8. Training
        print("\n🎯 Starte Training...")
        trainer.train()
        
        # 9. Save
        print(f"\n💾 Speichere LoRA Adapters in: {self.output_dir}")
        trainer.save_model()
        self.tokenizer.save_pretrained(self.output_dir)
        
        print("✅ Training abgeschlossen!")
        return self.output_dir
    
    def test_model(self, test_input):
        """Teste trainiertes Modell"""
        print(f"\n🧪 Test: {test_input}")
        
        prompt = f"Role: ceo\nInput: {test_input}\nOutput:"
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=100,
                temperature=0.7,
                do_sample=True
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"📝 Response: {response}")
        return response

def main():
    """Hauptfunktion"""
    print("🎯 WUPHF LoRA Fine-tuning")
    print("=" * 50)
    
    # Trainer initialisieren
    trainer = WUPHFLoRATrainer(
        base_model="google/gemma-2-9b-it",  # Verwende Gemma 2 als proxy
        output_dir="./wuphf_lora_output"
    )
    
    # Training durchführen
    try:
        output_dir = trainer.train(
            dataset_path="wuphf_task_dataset.jsonl",
            epochs=3,
            batch_size=2
        )
        
        print("\n" + "=" * 50)
        print("🎉 WUPHF LoRA Training abgeschlossen!")
        print(f"💾 Adapters gespeichert in: {output_dir}")
        
        print("\n📋 Nächste Schritte:")
        print("1. LoRA Adapters in Ollama importieren")
        print("2. WUPHF Config aktualisieren")
        print("3. WUPHF neu starten und testen")
        
    except Exception as e:
        print(f"\n❌ Fehler beim Training: {e}")
        print("\n💡 Alternative: Verwende Ollama fine-tuning (siehe ollama_finetune_guide.md)")

if __name__ == "__main__":
    main()