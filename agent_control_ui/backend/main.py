"""FastAPI Backend for Agent Control UI"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import json
import asyncio
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

print(f"Project root: {project_root}")
print(f"Python path: {sys.path[:3]}")

from main_agile_network import WUPHFAgileNetwork
from workflow.agile_orchestrator import WorkflowState, WorkflowPhase

app = FastAPI(title="Agent Control UI")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
agent_network: Optional[WUPHFAgileNetwork] = None
active_connections: List[WebSocket] = []
agent_messages: List[Dict[str, Any]] = []
agent_states: Dict[str, Dict[str, Any]] = {}


class ChatMessage(BaseModel):
    """Chat message model"""
    agent: str
    message: str
    timestamp: Optional[str] = None


class AgentTask(BaseModel):
    """Agent task model"""
    agent: str
    task: str
    parameters: Dict[str, Any] = {}


class WorkflowRequest(BaseModel):
    """Workflow request model"""
    customer_request: Dict[str, Any]
    quality_threshold: float = 0.8


# Initialize agent network
@app.on_event("startup")
async def startup_event():
    """Initialize agent network on startup"""
    global agent_network
    try:
        agent_network = WUPHFAgileNetwork(config_path="config.json")
        print("Agent network initialized successfully")
        
        # Initialize agent states
        agent_states = {
            "ceo": {"status": "idle", "current_task": None, "last_activity": None},
            "content": {"status": "idle", "current_task": None, "last_activity": None},
            "research": {"status": "idle", "current_task": None, "last_activity": None},
            "analyst": {"status": "idle", "current_task": None, "last_activity": None},
            "design": {"status": "idle", "current_task": None, "last_activity": None}
        }
    except Exception as e:
        print(f"Failed to initialize agent network: {e}")


@app.get("/")
async def get_root():
    """Serve the frontend"""
    with open("agent_control_ui/frontend/index.html", "r") as f:
        return HTMLResponse(content=f.read())


@app.get("/api/agents")
async def get_agents():
    """Get list of available agents"""
    if not agent_network:
        return {"error": "Agent network not initialized"}
    
    return {
        "agents": [
            {
                "id": "ceo",
                "name": "CEO/Orchestrator",
                "model": "Nemotron120B",
                "role": "Strategic leadership and task delegation"
            },
            {
                "id": "content",
                "name": "Content Agent",
                "model": "pitchdeck-2026:latest",
                "role": "Pitch deck creation with 2026 best practices"
            },
            {
                "id": "research",
                "name": "Research Agent",
                "model": "qwen2.5:7b",
                "role": "Market research and competitive analysis"
            },
            {
                "id": "analyst",
                "name": "Analyst Agent",
                "model": "gemma4:e4b",
                "role": "Quality assurance and data analysis"
            },
            {
                "id": "design",
                "name": "Design Agent",
                "model": "llama3.2:latest",
                "role": "Visual design and PDF generation"
            }
        ]
    }


@app.get("/api/agents/{agent_id}/state")
async def get_agent_state(agent_id: str):
    """Get current state of a specific agent"""
    if agent_id not in agent_states:
        return {"error": "Agent not found"}
    
    return agent_states[agent_id]


@app.get("/api/workflow/status")
async def get_workflow_status():
    """Get current workflow status"""
    if not agent_network:
        return {"error": "Agent network not initialized"}
    
    status = agent_network.get_network_status()
    return status


@app.post("/api/workflow/start")
async def start_workflow(request: WorkflowRequest):
    """Start a new workflow"""
    if not agent_network:
        return {"error": "Agent network not initialized"}
    
    try:
        # Update agent states to working
        for agent_id in agent_states:
            agent_states[agent_id]["status"] = "initializing"
            agent_states[agent_id]["last_activity"] = datetime.now().isoformat()
        
        # Broadcast state update
        await broadcast_update({
            "type": "workflow_starting",
            "agents": agent_states
        })
        
        # Process request (this would normally be async)
        result = agent_network.process_customer_request(
            request.customer_request,
            request.quality_threshold
        )
        
        # Update agent states
        for agent_id in agent_states:
            agent_states[agent_id]["status"] = "idle"
            agent_states[agent_id]["last_activity"] = datetime.now().isoformat()
        
        # Broadcast completion
        await broadcast_update({
            "type": "workflow_completed",
            "result": result,
            "agents": agent_states
        })
        
        return result
        
    except Exception as e:
        # Update agent states to error
        for agent_id in agent_states:
            agent_states[agent_id]["status"] = "error"
        
        await broadcast_update({
            "type": "workflow_error",
            "error": str(e),
            "agents": agent_states
        })
        
        return {"error": str(e)}


@app.post("/api/chat")
async def send_chat_message(message: ChatMessage):
    """Send a chat message to an agent"""
    if not agent_network:
        return {"error": "Agent network not initialized"}
    
    # Store message
    chat_entry = {
        "type": "chat",
        "agent": message.agent,
        "message": message.message,
        "timestamp": message.timestamp or datetime.now().isoformat(),
        "direction": "user_to_agent"
    }
    agent_messages.append(chat_entry)
    
    # Update agent state
    if message.agent in agent_states:
        agent_states[message.agent]["status"] = "processing"
        agent_states[message.agent]["current_task"] = f"Chat: {message.message[:50]}..."
        agent_states[message.agent]["last_activity"] = datetime.now().isoformat()
    
    # Broadcast message
    await broadcast_update(chat_entry)
    
    # Simulate agent response (in real implementation, this would call the agent)
    await asyncio.sleep(1)  # Simulate processing time
    
    response = {
        "type": "chat",
        "agent": message.agent,
        "message": f"Received: {message.message}. Processing...",
        "timestamp": datetime.now().isoformat(),
        "direction": "agent_to_user"
    }
    agent_messages.append(response)
    
    # Update agent state back to idle
    if message.agent in agent_states:
        agent_states[message.agent]["status"] = "idle"
        agent_states[message.agent]["current_task"] = None
        agent_states[message.agent]["last_activity"] = datetime.now().isoformat()
    
    await broadcast_update(response)
    
    return {"status": "sent", "response": response}


@app.get("/api/messages")
async def get_messages():
    """Get all chat messages"""
    return {"messages": agent_messages}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        # Send initial state
        await websocket.send_json({
            "type": "initial_state",
            "agents": agent_states,
            "messages": agent_messages[-10:]  # Last 10 messages
        })
        
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)


async def broadcast_update(message: Dict[str, Any]):
    """Broadcast update to all connected clients"""
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except:
            pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
