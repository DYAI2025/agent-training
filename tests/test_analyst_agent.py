"""Tests for Analyst Agent - QA testing and data analysis"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from agents.analyst_agent import AnalystAgent, AnalysisTask, AnalysisResult


@pytest.fixture
def analyst_agent():
    """Create AnalystAgent instance with mocked ollama"""
    with patch('agents.analyst_agent.ollama') as mock_ollama:
        agent = AnalystAgent(model="gemma4:e4b")
        agent.ollama = mock_ollama
        return agent


@pytest.fixture
def sample_pitch_deck():
    """Sample pitch deck for testing"""
    return {
        "title": "AI Startup Pitch",
        "slides": [
            {"title": "Problem", "content": "Current solutions are slow"},
            {"title": "Solution", "content": "Our AI is faster"},
            {"title": "Market", "content": "$10B market size"}
        ]
    }


@pytest.fixture
def sample_checklist():
    """Sample True North checklist"""
    return {
        "criteria": [
            {"id": "c1", "category": "Structure", "description": "Clear problem statement", "weight": 0.3},
            {"id": "c2", "category": "Content", "description": "Quantified market size", "weight": 0.4},
            {"id": "c3", "category": "Design", "description": "Visual consistency", "weight": 0.3}
        ]
    }


def test_analyst_agent_initialization():
    """Test AnalystAgent initialization"""
    with patch('agents.analyst_agent.ollama') as mock_ollama:
        agent = AnalystAgent(model="gemma4:e4b")
        assert agent.model == "gemma4:e4b"
        assert agent.ollama is not None


def test_analyze_pitch_deck_quality(analyst_agent, sample_pitch_deck, sample_checklist):
    """Test pitch deck quality analysis"""
    # Mock ollama response
    mock_response = Mock()
    mock_response.response = """
    {
        "overall_score": 0.75,
        "criteria_scores": [
            {"id": "c1", "score": 0.8, "feedback": "Problem statement is clear"},
            {"id": "c2", "score": 0.7, "feedback": "Market size needs more detail"},
            {"id": "c3", "score": 0.75, "feedback": "Design is consistent"}
        ],
        "strengths": ["Clear problem statement", "Good flow"],
        "weaknesses": ["Market size lacks detail", "Missing competitive analysis"],
        "improvement_suggestions": ["Add specific market data", "Include competitor comparison"]
    }
    """
    analyst_agent.ollama.generate.return_value = mock_response
    
    result = analyst_agent.analyze_pitch_deck_quality(
        pitch_deck=sample_pitch_deck,
        checklist=sample_checklist
    )
    
    assert isinstance(result, AnalysisResult)
    assert result.overall_score == 0.75
    assert len(result.criteria_scores) == 3
    assert len(result.strengths) == 2
    assert len(result.weaknesses) == 2
    assert len(result.improvement_suggestions) == 2
    assert result.passes_threshold(0.7) is True
    assert result.passes_threshold(0.8) is False


def test_analyze_data_patterns(analyst_agent):
    """Test data pattern analysis"""
    sample_data = [
        {"metric": "engagement", "value": 0.85},
        {"metric": "conversion", "value": 0.12},
        {"metric": "retention", "value": 0.45}
    ]
    
    # Mock ollama response
    mock_response = Mock()
    mock_response.response = """
    {
        "patterns": ["Engagement is high", "Conversion is low"],
        "anomalies": ["Retention is below average"],
        "insights": ["Focus on improving conversion"],
        "recommendations": ["A/B test conversion funnels"]
    }
    """
    analyst_agent.ollama.generate.return_value = mock_response
    
    result = analyst_agent.analyze_data_patterns(
        data=sample_data,
        analysis_type="performance"
    )
    
    assert isinstance(result, dict)
    assert "patterns" in result
    assert "anomalies" in result
    assert "insights" in result
    assert "recommendations" in result


def test_validate_compliance(analyst_agent, sample_pitch_deck):
    """Test compliance validation"""
    standards = {
        "requirements": [
            {"id": "r1", "description": "No misleading claims", "severity": "high"},
            {"id": "r2", "description": "Financial projections realistic", "severity": "medium"}
        ]
    }
    
    # Mock ollama response
    mock_response = Mock()
    mock_response.response = """
    {
        "compliant": true,
        "violations": [],
        "warnings": ["Financial projections are optimistic"],
        "recommendations": ["Add sensitivity analysis"]
    }
    """
    analyst_agent.ollama.generate.return_value = mock_response
    
    result = analyst_agent.validate_compliance(
        content=sample_pitch_deck,
        standards=standards
    )
    
    assert result["compliant"] is True
    assert len(result["violations"]) == 0
    assert len(result["warnings"]) == 1


def test_generate_qa_report(analyst_agent, sample_pitch_deck, sample_checklist):
    """Test QA report generation"""
    # Mock quality analysis
    mock_response = Mock()
    mock_response.response = """
    {
        "overall_score": 0.75,
        "criteria_scores": [
            {"id": "c1", "score": 0.8, "feedback": "Problem statement is clear"},
            {"id": "c2", "score": 0.7, "feedback": "Market size needs more detail"},
            {"id": "c3", "score": 0.75, "feedback": "Design is consistent"}
        ],
        "strengths": ["Clear problem statement"],
        "weaknesses": ["Market size lacks detail"],
        "improvement_suggestions": ["Add specific market data"]
    }
    """
    analyst_agent.ollama.generate.return_value = mock_response
    
    report = analyst_agent.generate_qa_report(
        pitch_deck=sample_pitch_deck,
        checklist=sample_checklist,
        threshold=0.8
    )
    
    assert "overall_score" in report
    assert "passes_threshold" in report
    assert "criteria_breakdown" in report
    assert "recommendations" in report
    assert report["passes_threshold"] is False


def test_analysis_result_dataclass():
    """Test AnalysisResult dataclass"""
    result = AnalysisResult(
        overall_score=0.85,
        criteria_scores=[
            {"id": "c1", "score": 0.9, "feedback": "Good"}
        ],
        strengths=["Strong content"],
        weaknesses=["Weak design"],
        improvement_suggestions=["Improve design"]
    )
    
    assert result.overall_score == 0.85
    assert result.passes_threshold(0.8) is True
    assert result.passes_threshold(0.9) is False


def test_analyst_agent_without_ollama():
    """Test AnalystAgent fallback when ollama is not available"""
    with patch('agents.analyst_agent.ollama', side_effect=ImportError):
        agent = AnalystAgent(model="gemma4:e4b")
        
        # Should still initialize with fallback
        assert agent.model == "gemma4:e4b"
        
        # Methods should return basic results
        result = agent.analyze_pitch_deck_quality(
            pitch_deck={"slides": []},
            checklist={"criteria": []}
        )
        
        assert isinstance(result, AnalysisResult)
        assert result.overall_score >= 0  # Fallback should return valid score


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
