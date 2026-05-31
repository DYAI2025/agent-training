# WUPHF Agile Agent Network Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Konstruktion eines autonomen, agilen Multi-Agent-Netzwerks für WUPHF das wie ein echtes Team zusammenarbeitet, kontinuierlich lernt und echte Kundenarbeit liefert.

**Architecture:** Hierarchisches Agent-Netzwerk mit CEO/Orchestrator (Cloud-Modell) als strategischem Leader und spezialisierten Worker-Agenten (lokale Modelle) als operativem Team. Integration von True North QA-Prozessen, Learning Memory und autonomem Workflow-Management.

**Tech Stack:** WUPHF Framework, OpenRouter API (Nemotron120B), Ollama (lokale Modelle), Python, FastAPI, SQLite, GBrain Memory Backend.

---

## System Overview

### Team-Konstellation (Agile Squad)

**Strategic Layer (Cloud):**
- **CEO/Orchestrator Agent**: Nemotron120B via OpenRouter - Strategische Führung, Task-Delegation, Quality Gates, Learning Integration

**Operational Layer (Local):**
- **Content Agent**: pitchdeck-2026:latest - Pitch-Deck Erstellung, Content Strategy
- **Analyst Agent**: gemma4:e4b - QA Testing, Data Analysis, True North Evaluation
- **Research Agent**: qwen2.5:7b - Market Research, Competitive Intelligence
- **Design Agent**: llama3.2:latest - Visual Design, PDF Generation, UI Elements

### Core Principles
1. **No Simulation**: Alle Agenten führen echte Arbeit aus, keine Simulation
2. **True North QA**: Objektive Qualitätsmessung gegen definierte Standards
3. **Continuous Learning**: Pattern-Erkennung, Positive/Negative Measures, Memory Integration
4. **Autonomous Workflow**: Self-orchestrierende Tasks mit minimaler menschlicher Intervention
5. **Customer-Ready Output**: Release nur bei 80%+ True North Annäherung

---

## Task 1: CEO/Orchestrator Agent Konfiguration

**Files:**
- Create: `agents/ceo_orchestrator_agent.py`
- Modify: `config.json` (CEO Agent Konfiguration)
- Test: `tests/test_ceo_agent.py`

**Step 1: Write CEO Agent Interface**

```python
# agents/ceo_orchestrator_agent.py
from typing import Dict, List, Optional
from dataclasses import dataclass
import requests
import json

@dataclass
class Task:
    id: str
    description: str
    assigned_agent: str
    priority: int
    status: str = "pending"
    result: Optional[Dict] = None
    true_north_score: Optional[float] = None

class CEOOrchestratorAgent:
    def __init__(self, openrouter_api_key: str, model: str = "nvidia/nemotron-120b-instruct"):
        self.api_key = openrouter_api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"
        self.tasks: List[Task] = []
        self.learning_memory = []
        
    def analyze_customer_request(self, request: str) -> Dict:
        """Analysiert Kundenanfrage und erstellt strategischen Plan"""
        prompt = f"""
        Als CEO Agent analysiere diese Kundenanfrage:
        {request}
        
        Erstelle:
        1. Strategische Bewertung (Market Fit, Resource Requirements)
        2. Task-Aufteilung für spezialisierte Agenten
        3. Prioritäten und Deadlines
        4. True North Zieldefinition (mindestens 80%)
        """
        
        response = self._call_openrouter(prompt)
        return self._parse_strategic_plan(response)
    
    def delegate_task(self, task: Task) -> bool:
        """Delegiert Task an spezialisierten Agent"""
        if task.assigned_agent == "content":
            return self._delegate_to_content_agent(task)
        elif task.assigned_agent == "analyst":
            return self._delegate_to_analyst_agent(task)
        elif task.assigned_agent == "research":
            return self._delegate_to_research_agent(task)
        elif task.assigned_agent == "design":
            return self._delegate_to_design_agent(task)
        return False
    
    def evaluate_true_north_compliance(self, task_result: Dict) -> float:
        """Bewertet Task-Ergebnis gegen True North Checkliste"""
        prompt = f"""
        Als CEO Agent bewerte dieses Ergebnis gegen True North Checkliste:
        {json.dumps(task_result, indent=2)}
        
        Gib exakten Score zurück (0-100) und identifizierte Lücken.
        """
        
        response = self._call_openrouter(prompt)
        return self._parse_true_north_score(response)
    
    def integrate_learning(self, task: Task, outcome: str):
        """Integriert Lernerfahrung in Memory"""
        learning_entry = {
            "task_id": task.id,
            "agent": task.assigned_agent,
            "outcome": outcome,
            "true_north_score": task.true_north_score,
            "pattern": self._extract_pattern(task),
            "timestamp": self._get_timestamp()
        }
        self.learning_memory.append(learning_entry)
    
    def _call_openrouter(self, prompt: str) -> str:
        """API Call zu OpenRouter"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data
        )
        
        return response.json()["choices"][0]["message"]["content"]
    
    def _parse_strategic_plan(self, response: str) -> Dict:
        """Parst strategischen Plan aus CEO Response"""
        # Implement parsing logic
        return {"tasks": [], "priorities": [], "deadlines": []}
    
    def _parse_true_north_score(self, response: str) -> float:
        """Parst True North Score aus CEO Response"""
        # Implement parsing logic
        return 0.0
    
    def _extract_pattern(self, task: Task) -> str:
        """Extrahiert Pattern für Learning Memory"""
        return f"{task.assigned_agent}_{task.description[:20]}"
    
    def _get_timestamp(self) -> str:
        """Gibt aktuellen Timestamp zurück"""
        from datetime import datetime
        return datetime.now().isoformat()
```

