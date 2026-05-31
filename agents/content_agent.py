"""
Content Agent for WUPHF Agile Agent Network.

This agent uses pitchdeck-2026:latest local model to create pitch decks
following 2026 best practices. It handles pitch deck creation, improvement
based on feedback, and content strategy.
"""

from typing import Dict

try:
    import ollama
except ImportError:
    ollama = None

class ContentAgent:
    """
    Content Agent - Creates pitch decks using pitchdeck-2026:latest model.
    
    This agent handles:
    - Pitch deck creation following 2026 best practices
    - Content improvement based on QA feedback
    - Content strategy and narrative development
    """
    
    def __init__(self, model: str = "pitchdeck-2026:latest"):
        """
        Initialize the Content Agent.
        
        Args:
            model: Ollama model identifier (default: pitchdeck-2026:latest)
        """
        self.model = model
        
    def create_pitch_deck(self, startup_details: Dict) -> Dict:
        """
        Create pitch deck based on startup details using 2026 best practices.
        
        Args:
            startup_details: Dictionary containing startup information
                - name: Company name
                - industry: Industry sector
                - funding_round: Current funding round
                - market_data: Optional market research data
        
        Returns:
            Dictionary containing:
            - slides: List of 11 slides with content
            - narrative: Overall narrative structure
        """
        if ollama is None:
            # Fallback for testing without ollama
            return {
                "slides": [
                    {"slide": 1, "title": "Title", "content": f"{startup_details.get('name', 'Company')}"},
                    {"slide": 2, "title": "Problem", "content": f"Problem in {startup_details.get('industry', 'Industry')}"},
                    {"slide": 3, "title": "Solution", "content": "AI-powered solution"},
                    {"slide": 4, "title": "Why Now", "content": "Market timing"},
                    {"slide": 5, "title": "Market", "content": "Market size"},
                    {"slide": 6, "title": "Competition", "content": "Competitive landscape"},
                    {"slide": 7, "title": "Product", "content": "Product demo"},
                    {"slide": 8, "title": "Traction", "content": "Growth metrics"},
                    {"slide": 9, "title": "Business Model", "content": "Revenue model"},
                    {"slide": 10, "title": "Team", "content": "Team overview"},
                    {"slide": 11, "title": "Ask", "content": "Funding request"}
                ],
                "narrative": "Generated from 2026 best practices"
            }
        
        prompt = f"""
        Erstelle professionelles Pitch-Deck für:
        {startup_details}
        
        Nutze 2026 Best Practices:
        - 30-Sekunden-Hook mit persönlicher Geschichte
        - 11-Slide-Struktur (Intro, Problem, Solution, Why Now, Market, Competition, Product, Traction, Business Model, Team, Ask)
        - VC-Frameworks (Sequoia: Klarheit, a16z: Founder-Market Fit, YC: 2-Satz-Test)
        - Quantitative Benchmarks (Seed ARR 0.25-1.5M, Series A 1.5-5M)
        - Unit Economics (LTV:CAC ≥ 3:1, Payback <12 Monate)
        - Berliner VC-Szene (KfW Capital, Deutschlandfonds, Climate Tech Hub)
        - Operation AI (Model Centricity, Defensibility, Usage Metrics)
        
        Gib zurück als strukturiertes JSON mit 11 Slides.
        """
        
        response = ollama.generate(model=self.model, prompt=prompt)
        return self._parse_pitch_deck(response['response'])
    
    def improve_pitch_deck(self, current_deck: Dict, feedback: Dict) -> Dict:
        """
        Improve pitch deck based on QA feedback.
        
        Args:
            current_deck: Current pitch deck content
            feedback: QA feedback with identified gaps and improvements
        
        Returns:
            Dictionary containing improved pitch deck
        """
        if ollama is None:
            # Fallback for testing without ollama
            improved_slides = current_deck.get("slides", [])
            for slide in improved_slides:
                slide["content"] += f" (Improved based on: {feedback.get('gap', 'feedback')})"
            return {
                "slides": improved_slides,
                "narrative": "Improved from feedback"
            }
        
        prompt = f"""
        Verbessere dieses Pitch-Deck basierend auf Feedback:
        
        Current Pitch-Deck: {current_deck}
        Feedback: {feedback}
        
        Fokus auf identifizierte Lücken und True North Kriterien:
        - 30-Sekunden-Hook Verbesserung
        - VC-Framework Tiefe
        - Quantitative Benchmarks Integration
        - Visuelle und narrative Elemente
        """
        
        response = ollama.generate(model=self.model, prompt=prompt)
        return self._parse_pitch_deck(response['response'])
    
    def _parse_pitch_deck(self, response: str) -> Dict:
        """
        Parse pitch deck from agent response.
        
        Args:
            response: Raw LLM response
        
        Returns:
            Parsed pitch deck dictionary with slides and narrative
        """
        # Try to parse as JSON first
        try:
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            # If not JSON, create structured response
            return {
                "slides": [
                    {"slide": 1, "title": "Title", "content": response[:200]},
                    {"slide": 2, "title": "Problem", "content": response[200:400]},
                    {"slide": 3, "title": "Solution", "content": response[400:600]},
                    {"slide": 4, "title": "Why Now", "content": response[600:800]},
                    {"slide": 5, "title": "Market", "content": response[800:1000]},
                    {"slide": 6, "title": "Competition", "content": response[1000:1200]},
                    {"slide": 7, "title": "Product", "content": response[1200:1400]},
                    {"slide": 8, "title": "Traction", "content": response[1400:1600]},
                    {"slide": 9, "title": "Business Model", "content": response[1600:1800]},
                    {"slide": 10, "title": "Team", "content": response[1800:2000]},
                    {"slide": 11, "title": "Ask", "content": response[2000:2200]}
                ],
                "narrative": "Generated from 2026 best practices"
            }