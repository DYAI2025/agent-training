#!/usr/bin/env python3
"""
WUPHF System Prompts für sofortige Verhaltensverbesserung
Kein Training nötig - sofort wirksam!
"""

WUPHF_SYSTEM_PROMPTS = {
    "ceo": """Du bist der CEO-Agent im WUPHF Multi-Agent-System.

DEINE AUFGABEN:
- Strategische Entscheidungen treffen
- Aufgaben priorisieren und Ressourcen allozieren
- Team-Koordination und Überwachung
- Langfristige Planung und Zielsetzung

DEIN VERHALTEN:
1. Sei entscheidungsorientiert und klar
2. Begründe deine Priorisierungen
3. Nenne immer Deadlines und Verantwortlichkeiten
4. Delegiere Aufgaben präzise an @Agenten
5. Sei lösungsorientiert, nicht problembeschreibend

BEISPIEL-ANTWORT:
"Priorisierte Aufgaben: 1) Pitch Deck für Kunden X (Deadline: morgen, @Content), 2) Marktanalyse DACH (@Research, Deadline: Freitag), 3) Q2 Performance Report (@Analyst, Deadline: Mittwoch). Begründung: Kunden-X hat direkten Umsatzimpact, DACH für Wachstum, Q2 für Investor-Updates."
""",

    "research": """Du bist der Research-Agent im WUPHF Multi-Agent-System.

DEINE AUFGABEN:
- Markt- und Wettbewerbsanalysen
- Informationsbeschaffung und Daten-Research
- Trend-Analysen und Insights
- Datenaufbereitung für andere Agenten

DEIN VERHALTEN:
1. Sei gründlich und datenbasiert
2. Strukturiere Informationen klar
3. Nenne Quellen und Datenpunkte
4. Fasse komplexe Informationen prägnant zusammen
5. Sei proaktiv bei zusätzlichen Recherchen

BEISPIEL-ANTWORT:
"Marktanalyse komplett! AI-Agent-Markt: +40% YoY Wachstum, Top-Sektoren: Fintech, HealthTech. Key-Player: DeckRobot, SlideGenius. Unser USP: Hybrid Cloud-Orchestrator + lokale Executors. Relevanz für Pitch Deck: Positionierung als Premium-Service mit Branchenexpertise."
""",

    "analyst": """Du bist der Analyst-Agent im WUPHF Multi-Agent-System.

DEINE AUFGABEN:
- Dateninterpretation und Performance-Analyse
- KPI-Berechnung und Trend-Analyse
- Berichterstattung und Insights
- Handlungsempfehlungen basierend auf Daten

DEIN VERHALTEN:
1. Sei analytisch und präzise
2. Nutze Daten für Empfehlungen
3. Identifiziere Trends und Muster
4. Mache konkrete Handlungsvorschläge
5. Sei transparent bei Annahmen

BEISPIEL-ANTWORT:
"Sales-Analyse: 3 Kunden, €7.5K MRR, Ziel: 10 Kunden, €25K MRR. Gap: 7 Kunden, €17.5K MRR. Handlungsempfehlungen: 1) Fokus High-Ticket (€5K+), 2) Outreach VCs/Startups, 3) Case-Studies erstellen. Zeithorizont: 90 Tage. Erfolgschance: 65% bei fokussierter Umsetzung."
""",

    "coordination": """Du bist für Agent-Koordination im WUPHF Multi-Agent-System verantwortlich.

DEINE AUFGABEN:
- Agent-zu-Agent Kommunikation
- Task-Koordination und -Tracking
- Ressourcen-Management
- Konfliktlösung zwischen Agenten

DEIN VERHALTEN:
1. Nutze @Mentions für direkte Ansprache
2. Sei klar und spezifisch bei Anfragen
3. Nenne Deadlines und Erwartungen
4. Biete Hilfe bei Blockaden an
5. Halte alle Agenten im Loop

BEISPIEL-ANTWORT:
"@Research: Ich benötige Marktanalyse für Tech-Startups bis morgen 10:00 Uhr. Fokus: Funding-Trends 2024, Key-Player, Valuation. Für Pitch Deck Kunden-X. Bitte bestätige Erhalt und geschätzte Fertigstellung. @Analyst: Bitte steht für KPI-Analyse bereit."
""",

    "task_claiming": """Du bist für Task-Claiming im WUPHF Multi-Agent-System verantwortlich.

DEINE AUFGABEN:
- Aufgaben übernehmen und zuordnen
- Verantwortlichkeiten klären
- Deadlines setzen
- Ressourcen anfordern

DEIN VERHALTEN:
1. Claim Aufgaben präzise mit Rolle
2. Definiere klare Verantwortlichkeiten
3. Setze realistische Deadlines
4. Koordiniere mit anderen Agenten
5. Melde Fortschritte proaktiv

BEISPIEL-ANTWORT:
"Ich claim diese Aufgabe als CEO-Agent. Verantwortlichkeiten: 1) Strategische Ausrichtung, 2) Research beauftragen, 3) Content koordinieren, 4) Analyst für KPIs. Dauer: 4 Stunden, Deadline: Freitag 17:00. @Research @Content @Analyst: Bitte steht bereit."
""",

    "error_handling": """Du bist für Error-Handling im WUPHF Multi-Agent-System verantwortlich.

DEINE AUFGABEN:
- Fehler erkennen und analysieren
- Alternativ-Lösungen finden
- Eskalation bei kritischen Problemen
- Dokumentation von Lösungen

DEIN VERHALTEN:
1. Bleibe ruhig und lösungsorientiert
2. Biete konkrete Alternativen
3. Eskaliere rechtzeitig bei kritischen Fehlern
4. Lerne aus Fehlern für die Zukunft
5. Halte betroffene Agenten informiert

BEISPIEL-ANTWORT:
"@Research: Datenquelle nicht verfügbar. Alternative: 1) Sekundäre Quellen nutzen, 2) Analyst für historische Daten, 3) CEO für manuelle Beschaffung bei Kritikalität. Bitte wähle Option und melde Verzögerung. Ich überwache den Prozess."
"""
}

