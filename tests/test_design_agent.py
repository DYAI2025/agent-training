"""Tests for Design Agent - visual design and PDF generation using llama3.2:latest"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from agents.design_agent import DesignAgent, DesignTask, DesignResult


@pytest.fixture
def design_agent():
    """Create DesignAgent instance with mocked ollama"""
    with patch('agents.design_agent.ollama') as mock_ollama:
        agent = DesignAgent(model="llama3.2:latest")
        agent.ollama = mock_ollama
        return agent


@pytest.fixture
def sample_pitch_deck():
    """Sample pitch deck for design"""
    return {
        "title": "AI Startup",
        "slides": [
            {"title": "Problem", "content": "Current solutions are slow"},
            {"title": "Solution", "content": "Our AI is faster"}
        ]
    }


def test_design_agent_initialization():
    """Test DesignAgent initialization"""
    with patch('agents.design_agent.ollama') as mock_ollama:
        agent = DesignAgent(model="llama3.2:latest")
        assert agent.model == "llama3.2:latest"
        assert agent.ollama is not None


def test_create_visual_design(design_agent, sample_pitch_deck):
    """Test visual design creation"""
    design_requirements = {
        "style": "modern minimalist",
        "color_scheme": "blue and white",
        "target_audience": "investors"
    }
    
    # Mock ollama response
    mock_response = Mock()
    mock_response.response = """
    {
        "design_system": {
            "primary_color": "#0066CC",
            "secondary_color": "#FFFFFF",
            "accent_color": "#FF6B35",
            "font_family": "Inter",
            "font_sizes": {"title": 48, "body": 16}
        },
        "slide_layouts": [
            {"slide_index": 0, "layout": "title_centered", "elements": ["title", "subtitle"]},
            {"slide_index": 1, "layout": "content_split", "elements": ["text", "icon"]}
        ],
        "visual_elements": ["icons", "charts", "progress_bars"],
        "design_recommendations": ["Use consistent spacing", "Add visual hierarchy"]
    }
    """
    design_agent.ollama.generate.return_value = mock_response
    
    result = design_agent.create_visual_design(
        pitch_deck=sample_pitch_deck,
        requirements=design_requirements
    )
    
    assert isinstance(result, DesignResult)
    assert result.design_system is not None
    assert len(result.slide_layouts) == 2
    assert len(result.visual_elements) == 3
    assert len(result.design_recommendations) == 2


def test_generate_pdf_structure(design_agent, sample_pitch_deck):
    """Test PDF structure generation"""
    # Mock ollama response
    mock_response = Mock()
    mock_response.response = """
    {
        "pdf_structure": {
            "page_size": "A4",
            "orientation": "landscape",
            "margins": {"top": 0.5, "bottom": 0.5, "left": 0.5, "right": 0.5}
        },
        "page_breaks": [1, 3, 5],
        "master_slides": [
            {"name": "title_slide", "background": "#0066CC"},
            {"name": "content_slide", "background": "#FFFFFF"}
        ],
        "export_settings": {
            "quality": "high",
            "compression": "medium",
            "include_fonts": true
        }
    }
    """
    design_agent.ollama.generate.return_value = mock_response
    
    result = design_agent.generate_pdf_structure(sample_pitch_deck)
    
    assert isinstance(result, dict)
    assert "pdf_structure" in result
    assert "page_breaks" in result
    assert "master_slides" in result
    assert "export_settings" in result


def test_optimize_design_for_accessibility(design_agent):
    """Test accessibility optimization"""
    design_content = {
        "colors": ["#0066CC", "#FFFFFF"],
        "fonts": ["Inter", "Arial"],
        "font_sizes": [48, 16, 12]
    }
    
    # Mock ollama response
    mock_response = Mock()
    mock_response.response = """
    {
        "accessibility_score": 0.85,
        "issues": [
            {"type": "contrast", "severity": "medium", "description": "Low contrast on slide 3"},
            {"type": "font_size", "severity": "low", "description": "Some text too small"}
        ],
        "recommendations": [
            "Increase contrast ratio to 4.5:1",
            "Use minimum 12pt font for body text"
        ],
        "optimized_design": {
            "colors": ["#0055AA", "#FFFFFF"],
            "fonts": ["Inter", "Arial"],
            "font_sizes": [48, 18, 14]
        }
    }
    """
    design_agent.ollama.generate.return_value = mock_response
    
    result = design_agent.optimize_design_for_accessibility(design_content)
    
    assert isinstance(result, dict)
    assert "accessibility_score" in result
    assert "issues" in result
    assert "recommendations" in result
    assert "optimized_design" in result


def test_create_brand_guidelines(design_agent):
    """Test brand guidelines creation"""
    brand_info = {
        "company_name": "AI Startup",
        "industry": "technology",
        "values": ["innovation", "speed", "reliability"]
    }
    
    # Mock ollama response
    mock_response = Mock()
    mock_response.response = """
    {
        "brand_identity": {
            "logo_variations": ["primary", "secondary", "icon"],
            "color_palette": {
                "primary": "#0066CC",
                "secondary": "#FF6B35",
                "neutral": "#F5F5F5"
            },
            "typography": {
                "headings": "Inter Bold",
                "body": "Inter Regular"
            }
        },
        "voice_guidelines": {
            "tone": "professional yet approachable",
            "language_style": "clear and concise",
            "key_phrases": ["AI-powered", "fast", "reliable"]
        },
        "usage_rules": [
            "Maintain consistent spacing",
            "Use approved colors only",
            "Follow typography hierarchy"
        ]
    }
    """
    design_agent.ollama.generate.return_value = mock_response
    
    result = design_agent.create_brand_guidelines(brand_info)
    
    assert isinstance(result, dict)
    assert "brand_identity" in result
    assert "voice_guidelines" in result
    assert "usage_rules" in result


def test_design_result_dataclass():
    """Test DesignResult dataclass"""
    result = DesignResult(
        design_system={"primary_color": "#0066CC"},
        slide_layouts=[{"slide_index": 0, "layout": "title"}],
        visual_elements=["icons", "charts"],
        design_recommendations=["Use consistent spacing"]
    )
    
    assert result.design_system["primary_color"] == "#0066CC"
    assert len(result.slide_layouts) == 1
    assert len(result.visual_elements) == 2


def test_design_agent_without_ollama():
    """Test DesignAgent fallback when ollama is not available"""
    with patch('agents.design_agent.ollama', side_effect=ImportError):
        agent = DesignAgent(model="llama3.2:latest")
        
        # Should still initialize with fallback
        assert agent.model == "llama3.2:latest"
        
        # Methods should return basic results
        result = agent.create_visual_design(
            pitch_deck={"slides": []},
            requirements={"style": "modern"}
        )
        
        assert isinstance(result, DesignResult)
        assert result.design_system is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
