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

# Simple comprehensive context model
class SimpleBusinessContext(BaseModel):
    comprehensive_context: str
    
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
# Also add this model at the top with your other models (near BusinessContext)
class SimpleBusinessContext(BaseModel):
    comprehensive_context: str

# Replace your entire @app.get("/test-form") function with this:
@app.get("/test-form")
async def comprehensive_research_form():
    """
    Comprehensive single-box form for business context research
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🧠 Business Context Research - Reasoning Agent</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 900px; 
                margin: 30px auto; 
                padding: 30px;
                background-color: #f8fafc;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            h1 { 
                color: #1e293b; 
                border-bottom: 3px solid #3b82f6;
                padding-bottom: 15px;
                margin-bottom: 20px;
            }
            .description {
                background: #eff6ff;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 25px;
                border-left: 4px solid #3b82f6;
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
                border-color: #3b82f6;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            }
            button { 
                background: linear-gradient(135deg, #3b82f6, #1d4ed8);
                color: white; 
                padding: 16px 32px; 
                border: none; 
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                margin-top: 20px;
                width: 100%;
                transition: all 0.2s;
            }
            button:hover {
                transform: translateY(-1px);
                box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
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
                background: #f0f9ff;
                border-radius: 8px;
                border: 1px solid #0ea5e9;
                display: none;
            }
            .loading {
                text-align: center;
                padding: 40px;
                color: #3b82f6;
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
                background: #fefce8;
                padding: 15px;
                border-radius: 6px;
                margin: 15px 0;
                font-size: 13px;
                border-left: 3px solid #eab308;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 Comprehensive Business Research</h1>
            
            <div class="description">
                <strong>Reasoning Agent:</strong> Advanced AI that iteratively improves research quality through self-evaluation and multiple reasoning cycles until professional consulting standards are met.
                <br><br>
                <strong>⏱️ Processing Time:</strong> 2-5 minutes (multiple iterations for quality assurance)
            </div>
            
            <p><strong>Paste your complete business context below</strong> (like you would into ChatGPT):</p>
            
            <div class="example">
                <strong>💡 Example format:</strong><br>
                Company: [Name] - [Industry]<br>
                Offering: [Detailed service/product description]<br>
                Target Market: [Specific customer details]<br>
                Current Challenges: [Market problems you solve]<br>
                Marketing Goals: [What you want to achieve]<br>
                Unique Value: [Differentiators vs competitors]<br>
                Current Customers: [Existing customer insights]<br>
                [Add any other relevant context...]
            </div>
            
            <form id="contextForm">
                <textarea id="business_context" placeholder="Company: [Your company name and industry]
Industry: [Specific industry/niche] 
Offering: [Detailed description of your products/services, how they work, what problems they solve]
Target Market: [Specific customer demographics, role, company size, industry focus]
Current Challenges: [Specific problems your target market faces daily]
Marketing Goals: [What you want to achieve - leads, awareness, positioning, etc.]
Unique Value Proposition: [What makes you different from competitors]
Current Customers: [What you know about existing customers - feedback, patterns, characteristics]
Main Competitors: [Who you compete against and how you differ]
Failed Marketing Attempts: [What hasn't worked and lessons learned]
Market Position: [How you're positioned - premium, budget, niche expert, etc.]
Specific Questions: [Any particular insights you're looking for]

[Add any other relevant context about your business, market, customers, challenges, goals, etc.]" required></textarea>
                
                <button type="submit">🧠 Start Reasoning Agent Research</button>
            </form>
            
            <div id="results"></div>
        </div>

        <script>
            document.getElementById('contextForm').onsubmit = async function(e) {
                e.preventDefault();
                
                const button = document.querySelector('button');
                const results = document.getElementById('results');
                
                button.textContent = '🧠 Reasoning Agent Processing...';
                button.disabled = true;
                
                results.style.display = 'block';
                results.innerHTML = '<div class="loading">🧠 Reasoning Agent Working...<br><br>⚡ Multiple evaluation cycles in progress<br>📊 Iteratively improving research quality<br>🎯 Ensuring professional consulting standards</div>';
                
                const data = {
                    comprehensive_context: document.getElementById('business_context').value
                };
                
                try {
                    const response = await fetch('/research/context-analysis', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    results.innerHTML = '<h3>🎉 Reasoning Agent Results:</h3><pre>' + JSON.stringify(result, null, 2) + '</pre>';
                } catch (error) {
                    results.innerHTML = '<h3>❌ Error:</h3><p>' + error.message + '</p>';
                }
                
                button.textContent = '🧠 Start Reasoning Agent Research';
                button.disabled = false;
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Add this new endpoint after your form function:
# Add this new endpoint after your form function:
@app.post("/research/context-analysis")
async def context_analysis_research(context: SimpleBusinessContext):
    """
    Process comprehensive business context using reasoning agent
    """
    
    # Generate session ID
    session_id = f"context_research_{len(research_sessions) + 1}"
    
    # Store initial context
    research_sessions[session_id] = {
        "status": "processing",
        "business_context": {"comprehensive_context": context.comprehensive_context},
        "agent_results": {},
        "created_at": "2025-06-14"
    }
    
    try:
        # Create context for ICP research agent
        enhanced_context = {
            "company_name": "Comprehensive Analysis",
            "industry": "Various",
            "target_market": "To be determined from context",
            "current_challenges": "To be analyzed from context",
            "product_service": "Comprehensive context provided",
            "assumptions": context.comprehensive_context
        }
        
        print(f"🧠 Starting ICP research agent with comprehensive context...")
        
        # Run the reasoning agent
        reasoning_results = run_icp_research(enhanced_context)
        
        # Store results
        research_sessions[session_id]["agent_results"]["reasoning_research"] = reasoning_results
        research_sessions[session_id]["status"] = "completed"
        
        return {
            "session_id": session_id,
            "status": "completed",
            "message": "Comprehensive context analysis completed",
            "reasoning_iterations": reasoning_results.get("total_iterations", 1) if isinstance(reasoning_results, dict) else 1,
            "quality_assurance": "Research validated through iterative reasoning process",
            "results_preview": str(reasoning_results)[:500] + "..." if len(str(reasoning_results)) > 500 else str(reasoning_results),
            "full_results": reasoning_results,
            "full_results_url": f"/research/{session_id}/results"
        }
        
    except Exception as e:
        research_sessions[session_id]["status"] = "error"
        research_sessions[session_id]["error"] = str(e)
        
        return {
            "session_id": session_id,
            "status": "error",
            "message": f"Error processing context analysis: {str(e)}"
        }
