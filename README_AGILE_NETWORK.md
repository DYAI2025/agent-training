# WUPHF Agile Agent Network

An autonomous multi-agent system for creating professional pitch decks using AI agents that work together like an agile team.

## Overview

The WUPHF Agile Agent Network is a sophisticated multi-agent orchestration system that coordinates specialized AI agents to create high-quality pitch decks. The system uses a CEO/Orchestrator agent (via OpenRouter's Nemotron120B) to delegate tasks to specialized worker agents (via local Ollama models), following agile methodology with continuous improvement through learning memory.

## Architecture

### Agent Composition

1. **CEO/Orchestrator Agent** (Nemotron120B via OpenRouter)
   - Strategic leadership and decision-making
   - Customer request analysis
   - Task delegation to specialized agents
   - True North QA evaluation
   - Learning integration

2. **Content Agent** (pitchdeck-2026:latest via Ollama)
   - Pitch deck creation with 2026 best practices
   - Content improvement based on feedback
   - Few-shot learning integration

3. **Research Agent** (qwen2.5:7b via Ollama)
   - Market research and competitive analysis
   - Trend identification
   - Customer insights gathering

4. **Analyst Agent** (gemma4:e4b via Ollama)
   - Quality assurance testing
   - Data analysis and pattern recognition
   - Compliance validation
   - QA report generation

5. **Design Agent** (llama3.2:latest via Ollama)
   - Visual design creation
   - PDF structure generation
   - Accessibility optimization
   - Brand guidelines development

### Workflow Phases

The agile workflow follows these phases:

1. **Initialization** - Customer request analysis and workflow setup
2. **Research** - Market research and competitive analysis
3. **Content Creation** - Pitch deck content generation
4. **Analysis** - Quality assurance against True North checklist
5. **Design** - Visual design and PDF generation
6. **Iteration** - Continuous improvement cycles (max 3 iterations)
7. **Finalization** - CEO evaluation and delivery

### Learning Memory System

The system includes a sophisticated learning memory that:

- Stores all agent experiences (successes, failures, insights)
- Detects patterns in agent performance
- Generates actionable learning insights
- Applies learning to improve future task execution
- Provides agent performance summaries
- Supports memory export/import for backup

## Installation

### Prerequisites

- Python 3.12+
- Ollama (for local models)
- OpenRouter API key (for CEO agent)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd autoresearch
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Ollama:
```bash
# Linux/Mac
curl -fsSL https://ollama.com/install.sh | sh

# Or visit https://ollama.com/download for other platforms
```

4. Pull required Ollama models:
```bash
ollama pull gemma4:e4b
ollama pull qwen2.5:7b
ollama pull llama3.2:latest
```

5. Create custom pitchdeck model (if not already created):
```bash
# The pitchdeck-2026:latest model should be created using the training script
# See agents/content_agent.py for model requirements
```

6. Configure environment variables:
```bash
export OPENROUTER_API_KEY="your-openrouter-api-key"
```

## Configuration

The system is configured via `config.json`:

```json
{
  "agent_network": {
    "name": "WUPHF Agile Agent Network",
    "version": "1.0.0"
  },
  "ceo_agent": {
    "model": "nvidia/nemotron-120b",
    "api_provider": "openrouter",
    "api_url": "https://openrouter.ai/api/v1/chat/completions"
  },
  "specialized_agents": {
    "content_agent": {
      "model": "pitchdeck-2026:latest",
      "api_provider": "ollama"
    },
    "research_agent": {
      "model": "qwen2.5:7b",
      "api_provider": "ollama"
    },
    "analyst_agent": {
      "model": "gemma4:e4b",
      "api_provider": "ollama"
    },
    "design_agent": {
      "model": "llama3.2:latest",
      "api_provider": "ollama"
    }
  },
  "workflow": {
    "agile_orchestrator": {
      "max_iterations": 3,
      "quality_threshold": 0.8
    }
  }
}
```

## Usage

### Command Line Interface

```bash
# Show network status
python main_agile_network.py --status

# Process a customer request
python main_agile_network.py --request '{"customer_id": "123", "request_type": "pitch_deck", "topic": "AI startup", "target_audience": "investors"}'

# Use custom config
python main_agile_network.py --config /path/to/config.json --status
```

### Python API

```python
from main_agile_network import WUPHFAgileNetwork

# Initialize the network
network = WUPHFAgileNetwork(config_path="config.json")

# Process a customer request
customer_request = {
    "customer_id": "cust_123",
    "request_type": "pitch_deck",
    "topic": "AI-powered productivity tool",
    "target_audience": "investors",
    "requirements": {
        "style": "modern minimalist",
        "length": "10-12 slides",
        "focus": ["problem", "solution", "market", "team"]
    }
}

result = network.process_customer_request(
    customer_request=customer_request,
    quality_threshold=0.8
)

if result["success"]:
    print(f"Quality score: {result['quality_score']}")
    print(f"Iterations: {result['iterations']}")
    print(f"Pitch deck: {result['final_pitch_deck']}")
else:
    print(f"Error: {result['error']}")

# Get network status
status = network.get_network_status()
print(f"Network status: {status}")
```

### Direct Agent Usage

```python
from agents.content_agent import ContentAgent
from agents.research_agent import ResearchAgent
from agents.analyst_agent import AnalystAgent
from agents.design_agent import DesignAgent

# Create agents
content_agent = ContentAgent(model="pitchdeck-2026:latest")
research_agent = ResearchAgent(model="qwen2.5:7b")
analyst_agent = AnalystAgent(model="gemma4:e4b")
design_agent = DesignAgent(model="llama3.2:latest")

# Use agents individually
research_data = research_agent.conduct_market_research(
    query="AI productivity tools",
    focus_areas=["market", "competitors"],
    target_audience="investors"
)

pitch_deck = content_agent.create_pitch_deck(
    topic="AI productivity tool",
    research_data=research_data,
    requirements={"style": "modern"}
)

quality_result = analyst_agent.analyze_pitch_deck_quality(
    pitch_deck=pitch_deck,
    checklist=true_north_checklist
)

design_result = design_agent.create_visual_design(
    pitch_deck=pitch_deck,
    requirements={"style": "modern minimalist"}
)
```

## Testing

### Run All Tests

```bash
python -m pytest tests/ -v
```

### Run Specific Test Suite

```bash
# Test individual agents
python -m pytest tests/test_ceo_agent.py -v
python -m pytest tests/test_content_agent.py -v
python -m pytest tests/test_research_agent.py -v
python -m pytest tests/test_analyst_agent.py -v
python -m pytest tests/test_design_agent.py -v

# Test workflow
python -m pytest tests/test_agile_orchestrator.py -v

# Test memory system
python -m pytest tests/test_learning_memory.py -v

# Test main application
python -m pytest tests/test_main_agile_network.py -v

# Test configuration
python -m pytest tests/test_config.py -v
```

### Test Coverage

```bash
python -m pytest tests/ --cov=. --cov-report=html
```

## True North Quality Standards

The system uses a True North checklist to ensure pitch deck quality:

- **Structure**: Clear problem statement and solution presentation
- **Content**: Quantified market size, traction, and competitive analysis
- **Design**: Visual consistency, professional appearance, accessibility compliance

The default quality threshold is 80% (0.8), but this can be configured in `config.json`.

## Learning and Improvement

The system continuously improves through:

1. **Pattern Recognition**: Identifies successful and failure patterns
2. **Performance Tracking**: Monitors agent success rates and quality scores
3. **Insight Generation**: Creates actionable recommendations
4. **Learning Application**: Applies insights to future tasks

View learning insights:

```python
status = network.get_network_status()
for insight in status["learning_insights"]:
    print(f"{insight['type']}: {insight['description']}")
    print(f"Recommendation: {insight['recommendation']}")
```

## Troubleshooting

### Ollama Connection Issues

```bash
# Check Ollama is running
ollama list

# Restart Ollama
# Linux/Mac
brew services restart ollama  # or systemctl restart ollama

# Test connection
curl http://localhost:11434/api/tags
```

### OpenRouter API Issues

```bash
# Verify API key
echo $OPENROUTER_API_KEY

# Test API connection
curl -X POST https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "nvidia/nemotron-120b", "messages": [{"role": "user", "content": "Hello"}]}'
```

### Model Not Found

```bash
# Pull missing models
ollama pull gemma4:e4b
ollama pull qwen2.5:7b
ollama pull llama3.2:latest

# Create custom model if needed
python scripts/create_pitchdeck_model.py
```

## Development

### Project Structure

```
autoresearch/
├── agents/              # Agent implementations
│   ├── ceo_orchestrator_agent.py
│   ├── content_agent.py
│   ├── research_agent.py
│   ├── analyst_agent.py
│   └── design_agent.py
├── workflow/            # Workflow orchestration
│   └── agile_orchestrator.py
├── memory/              # Learning memory system
│   └── learning_memory.py
├── tests/               # Test suites
│   ├── test_ceo_agent.py
│   ├── test_content_agent.py
│   ├── test_research_agent.py
│   ├── test_analyst_agent.py
│   ├── test_design_agent.py
│   ├── test_agile_orchestrator.py
│   ├── test_learning_memory.py
│   ├── test_main_agile_network.py
│   └── test_config.py
├── config.json          # System configuration
├── main_agile_network.py # Main entry point
└── README_AGILE_NETWORK.md
```

### Adding New Agents

1. Create agent class in `agents/`
2. Follow the pattern of existing agents
3. Add unit tests in `tests/`
4. Update `config.json` with agent configuration
5. Update `main_agile_network.py` to initialize the agent

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Write docstrings for all classes and methods
- Maintain test coverage above 80%

## Performance Optimization

- **Caching**: The system uses prompt caching for the CEO agent (~97% hit rate)
- **Parallel Execution**: Research and analysis can run in parallel where appropriate
- **Model Selection**: Local models for specialized tasks reduce API costs
- **Iteration Limits**: Max 3 iterations prevent infinite loops

## Security

- API keys stored in environment variables, not in code
- No sensitive data in git repository
- Input validation on all customer requests
- Compliance checking for regulatory requirements

## License

[Specify your license here]

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Support

For issues and questions:
- Create an issue in the repository
- Check existing documentation
- Review test files for usage examples

## Acknowledgments

- **Nemotron120B** by NVIDIA via OpenRouter
- **Ollama** for local model hosting
- **Gemma4, Qwen2.5, Llama3.2** model providers
- **WUPHF** platform for agent orchestration