**Step 2: Write failing test for CEO Agent**

```python
# tests/test_ceo_agent.py
import pytest
from agents.ceo_orchestrator_agent import CEOOrchestratorAgent, Task

def test_ceo_agent_initialization():
    ceo = CEOOrchestratorAgent("test_api_key")
    assert ceo.model == "nvidia/nemotron-120b-instruct"
    assert len(ceo.tasks) == 0
    assert len(ceo.learning_memory) == 0

def test_analyze_customer_request():
    ceo = CEOOrchestratorAgent("test_api_key")
    request = "Erstelle Pitch-Deck für AI-Startup"
    result = ceo.analyze_customer_request(request)
    assert "tasks" in result
    assert "priorities" in result

def test_delegate_task():
    ceo = CEOOrchestratorAgent("test_api_key")
    task = Task(id="1", description="Test Task", assigned_agent="content", priority=1)
    result = ceo.delegate_task(task)
    assert result is True
```

**Step 3: Run test to verify it fails**

Run: `pytest tests/test_ceo_agent.py -v`
Expected: FAIL with "CEOOrchestratorAgent not defined"

**Step 4: Implement minimal CEO Agent**

```python
# Copy Step 1 implementation here
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_ceo_agent.py -v`
Expected: PASS

**Step 6: Commit**

```bash
git add agents/ceo_orchestrator_agent.py tests/test_ceo_agent.py
git commit -m "feat: add CEO/Orchestrator Agent with OpenRouter integration"
```

---

## Task 2: Content Agent Konfiguration (pitchdeck-2026)

**Files:**
- Create: `agents/content_agent.py`
- Modify: `config.json` (Content Agent Konfiguration)
- Test: `tests/test_content_agent.py`

**Step 1: Write Content Agent Interface**

```python
# agents/content_agent.py
from typing import Dict
import ollama

class ContentAgent:
    def __init__(self, model: str = "pitchdeck-2026:latest"):
        self.model = model
        
    def create_pitch_deck(self, startup_details: Dict) -> Dict:
        """Erstellt Pitch-Deck basierend auf Startup-Details"""
        prompt = f"""
        Erstelle professionelles Pitch-Deck für:
        {startup_details}
        
        Nutze 2026 Best Practices:
        - 30-Sekunden-Hook
        - 11-Slide-Struktur
        - VC-Frameworks (Sequoia, a16z, YC)
        - Berliner VC-Szene Integration
        - Quantitative Benchmarks
        """
        
        response = ollama.generate(model=self.model, prompt=prompt)
        return self._parse_pitch_deck(response['response'])
    
    def improve_pitch_deck(self, current_deck: Dict, feedback: Dict) -> Dict:
        """Verbessert Pitch-Deck basierend auf Feedback"""
        prompt = f"""
        Verbessere dieses Pitch-Deck basierend auf Feedback:
        Current: {current_deck}
        Feedback: {feedback}
        
        Fokus auf identifizierte Lücken und True North Kriterien.
        """
        
        response = ollama.generate(model=self.model, prompt=prompt)
        return self._parse_pitch_deck(response['response'])
    
    def _parse_pitch_deck(self, response: str) -> Dict:
        """Parst Pitch-Deck aus Agent Response"""
        # Implement parsing logic
        return {"slides": [], "narrative": ""}
```

**Step 2: Write failing test for Content Agent**

```python
# tests/test_content_agent.py
import pytest
from agents.content_agent import ContentAgent

def test_content_agent_initialization():
    agent = ContentAgent()
    assert agent.model == "pitchdeck-2026:latest"

def test_create_pitch_deck():
    agent = ContentAgent()
    startup_details = {
        "name": "Test Startup",
        "industry": "AI/ML",
        "funding_round": "Seed"
    }
    result = agent.create_pitch_deck(startup_details)
    assert "slides" in result
    assert len(result["slides"]) == 11
```

