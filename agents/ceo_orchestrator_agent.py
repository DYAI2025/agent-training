"""
CEO/Orchestrator Agent for WUPHF Agile Agent Network.

This is the strategic leader agent that uses Nemotron120B via OpenRouter API.
It handles customer request analysis, task delegation to specialized agents,
True North QA evaluation, and learning integration.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import requests
import uuid
import re
from datetime import datetime


@dataclass
class Task:
    """
    Task dataclass for tracking work items in the agent network.
    
    Attributes:
        id: Unique identifier for the task
        description: Detailed description of the task
        assigned_agent: The agent responsible for executing the task
        priority: Task priority level (high, medium, low)
        status: Current status of the task (pending, in_progress, completed, failed)
        result: The result or output from task execution
        true_north_score: QA score based on True North compliance (0-100)
    """
    id: str
    description: str
    assigned_agent: str
    priority: str
    status: str
    result: Optional[str] = None
    true_north_score: Optional[float] = None


class CEOOrchestratorAgent:
    """
    CEO/Orchestrator Agent - Strategic leader for the WUPHF Agile Agent Network.
    
    This agent uses Nemotron120B via OpenRouter API to:
    - Analyze customer requests strategically
    - Delegate tasks to specialized agents
    - Evaluate True North compliance for QA
    - Integrate learning from task patterns
    """
    
    def __init__(
        self,
        openrouter_api_key: str,
        model: str = "nvidia/nemotron-120b",
        temperature: float = 0.3,
        max_tokens: int = 1000,
        api_url: str = "https://openrouter.ai/api/v1/chat/completions"
    ):
        """
        Initialize the CEO Orchestrator Agent.
        
        Args:
            openrouter_api_key: API key for OpenRouter
            model: Model identifier (default: nvidia/nemotron-120b)
            temperature: Sampling temperature for LLM (default: 0.3)
            max_tokens: Maximum tokens in response (default: 1000)
            api_url: OpenRouter API endpoint URL
        """
        self.openrouter_api_key = openrouter_api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_url = api_url
    
    def analyze_customer_request(
        self,
        request: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze customer request strategically using Nemotron120B.
        
        Args:
            request: The customer's request or problem statement
            context: Additional context about the request (optional)
        
        Returns:
            Dictionary containing strategic plan with:
            - strategic_plan: Overall approach
            - required_agents: List of specialized agents needed
            - timeline: Estimated timeline
            - priority: Recommended priority level
        """
        prompt = f"""You are the CEO of an AI agent network. Analyze this customer request strategically.

Customer Request: {request}
"""
        if context:
            prompt += f"\nAdditional Context: {context}\n"
        
        prompt += """
Provide a strategic analysis in the following format:
Strategic Plan:
- Primary goal: [description]
- Required agents: [agent1, agent2, ...]
- Timeline: [estimate]
- Priority: [high/medium/low]
"""
        
        response = self._call_openrouter(prompt)
        strategic_plan = self._parse_strategic_plan(response)
        
        return strategic_plan
    
    def delegate_task(
        self,
        description: str,
        assigned_agent: str,
        priority: str = "medium",
        task_id: Optional[str] = None
    ) -> Task:
        """
        Delegate a task to a specialized agent.
        
        Args:
            description: Task description
            assigned_agent: The agent to assign the task to
            priority: Task priority (high, medium, low)
            task_id: Optional custom task ID
        
        Returns:
            Task object with delegation details
        """
        if task_id is None:
            task_id = f"task-{uuid.uuid4().hex[:8]}"
        
        task = Task(
            id=task_id,
            description=description,
            assigned_agent=assigned_agent,
            priority=priority,
            status="pending"
        )
        
        return task
    
    def evaluate_true_north_compliance(
        self,
        task_result: str,
        task_description: str
    ) -> Dict[str, Any]:
        """
        Evaluate task result against True North principles for QA.
        
        Args:
            task_result: The result produced by the task
            task_description: Original task description
        
        Returns:
            Dictionary containing:
            - score: Compliance score (0-100)
            - analysis: Detailed analysis of compliance
        """
        prompt = f"""You are a Quality Assurance evaluator. Evaluate this task result against True North principles.

Task Description: {task_description}
Task Result: {task_result}

True North Principles:
- Alignment with mission and values
- Customer value creation
- Quality and excellence
- Innovation and continuous improvement

Provide evaluation in the following format:
True North Score: [0-100]
Analysis:
- [key point 1]
- [key point 2]
- [key point 3]
"""
        
        response = self._call_openrouter(prompt)
        score = self._parse_true_north_score(response)
        
        return {
            "score": score,
            "analysis": response,
            "timestamp": self._get_timestamp()
        }
    
    def integrate_learning(
        self,
        task_history: List[Task]
    ) -> Dict[str, Any]:
        """
        Integrate learning from task history for pattern recognition.
        
        Args:
            task_history: List of completed tasks for analysis
        
        Returns:
            Dictionary containing:
            - pattern: Identified pattern
            - recommendation: Actionable recommendation
        """
        if not task_history:
            return {
                "pattern": "No pattern",
                "recommendation": "Collect more task data",
                "timestamp": self._get_timestamp()
            }
        
        # Format task history for the prompt
        history_text = "\n".join([
            f"Task {task.id}: {task.description} | Agent: {task.assigned_agent} | "
            f"Priority: {task.priority} | Status: {task.status} | "
            f"True North Score: {task.true_north_score}"
            for task in task_history
        ])
        
        prompt = f"""You are a learning system. Analyze this task history to identify patterns.

Task History:
{history_text}

Identify patterns in:
- Agent performance
- Task completion rates
- True North compliance trends
- Priority vs. outcome relationships

Provide analysis in the following format:
Pattern Identified:
- Type: [pattern type]
- Context: [context description]
- Recommendation: [actionable recommendation]
"""
        
        response = self._call_openrouter(prompt)
        pattern = self._extract_pattern(response)
        
        return {
            "pattern": pattern,
            "recommendation": pattern.get("recommendation", ""),
            "timestamp": self._get_timestamp()
        }
    
    def _call_openrouter(self, prompt: str) -> str:
        """
        Private method to call OpenRouter API.
        
        Args:
            prompt: The prompt to send to the LLM
        
        Returns:
            The LLM response text
        
        Raises:
            Exception: If API call fails
        """
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://wuphf.ai",
            "X-Title": "WUPHF CEO Agent"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        response = requests.post(
            self.api_url,
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(
                f"OpenRouter API call failed with status {response.status_code}: "
                f"{response.text}"
            )
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    def _parse_strategic_plan(self, response: str) -> Dict[str, Any]:
        """
        Private method to parse strategic plan from LLM response.
        
        Args:
            response: Raw LLM response
        
        Returns:
            Parsed strategic plan dictionary
        """
        strategic_plan = {
            "primary_goal": "",
            "required_agents": [],
            "timeline": "",
            "priority": "medium"
        }
        
        # Extract primary goal
        goal_match = re.search(r"Primary goal:\s*(.+)", response, re.IGNORECASE)
        if goal_match:
            strategic_plan["primary_goal"] = goal_match.group(1).strip()
        
        # Extract required agents
        agents_match = re.search(r"Required agents:\s*(.+)", response, re.IGNORECASE)
        if agents_match:
            agents_text = agents_match.group(1).strip()
            # Parse comma-separated or bracketed list
            agents_text = agents_text.strip("[]")
            strategic_plan["required_agents"] = [
                a.strip() for a in agents_text.split(",")
            ]
        
        # Extract timeline
        timeline_match = re.search(r"Timeline:\s*(.+)", response, re.IGNORECASE)
        if timeline_match:
            strategic_plan["timeline"] = timeline_match.group(1).strip()
        
        # Extract priority
        priority_match = re.search(r"Priority:\s*(.+)", response, re.IGNORECASE)
        if priority_match:
            strategic_plan["priority"] = priority_match.group(1).strip().lower()
        
        return strategic_plan
    
    def _parse_true_north_score(self, response: str) -> float:
        """
        Private method to parse True North score from LLM response.
        
        Args:
            response: Raw LLM response
        
        Returns:
            True North score as float (0-100)
        """
        score_match = re.search(r"True North Score:\s*(\d+)", response, re.IGNORECASE)
        if score_match:
            return float(score_match.group(1))
        return 0.0
    
    def _extract_pattern(self, response: str) -> Dict[str, str]:
        """
        Private method to extract pattern from LLM response.
        
        Args:
            response: Raw LLM response
        
        Returns:
            Pattern dictionary with type, context, and recommendation
        """
        pattern = {
            "type": "",
            "context": "",
            "recommendation": ""
        }
        
        # Extract pattern type
        type_match = re.search(r"Type:\s*(.+)", response, re.IGNORECASE)
        if type_match:
            pattern["type"] = type_match.group(1).strip()
        
        # Extract context
        context_match = re.search(r"Context:\s*(.+)", response, re.IGNORECASE)
        if context_match:
            pattern["context"] = context_match.group(1).strip()
        
        # Extract recommendation
        rec_match = re.search(r"Recommendation:\s*(.+)", response, re.IGNORECASE)
        if rec_match:
            pattern["recommendation"] = rec_match.group(1).strip()
        
        return pattern
    
    def _get_timestamp(self) -> str:
        """
        Private method to get current timestamp.
        
        Returns:
            ISO format timestamp string
        """
        return datetime.now().isoformat()
