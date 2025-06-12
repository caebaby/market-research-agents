from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from typing import Dict, Any
import json

# Import our new agent
from agents.icp_intelligence_agent import run_icp_research

app = FastAPI(title="Market Research Agent Team", version="2.0.0")

# Business context model (enhanced)
class BusinessContext(BaseModel):
    company_name: str
    industry: str
    target_market: str
    current_challenges: str
    product_service: str = ""
    assumptions: str = ""
    
# In-memory storage for now (we'll add database later)
research_sessions = {}

@app.get("/")
async def root():
    return {
        "message": "Market Research Agent Team - Phase 2 Live! 🤖",
        "version": "2.0.0",
        "status": "ICP Intelligence Agent Ready",
        "agents": [
            "ICP Intelligence Agent ✅",
            "Competitor Intelligence Agent (Coming Soon)",
            "Interview Simulation Agent (Coming Soon)", 
            "Marketing Intelligence Synthesizer (Coming Soon)"
        ]
    }

@app.post("/research/icp-analysis")
async def start_icp_research(context: BusinessContext):
    """
    Start ICP research using our AI agent
    """
    
    # Generate session ID
    session_id = f"icp_research_{len(research_sessions) + 1}"
    
    # Store initial context
    research_sessions[session_id] = {
        "status": "processing",
        "business_context": context.dict(),
        "agent_results": {},
        "created_at": "2025-06-12"
    }
    
    try:
        # Run the ICP Intelligence Agent
        print(f"🤖 Starting ICP research for {context.company_name}...")
        
        # Convert to dict for agent
        business_dict = context.dict()
        
        # Run the agent (this will take 30-60 seconds)
        icp_results = run_icp_research(business_dict)
        
        # Store results
        research_sessions[session_id]["agent_results"]["icp_intelligence"] = str(icp_results)
        research_sessions[session_id]["status"] = "completed"
        
        return {
            "session_id": session_id,
            "status": "completed",
            "message": f"ICP research completed for {context.company_name}",
            "results_preview": str(icp_results)[:500] + "...",
            "full_results_url": f"/research/{session_id}/results"
        }
        
    except Exception as e:
        # Handle errors gracefully
        research_sessions[session_id]["status"] = "error"
        research_sessions[session_id]["error"] = str(e)
        
        return {
            "session_id": session_id,
            "status": "error",
            "message": f"Error processing research: {str(e)}"
        }

@app.get("/research/{session_id}/results")
async def get_research_results(session_id: str):
    """
    Get the full research results
    """
    if session_id not in research_sessions:
        raise HTTPException(status_code=404, detail="Research session not found")
    
    session = research_sessions[session_id]
    
    return {
        "session_id": session_id,
        "status": session["status"],
        "business_context": session["business_context"],
        "agent_results": session.get("agent_results", {}),
        "created_at": session["created_at"]
    }

# Health check for deployment
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "market-research-agents", "phase": "2"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