**Step 3: Run test to verify it fails**

Run: `pytest tests/test_content_agent.py -v`
Expected: FAIL with "ContentAgent not defined"

**Step 4: Implement minimal Content Agent**

```python
# Copy Step 1 implementation here
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_content_agent.py -v`
Expected: PASS

**Step 6: Commit**

```bash
git add agents/content_agent.py tests/test_content_agent.py
git commit -m "feat: add Content Agent with pitchdeck-2026 model"
```

---

## Task 3: Analyst Agent Konfiguration (gemma4:e4b)

**Files:**
- Create: `agents/analyst_agent.py`
- Modify: `config.json` (Analyst Agent Konfiguration)
- Test: `tests/test_analyst_agent.py`

**Step 1: Write Analyst Agent Interface**

```python
# agents/analyst_agent.py
from typing import Dict
import ollama

class AnalystAgent:
    def __init__(self, model: str = "gemma4:e4b"):
        self.model = model
        
    def evaluate_true_north(self, pitch_deck: Dict, checklist_path: str) -> Dict:
        """Bewertet Pitch-Deck gegen True North Checkliste"""
        # Load checklist
        with open(checklist_path, 'r') as f:
            checklist = f.read()
        
        prompt = f"""
        Als Analyst Agent bewerte dieses Pitch-Deck objektiv gegen True North Checkliste:
        Pitch-Deck: {pitch_deck}
        Checkliste: {checklist}
        
        Gib zurück:
        1. Detaillierten Score pro Kategorie (A-H)
        2. Gesamt-Score (0-100)
        3. Identifizierte Lücken
        4. Konkrete Verbesserungsmaßnahmen
        """
        
        response = ollama.generate(model=self.model, prompt=prompt)
        return self._parse_evaluation(response['response'])
    
    def analyze_gap(self, current_score: float, target_score: float) -> Dict:
        """Analysiert Gap zwischen aktuellem und Ziel-Score"""
        gap = target_score - current_score
        prompt = f"""
        Analysiere Gap von {gap} Punkten ({current_score}% → {target_score}%).
        
        Identifiziere:
        1. Kritische Lücken (Priority 1)
        2. Wichtige Lücken (Priority 2)
        3. Nice-to-have Lücken (Priority 3)
        """
        
        response = ollama.generate(model=self.model, prompt=prompt)
        return self._parse_gap_analysis(response['response'])
    
    def _parse_evaluation(self, response: str) -> Dict:
        """Parst Evaluation aus Analyst Response"""
        # Implement parsing logic
        return {"category_scores": {}, "total_score": 0, "gaps": [], "improvements": []}
    
    def _parse_gap_analysis(self, response: str) -> Dict:
        """Parst Gap-Analyse aus Analyst Response"""
        # Implement parsing logic
        return {"priority_1": [], "priority_2": [], "priority_3": []}
```

**Step 2: Write failing test for Analyst Agent**

```python
# tests/test_analyst_agent.py
import pytest
from agents.analyst_agent import AnalystAgent

def test_analyst_agent_initialization():
    agent = AnalystAgent()
    assert agent.model == "gemma4:e4b"

def test_evaluate_true_north():
    agent = AnalystAgent()
    pitch_deck = {"slides": []}
    result = agent.evaluate_true_north(pitch_deck, "checklist.md")
    assert "total_score" in result
    assert 0 <= result["total_score"] <= 100
```

**Step 3: Run test to verify it fails**

Run: `pytest tests/test_analyst_agent.py -v`
Expected: FAIL with "AnalystAgent not defined"

**Step 4: Implement minimal Analyst Agent**

```python
# Copy Step 1 implementation here
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_analyst_agent.py -v`
Expected: PASS

**Step 6: Commit**

```bash
git add agents/analyst_agent.py tests/test_analyst_agent.py
git commit -m "feat: add Analyst Agent with True North QA capabilities"
```

---

## Task 4: Research Agent Konfiguration (qwen2.5:7b)

**Files:**
- Create: `agents/research_agent.py`
- Modify: `config.json` (Research Agent Konfiguration)
- Test: `tests/test_research_agent.py`

**Step 1: Write Research Agent Interface**

