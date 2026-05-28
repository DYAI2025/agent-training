"""Tests for Research Agent - market research using qwen2.5:7b"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from agents.research_agent import ResearchAgent, ResearchTask, ResearchResult


@pytest.fixture
def research_agent():
    """Create ResearchAgent instance with mocked ollama"""
    with patch('agents.research_agent.ollama') as mock_ollama:
        agent = ResearchAgent(model="qwen2.5:7b")
        agent.ollama = mock_ollama
        return agent


@pytest.fixture
def sample_research_query():
    """Sample research query"""
    return {
        "topic": "AI pitch deck market",
        "focus_areas": ["market size", "competitors", "trends"],
        "target_audience": "investors"
    }


def test_research_agent_initialization():
    """Test ResearchAgent initialization"""
    with patch('agents.research_agent.ollama') as mock_ollama:
        agent = ResearchAgent(model="qwen2.5:7b")
        assert agent.model == "qwen2.5:7b"
        assert agent.ollama is not None


def test_conduct_market_research(research_agent, sample_research_query):
    """Test market research"""
    # Mock ollama response
    mock_response = Mock()
    mock_response.response = """
    {
        "market_size": {
            "total_addressable_market": "$50B",
            "serviceable_addressable_market": "$15B",
            "serviceable_obtainable_market": "$3B",
            "growth_rate": "25% CAGR"
        },
        "competitors": [
            {"name": "Competitor A", "strengths": ["Strong brand"], "weaknesses": ["High price"]},
            {"name": "Competitor B", "strengths": ["Good features"], "weaknesses": ["Limited reach"]}
        ],
        "trends": [
            {"trend": "AI-powered tools", "impact": "high", "timeline": "2024-2026"},
            {"trend": "Remote collaboration", "impact": "medium", "timeline": "2023-2025"}
        ],
        "insights": ["Market is growing rapidly", "Competition is fragmented"],
        "sources": ["Industry Report 2024", "Market Analysis"]
    }
    """
    research_agent.ollama.generate.return_value = mock_response
    
    result = research_agent.conduct_market_research(
        query=sample_research_query["topic"],
        focus_areas=sample_research_query["focus_areas"],
        target_audience=sample_research_query["target_audience"]
    )
    
    assert isinstance(result, ResearchResult)
    assert result.market_size is not None
    assert len(result.competitors) == 2
    assert len(result.trends) == 2
    assert len(result.insights) == 2
    assert len(result.sources) == 2


def test_analyze_competitors(research_agent):
    """Test competitor analysis"""
    competitors = ["Competitor A", "Competitor B"]
    
    # Mock ollama response
    mock_response = Mock()
    mock_response.response = """
    {
        "analysis": [
            {
                "name": "Competitor A",
                "strengths": ["Strong brand", "Large user base"],
                "weaknesses": ["High price", "Complex UI"],
                "market_position": "Market leader",
                "key_differentiators": ["Brand recognition"]
            },
            {
                "name": "Competitor B",
                "strengths": ["Good features", "Low price"],
                "weaknesses": ["Limited reach", "New entrant"],
                "market_position": "Challenger",
                "key_differentiators": ["Price competitiveness"]
            }
        ],
        "market_gaps": ["Mid-market segment underserved", "Enterprise features lacking"],
        "opportunities": ["Target mid-market", "Add enterprise features"]
    }
    """
    research_agent.ollama.generate.return_value = mock_response
    
    result = research_agent.analyze_competitors(competitors)
    
    assert isinstance(result, dict)
    assert "analysis" in result
    assert "market_gaps" in result
    assert "opportunities" in result
    assert len(result["analysis"]) == 2


def test_identify_market_trends(research_agent):
    """Test market trend identification"""
    industry = "AI and productivity tools"
    
    # Mock ollama response
    mock_response = Mock()
    mock_response.response = """
    {
        "current_trends": [
            {"name": "AI-powered automation", "impact": "high", "growth_stage": "rapid"},
            {"name": "Remote collaboration", "impact": "medium", "growth_stage": "mature"}
        ],
        "emerging_trends": [
            {"name": "Voice interfaces", "impact": "medium", "growth_stage": "early"},
            {"name": "AI agents", "impact": "high", "growth_stage": "emerging"}
        ],
        "declining_trends": [
            {"name": "Manual workflows", "impact": "low", "growth_stage": "declining"}
        ],
        "recommendations": ["Focus on AI automation", "Prepare for voice interfaces"]
    }
    """
    research_agent.ollama.generate.return_value = mock_response
    
    result = research_agent.identify_market_trends(industry)
    
    assert isinstance(result, dict)
    assert "current_trends" in result
    assert "emerging_trends" in result
    assert "declining_trends" in result
    assert "recommendations" in result


def test_gather_customer_insights(research_agent):
    """Test customer insights gathering"""
    customer_segment = "SMB owners"
    
    # Mock ollama response
    mock_response = Mock()
    mock_response.response = """
    {
        "pain_points": [
            {"point": "Time constraints", "severity": "high", "frequency": "common"},
            {"point": "Budget limitations", "severity": "medium", "frequency": "common"}
        ],
        "needs": [
            {"need": "Quick solutions", "priority": "high"},
            {"need": "Cost-effective tools", "priority": "high"}
        ],
        "behaviors": ["Price-sensitive", "Value quick implementation"],
        "preferences": ["SaaS over on-premise", "Monthly subscriptions"]
    }
    """
    research_agent.ollama.generate.return_value = mock_response
    
    result = research_agent.gather_customer_insights(customer_segment)
    
    assert isinstance(result, dict)
    assert "pain_points" in result
    assert "needs" in result
    assert "behaviors" in result
    assert "preferences" in result


def test_research_result_dataclass():
    """Test ResearchResult dataclass"""
    result = ResearchResult(
        market_size={"tam": "$50B"},
        competitors=[{"name": "Competitor A"}],
        trends=[{"trend": "AI tools"}],
        insights=["Market growing"],
        sources=["Report 2024"]
    )
    
    assert result.market_size["tam"] == "$50B"
    assert len(result.competitors) == 1
    assert len(result.trends) == 1


def test_research_agent_without_ollama():
    """Test ResearchAgent fallback when ollama is not available"""
    with patch('agents.research_agent.ollama', side_effect=ImportError):
        agent = ResearchAgent(model="qwen2.5:7b")
        
        # Should still initialize with fallback
        assert agent.model == "qwen2.5:7b"
        
        # Methods should return basic results
        result = agent.conduct_market_research(
            query="test",
            focus_areas=["market"],
            target_audience="investors"
        )
        
        assert isinstance(result, ResearchResult)
        assert result.market_size is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
