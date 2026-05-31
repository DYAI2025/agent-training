#!/usr/bin/env python3
"""
WUPHF Training mit Ollama API
Einfache Methode für direktes Training auf gemma4:e4b
"""

import json
import requests
import time
from typing import List, Dict

class WUPHFOllamaTrainer:
    def __init__(self, model="gemma4:e4b", base_url="http://localhost:11434"):
        """
        Initialisiere WUPHF Ollama Trainer
        
        Args:
            model: Ollama model name
            base_url: Ollama API base URL
        """
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        
        print(f"🎯 WUPHF Ollama Trainer")
        print(f"🤖 Model: {model}")
        print(f"🌐 API: {base_url}")
        
    def check_ollama_connection(self):
        """Prüfe Ollama Verbindung"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                print(f"✅ Ollama verbunden")
                print(f"📦 Verfügbare Modelle: {model_names}")
                
                if self.model in model_names:
                    print(f"✅ Model {self.model} verfügbar")
                    return True
                else:
                    print(f"❌ Model {self.model} nicht gefunden")
                    return False
        except Exception as e:
            print(f"❌ Ollama Verbindung fehlgeschlagen: {e}")
            return False
    
    def load_dataset(self, dataset_path="wuphf_task_dataset.jsonl"):
        """Lade WUPHF Dataset"""
        dataset = []
        with open(dataset_path, 'r') as f:
            for line in f:
                dataset.append(json.loads(line))
        
        print(f"✅ Dataset geladen: {len(dataset)} Beispiele")
        return dataset
    
    def create_fewshot_examples(self, dataset):
        """Erstelle Few-Shot Beispiele für In-Context Learning"""
        examples = []
        
        for item in dataset:
            example = {
                "role": item['role'],
                "input": item['input'], 
                "output": item['output']
            }
            examples.append(example)
        
        print(f"✅ Few-Shot Beispiele erstellt: {len(examples)}")
        return examples
    
    def generate_with_context(self, prompt: str, examples: List[Dict], role: str = "ceo"):
        """Generiere Antwort mit Few-Shot Context"""
        
        # Erstelle Few-Shot Prompt
        fewshot_prompt = f"Du bist ein {role} Agent im WUPHF Multi-Agent-System.\n\n"
        
        # Füge Beispiele hinzu (max 3 für Context)
        for i, example in enumerate(examples[:3]):
            if example['role'] == role:
                fewshot_prompt += f"Beispiel {i+1}:\n"
                fewshot_prompt += f"Role: {example['role']}\n"
                fewshot_prompt += f"Input: {example['input']}\n"
                fewshot_prompt += f"Output: {example['output']}\n\n"
        
        # Füge aktuelle Anfrage hinzu
        fewshot_prompt += f"Aktuelle Anfrage:\n"
        fewshot_prompt += f"Role: {role}\n"
        fewshot_prompt += f"Input: {prompt}\n"
        fewshot_prompt += f"Output:"
        
        # API Call
        try:
            response = requests.post(
                f"{self.api_url}/generate",
                json={
                    "model": self.model,
                    "prompt": fewshot_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "num_predict": 256
                    }
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                print(f"❌ API Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Generation Error: {e}")
            return None
    
    def test_wuphf_behavior(self, dataset):
        """Teste WUPHF-spezifisches Verhalten"""
        print("\n🧪 Teste WUPHF Verhalten mit Few-Shot Learning...")
        
        examples = self.create_fewshot_examples(dataset)
        
        test_cases = [
            {
                "role": "ceo",
                "input": "Priorisiere die nächsten 3 Aufgaben für das Team",
                "expected_keywords": ["Priorisiere", "Aufgaben", "Deadline", "Begründung"]
            },
            {
                "role": "coordination",
                "input": "@Research: Brauche Marktanalyse für Tech-Startups bis morgen",
                "expected_keywords": ["@Research", "Marktanalyse", "Deadline", "Fokus"]
            },
            {
                "role": "analyst", 
                "input": "Analysiere die aktuellen Sales-Zahlen",
                "expected_keywords": ["Sales", "Analyse", "Empfehlung", "Zahlen"]
            }
        ]
        
        results = []
        for i, test in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}: {test['role']}")
            print(f"   Input: {test['input']}")
            
            response = self.generate_with_context(test['input'], examples, test['role'])
            
            if response:
                print(f"   Response: {response[:200]}...")
                
                # Prüfe Keywords
                keywords_found = [kw for kw in test['expected_keywords'] if kw.lower() in response.lower()]
                print(f"   Keywords gefunden: {keywords_found}/{len(test['expected_keywords'])}")
                
                results.append({
                    "test": i,
                    "role": test['role'],
                    "success": len(keywords_found) >= len(test['expected_keywords']) // 2,
                    "response": response
                })
            else:
                print("   ❌ Keine Response")
                results.append({"test": i, "role": test['role'], "success": False})
        
        return results
    
    def create_wuphf_system_prompt(self):
        """Erstelle WUPHF-spezifischen System Prompt"""
        system_prompt = """
