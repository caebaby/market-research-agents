from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from typing import Dict, Any
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Agent imports - simplified approach
AGENTS_AVAILABLE = False
agent_function = None

# Try to import the working function from your ICP agent
try:
    from agents.icp_intelligence_agent import run_reasoning_icp_research
    agent_function = run_reasoning_icp_research
    AGENTS_AVAILABLE = True
    print("✅ Successfully imported run_reasoning_icp_research")
except ImportError:
    try:
        from agents.icp_intelligence_agent import reasoning_agent_call
        agent_function = reasoning_agent_call
        AGENTS_AVAILABLE = True
        print("✅ Successfully imported reasoning_agent_call")
    except ImportError as e:
        print(f"❌ Agent import failed: {e}")
        AGENTS_AVAILABLE = False
        
        def agent_function(context):
            return {
                "error": "Agent system not available",
                "message": "Please check agent imports",
                "context_received": True
            }

app = FastAPI(title="Market Research Agent Team", version="3.0.0")

# Data Models
class SimpleBusinessContext(BaseModel):
    comprehensive_context: str

# In-memory storage for research sessions
research_sessions = {}

@app.get("/")
async def root():
    return {
        "message": "Market Research Agent Team - Live! 🚀",
        "version": "3.0.0",
        "research_form": "/research",
        "status": "Multi-Agent System Ready" if AGENTS_AVAILABLE else "Agent System Loading",
        "agents_available": AGENTS_AVAILABLE
    }

