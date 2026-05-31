"""Analyst Agent - QA testing and data analysis using gemma4:e4b"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import json
import sys

try:
    import ollama
except ImportError:
    ollama = None


@dataclass
class AnalysisTask:
    """Task for analysis agent"""
    task_type: str  # "quality_analysis", "data_analysis", "compliance_check"
    data: Dict[str, Any]
    criteria: Optional[Dict[str, Any]] = None
    threshold: float = 0.8


@dataclass
class AnalysisResult:
    """Result from analysis"""
    overall_score: float
    criteria_scores: List[Dict[str, Any]]
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: List[str]
    
    def passes_threshold(self, threshold: float) -> bool:
        """Check if result meets threshold"""
        return self.overall_score >= threshold


class AnalystAgent:
    """Analyst Agent for QA testing and data analysis"""
    
    def __init__(self, model: str = "gemma4:e4b"):
        self.model = model
        self.ollama = ollama
        
    def analyze_pitch_deck_quality(
        self, 
        pitch_deck: Dict[str, Any], 
        checklist: Dict[str, Any]
    ) -> AnalysisResult:
        """Analyze pitch deck quality against True North checklist"""
        
        if self.ollama is None:
            # Fallback for testing without ollama
            return self._fallback_quality_analysis(pitch_deck, checklist)
        
        prompt = self._build_quality_analysis_prompt(pitch_deck, checklist)
        
        try:
            response = self.ollama.generate(
                model=self.model,
                prompt=prompt,
                format="json"
            )
            
            result_data = json.loads(response.response)
            return AnalysisResult(
                overall_score=result_data.get("overall_score", 0.5),
                criteria_scores=result_data.get("criteria_scores", []),
                strengths=result_data.get("strengths", []),
                weaknesses=result_data.get("weaknesses", []),
                improvement_suggestions=result_data.get("improvement_suggestions", [])
            )
        except Exception as e:
            print(f"Error in quality analysis: {e}", file=sys.stderr)
            return self._fallback_quality_analysis(pitch_deck, checklist)
    
    def analyze_data_patterns(
        self, 
        data: List[Dict[str, Any]], 
        analysis_type: str = "performance"
    ) -> Dict[str, Any]:
        """Analyze data patterns and generate insights"""
        
        if self.ollama is None:
            return self._fallback_data_analysis(data, analysis_type)
        
        prompt = self._build_data_analysis_prompt(data, analysis_type)
        
        try:
            response = self.ollama.generate(
                model=self.model,
                prompt=prompt,
                format="json"
            )
            
            return json.loads(response.response)
        except Exception as e:
            print(f"Error in data analysis: {e}", file=sys.stderr)
            return self._fallback_data_analysis(data, analysis_type)
    
    def validate_compliance(
        self, 
        content: Dict[str, Any], 
        standards: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate content against compliance standards"""
        
        if self.ollama is None:
            return self._fallback_compliance_check(content, standards)
        
        prompt = self._build_compliance_prompt(content, standards)
        
        try:
            response = self.ollama.generate(
                model=self.model,
                prompt=prompt,
                format="json"
            )
            
            return json.loads(response.response)
        except Exception as e:
            print(f"Error in compliance check: {e}", file=sys.stderr)
            return self._fallback_compliance_check(content, standards)
    
    def generate_qa_report(
        self,
        pitch_deck: Dict[str, Any],
        checklist: Dict[str, Any],
        threshold: float = 0.8
    ) -> Dict[str, Any]:
        """Generate comprehensive QA report"""
        
        quality_result = self.analyze_pitch_deck_quality(pitch_deck, checklist)
        
        return {
            "overall_score": quality_result.overall_score,
            "passes_threshold": quality_result.passes_threshold(threshold),
            "threshold": threshold,
            "criteria_breakdown": quality_result.criteria_scores,
            "strengths": quality_result.strengths,
            "weaknesses": quality_result.weaknesses,
            "recommendations": quality_result.improvement_suggestions,
            "summary": self._generate_summary(quality_result, threshold)
        }
    
    def _build_quality_analysis_prompt(
        self, 
        pitch_deck: Dict[str, Any], 
        checklist: Dict[str, Any]
    ) -> str:
        """Build prompt for quality analysis"""
        
        prompt = f"""You are a QA analyst specializing in pitch deck evaluation. Analyze the following pitch deck against the True North checklist.

PITCH DECK:
{json.dumps(pitch_deck, indent=2)}

TRUE NORTH CHECKLIST:
{json.dumps(checklist, indent=2)}

Provide analysis in JSON format:
{{
    "overall_score": <float 0-1>,
    "criteria_scores": [
        {{
            "id": "<criterion_id>",
            "score": <float 0-1>,
            "feedback": "<specific feedback>"
        }}
    ],
    "strengths": ["<strength 1>", "<strength 2>"],
    "weaknesses": ["<weakness 1>", "<weakness 2>"],
    "improvement_suggestions": ["<suggestion 1>", "<suggestion 2>"]
}}

Be specific and actionable in your feedback."""
        
        return prompt
    
    def _build_data_analysis_prompt(
        self, 
        data: List[Dict[str, Any]], 
        analysis_type: str
    ) -> str:
        """Build prompt for data analysis"""
        
        prompt = f"""You are a data analyst. Analyze the following data for {analysis_type} patterns.

DATA:
{json.dumps(data, indent=2)}

Provide analysis in JSON format:
{{
    "patterns": ["<pattern 1>", "<pattern 2>"],
    "anomalies": ["<anomaly 1>"],
    "insights": ["<insight 1>"],
    "recommendations": ["<recommendation 1>"]
}}

Focus on actionable insights."""
        
        return prompt
    
    def _build_compliance_prompt(
        self, 
        content: Dict[str, Any], 
        standards: Dict[str, Any]
    ) -> str:
        """Build prompt for compliance validation"""
        
        prompt = f"""You are a compliance officer. Validate the following content against the provided standards.

CONTENT:
{json.dumps(content, indent=2)}

STANDARDS:
{json.dumps(standards, indent=2)}

Provide validation in JSON format:
{{
    "compliant": <boolean>,
    "violations": ["<violation 1>"],
    "warnings": ["<warning 1>"],
    "recommendations": ["<recommendation 1>"]
}}

Be thorough but fair in your assessment."""
        
        return prompt
    
    def _generate_summary(
        self, 
        result: AnalysisResult, 
        threshold: float
    ) -> str:
        """Generate summary of analysis"""
        
        if result.passes_threshold(threshold):
            return f"Pitch deck PASSES quality threshold ({result.overall_score:.2%} >= {threshold:.0%}). Strong in: {', '.join(result.strengths[:2])}."
        else:
            return f"Pitch deck FAILS quality threshold ({result.overall_score:.2%} < {threshold:.0%}). Key issues: {', '.join(result.weaknesses[:2])}."
    
    def _fallback_quality_analysis(
        self, 
        pitch_deck: Dict[str, Any], 
        checklist: Dict[str, Any]
    ) -> AnalysisResult:
        """Fallback quality analysis when ollama is not available"""
        
        # Simple heuristic-based analysis
        criteria = checklist.get("criteria", [])
        criteria_scores = []
        
        for criterion in criteria:
            score = 0.7  # Default moderate score
            feedback = f"Basic check for {criterion.get('description', 'criterion')}"
            criteria_scores.append({
                "id": criterion.get("id", "unknown"),
                "score": score,
                "feedback": feedback
            })
        
        overall_score = sum(c["score"] for c in criteria_scores) / len(criteria_scores) if criteria_scores else 0.5
        
        return AnalysisResult(
            overall_score=overall_score,
            criteria_scores=criteria_scores,
            strengths=["Structured content present"],
            weaknesses=["Detailed analysis requires ollama"],
            improvement_suggestions=["Install ollama for detailed analysis"]
        )
    
    def _fallback_data_analysis(
        self, 
        data: List[Dict[str, Any]], 
        analysis_type: str
    ) -> Dict[str, Any]:
        """Fallback data analysis when ollama is not available"""
        
        return {
            "patterns": [f"Basic pattern detected in {analysis_type}"],
            "anomalies": [],
            "insights": ["Install ollama for detailed insights"],
            "recommendations": ["Install ollama for advanced analysis"]
        }
    
    def _fallback_compliance_check(
        self, 
        content: Dict[str, Any], 
        standards: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Fallback compliance check when ollama is not available"""
        
        return {
            "compliant": True,
            "violations": [],
            "warnings": ["Basic compliance check - install ollama for detailed validation"],
            "recommendations": ["Install ollama for thorough compliance checking"]
        }


if __name__ == "__main__":
    # Quick test
    agent = AnalystAgent()
    
    test_pitch_deck = {
        "title": "Test Pitch",
        "slides": [{"title": "Problem", "content": "Test content"}]
    }
    
    test_checklist = {
        "criteria": [
            {"id": "c1", "category": "Structure", "description": "Clear problem", "weight": 0.5}
        ]
    }
    
    result = agent.analyze_pitch_deck_quality(test_pitch_deck, test_checklist)
    print(f"Overall score: {result.overall_score}")
    print(f"Strengths: {result.strengths}")
