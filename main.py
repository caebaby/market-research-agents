from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from typing import Dict, Any
import json

# Import our new agent
try:
    from agents.icp_intelligence_agent import run_icp_research
    AGENTS_AVAILABLE = True
except ImportError as e:
    print(f"Agent import failed: {e}")
    AGENTS_AVAILABLE = False
    
    def run_icp_research(context):
        return "Agent system loading... Please try again in a moment."

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
@app.get("/test-form")
async def test_form():
    """
    Simple HTML form to test the ICP agent
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test ICP Intelligence Agent</title>
        <style>
            body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
            input, textarea { width: 100%; padding: 10px; margin: 10px 0; }
            button { background: #007cba; color: white; padding: 15px 30px; border: none; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>🤖 Test ICP Intelligence Agent</h1>
        <form id="testForm">
            <label>Company Name:</label>
            <input type="text" id="company_name" value="Test Digital Agency" required>
            
            <label>Industry:</label>
            <input type="text" id="industry" value="Digital Marketing" required>
            
            <label>Target Market:</label>
            <input type="text" id="target_market" value="Small business owners who need help with online marketing" required>
            
            <label>Current Challenges:</label>
            <textarea id="current_challenges" rows="3" required>Struggling to generate consistent leads and convert website visitors into customers</textarea>
            
            <label>Product/Service:</label>
            <input type="text" id="product_service" value="Marketing consulting and lead generation services">
            
            <button type="submit">🚀 Run ICP Research</button>
        </form>
        
        <div id="results" style="margin-top: 30px;"></div>
        
        <script>
            document.getElementById('testForm').onsubmit = async function(e) {
                e.preventDefault();
                
                const button = document.querySelector('button');
                const results = document.getElementById('results');
                
                button.textContent = '🤖 Agent Working...';
                button.disabled = true;
                
                const data = {
                    company_name: document.getElementById('company_name').value,
                    industry: document.getElementById('industry').value,
                    target_market: document.getElementById('target_market').value,
                    current_challenges: document.getElementById('current_challenges').value,
                    product_service: document.getElementById('product_service').value,
                    assumptions: ''
                };
                
                try {
                    const response = await fetch('/research/icp-analysis', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    results.innerHTML = '<h3>Results:</h3><pre>' + JSON.stringify(result, null, 2) + '</pre>';
                } catch (error) {
                    results.innerHTML = '<h3>Error:</h3><p>' + error.message + '</p>';
                }
                
                button.textContent = '🚀 Run ICP Research';
                button.disabled = false;
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
