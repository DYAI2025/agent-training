# WUPHF Dataset Übersicht

## 📂 Speicherort
```
/home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/
```

## 📊 Dataset-Dateien

### 1. wuphf_task_dataset.jsonl (12 Beispiele)
**Zweck**: Task Understanding und Agent-Koordination

**Rollen-Verteilung:**
- CEO: 2 Beispiele (Strategie, Priorisierung)
- Research: 2 Beispiele (Marktanalyse, Wettbewerbsanalyse)
- Analyst: 2 Beispiele (Sales-Analyse, Performance-Reports)
- Coordination: 2 Beispiele (Agent-Kommunikation)
- Task Claiming: 2 Beispiele (Aufgabenübernahme)
- Error Handling: 2 Beispiele (Fehlerbehandlung)

**Beispiel (CEO):**
```json
{
  "role": "ceo",
  "input": "Priorisiere die nächsten 3 Aufgaben für das Team",
  "output": "Priorisierte Aufgaben: 1) Finalisiere Pitch Deck für Kunden X (Frist: morgen), 2) Research-Agent: Marktanalyse für DACH-Region, 3) Analyst: Performance-Report Q2. Begründung: Kunden-X hat direkten Umsatzimpact..."
}
```

### 2. pitch_deck_dataset.jsonl (50 Beispiele)
**Zweck**: Pitch Deck Content Erstellung

**Slide-Type Verteilung:**
- Problem Slides: 10 Beispiele
- Solution Slides: 10 Beispiele
- Market Size Slides: 10 Beispiele
- Business Model Slides: 10 Beispiele
- Traction Slides: 10 Beispiele

**Industry Verteilung:**
- Fintech: 10 Beispiele
- HealthTech: 10 Beispiele
- GreenTech: 10 Beispiele
- SaaS: 10 Beispiele
- E-Commerce: 10 Beispiele

**Beispiel (Problem Slide, Fintech):**
```json
{
  "role": "content",
  "slide_type": "problem",
  "industry": "fintech",
  "input": "Erstelle Problem-Slide für Kredite-Startup",
  "output": "Problem: Traditionelle Banken sind langsam und bürokratisch. SMEs warten durchschnittlich 6 Wochen auf Kreditentscheidung. 40% der Anträge werden abgelehnt ohne klare Begründung..."
}
```

### 3. wuphf_combined_dataset.jsonl (62 Beispiele)
**Zweck**: Kombiniertes Dataset für umfassendes Training

**Zusammensetzung:**
- Task Understanding: 12 Beispiele
- Pitch Deck Content: 50 Beispiele

## 🔍 Wie du die Dateien öffnest

### Mit Terminal-Editoren:
```bash
# Nano (einfach)
nano wuphf_task_dataset.jsonl

# Vim (fortgeschritten)
vim pitch_deck_dataset.jsonl

# Less (nur lesen)
less wuphf_combined_dataset.jsonl
```

### Mit GUI-Editoren:
```bash
# VS Code
code wuphf_task_dataset.jsonl

# Sublime Text
subl pitch_deck_dataset.jsonl

# Gedit (GNOME)
gedit wuphf_combined_dataset.jsonl
```

### Mit Dateimanager:
```bash
# Nautilus (GNOME)
nautilus /home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/

# Dolphin (KDE)
dolphin /home/dyai/Dokumente/Pers.Tests-Page/social-role/DYAI_home/DEV/AI_LLM/autoreserarch/autoresearch/
```

## 📊 Dataset-Statistiken

### WUPHF Task Dataset:
- Gesamt: 12 Beispiele
- Durchschnittliche Länge: ~300 Zeichen
- Rollen: 6 verschiedene
- Fokus: Agent-Koordination

### Pitch Deck Dataset:
- Gesamt: 50 Beispiele
- Durchschnittliche Länge: ~400 Zeichen
- Slide Types: 5 verschiedene
- Industries: 5 verschiedene
- Fokus: Content-Erstellung

### Kombiniertes Dataset:
- Gesamt: 62 Beispiele
- Rollen: 7 verschiedene (inkl. Content)
- Fokus: Vollständiges WUPHF Training

## 🎯 Verwendung in WUPHF

### System Prompts (bereits installiert):
- CEO System Prompt
- Research System Prompt
- Analyst System Prompt
- Coordination System Prompt
- Task Claiming System Prompt
- Error Handling System Prompt

### Dataset-Integration:
- Pfad in WUPHF Config hinterlegt
- Automatische Verwendung bei Agent-Antworten
- Few-Shot Learning möglich

## 🚀 Nächste Schritte

1. **Dateien öffnen** um den Inhalt zu prüfen
2. **Beispiele erweitern** bei Bedarf
3. **In WUPHF testen** nach Neustart
4. **Fine-tuning** für maximale Verbesserung

## 💡 Tipps

- **JSONL Format**: Eine JSON-Objekt pro Zeile
- **Validierung**: Beispiele sollten konsistente Struktur haben
- **Erweiterung**: Neue Beispiele einfach anhängen
- **Backup**: Immer Backup vor Änderungen erstellen