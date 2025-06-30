from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from typing import Dict, Any
import json
from dotenv import load_dotenv
# from agents.avatar_agnostic_coordinator import run_avatar_agnostic_research

# Load environment variables
load_dotenv()

# CrewAI imports (Gemini's approach)
from crewai import Crew, Process, Task
from crewai_tools import SerperDevTool

# Agent imports - we'll handle different structures
AGENTS_AVAILABLE = False
icp_agent = None
interview_agent = None 
marketing_agent = None

# Try to import agents with multiple fallback approaches
try:
    # Try Gemini's expected structure first
    from agents.icp_intelligence_agent import ICPIntelligenceAgent
    from agents.dynamic_interview_agent import DynamicInterviewAgent  
    from agents.marketing_intelligence_synthesizer import MarketingIntelligenceSynthesizer
    
    # Initialize search tool
    search_tool = SerperDevTool()
    
    # Create agent instances (Gemini style)
    icp_agent = ICPIntelligenceAgent().agent()
    interview_agent = DynamicInterviewAgent().agent()
    marketing_agent = MarketingIntelligenceSynthesizer().agent()
    
    AGENTS_AVAILABLE = True
    print("✅ Successfully imported Gemini-style agents")
    
except ImportError as e1:
    try:
        # Try your original structure
        from agents.icp_intelligence_agent import ReasoningICPAgent
        from agents.interview_agent import InterviewAgent  # Guess at name
        from agents.marketing_synthesis_agent import MarketingAgent  # Guess at name
        
        search_tool = SerperDevTool()
        
        # Create agent instances (your style)
        icp_instance = ReasoningICPAgent()
        icp_agent = icp_instance.create_research_agent()
        
        # We'll handle these if they exist
        try:
            interview_instance = InterviewAgent()
            interview_agent = interview_instance.create_interview_agent()
        except:
            interview_agent = None
            
        try:
            marketing_instance = MarketingAgent()
            marketing_agent = marketing_instance.create_marketing_agent()
        except:
            marketing_agent = None
            
        AGENTS_AVAILABLE = True
        print("✅ Successfully imported your original-style agents")
        
    except ImportError as e2:
        print(f"❌ Agent import failed: {e1}, {e2}")
        AGENTS_AVAILABLE = False

app = FastAPI(title="Market Research Agent Team - HYBRID POWER", version="3.0.0")

# Data Models
class SimpleBusinessContext(BaseModel):
    comprehensive_context: str

# In-memory storage for research sessions
research_sessions = {}

@app.get("/")
async def root():
    return {
        "message": "Market Research Agent Team - HYBRID POWER! 🚀",
        "version": "3.0.0",
        "status": "Gemini Coordination + FastAPI Power",
        "agents_available": AGENTS_AVAILABLE,
        "coordination": "CrewAI Sequential Processing",
        "agents": [
            "ICP Intelligence Agent ✅" if icp_agent else "ICP Intelligence Agent ❌",
            "Interview Agent ✅" if interview_agent else "Interview Agent ❌", 
            "Marketing Synthesis Agent ✅" if marketing_agent else "Marketing Synthesis Agent ❌"
        ]
    }

