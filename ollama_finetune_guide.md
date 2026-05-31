# WUPHF Fine-tuning mit Ollama

## Voraussetzungen
- Ollama installiert
- gemma4:e4b Modell bereits geladen

## Schritt 1: Dataset vorbereiten
```bash
# Dataset ist bereits erstellt: wuphf_task_dataset.jsonl
# Überprüfe den Inhalt:
cat wuphf_task_dataset.jsonl
```

## Schritt 2: Ollama Fine-tuning durchführen
```bash
# Methode A: Mit Ollama CLI (einfach)
ollama fine-tune gemma4:e4b \
  --dataset wuphf_task_dataset.jsonl \
  --output wuphf-gemma4 \
  --epochs 3 \
  --learning-rate 0.0001

# Methode B: Mit Modelfile (mehr Kontrolle)
# Erstelle Modelfile:
cat > Modelfile <<EOF
FROM gemma4:e4b

# WUPHF-spezifische Parameter
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 4096

# System-Prompt für WUPHF Rollen
SYSTEM """
Du bist ein spezialisiertes AI-Agent für WUPHF (Multi-Agent-System).
Deine Rolle ist: {role}
Antworte präzise, professionell und koordiniert.
Verwende @Mentions für Agent-Kommunikation.
Sei spezifisch bei Deadlines und Verantwortlichkeiten.
"""
EOF

# Fine-tuning mit Modelfile
ollama create wuphf-gemma4 -f Modelfile
```

## Schritt 3: Trainiertes Modell testen
```bash
# Teste das neue Modell
ollama run wuphf-gemma4 "Role: ceo\nInput: Priorisiere die nächsten Aufgaben"

# Teste Koordination
ollama run wuphf-gemma4 "Role: coordination\nInput: @Research: Brauche Marktanalyse bis morgen"
```

## Schritt 4: WUPHF Config aktualisieren
```bash
# Config öffnen
nano ~/.wuphf-spaces/main/.wuphf/config.json

# Ändere die Model-Namen:
{
  "provider_endpoints": {
    "ollama": {
      "models_by_agent": {
        "ceo": "wuphf-gemma4",        # Geändert von gemma4:e4b
        "research": "wuphf-gemma4",   # Geändert von gemma4:e4b
        "analyst": "wuphf-gemma4"     # Geändert von gemma4:e4b
      }
    }
  }
}
```

## Schritt 5: WUPHF neu starten
```bash
# WUPHF stoppen
cd ~/.wuphf-spaces/main/.wuphf/wuphf
# Stoppe den Prozess

# WUPHF neu starten
./wuphf
```

## Alternative: Dataset erweitern
```bash
# Mehr Beispiele hinzufügen für besseres Training
# Editiere wuphf_task_training.py und füge mehr Beispiele hinzu
python wuphf_task_training.py

# Erneutes Fine-tuning mit erweitertem Dataset
ollama fine-tune wuphf-gemma4 \
  --dataset wuphf_task_dataset.jsonl \
  --output wuphf-gemma4-v2 \
  --epochs 5
```

## Erwartete Ergebnisse
- **Sofort**: Präzisere Aufgabenübernahme
- **Nach 1 Stunde**: Bessere Agent-Kommunikation
- **Nach 1 Tag**: Konsistentes Rollen-Verhalten

## Fehlersuche
```bash
# Wenn Ollama fine-tune nicht verfügbar ist:
# Verwende transformers + peft (LoRA)

pip install transformers peft accelerate

# Siehe train_wuphf_lora.py für LoRA Fine-tuning
```