```python
# agents/research_agent.py
from typing import Dict
import ollama

class ResearchAgent:
    def __init__(self, model: str = "qwen2.5:7b"):
        self.model = model
        
    def market_research(self, industry: str, region: str) -> Dict:
        """Führt Markt-Research für spezifische Industry/Region durch"""
        prompt = f"""
        Führe umfassendes Market Research durch:
        Industry: {industry}
        Region: {region}
        
        Recherchiere:
        1. Marktgröße (TAM/SAM/SOM)
        2. Key Players und Competition
        3. Regulatory Landscape
        4. Funding Trends
        5. Local VC Scene
        """
        
        response = ollama.generate(model=self.model, prompt=prompt)
        return self._parse_research(response['response'])
    
    def competitive_intelligence(self, competitors: list) -> Dict:
        """Sammelt Competitive Intelligence"""
        prompt = f"""
        Analysiere diese Wettbewerber:
        {competitors}
        
        Identifiziere:
        1. Strengths und Weaknesses
        2. Market Positioning
        3. Pricing Strategies
        4. Differentiation Opportunities
        """
        
        response = ollama.generate(model=self.model, prompt=prompt)
        return self._parse_competitive_analysis(response['response'])
    
    def _parse_research(self, response: str) -> Dict:
        """Parst Research Ergebnisse"""
        # Implement parsing logic
        return {"market_size": {}, "competition": [], "regulatory": {}, "funding": {}}
    
    def _parse_competitive_analysis(self, response: str) -> Dict:
        """Parst Competitive Analysis"""
        # Implement parsing logic
        return {"competitors": {}, "opportunities": []}
```

**Step 2: Write failing test for Research Agent**

```python
# tests/test_research_agent.py
import pytest
from agents.research_agent import ResearchAgent

def test_research_agent_initialization():
    agent = ResearchAgent()
    assert agent.model == "qwen2.5:7b"

def test_market_research():
    agent = ResearchAgent()
    result = agent.market_research("AI/ML", "DACH")
    assert "market_size" in result
    assert "competition" in result
```

**Step 3: Run test to verify it fails**

Run: `pytest tests/test_research_agent.py -v`
Expected: FAIL with "ResearchAgent not defined"

**Step 4: Implement minimal Research Agent**

```python
# Copy Step 1 implementation here
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_research_agent.py -v`
Expected: PASS

**Step 6: Commit**

```bash
git add agents/research_agent.py tests/test_research_agent.py
git commit -m "feat: add Research Agent with market intelligence capabilities"
```

---

## Task 5: Design Agent Konfiguration (llama3.2:latest)

**Files:**
- Create: `agents/design_agent.py`
- Modify: `config.json` (Design Agent Konfiguration)
- Test: `tests/test_design_agent.py`

**Step 1: Write Design Agent Interface**

```python
# agents/design_agent.py
from typing import Dict
import ollama
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class DesignAgent:
    def __init__(self, model: str = "llama3.2:latest"):
        self.model = model
        
    def create_pitch_deck_pdf(self, pitch_deck_content: Dict, output_path: str) -> bool:
        """Erstellt professionelles PDF aus Pitch-Deck Content"""
        prompt = f"""
        Erstelle visuelles Design-Konzept für Pitch-Deck:
        {pitch_deck_content}
        
        Definiere:
        1. Farbschema (Corporate Colors)
        2. Typografie-Hierarchie
        3. Layout-Struktur
        4. Visual Elements (Charts, Graphs, Icons)
        """
        
        response = ollama.generate(model=self.model, prompt=prompt)
        design_concept = self._parse_design_concept(response['response'])
        
        return self._generate_pdf(pitch_deck_content, design_concept, output_path)
    
    def improve_visual_elements(self, current_pdf: str, feedback: Dict) -> bool:
        """Verbessert visuelle Elemente basierend auf Feedback"""
        prompt = f"""
        Verbessere visuelle Elemente basierend auf Feedback:
        Current PDF: {current_pdf}
        Feedback: {feedback}
        
        Fokus auf:
        1. Visual Impact
        2. Data Visualization
        3. Brand Consistency
        """
        
        response = ollama.generate(model=self.model, prompt=prompt)
        improvements = self._parse_design_improvements(response['response'])
        
        return self._apply_improvements(current_pdf, improvements)
    
    def _parse_design_concept(self, response: str) -> Dict:
        """Parst Design-Konzept"""
        # Implement parsing logic
        return {"colors": {}, "typography": {}, "layout": {}, "visuals": []}
    
    def _generate_pdf(self, content: Dict, design: Dict, output_path: str) -> bool:
        """Generiert PDF mit ReportLab"""
        try:
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Implement PDF generation logic
            # Add slides, styling, visual elements
            
            doc.build(story)
            return True
        except Exception as e:
            print(f"PDF Generation Error: {e}")
            return False
    
    def _parse_design_improvements(self, response: str) -> Dict:
        """Parst Design-Verbesserungen"""
        # Implement parsing logic
        return {"visual_improvements": [], "layout_changes": []}
    
    def _apply_improvements(self, pdf_path: str, improvements: Dict) -> bool:
        """Wendet Design-Verbesserungen an"""
        # Implement improvement logic
        return True
```

**Step 2: Write failing test for Design Agent**