@app.get("/test-form")
async def comprehensive_research_form():
    """
    Hybrid form for comprehensive business context research
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚀 HYBRID POWER - Market Research Agents</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 900px; 
                margin: 30px auto; 
                padding: 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            }
            h1 { 
                color: #1e293b; 
                border-bottom: 3px solid #667eea;
                padding-bottom: 15px;
                margin-bottom: 20px;
            }
            .power-badge {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 10px 20px;
                border-radius: 25px;
                font-weight: bold;
                display: inline-block;
                margin-bottom: 20px;
            }
            .description {
                background: linear-gradient(135deg, #e0f2fe, #f3e5f5);
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 25px;
                border-left: 4px solid #667eea;
            }
            textarea { 
                width: 100%; 
                height: 450px; 
                padding: 20px; 
                font-size: 14px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                font-family: 'SF Mono', Monaco, monospace;
                line-height: 1.5;
                resize: vertical;
                box-sizing: border-box;
            }
            textarea:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            button { 
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white; 
                padding: 16px 32px; 
                border: none; 
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                margin-top: 20px;
                width: 100%;
                transition: all 0.3s;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
            }
            button:disabled {
                background: #9ca3af;
                transform: none;
                box-shadow: none;
                cursor: not-allowed;
            }
            #results {
                margin-top: 30px;
                padding: 25px;
                background: linear-gradient(135deg, #f0f9ff, #fdf4ff);
                border-radius: 8px;
                border: 1px solid #667eea;
                display: none;
            }
            .loading {
                text-align: center;
                padding: 40px;
                color: #667eea;
                font-weight: 600;
            }
            pre {
                white-space: pre-wrap;
                font-size: 13px;
                max-height: 500px;
                overflow-y: auto;
                background: white;
                padding: 15px;
                border-radius: 6px;
                border: 1px solid #e5e7eb;
            }
            .example {
                background: linear-gradient(135deg, #fefce8, #fdf2f8);
                padding: 15px;
                border-radius: 6px;
                margin: 15px 0;
                font-size: 13px;
                border-left: 3px solid #667eea;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 HYBRID POWER Market Research</h1>
            
            <div class="power-badge">
                Gemini Coordination + Claude Intelligence + Your Production System
            </div>
            
            <div class="description">
                <strong>🔥 HYBRID SYSTEM:</strong> Combines Gemini's perfect agent coordination with Claude's comprehensive research depth and your production FastAPI infrastructure.
                <br><br>
                <strong>⚡ 3-Agent Pipeline:</strong> ICP Intelligence → Interview Simulation → Marketing Synthesis
                <br>
                <strong>⏱️ Processing Time:</strong> 3-7 minutes (full professional analysis)
            </div>
            
            <p><strong>Paste your complete business context below:</strong></p>
            
            <div class="example">
                <strong>💡 Example format:</strong><br>
                Company: [Name] - [Industry]<br>
                Offering: [Detailed service/product description]<br>
                Target Market: [Specific customer details]<br>
                Current Challenges: [Market problems you solve]<br>
                Marketing Goals: [What you want to achieve]<br>
                Unique Value: [Differentiators vs competitors]<br>
                [Add any other relevant context...]
            </div>
            
            <form id="contextForm">
                <textarea id="business_context" placeholder="Company: [Your company name and industry]
Industry: [Specific industry/niche] 
Offering: [Detailed description of your products/services]
Target Market: [Specific customer demographics and characteristics]
Current Challenges: [Problems your target market faces]
Marketing Goals: [What you want to achieve]
Unique Value Proposition: [What makes you different]
Current Customers: [What you know about existing customers]
Competitors: [Who you compete against]
Specific Questions: [Any particular insights you're looking for]

[Add any other relevant context about your business, market, customers, etc.]" required></textarea>
                
                <button type="submit">🚀 Launch HYBRID Analysis</button>
            </form>
            
            <div id="results"></div>
        </div>

        <script>
            document.getElementById('contextForm').onsubmit = async function(e) {
                e.preventDefault();
                
                const button = document.querySelector('button');
                const results = document.getElementById('results');
                
                button.textContent = '🚀 HYBRID Agents Processing...';
                button.disabled = true;
                
                results.style.display = 'block';
                results.innerHTML = '<div class="loading">🚀 HYBRID POWER ENGAGED...<br><br>⚡ ICP Intelligence Agent analyzing...<br>🎤 Interview Agent preparing...<br>🎯 Marketing Synthesizer standing by...<br><br>🔥 Professional-grade analysis in progress!</div>';
                
                const data = {
                    comprehensive_context: document.getElementById('business_context').value
                };
                
                try {
                    const response = await fetch('/research/hybrid-analysis', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    
                    if (result.status === 'completed') {
                        results.innerHTML = '<h3>🎉 HYBRID Analysis Complete!</h3><pre>' + JSON.stringify(result, null, 2) + '</pre>';
                    } else {
                        results.innerHTML = '<h3>⚡ Processing Status:</h3><pre>' + JSON.stringify(result, null, 2) + '</pre>';
                    }
                } catch (error) {
                    results.innerHTML = '<h3>❌ Error:</h3><p>' + error.message + '</p>';
                }
                
                button.textContent = '🚀 Launch HYBRID Analysis';
                button.disabled = false;
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/research/hybrid-analysis")
async def hybrid_analysis_research(context: SimpleBusinessContext):
    """
    CONTEXT-DRIVEN AI RESEARCH: Smart agents that adapt to any business context
    """
    
    # Generate session ID
    session_id = f"context_driven_{len(research_sessions) + 1}"
    
    # Store initial context
    research_sessions[session_id] = {
        "status": "processing",
        "business_context": {"comprehensive_context": context.comprehensive_context},
        "agent_results": {},
        "approach": "context_driven_smart_agents",
        "created_at": "2025-06-28"
    }
    
    try:
        print(f"🧠 Starting Context-Driven Research with Smart Agent Coordination...")
        
        # Run the context-driven coordinator
        # research_results = run_avatar_agnostic_research(context.comprehensive_context)
        research_results = {"success": False, "error": "Coordinator temporarily disabled for testing"}
        
        # Store results
        research_sessions[session_id]["agent_results"]["context_driven_research"] = research_results
        
        if research_results["success"]:
            research_sessions[session_id]["status"] = "completed"
            
            return {
                "session_id": session_id,
                "status": "completed",
                "message": "Context-driven research completed - agents adapted to business context",
                "approach": "smart_agents_pure_context",
                "crew_execution": research_results["crew_execution"],
                "tasks_completed": research_results["processing_summary"]["tasks_completed"],
                "results_preview": research_results["results"][:500] + "..." if len(research_results["results"]) > 500 else research_results["results"],
                "full_results": research_results,
                "full_results_url": f"/research/{session_id}/results"
            }
        else:
            research_sessions[session_id]["status"] = "error"
            return {
                "session_id": session_id,
                "status": "error", 
                "message": "Smart agent coordination encountered errors",
                "error_details": research_results.get("error", "Unknown error"),
                "troubleshooting": "Check CrewAI setup and agent configurations"
            }
        
    except Exception as e:
        research_sessions[session_id]["status"] = "error"
        research_sessions[session_id]["error"] = str(e)
        
        return {
            "session_id": session_id,
            "status": "error",
            "message": f"Error in context-driven research: {str(e)}",
            "troubleshooting": "Check import paths and CrewAI dependencies"
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
        "approach": session.get("approach", "unknown"),
        "created_at": session["created_at"]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "hybrid-market-research-agents", 
        "version": "3.0.0",
        "coordination": "gemini_crewai",
        "agents_available": AGENTS_AVAILABLE
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