@app.get("/research")
async def main_research_form():
    """
    Main ICP Research Intelligence Form
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🧠 ICP Research Intelligence - Structured Input</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1000px; 
                margin: 20px auto; 
                padding: 20px;
                background-color: #f0f4f8;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 16px;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            }
            h1 { 
                color: #0f172a; 
                font-size: 2.5em;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .subtitle {
                color: #64748b;
                font-size: 1.1em;
                margin-bottom: 30px;
                line-height: 1.6;
            }
            .form-section {
                margin-bottom: 30px;
                border-bottom: 1px solid #e5e7eb;
                padding-bottom: 25px;
            }
            .form-section:last-of-type {
                border-bottom: none;
            }
            .section-title {
                font-size: 1.3em;
                color: #1e293b;
                margin-bottom: 15px;
                font-weight: 600;
            }
            label {
                display: block;
                color: #475569;
                font-weight: 500;
                margin-bottom: 8px;
                font-size: 0.95em;
            }
            .required::after {
                content: " *";
                color: #ef4444;
            }
            input[type="text"], textarea, select {
                width: 100%;
                padding: 12px 16px;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                font-size: 15px;
                transition: all 0.2s;
                box-sizing: border-box;
            }
            input[type="text"]:focus, textarea:focus, select:focus {
                outline: none;
                border-color: #3b82f6;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            }
            textarea {
                resize: vertical;
                min-height: 120px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.5;
            }
            .radio-group {
                display: flex;
                gap: 20px;
                margin-bottom: 10px;
            }
            .radio-option {
                display: flex;
                align-items: center;
                gap: 8px;
            }
            input[type="radio"] {
                width: 18px;
                height: 18px;
                accent-color: #3b82f6;
            }
            .help-text {
                color: #6b7280;
                font-size: 0.875em;
                margin-top: 5px;
                font-style: italic;
            }
            .example-text {
                color: #059669;
                font-size: 0.85em;
                margin-top: 5px;
                background-color: #ecfdf5;
                padding: 8px 12px;
                border-radius: 6px;
                border-left: 3px solid #10b981;
            }
            button {
                background: linear-gradient(135deg, #3b82f6, #1d4ed8);
                color: white;
                padding: 16px 40px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 18px;
                font-weight: 600;
                margin-top: 20px;
                width: 100%;
                transition: all 0.2s;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 24px rgba(59, 130, 246, 0.3);
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
            .progress-indicator {
                background: #eff6ff;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
                border: 1px solid #3b82f6;
            }
            .validation-error {
                color: #dc2626;
                font-size: 0.875em;
                margin-top: 5px;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 ICP Research Intelligence System</h1>
            <div class="subtitle">
                Complete all fields to activate our multi-agent research team. They'll conduct deep market analysis, 
                simulate customer interviews, and deliver professional-grade GTM strategy insights.
            </div>

            <div class="progress-indicator">
                <strong>What happens next:</strong> Your input triggers our AI agent team to conduct weeks worth of research in minutes, 
                including simulated customer interviews and competitive analysis.
            </div>

            <form id="icpResearchForm">
                <!-- Section 1: Business Type -->
                <div class="form-section">
                    <div class="section-title">1. Business Model</div>
                    <label class="required">Business Type</label>
                    <div class="radio-group">
                        <div class="radio-option">
                            <input type="radio" id="b2b" name="business_type" value="B2B" required>
                            <label for="b2b">B2B</label>
                        </div>
                        <div class="radio-option">
                            <input type="radio" id="b2c" name="business_type" value="B2C" required>
                            <label for="b2c">B2C</label>
                        </div>
                        <div class="radio-option">
                            <input type="radio" id="b2b2c" name="business_type" value="B2B2C" required>
                            <label for="b2b2c">B2B2C</label>
                        </div>
                    </div>
                </div>

                <!-- Section 2: Company Information -->
                <div class="form-section">
                    <div class="section-title">2. Company Information</div>
                    
                    <label for="company_name" class="required">Company Name</label>
                    <input type="text" id="company_name" name="company_name" required>
                    
                    <label for="industry" class="required">Industry (Be Specific)</label>
                    <input type="text" id="industry" name="industry" placeholder="e.g., Financial Services - Independent Financial Advisors" required>
                    <div class="example-text">Example: "SaaS - Project Management for Creative Agencies"</div>
                </div>

                <!-- Section 3: Product/Service -->
                <div class="form-section">
                    <div class="section-title">3. Your Offering</div>
                    
                    <label for="product_service" class="required">Product/Service Description</label>
                    <textarea id="product_service" name="product_service" rows="6" required placeholder="Describe what you offer and HOW it works. Include your unique methodology if applicable.

Example structure:
- Component 1: [What it does and why it matters]
- Component 2: [What it does and why it matters]
- etc."></textarea>
                    <div class="help-text">Be detailed - this drives the quality of insights</div>
                </div>

                <!-- Section 4: Target Customer -->
                <div class="form-section">
                    <div class="section-title">4. Target Customer Profile</div>
                    
                    <label for="target_description" class="required">Target Customer Description (One Sentence)</label>
                    <input type="text" id="target_description" name="target_description" 
                           placeholder="e.g., Mid-career financial advisors with 5-10 years experience who are stuck and frustrated with current practice growth" required>
                    
                    <label for="demographics" class="required">Demographics & Characteristics</label>
                    <textarea id="demographics" name="demographics" rows="8" required placeholder="- Age: [Range]
- Gender: [If relevant]
- Education: [Level]
- Income: [Current range]
- Company size: [For B2B]
- Location: [Geographic focus]
- Career stage: [Experience level]
- Other relevant traits: [Industry-specific]"></textarea>
                </div>

                <!-- Section 5: Customer Context -->
                <div class="form-section">
                    <div class="section-title">5. Customer Reality</div>
                    
                    <label for="customer_context" class="required">Customer Context/Situation</label>
                    <textarea id="customer_context" name="customer_context" rows="4" required 
                              placeholder="Describe their day-to-day reality, responsibilities, and pressures"></textarea>
                    <div class="example-text">Example: "Managing financial advisory practices with client relationship responsibilities, compliance requirements, and commission-based income structures..."</div>
                </div>

                <!-- Section 6: Problems & Pain Points -->
                <div class="form-section">
                    <div class="section-title">6. Problems Your Offering Solves</div>
                    
                    <label for="problems_solved" class="required">List 5-7 Specific Problems (Most Painful First)</label>
                    <textarea id="problems_solved" name="problems_solved" rows="8" required placeholder="1. [Most urgent/painful problem]
2. [Second most painful]
3. [Third problem]
4. [Fourth problem]
5. [Fifth problem]

Be specific - not 'lack of growth' but 'commission income volatility creating financial stress'"></textarea>
                </div>

                <!-- Section 7: Voice of Customer -->
                <div class="form-section">
                    <div class="section-title">7. Voice of Customer</div>
                    
                    <label for="customer_complaints" class="required">Customer Complaints (7-10 Exact Quotes)</label>
                    <textarea id="customer_complaints" name="customer_complaints" rows="10" required placeholder='- "Quote 1 expressing frustration"
- "Quote 2 about their pain"
- "Quote 3 showing emotion"
- "Quote 4 about challenges"
- "Quote 5 about obstacles"

These should sound like real people talking, not marketing speak'></textarea>
                    
                    <label for="stated_goals" class="required">Customer's Stated Goals (In Their Words)</label>
                    <textarea id="stated_goals" name="stated_goals" rows="6" required placeholder="- Goal 1 (in their words)
- Goal 2
- Goal 3
- Goal 4
- Goal 5"></textarea>
                    
                    <label for="success_vision" class="required">What Success Looks Like (Customer Quotes)</label>
                    <textarea id="success_vision" name="success_vision" rows="6" required placeholder='"Success quote 1"
"Success quote 2"
"Success quote 3"
"Success quote 4"
"Success quote 5"'></textarea>
                </div>

                <!-- Section 8: Market Details -->
                <div class="form-section">
                    <div class="section-title">8. Market Segmentation</div>
                    
                    <label for="market_details" class="required">Target Market Details</label>
                    <textarea id="market_details" name="market_details" rows="6" required placeholder="- Primary segment: [Description]
- Company characteristics: [For B2B]
- Current situation: [What stage/state they're in]
- Aspirational direction: [Where they want to go]"></textarea>
                </div>

                <!-- Section 9: Marketing Goal -->
                <div class="form-section">
                    <div class="section-title">9. Your Marketing Objective</div>
                    
                    <label for="marketing_goal" class="required">Marketing Goal (Specific Action)</label>
                    <textarea id="marketing_goal" name="marketing_goal" rows="3" required 
                              placeholder="What specific action do you want them to take?"></textarea>
                    <div class="example-text">Example: "Generate qualified leads for discovery calls with financial advisors who are frustrated with commission volatility and want predictable revenue"</div>
                </div>

                <!-- Section 10: Additional Context -->
                <div class="form-section">
                    <div class="section-title">10. Additional Context</div>
                    
                    <label for="additional_context">Company Story & Differentiators</label>
                    <textarea id="additional_context" name="additional_context" rows="8" 
                              placeholder="- Founder story/credibility
- Company values/culture
- Main differentiators
- Social proof (current customers, results)
- Unique positioning
- Content/marketing assets you already have"></textarea>
                </div>

                <button type="submit">🚀 Activate Multi-Agent Research Team</button>
            </form>

            <div id="results"></div>
        </div>

        <script>
            document.getElementById('icpResearchForm').onsubmit = async function(e) {
                e.preventDefault();
                
                const button = document.querySelector('button');
                const results = document.getElementById('results');
                
                // Collect all form data
                const formData = new FormData(e.target);
                const data = {};
                
                // Build structured context from form fields
                let comprehensiveContext = `BUSINESS TYPE: ${formData.get('business_type')}\\n\\n`;
                comprehensiveContext += `COMPANY NAME: ${formData.get('company_name')}\\n\\n`;
                comprehensiveContext += `INDUSTRY: ${formData.get('industry')}\\n\\n`;
                comprehensiveContext += `PRODUCT/SERVICE DESCRIPTION:\\n${formData.get('product_service')}\\n\\n`;
                comprehensiveContext += `TARGET CUSTOMER DESCRIPTION: ${formData.get('target_description')}\\n\\n`;
                comprehensiveContext += `DEMOGRAPHICS & CHARACTERISTICS:\\n${formData.get('demographics')}\\n\\n`;
                comprehensiveContext += `CUSTOMER CONTEXT/SITUATION:\\n${formData.get('customer_context')}\\n\\n`;
                comprehensiveContext += `PROBLEMS YOUR OFFERING SOLVES:\\n${formData.get('problems_solved')}\\n\\n`;
                comprehensiveContext += `CUSTOMER COMPLAINTS (EXACT QUOTES):\\n${formData.get('customer_complaints')}\\n\\n`;
                comprehensiveContext += `CUSTOMER'S STATED GOALS:\\n${formData.get('stated_goals')}\\n\\n`;
                comprehensiveContext += `WHAT SUCCESS LOOKS LIKE (IN THEIR WORDS):\\n${formData.get('success_vision')}\\n\\n`;
                comprehensiveContext += `TARGET MARKET DETAILS:\\n${formData.get('market_details')}\\n\\n`;
                comprehensiveContext += `MARKETING GOAL:\\n${formData.get('marketing_goal')}\\n\\n`;
                
                if (formData.get('additional_context')) {
                    comprehensiveContext += `ADDITIONAL CONTEXT:\\n${formData.get('additional_context')}`;
                }
                
                // Prepare request data
                const requestData = {
                    comprehensive_context: comprehensiveContext
                };
                
                button.textContent = '🧠 Multi-Agent Team Processing...';
                button.disabled = true;
                
                results.style.display = 'block';
                results.innerHTML = `<div class="loading">
                    🤖 Activating Agent Team...<br><br>
                    📊 ICP Intelligence Agent: Analyzing market data<br>
                    🎭 Interview Simulation Agent: Conducting virtual customer interviews<br>
                    🔍 Competitor Analysis: Mapping competitive landscape<br>
                    ✨ Synthesis Agent: Creating GTM strategy<br><br>
                    ⏱️ Estimated time: 3-5 minutes for deep analysis
                </div>`;
                
                try {
                    const response = await fetch('/research/context-analysis', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(requestData)
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    const result = await response.json();
                    results.innerHTML = '<h3>🎉 Multi-Agent Research Complete:</h3><pre>' + JSON.stringify(result, null, 2) + '</pre>';
                } catch (error) {
                    results.innerHTML = '<h3>❌ Error:</h3><p>' + error.message + '</p>';
                }
                
                button.textContent = '🚀 Activate Multi-Agent Research Team';
                button.disabled = false;
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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
        "created_at": "2025-06-30"
    }
    
    try:
        if not AGENTS_AVAILABLE:
            return {
                "session_id": session_id,
                "status": "error",
                "message": "Agent system not available. Check deployment logs for import errors."
            }
        
        print(f"🧠 Starting reasoning agent with comprehensive context...")
        
        # Call the agent function
        agent_results = agent_function(context.comprehensive_context)
        
        # Store results
        research_sessions[session_id]["agent_results"]["reasoning_research"] = agent_results
        research_sessions[session_id]["status"] = "completed"
        
        return {
            "session_id": session_id,
            "status": "completed",
            "message": "Comprehensive context analysis completed",
            "agents_available": AGENTS_AVAILABLE,
            "context_length": len(context.comprehensive_context),
            "results_preview": str(agent_results)[:500] + "..." if len(str(agent_results)) > 500 else str(agent_results),
            "full_results": agent_results,
            "full_results_url": f"/research/{session_id}/results"
        }
        
    except Exception as e:
        research_sessions[session_id]["status"] = "error"
        research_sessions[session_id]["error"] = str(e)
        
        return {
            "session_id": session_id,
            "status": "error",
            "message": f"Error processing context analysis: {str(e)}",
            "agents_available": AGENTS_AVAILABLE,
            "troubleshooting": "Check deployment logs for agent import status"
        }

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
        "created_at": "2025-06-30"
    }
    
    try:
        print(f"🧠 Starting Context-Driven Research with Smart Agent Coordination...")
        
        # For now, use the same agent function until coordinator is fixed
        research_results = agent_function(context.comprehensive_context) if AGENTS_AVAILABLE else {
            "success": False, 
            "error": "Coordinator temporarily disabled for testing"
        }
        
        # Store results
        research_sessions[session_id]["agent_results"]["context_driven_research"] = research_results
        
        if research_results.get("success", True) and "error" not in research_results:
            research_sessions[session_id]["status"] = "completed"
            
            return {
                "session_id": session_id,
                "status": "completed",
                "message": "Context-driven research completed",
                "results": research_results,
                "full_results_url": f"/research/{session_id}/results"
            }
        else:
            research_sessions[session_id]["status"] = "error"
            return {
                "session_id": session_id,
                "status": "error", 
                "message": "Research encountered errors",
                "error_details": research_results.get("error", "Unknown error")
            }
        
    except Exception as e:
        research_sessions[session_id]["status"] = "error"
        research_sessions[session_id]["error"] = str(e)
        
        return {
            "session_id": session_id,
            "status": "error",
            "message": f"Error in context-driven research: {str(e)}"
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
        "service": "market-research-agents", 
        "version": "3.0.0",
        "agents_available": AGENTS_AVAILABLE
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