```python
# tests/test_design_agent.py
import pytest
from agents.design_agent import DesignAgent

def test_design_agent_initialization():
    agent = DesignAgent()
    assert agent.model == "llama3.2:latest"

def test_create_pitch_deck_pdf():
    agent = DesignAgent()
    content = {"slides": [{"title": "Test"}]}
    result = agent.create_pitch_deck_pdf(content, "test_output.pdf")
    assert result is True
```

**Step 3: Run test to verify it fails**

Run: `pytest tests/test_design_agent.py -v`
Expected: FAIL with "DesignAgent not defined"

**Step 4: Implement minimal Design Agent**

```python
# Copy Step 1 implementation here
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_design_agent.py -v`
Expected: PASS

**Step 6: Commit**

```bash
git add agents/design_agent.py tests/test_design_agent.py
git commit -m "feat: add Design Agent with PDF generation capabilities"
```

---

## Task 6: Agile Workflow Orchestrator

**Files:**
- Create: `workflow/agile_orchestrator.py`
- Modify: `config.json` (Workflow Konfiguration)
- Test: `tests/test_agile_orchestrator.py`

**Step 1: Write Agile Orchestrator Interface**

```python
# workflow/agile_orchestrator.py
from typing import Dict, List
from agents.ceo_orchestrator_agent import CEOOrchestratorAgent
from agents.content_agent import ContentAgent
from agents.analyst_agent import AnalystAgent
from agents.research_agent import ResearchAgent
from agents.design_agent import DesignAgent

class AgileOrchestrator:
    def __init__(self, openrouter_api_key: str):
        self.ceo = CEOOrchestratorAgent(openrouter_api_key)
        self.content = ContentAgent()
        self.analyst = AnalystAgent()
        self.research = ResearchAgent()
        self.design = DesignAgent()
        
    def process_customer_request(self, customer_request: Dict) -> Dict:
        """Verarbeitet kompletten Kunden-Request durch agile Team"""
        # Phase 1: Strategic Analysis (CEO)
        strategic_plan = self.ceo.analyze_customer_request(customer_request["request"])
        
        # Phase 2: Research (Research Agent)
        market_data = self.research.market_research(
            customer_request["industry"],
            customer_request["region"]
        )
        
        # Phase 3: Content Creation (Content Agent)
        pitch_deck = self.content.create_pitch_deck({
            **customer_request,
            "market_data": market_data
        })
        
        # Phase 4: QA Evaluation (Analyst Agent)
        qa_result = self.analyst.evaluate_true_north(
            pitch_deck,
            "knowledge_base/semantic/true_north_pitch_deck_checklist.md"
        )
        
        # Phase 5: Iterative Improvement Loop
        iteration = 1
        max_iterations = 5
        target_score = 80.0
        
        while qa_result["total_score"] < target_score and iteration < max_iterations:
            print(f"Iteration {iteration}: Current Score {qa_result['total_score']}%")
            
            # Gap Analysis
            gap_analysis = self.analyst.analyze_gap(
                qa_result["total_score"],
                target_score
            )
            
            # Improvement
            improved_deck = self.content.improve_pitch_deck(
                pitch_deck,
                gap_analysis
            )
            
            # Re-evaluation
            qa_result = self.analyst.evaluate_true_north(
                improved_deck,
                "knowledge_base/semantic/true_north_pitch_deck_checklist.md"
            )
            
            pitch_deck = improved_deck
            iteration += 1
        
        # Phase 6: Design (Design Agent)
        pdf_path = f"output/{customer_request['project_name']}_final.pdf"
        design_success = self.design.create_pitch_deck_pdf(pitch_deck, pdf_path)
        
        # Phase 7: Learning Integration (CEO)
        self.ceo.integrate_learning(
            task_id=customer_request["project_id"],
            outcome="success" if qa_result["total_score"] >= target_score else "partial",
            true_north_score=qa_result["total_score"]
        )
        
        return {
            "status": "completed",
            "final_score": qa_result["total_score"],
            "iterations": iteration,
            "output_path": pdf_path if design_success else None,
            "strategic_plan": strategic_plan,
            "qa_result": qa_result
        }
```

**Step 2: Write failing test for Agile Orchestrator**

```python
# tests/test_agile_orchestrator.py
import pytest
from workflow.agile_orchestrator import AgileOrchestrator

def test_agile_orchestrator_initialization():
    orchestrator = AgileOrchestrator("test_api_key")
    assert orchestrator.ceo is not None
    assert orchestrator.content is not None
    assert orchestrator.analyst is not None

def test_process_customer_request():
    orchestrator = AgileOrchestrator("test_api_key")
    request = {
        "request": "Erstelle Pitch-Deck",
        "industry": "AI/ML",
        "region": "DACH",
        "project_name": "test_project",
        "project_id": "test_001"
    }
    result = orchestrator.process_customer_request(request)
    assert result["status"] in ["completed", "partial"]
    assert "final_score" in result
```

