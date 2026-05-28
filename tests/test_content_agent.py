# tests/test_content_agent.py
import pytest
from unittest.mock import Mock, patch
from agents.content_agent import ContentAgent

def test_content_agent_initialization():
    agent = ContentAgent()
    assert agent.model == "pitchdeck-2026:latest"

@patch('agents.content_agent.ollama')
def test_create_pitch_deck(mock_ollama):
    mock_ollama.generate.return_value = {'response': '{"slides": [{"title": "Test"}], "narrative": "Test narrative"}'}
    
    agent = ContentAgent()
    startup_details = {
        "name": "Test Startup",
        "industry": "AI/ML",
        "funding_round": "Seed"
    }
    result = agent.create_pitch_deck(startup_details)
    assert "slides" in result
    assert "narrative" in result
    mock_ollama.generate.assert_called_once()

@patch('agents.content_agent.ollama')
def test_improve_pitch_deck(mock_ollama):
    mock_ollama.generate.return_value = {'response': '{"slides": [{"title": "Improved"}], "narrative": "Improved"}'}
    
    agent = ContentAgent()
    current_deck = {"slides": [{"title": "Test"}]}
    feedback = {"gap": "Missing hook"}
    result = agent.improve_pitch_deck(current_deck, feedback)
    assert "slides" in result
    mock_ollama.generate.assert_called_once()