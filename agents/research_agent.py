"""Research Agent - market research using qwen2.5:7b"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import json
import sys

try:
    import ollama
except ImportError:
    ollama = None


@dataclass
class ResearchTask:
    """Task for research agent"""
    task_type: str  # "market_research", "competitor_analysis", "trend_identification", "customer_insights"
    query: str
    focus_areas: List[str]
    target_audience: Optional[str] = None


@dataclass
class ResearchResult:
    """Result from research"""
    market_size: Dict[str, Any]
    competitors: List[Dict[str, Any]]
    trends: List[Dict[str, Any]]
    insights: List[str]
    sources: List[str]


class ResearchAgent:
    """Research Agent for market research and competitive analysis"""
    
    def __init__(self, model: str = "qwen2.5:7b"):
        self.model = model
        self.ollama = ollama
        
    def conduct_market_research(
        self,
        query: str,
        focus_areas: List[str],
        target_audience: str = "general"
    ) -> ResearchResult:
        """Conduct comprehensive market research"""
        
        if self.ollama is None:
            return self._fallback_market_research(query, focus_areas)
        
        prompt = self._build_market_research_prompt(query, focus_areas, target_audience)
        
        try:
            response = self.ollama.generate(
                model=self.model,
                prompt=prompt,
                format="json"
            )
            
            result_data = json.loads(response.response)
            return ResearchResult(
                market_size=result_data.get("market_size", {}),
                competitors=result_data.get("competitors", []),
                trends=result_data.get("trends", []),
                insights=result_data.get("insights", []),
                sources=result_data.get("sources", [])
            )
        except Exception as e:
            print(f"Error in market research: {e}", file=sys.stderr)
            return self._fallback_market_research(query, focus_areas)
    
    def analyze_competitors(
        self,
        competitors: List[str],
        focus_areas: List[str] = None
    ) -> Dict[str, Any]:
        """Analyze specific competitors"""
        
        if focus_areas is None:
            focus_areas = ["strengths", "weaknesses", "market_position"]
        
        if self.ollama is None:
            return self._fallback_competitor_analysis(competitors)
        
        prompt = self._build_competitor_analysis_prompt(competitors, focus_areas)
        
        try:
            response = self.ollama.generate(
                model=self.model,
                prompt=prompt,
                format="json"
            )
            
            return json.loads(response.response)
        except Exception as e:
            print(f"Error in competitor analysis: {e}", file=sys.stderr)
            return self._fallback_competitor_analysis(competitors)
    
    def identify_market_trends(
        self,
        industry: str,
        time_horizon: str = "2-3 years"
    ) -> Dict[str, Any]:
        """Identify current and emerging market trends"""
        
        if self.ollama is None:
            return self._fallback_trend_identification(industry)
        
        prompt = self._build_trend_identification_prompt(industry, time_horizon)
        
        try:
            response = self.ollama.generate(
                model=self.model,
                prompt=prompt,
                format="json"
            )
            
            return json.loads(response.response)
        except Exception as e:
            print(f"Error in trend identification: {e}", file=sys.stderr)
            return self._fallback_trend_identification(industry)
    
    def gather_customer_insights(
        self,
        customer_segment: str,
        research_methods: List[str] = None
    ) -> Dict[str, Any]:
        """Gather insights about customer segment"""
        
        if research_methods is None:
            research_methods = ["interviews", "surveys", "behavioral_analysis"]
        
        if self.ollama is None:
            return self._fallback_customer_insights(customer_segment)
        
        prompt = self._build_customer_insights_prompt(customer_segment, research_methods)
        
        try:
            response = self.ollama.generate(
                model=self.model,
                prompt=prompt,
                format="json"
            )
            
            return json.loads(response.response)
        except Exception as e:
            print(f"Error in gathering customer insights: {e}", file=sys.stderr)
            return self._fallback_customer_insights(customer_segment)
    
    def _build_market_research_prompt(
        self,
        query: str,
        focus_areas: List[str],
        target_audience: str
    ) -> str:
        """Build prompt for market research"""
        
        prompt = f"""You are a market research analyst. Conduct comprehensive market research on the following topic.

RESEARCH QUERY: {query}
FOCUS AREAS: {', '.join(focus_areas)}
TARGET AUDIENCE: {target_audience}

Provide research results in JSON format:
{{
    "market_size": {{
        "total_addressable_market": "<TAM>",
        "serviceable_addressable_market": "<SAM>",
        "serviceable_obtainable_market": "<SOM>",
        "growth_rate": "<CAGR>"
    }},
    "competitors": [
        {{
            "name": "<competitor_name>",
            "strengths": ["<strength 1>"],
            "weaknesses": ["<weakness 1>"]
        }}
    ],
    "trends": [
        {{
            "trend": "<trend_name>",
            "impact": "<high/medium/low>",
            "timeline": "<timeframe>"
        }}
    ],
    "insights": ["<key insight 1>", "<key insight 2>"],
    "sources": ["<source 1>", "<source 2>"]
}}