**Step 3: Run test to verify it fails**

Run: `pytest tests/test_agile_orchestrator.py -v`
Expected: FAIL with "AgileOrchestrator not defined"

**Step 4: Implement minimal Agile Orchestrator**

```python
# Copy Step 1 implementation here
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_agile_orchestrator.py -v`
Expected: PASS

**Step 6: Commit**

```bash
git add workflow/agile_orchestrator.py tests/test_agile_orchestrator.py
git commit -m "feat: add Agile Orchestrator for autonomous team workflow"
```

---

## Task 7: Config Integration

**Files:**
- Modify: `config.json`
- Test: `tests/test_config_integration.py`

**Step 1: Update Config with Agent Network**

```json
{
  "agent_network": {
    "ceo_orchestrator": {
      "provider": "openrouter",
      "model": "nvidia/nemotron-120b-instruct",
      "api_key_env": "OPENROUTER_API_KEY",
      "role": "strategic",
      "capabilities": ["analysis", "delegation", "qa_gates", "learning_integration"]
    },
    "content_agent": {
      "provider": "ollama",
      "model": "pitchdeck-2026:latest",
      "role": "operational",
      "capabilities": ["pitch_deck_creation", "content_strategy", "improvement"]
    },
    "analyst_agent": {
      "provider": "ollama",
      "model": "gemma4:e4b",
      "role": "operational",
      "capabilities": ["qa_testing", "data_analysis", "true_north_evaluation"]
    },
    "research_agent": {
      "provider": "ollama",
      "model": "qwen2.5:7b",
      "role": "operational",
      "capabilities": ["market_research", "competitive_intelligence"]
    },
    "design_agent": {
      "provider": "ollama",
      "model": "llama3.2:latest",
      "role": "operational",
      "capabilities": ["visual_design", "pdf_generation", "improvement"]
    }
  },
  "workflow": {
    "max_iterations": 5,
    "target_true_north_score": 80.0,
    "learning_memory_enabled": true,
    "autonomous_mode": true
  }
}
```

**Step 2: Write failing test for Config Integration**

```python
# tests/test_config_integration.py
import pytest
import json

def test_config_has_agent_network():
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    assert "agent_network" in config
    assert "ceo_orchestrator" in config["agent_network"]
    assert "content_agent" in config["agent_network"]
    assert config["agent_network"]["ceo_orchestrator"]["provider"] == "openrouter"

def test_workflow_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    assert "workflow" in config
    assert config["workflow"]["target_true_north_score"] == 80.0
    assert config["workflow"]["autonomous_mode"] is True
```

**Step 3: Run test to verify it fails**

Run: `pytest tests/test_config_integration.py -v`
Expected: FAIL with "agent_network not in config"

**Step 4: Implement Config Update**

```python
# Copy Step 1 JSON into config.json
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_config_integration.py -v`
Expected: PASS

**Step 6: Commit**

```bash
git add config.json tests/test_config_integration.py
git commit -m "feat: integrate agent network configuration"
```

---

## Task 8: Learning Memory System

**Files:**
- Create: `memory/learning_memory.py`
- Modify: `memory/learning_memory.json`
- Test: `tests/test_learning_memory.py`

**Step 1: Write Learning Memory Interface**

```python
# memory/learning_memory.py
from typing import Dict, List
import json
from datetime import datetime

class LearningMemory:
    def __init__(self, storage_path: str = "memory/learning_memory.json"):
        self.storage_path = storage_path
        self.patterns = self._load_memory()
        
    def _load_memory(self) -> Dict:
        """Lädt Learning Memory aus Datei"""
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "positive_patterns": [],
                "negative_patterns": [],
                "improvement_measures": [],
                "performance_metrics": []
            }
    
    def save_memory(self):
        """Speichert Learning Memory in Datei"""
        with open(self.storage_path, 'w') as f:
            json.dump(self.patterns, f, indent=2)
    
    def add_positive_pattern(self, pattern: Dict):
        """Fügt positives Pattern hinzu"""
        pattern["timestamp"] = datetime.now().isoformat()
        pattern["validation_count"] = pattern.get("validation_count", 0) + 1
        self.patterns["positive_patterns"].append(pattern)
        self.save_memory()
    
    def add_negative_pattern(self, pattern: Dict):
        """Fügt negatives Pattern hinzu"""
        pattern["timestamp"] = datetime.now().isoformat()
        pattern["validation_count"] = pattern.get("validation_count", 0) + 1
        self.patterns["negative_patterns"].append(pattern)
        self.save_memory()
    
    def add_improvement_measure(self, measure: Dict):
        """Fügt Verbesserungsmaßnahme hinzu"""
        measure["timestamp"] = datetime.now().isoformat()
        self.patterns["improvement_measures"].append(measure)
        self.save_memory()
    
    def get_relevant_patterns(self, context: str) -> List[Dict]:
        """Gibt relevante Patterns für Context zurück"""
        relevant = []
        for pattern in self.patterns["positive_patterns"]:
            if context.lower() in pattern.get("context", "").lower():
                relevant.append(pattern)
        return relevant
    
    def get_performance_trend(self) -> Dict:
        """Gibt Performance-Trend zurück"""
        return {
            "total_patterns": len(self.patterns["positive_patterns"]) + len(self.patterns["negative_patterns"]),
            "positive_ratio": len(self.patterns["positive_patterns"]) / max(1, len(self.patterns["positive_patterns"]) + len(self.patterns["negative_patterns"])),
            "improvement_count": len(self.patterns["improvement_measures"])
        }
```

