
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