Du bist ein spezialisiertes AI-Agent für WUPHF (Multi-Agent-Orchestrierungssystem).

DEINE ROLLE:
- CEO: Strategische Entscheidungen, Priorisierung, Ressourcen-Allokation
- Research: Informationsbeschaffung, Marktanalyse, Daten-Research  
- Analyst: Dateninterpretation, Performance-Analyse, Berichterstattung
- Coordination: Agent-zu-Agent Kommunikation, Task-Koordination

DEIN VERHALTEN:
1. Sei präzise und spezifisch bei Aufgabenbeschreibungen
2. Verwende @Mentions für direkte Agent-Kommunikation
3. Nenne immer Deadlines und Verantwortlichkeiten
4. Bei Fehlern: Biete Alternativen und eskaliere wenn nötig
5. Sei kooperativ und lösungsorientiert

KOMMUNIKATIONSSTIL:
- Professionell und direkt
- Klare Handlungsaufforderungen
- Strukturierte Antworten mit Punkten
- Konstruktives Feedback
"""
        return system_prompt
    
    def save_wuphf_config(self, output_path="wuphf_model_config.json"):
        """Speichere WUPHF Model Konfiguration"""
        config = {
            "model": self.model,
            "system_prompt": self.create_wuphf_system_prompt(),
            "training_method": "few_shot_in_context",
            "dataset_size": len(self.load_dataset()),
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open(output_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Konfiguration gespeichert: {output_path}")
        return config

def main():
    """Hauptfunktion"""
    print("🎯 WUPHF Training mit Ollama API")
    print("=" * 50)
    
    # Trainer initialisieren
    trainer = WUPHFOllamaTrainer(model="gemma4:e4b")
    
    # Verbindung prüfen
    if not trainer.check_ollama_connection():
        print("\n❌ Ollama nicht verfügbar. Starte Ollama zuerst:")
        print("   ollama serve")
        return
    
    # Dataset laden
    dataset = trainer.load_dataset()
    
    # WUPHF Verhalten testen
    results = trainer.test_wuphf_behavior(dataset)
    
    # Ergebnisse zusammenfassen
    print("\n" + "=" * 50)
    print("📊 Test-Ergebnisse:")
    successful = sum(1 for r in results if r['success'])
    print(f"✅ Erfolgreich: {successful}/{len(results)}")
    
    # Konfiguration speichern
    trainer.save_wuphf_config()
    
    print("\n🎉 WUPHF Training Setup abgeschlossen!")
    print("\n📋 Nächste Schritte:")
    print("1. WUPHF Config mit System Prompt aktualisieren")
    print("2. WUPHF neu starten mit Few-Shot Context")
    print("3. Agent-Verhalten im Echtbetrieb beobachten")
    
    print("\n💡 Alternative: Für echtes Fine-tuning, siehe train_wuphf_lora.py")

if __name__ == "__main__":
    main()