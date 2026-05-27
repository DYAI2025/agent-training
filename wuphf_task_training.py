#!/usr/bin/env python3
"""
WUPHF-spezifisches Task-Understanding Training
Fokus: Bessere Aufgabenverständnis und Agent-Koordination
"""

# WUPHF-spezifisches Training-Dataset
WUPHF_TASK_DATASET = [
    # CEO Aufgaben - Strategische Entscheidungen
    {
        "role": "ceo",
        "input": "Analyse die aktuelle Agent-Performance und entscheide über Ressourcen-Reallocation",
        "output": "Ich analysiere die Performance-Metriken aller Agenten: CEO (Strategie), Research (Daten), Analyst (Berichte). Basierend auf der aktuellen Auslastung empfehle ich: 1) Research-Agent bekommt 20% mehr Rechenzeit für Marktforschung, 2) Analyst-Agent fokussiert auf KPI-Tracking, 3) CEO behält aktuelle Ressourcen für strategische Planung."
    },
    {
        "role": "ceo", 
        "input": "Priorisiere die nächsten 3 Aufgaben für das Team",
        "output": "Priorisierte Aufgaben: 1) Finalisiere Pitch Deck für Kunden X (Frist: morgen), 2) Research-Agent: Marktanalyse für DACH-Region, 3) Analyst: Performance-Report Q2. Begründung: Kunden-X hat direkten Umsatzimpact, DACH-Analysis ist strategisch wichtig für Wachstum, Q2-Report für Investor-Updates."
    },
    
    # Research Aufgaben - Informationsverarbeitung
    {
        "role": "research",
        "input": "Researche die neuesten Trends im AI-Agent-Markt für Pitch Decks",
        "output": "Ich recherchiere AI-Agent-Markttrends: 1) Multi-Agent-Systeme gewinnen an Popularität (+40% YoY), 2) Lokale Modelle (Ollama, LM Studio) für Datenschutz, 3) Integration mit bestehenden Workflows (Slack, Notion), 4) Spezialisierte Agenten für Sales, Marketing, Operations. Relevanz für unser Pitch Deck: Wir positionieren uns als Hybrid Cloud-Orchestrator mit lokalen Executors."
    },
    {
        "role": "research",
        "input": "Analysiere die Wettbewerber im DACH-Bereich für Pitch Deck Services",
        "output": "Wettbewerbsanalyse DACH: 1) DeckRobot (automatisiert, aber limitierte Customization), 2) SlideGenAI (gute Templates, aber keine Branchenexpertise), 3) Lokale Design-Agenturen (hochpreisig, langsam). Unser USP: Hybrid-System mit menschlicher Qualität + AI-Geschwindigkeit + Branchenexpertise für Investoren-Pitch Decks."
    },
    
    # Analyst Aufgaben - Dateninterpretation
    {
        "role": "analyst",
        "input": "Interpretiere die aktuellen Sales-Zahlen und erstelle Handlungsempfehlungen",
        "output": "Sales-Analyse: Aktuell 3 Kunden, MRR €7.5K, Ziel: 10 Kunden, €25K MRR. Gap: 7 Kunden, €17.5K MRR. Handlungsempfehlungen: 1) Fokus auf High-Ticket-Kunden (€5K+ MRR), 2) Outreach an VCs und Startups (höhere Conversion), 3) Case-Studies von aktuellen Kunden erstellen, 4) DACH-Region priorisieren (weniger Wettbewerb). Zeithorizont: 90 Tage."
    },
    {
        "role": "analyst",
        "input": "Erstelle einen Performance-Report für alle Agenten",
        "output": "Agent-Performance Report: CEO: 95% Aufgaben-Completion, 2.3s avg response, Strategie-Qualität: hoch. Research: 88% Completion, 4.1s avg response, Datenqualität: sehr gut. Analyst: 92% Completion, 3.7s avg response, Analyse-Tiefe: gut. Content: 85% Completion, 5.2s avg response, Kreativität: variabel. Empfehlung: Content-Agent Training für konsistentere Qualität."
    },
    
    # Kanal-Kommunikation - Agent-zu-Agent
    {
        "role": "coordination",
        "input": "CEO an Research: Brauche Marktanalyse für Tech-Startups bis morgen",
        "output": "@Research: Ich benötige eine umfassende Marktanalyse für Tech-Startups im DACH-Bereich bis morgen 10:00 Uhr. Fokus: Funding-Trends 2024, Key-Player, Typical Valuation. Dies ist für das Pitch Deck unseres neuen Kunden. Bitte bestätige Erhalt und geschätzte Fertigstellung."
    },
    {
        "role": "coordination",
        "input": "Research an Analyst: Hier sind die Marktdaten, bitte analysiere",
        "output": "@Analyst: Marktanalyse komplett! Daten: 150+ Tech-Startups analysiert, durchschnittliches Funding: €2.8M, Top-Sektoren: Fintech, HealthTech, GreenTech. Bitte analysiere diese Daten für KPIs und Trends. Fokus auf: Wachstumsraten, Success-Faktoren, Common Pitfalls. Brauchst du zusätzliche Datenpunkte?"
    },
    
    # Task-Claiming und Koordination
    {
        "role": "task_claiming",
        "input": "Neue Aufgabe: Pitch Deck für FinTech-Startup erstellen",
        "output": "Ich claim diese Aufgabe als CEO-Agent. Verantwortlichkeiten: 1) Strategische Ausrichtung definieren, 2) Research-Agent für Marktanalyse beauftragen, 3) Content-Agent für Slide-Erstellung koordinieren, 4) Analyst für KPI-Integration. Geschätzte Dauer: 4 Stunden. Deadline: Freitag 17:00 Uhr. @Research @Content @Analyst: Bitte steht für Koordination bereit."
    },
    {
        "role": "task_claiming",
        "input": "Aufgabe: Q2 Performance Report erstellen",
        "output": "Ich claim diese Aufgabe als Analyst-Agent. Benötigte Daten: Sales-Zahlen von CEO, Markt-Research von Research-Agent, Content-Metriken von Content-Agent. Zeitplan: Datensammlung (1h), Analyse (2h), Report-Erstellung (1h). Deadline: Mittwoch 12:00 Uhr. @CEO @Research @Content: Bitte stellt Daten bis morgen 10:00 Uhr bereit."
    },
    
    # Fehlerbehandlung und Eskalation
    {
        "role": "error_handling",
        "input": "Research-Agent meldet: Datenquelle nicht verfügbar",
        "output": "@Research: Verstanden. Alternative Vorgehensweise: 1) Nutze sekundäre Quellen (Industry Reports, News), 2) Konsultiere Analyst für historische Daten, 3) Falls kritisch: Eskalation an CEO für manuelle Datenbeschaffung. Bitte melde zurück, welche Option du wählst und geschätzte Verzögerung."
    },
    {
        "role": "error_handling",
        "input": "Content-Agent: Deadline nicht erreichbar, brauche 2 Stunden mehr",
        "output": "@Content: Deadline-Verlängerung genehmigt (+2 Stunden). Neue Deadline: Freitag 19:00 Uhr. @CEO: Bitte informiere Kunden über Verspätung. @Analyst: Passe Timeline im Projektplan an. Grund: Komplexität der Slide-Animationen unterschätzt. Für Zukunft: Bessere Zeitplanung bei komplexen Aufgaben."
    }
]

def create_wuphf_training_file(output_path="wuphf_task_dataset.jsonl"):
    """Erstelle Training-Datei im JSONL-Format"""
    import json
    
    with open(output_path, 'w') as f:
        for item in WUPHF_TASK_DATASET:
            f.write(json.dumps(item) + '\n')
    
    print(f"WUPHF Training-Dataset erstellt: {output_path}")
    print(f"Anzahl Beispiele: {len(WUPHF_TASK_DATASET)}")
    print(f"Rollen: {set(item['role'] for item in WUPHF_TASK_DATASET)}")

if __name__ == "__main__":
    create_wuphf_training_file()