Be specific and provide realistic estimates based on current market conditions."""
        
        return prompt
    
    def _build_competitor_analysis_prompt(
        self,
        competitors: List[str],
        focus_areas: List[str]
    ) -> str:
        """Build prompt for competitor analysis"""
        
        prompt = f"""You are a competitive intelligence analyst. Analyze the following competitors.

COMPETITORS: {', '.join(competitors)}
FOCUS AREAS: {', '.join(focus_areas)}

Provide analysis in JSON format:
{{
    "analysis": [
        {{
            "name": "<competitor_name>",
            "strengths": ["<strength 1>"],
            "weaknesses": ["<weakness 1>"],
            "market_position": "<position>",
            "key_differentiators": ["<differentiator 1>"]
        }}
    ],
    "market_gaps": ["<gap 1>", "<gap 2>"],
    "opportunities": ["<opportunity 1>", "<opportunity 2>"]
}}

Focus on actionable insights."""
        
        return prompt
    
    def _build_trend_identification_prompt(
        self,
        industry: str,
        time_horizon: str
    ) -> str:
        """Build prompt for trend identification"""
        
        prompt = f"""You are a trend analyst. Identify current and emerging trends in the following industry.

INDUSTRY: {industry}
TIME HORIZON: {time_horizon}

Provide trend analysis in JSON format:
{{
    "current_trends": [
        {{"name": "<trend>", "impact": "<high/medium/low>", "growth_stage": "<stage>"}}
    ],
    "emerging_trends": [
        {{"name": "<trend>", "impact": "<high/medium/low>", "growth_stage": "<stage>"}}
    ],
    "declining_trends": [
        {{"name": "<trend>", "impact": "<high/medium/low>", "growth_stage": "<stage>"}}
    ],
    "recommendations": ["<recommendation 1>", "<recommendation 2>"]
}}

Focus on trends relevant to business strategy."""
        
        return prompt
    
    def _build_customer_insights_prompt(
        self,
        customer_segment: str,
        research_methods: List[str]
    ) -> str:
        """Build prompt for customer insights"""
        
        prompt = f"""You are a customer research analyst. Gather insights about the following customer segment.

CUSTOMER SEGMENT: {customer_segment}
RESEARCH METHODS: {', '.join(research_methods)}

Provide insights in JSON format:
{{
    "pain_points": [
        {{"point": "<pain point>", "severity": "<high/medium/low>", "frequency": "<common/rare>"}}
    ],
    "needs": [
        {{"need": "<need>", "priority": "<high/medium/low>"}}
    ],
    "behaviors": ["<behavior 1>", "<behavior 2>"],
    "preferences": ["<preference 1>", "<preference 2>"]
}}

Focus on actionable insights for product development."""
        
        return prompt
    
    def _fallback_market_research(
        self,
        query: str,
        focus_areas: List[str]
    ) -> ResearchResult:
        """Fallback market research when ollama is not available"""
        
        return ResearchResult(
            market_size={
                "total_addressable_market": "TBD - requires ollama",
                "serviceable_addressable_market": "TBD - requires ollama",
                "serviceable_obtainable_market": "TBD - requires ollama",
                "growth_rate": "TBD - requires ollama"
            },
            competitors=[],
            trends=[],
            insights=[f"Basic research for: {query}. Install ollama for detailed analysis."],
            sources=["Fallback mode - no ollama"]
        )
    
    def _fallback_competitor_analysis(
        self,
        competitors: List[str]
    ) -> Dict[str, Any]:
        """Fallback competitor analysis when ollama is not available"""
        
        return {
            "analysis": [
                {
                    "name": comp,
                    "strengths": ["Analysis requires ollama"],
                    "weaknesses": ["Analysis requires ollama"],
                    "market_position": "Unknown",
                    "key_differentiators": []
                }
                for comp in competitors
            ],
            "market_gaps": ["Install ollama for detailed analysis"],
            "opportunities": ["Install ollama for detailed analysis"]
        }
    
    def _fallback_trend_identification(
        self,
        industry: str
    ) -> Dict[str, Any]:
        """Fallback trend identification when ollama is not available"""
        
        return {
            "current_trends": [],
            "emerging_trends": [],
            "declining_trends": [],
            "recommendations": [f"Install ollama for detailed trend analysis in {industry}"]
        }
    
    def _fallback_customer_insights(
        self,
        customer_segment: str
    ) -> Dict[str, Any]:
        """Fallback customer insights when ollama is not available"""
        
        return {
            "pain_points": [],
            "needs": [],
            "behaviors": [],
            "preferences": [f"Install ollama for detailed insights on {customer_segment}"]
        }


if __name__ == "__main__":
    # Quick test
    agent = ResearchAgent()
    
    result = agent.conduct_market_research(
        query="AI pitch deck tools",
        focus_areas=["market size", "competitors"],
        target_audience="investors"
    )
    
    print(f"Market size: {result.market_size}")
    print(f"Insights: {result.insights}")