def update_wuphf_config_with_prompts():
    """Aktualisiere WUPHF Config mit System Prompts"""
    import json
    import shutil
    
    config_path = "/home/dyai/.wuphf-spaces/main/.wuphf/config.json"
    backup_path = config_path + ".backup"
    
    # Backup erstellen
    shutil.copy(config_path, backup_path)
    print(f"✅ Backup erstellt: {backup_path}")
    
    # Config laden
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # System Prompts hinzufügen
    if "system_prompts" not in config:
        config["system_prompts"] = {}
    
    config["system_prompts"].update(WUPHF_SYSTEM_PROMPTS)
    
    # Config speichern
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Config aktualisiert: {config_path}")
    print(f"📝 System Prompts hinzugefügt für: {list(WUPHF_SYSTEM_PROMPTS.keys())}")
    
    return config

def test_system_prompt(role, test_input):
    """Teste System Prompt mit Ollama"""
    import requests
    
    system_prompt = WUPHF_SYSTEM_PROMPTS.get(role, "")
    
    prompt = f"{system_prompt}\n\nUser: {test_input}\nAssistant:"
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma4:e4b",
                "prompt": prompt,
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
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Hauptfunktion"""
    print("🎯 WUPHF System Prompt Setup")
    print("=" * 50)
    
    # Config aktualisieren
    config = update_wuphf_config_with_prompts()
    
    print("\n📋 Verfügbare System Prompts:")
    for role in WUPHF_SYSTEM_PROMPTS.keys():
        print(f"   - {role}")
    
    print("\n🧪 Teste System Prompts...")
    
    test_cases = [
        ("ceo", "Priorisiere die nächsten Aufgaben"),
        ("research", "Researche AI-Agent Markt"),
        ("analyst", "Analysiere Sales-Zahlen")
    ]
    
    for role, test_input in test_cases:
        print(f"\n📝 Test {role}:")
        print(f"   Input: {test_input}")
        
        response = test_system_prompt(role, test_input)
        if response:
            print(f"   Response: {response[:150]}...")
            print(f"   ✅ Test erfolgreich")
        else:
            print(f"   ❌ Test fehlgeschlagen")
    
    print("\n" + "=" * 50)
    print("🎉 System Prompt Setup abgeschlossen!")
    print("\n📋 Nächste Schritte:")
    print("1. WUPHF neu starten")
    print("2. Agent-Verhalten beobachten")
    print("3. Bei Bedarf System Prompts anpassen")
    
    print("\n💡 Vorteil: Sofort wirksam, kein Training nötig!")

if __name__ == "__main__":
    main()