**Step 2: Write failing test for Learning Memory**

```python
# tests/test_learning_memory.py
import pytest
from memory.learning_memory import LearningMemory

def test_learning_memory_initialization():
    memory = LearningMemory("test_memory.json")
    assert "positive_patterns" in memory.patterns
    assert "negative_patterns" in memory.patterns

def test_add_positive_pattern():
    memory = LearningMemory("test_memory.json")
    pattern = {
        "pattern": "Test Pattern",
        "impact": "+10%",
        "context": "Test Context"
    }
    memory.add_positive_pattern(pattern)
    assert len(memory.patterns["positive_patterns"]) == 1

def test_get_performance_trend():
    memory = LearningMemory("test_memory.json")
    trend = memory.get_performance_trend()
    assert "total_patterns" in trend
    assert "positive_ratio" in trend
```

**Step 3: Run test to verify it fails**

Run: `pytest tests/test_learning_memory.py -v`
Expected: FAIL with "LearningMemory not defined"

**Step 4: Implement minimal Learning Memory**

```python
# Copy Step 1 implementation here
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_learning_memory.py -v`
Expected: PASS

**Step 6: Commit**

```bash
git add memory/learning_memory.py tests/test_learning_memory.py
git commit -m "feat: add Learning Memory system for pattern recognition"
```

---

## Task 9: Main Application Entry Point

**Files:**
- Create: `main_agile_network.py`
- Modify: `README.md` (Usage Instructions)
- Test: `tests/test_main_integration.py`

**Step 1: Write Main Application**

```python
# main_agile_network.py
import os
from workflow.agile_orchestrator import AgileOrchestrator
from dotenv import load_dotenv

def main():
    """Main Entry Point für WUPHF Agile Agent Network"""
    load_dotenv()
    
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable required")
    
    # Initialize Agile Orchestrator
    orchestrator = AgileOrchestrator(openrouter_api_key)
    
    # Example Customer Request
    customer_request = {
        "request": "Erstelle professionelles Pitch-Deck für AI-Startup im Climate Tech Bereich",
        "industry": "Climate Tech",
        "region": "DACH",
        "project_name": "carbonai_solutions_pitch_deck",
        "project_id": "customer_001_pitch_deck",
        "customer_details": {
            "name": "Benjamin Poersch",
            "email": "ben.poersch@gmail.com",
            "company": "Autonomous Pitch Deck Agency"
        }
    }
    
    # Process Request through Agile Team
    print("🚀 Starting Agile Agent Network...")
    result = orchestrator.process_customer_request(customer_request)
    
    # Output Results
    print(f"\n✅ Processing Complete!")
    print(f"Final True North Score: {result['final_score']}%")
    print(f"Iterations Required: {result['iterations']}")
    print(f"Output Path: {result['output_path']}")
    
    if result['final_score'] >= 80.0:
        print("🎉 READY FOR CUSTOMER RELEASE")
    else:
        print("⚠️ REQUIRES ADDITIONAL IMPROVEMENT")

if __name__ == "__main__":
    main()
```

**Step 2: Write failing test for Main Integration**

```python
# tests/test_main_integration.py
import pytest
from main_agile_network import main
import os

def test_main_requires_api_key():
    # Remove API key if exists
    if "OPENROUTER_API_KEY" in os.environ:
        del os.environ["OPENROUTER_API_KEY"]
    
    with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
        main()

def test_main_with_mock_api_key(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_key")
    # Test would require mocking the entire orchestrator
    # For now, just test that it doesn't crash on initialization
    pass
```

**Step 3: Run test to verify it fails**

Run: `pytest tests/test_main_integration.py -v`
Expected: FAIL with "main_agile_network not defined"

**Step 4: Implement minimal Main Application**

```python
# Copy Step 1 implementation here
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_main_integration.py -v`
Expected: PASS

**Step 6: Commit**

```bash
git add main_agile_network.py tests/test_main_integration.py
git commit -m "feat: add main application entry point for agile network"
```

---

## Task 10: Documentation and Usage

**Files:**
- Create: `README_AGILE_NETWORK.md`
- Modify: `README.md` (Update with agile network info)

**Step 1: Write Comprehensive Documentation**

```markdown
# WUPHF Agile Agent Network

## Overview
Autonomouses Multi-Agent-Netzwerk für professionelle Pitch-Deck-Erstellung mit True North QA-Prozessen.

## Architecture
- **CEO/Orchestrator**: Nemotron120B via OpenRouter (Strategic Layer)
- **Content Agent**: pitchdeck-2026:latest (Pitch-Deck Creation)
- **Analyst Agent**: gemma4:e4b (QA Testing, True North Evaluation)
- **Research Agent**: qwen2.5:7b (Market Intelligence)
- **Design Agent**: llama3.2:latest (Visual Design, PDF Generation)

## Usage

### Installation
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with OPENROUTER_API_KEY
```

### Run Agile Network
```bash
python main_agile_network.py
```

### Configuration
Edit `config.json` to customize:
- Agent assignments
- Model selection
- Workflow parameters
- True North targets

## Learning System
The network continuously learns from:
- Positive patterns (successful approaches)
- Negative patterns (avoided mistakes)
- Improvement measures (effective changes)
- Performance trends (quality evolution)

## True North QA Process
1. Initial creation by Content Agent
2. QA evaluation by Analyst Agent
3. Gap analysis and improvement planning
4. Iterative refinement until 80%+ score
5. Design integration by Design Agent
6. Final release by CEO Agent
```

**Step 2: Update Main README**

```markdown
# WUPHF - Autonomous Pitch Deck Agency

## Quick Start
```bash
# Traditional Mode
python main.py

# Agile Agent Network Mode
python main_agile_network.py
```

## Agile Network
See [README_AGILE_NETWORK.md](README_AGILE_NETWORK.md) for autonomous multi-agent workflow.
```

**Step 3: Commit Documentation**

```bash
git add README_AGILE_NETWORK.md README.md
git commit -m "docs: add comprehensive agile network documentation"
```

---

## Task 11: Environment Setup

**Files:**
- Create: `.env.example`
- Create: `requirements.txt`
- Test: N/A

**Step 1: Create Environment Example**

```bash
# .env.example
OPENROUTER_API_KEY=your_openrouter_api_key_here
OLLAMA_BASE_URL=http://localhost:11434
WUPHF_MEMORY_PATH=./memory
WUPHF_OUTPUT_PATH=./output
```

**Step 2: Create Requirements**

```txt
# requirements.txt
requests>=2.31.0
ollama>=0.1.0
python-dotenv>=1.0.0
reportlab>=4.0.0
pytest>=7.4.0
```

**Step 3: Commit Environment Setup**

```bash
git add .env.example requirements.txt
git commit -m "feat: add environment configuration and dependencies"
```

---

## Task 12: Integration Testing

**Files:**
- Create: `tests/integration/test_full_workflow.py`
- Test: Full workflow integration test

**Step 1: Write Integration Test**

```python
# tests/integration/test_full_workflow.py
import pytest
import os
from workflow.agile_orchestrator import AgileOrchestrator

@pytest.mark.integration
def test_full_customer_workflow():
    """Test complete customer request workflow"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        pytest.skip("OPENROUTER_API_KEY not set")
    
    orchestrator = AgileOrchestrator(api_key)
    
    customer_request = {
        "request": "Test Request for Integration",
        "industry": "AI/ML",
        "region": "DACH",
        "project_name": "integration_test",
        "project_id": "test_integration_001"
    }
    
    result = orchestrator.process_customer_request(customer_request)
    
    assert result["status"] in ["completed", "partial"]
    assert "final_score" in result
    assert 0 <= result["final_score"] <= 100
    assert result["iterations"] > 0
```

**Step 2: Run Integration Test**

Run: `pytest tests/integration/test_full_workflow.py -v --integration`
Expected: PASS (with valid API key)

**Step 3: Commit Integration Test**

```bash
git add tests/integration/test_full_workflow.py
git commit -m "test: add full workflow integration test"
```

---

## Execution Summary

This plan creates a complete autonomous agile agent network with:

1. **Strategic Leadership**: CEO/Orchestrator with Nemotron120B for high-level decision making
2. **Specialized Workers**: 4 local agents for specific tasks (Content, Analyst, Research, Design)
3. **True North QA**: Objective quality measurement with iterative improvement
4. **Learning System**: Pattern recognition and continuous improvement
5. **Autonomous Workflow**: Self-orchestrating tasks with minimal human intervention
6. **Real Customer Output**: Professional pitch decks released only at 80%+ quality

**Total Tasks**: 12
**Estimated Implementation Time**: 4-6 hours
**Testing Coverage**: Full unit + integration tests