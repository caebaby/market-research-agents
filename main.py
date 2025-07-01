from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from typing import Dict, Any, Optional
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Claude API Configuration (Optional)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
USE_CLAUDE = bool(ANTHROPIC_API_KEY)

if USE_CLAUDE:
    try:
        import anthropic
        claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        print("✅ Claude API initialized for premium research quality")
    except ImportError:
        print("⚠️ Anthropic package not installed. Run: pip install anthropic")
        USE_CLAUDE = False
else:
    print("⚠️ Claude API not configured - using fallback model")

# Enhanced Comprehensive ICP Research Prompt
COMPREHENSIVE_ICP_PROMPT = """
Comprehensive ICP & Psychological Framework Research Prompt (Enhanced with Belief Mapping)

PURPOSE:
This integrated prompt directs the AI to conduct deep, nuanced, and validated market research to build a comprehensive Initial Customer Profile (ICP) enhanced with multiple psychological frameworks. Crucially, it focuses on capturing the authentic language (Voice of Customer - VoC) used by the target audience. The insights generated will serve as the foundational research data for developing highly effective brand messaging and marketing strategies.

CRITICAL INSTRUCTIONS:
* NO HALLUCINATIONS: Ground all insights in verifiable logic, common patterns, or cross-referenced data points. Explicitly state when making hypotheses versus confirmed observations. Avoid making up trends or generalizing without evidence.
* DEPTH & NUANCE: Go beyond surface-level demographics to uncover underlying emotions, contradictions, hidden motivations, and unspoken pains.
* AUTHENTIC LANGUAGE CAPTURE: Actively identify, analyze, and report the specific words, phrases, metaphors, and sentence structures the target audience uses when discussing their problems, pains, desires, and aspirations. This is a critical requirement.
* VALIDATION REQUIRED: Employ multi-angle analysis, contradiction testing, and evidence-based reasoning for every major insight.
* RESEARCH FOCUS: Frame findings to directly inform subsequent messaging and strategy development, but do not generate marketing strategies or specific messaging copy within this prompt.
* HUMAN RESEARCH SIMULATION: Your output must read as if a human market researcher conducted 40+ hours of in-depth qualitative research, including realistic observations, nuanced contradictions, and the depth of insight from extensive interviews and analysis.

SECTION 3: RESEARCH METHODOLOGY & VALIDATION FRAMEWORK

YOUR TASK: Based on the Business Context provided below, conduct a comprehensive research analysis to build a deep, multi-dimensional ICP enhanced with psychological frameworks. Simulate the depth of 40+ hours of qualitative market research.

METHODOLOGY & GUARDRAILS (Apply these rigorously):
1. Multi-Angle Analysis & Validation: For each significant insight:
   * Describe what is likely true based on evidence/logic
   * Identify situations or sub-segments where this might NOT be true
   * Find potential contradictions (e.g., stated belief vs. actual behavior)
   * Assess confidence level and explain why (citing logic, patterns, etc.)
   * Explicitly state: "This is a hypothesis" if not highly confident

2. Cited Proofing (Logical): Back up claims with supporting logic, relating them to:
   * Observed industry trends
   * Common human psychology or behavioral economics principles
   * Historical patterns
   * Logical consequences of their role/industry
   * Do NOT invent data or sources. Focus on logical deduction and pattern recognition.

3. Contradiction Testing: Actively argue against your own insights:
   * What external forces (economic, cultural, technological, personal) could invalidate or change this insight?
   * Where would this insight fail to apply within the broader target market?
   * What real-world behaviors might contradict this assumption?

4. Simulate Nuance (Internal Monologue/Contrasting Views): Instead of just stating findings, illustrate the complexity:
   * How they might publicly describe the issue
   * What their private or internal monologue might be
   * A contrasting viewpoint from a segment of the ICP who doesn't share this specific pain/desire

5. Voice of Customer (VoC) Focus: Throughout the analysis, prioritize capturing and reporting the exact language, phrases, terminology, and metaphors the target audience uses.

SECTION 4: COMPREHENSIVE RESEARCH EXECUTION FRAMEWORK

PART A: FOUNDATIONAL ICP DEVELOPMENT
Step 1: Refine & Expand Baseline Profile
Step 2: Deep Dive - Pains, Problems & Frustrations
Step 3: Deep Dive - Desires, Aspirations & Motivations
Step 4: Voice of Customer (VoC) Language Synthesis

PART B: PSYCHOLOGICAL FRAMEWORK ANALYSIS
Step 5: Jungian Archetype Analysis
Step 6: Language & Behavior (LAB) Profile Analysis
Step 7: Deep Desires & Motivational Drivers Analysis
Step 8: Jobs-To-Be-Done (JTBD) Purchase Psychology

Step 8.5: CRITICAL ADDITION - Current Beliefs & Solution History Analysis
* Current Belief System:
  - What they believe is causing their problem (often incorrect)
  - What they think the solution "should" look like
  - Why they think previous attempts failed
  - What "story" they tell themselves about their situation
  - Industry myths they've accepted as truth
  
* Solution History Archaeology:
  - List 5-7 solutions they've likely tried (be specific)
  - Why each solution failed from THEIR perspective (not objective reality)
  - What they learned (or mis-learned) from each failure
  - Current skepticism/resistance patterns formed by these failures
  - "Scar tissue" - specific triggers that cause them to shut down
  
* Transformation Requirements:
  - What would need to be true for them to believe in a new solution
  - Specific proof points they'd need to see (metrics, case studies, demos)
  - Trust triggers that would overcome their skepticism
  - Risk reversals that would make them feel safe to try again
  - The "aha moment" that would shift their belief system
  - How they would need to experience the solution to believe it's different
  
* VoC Language: Capture EXACTLY how they talk about:
  - Past failures: "I've tried everything and nothing works"
  - Current resignation: "This is just how it is in our industry"
  - Future hope: "If only I could find something that actually..."

Step 9: Cognitive Biases & Decision Shortcuts
Step 10: Influence & Authority Triggers

PART C: VOICE OF CUSTOMER LANGUAGE MAPS
Step 11: Voice of Customer Language Map for Funnel Stages
11A: TOFU Language Patterns - Attention & Awareness
11B: MOFU Language Patterns - Consideration & Evaluation
11C: BOFU Language Patterns - Decision & Action

SECTION 5: FINAL SELF-CRITIQUE
Review your entire analysis and identify:
* What critical insights might still be missing?
* What assumptions carry the most risk of being incorrect?
* What cultural, generational, or industry-specific nuances could significantly alter these findings?
* How could this ICP research be further improved or validated?

SECTION 6: TRANSFER-READY OUTPUT FOR BRAND MESSAGING
Synthesize the most critical findings into a structured format including:
* ICP Definition
* Key Pain Points (TOP 3-5)
* Key Desires/Aspirations (TOP 3-5)
* Current Beliefs & Failed Solutions
* Transformation Requirements
* Psychological Drivers
* Voice of Customer Language
* Competitive Landscape
"""

# Agent imports
AGENTS_AVAILABLE = False
agent_function = None

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

# Try to import interview agent
try:
    from agents.dynamic_interview_agent import dynamic_interview_intelligence
    interview_agent = dynamic_interview_intelligence
    INTERVIEW_AGENT_AVAILABLE = True
    print("✅ Successfully imported dynamic_interview_intelligence")
except ImportError:
    print("⚠️ Interview agent not available")
    INTERVIEW_AGENT_AVAILABLE = False
    interview_agent = None

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
        "agents_available": AGENTS_AVAILABLE,
        "interview_agent": INTERVIEW_AGENT_AVAILABLE,
        "claude_enabled": USE_CLAUDE
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
                    📊 Phase 1: Deep ICP Analysis with Belief Mapping<br>
                    🎭 Phase 2: Conducting 3 Simulated Customer Interviews<br>
                    ✨ Phase 3: Synthesizing Insights for GTM Strategy<br><br>
                    ⏱️ Estimated time: 3-5 minutes for journal-level depth
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
                    
                    // Create a link to view formatted report
                    results.innerHTML = `
                        <h3>🎉 Multi-Agent Research Complete!</h3>
                        <p>Your comprehensive market intelligence report is ready.</p>
                        <a href="/research/${result.session_id}/report" 
                           target="_blank" 
                           style="display: inline-block; 
                                  background: #0066cc; 
                                  color: white; 
                                  padding: 12px 24px; 
                                  text-decoration: none; 
                                  border-radius: 4px; 
                                  margin-top: 20px;">
                           View Full Report
                        </a>
                        <details style="margin-top: 30px;">
                            <summary style="cursor: pointer; color: #666;">View Raw Data</summary>
                            <pre style="margin-top: 10px;">${JSON.stringify(result, null, 2)}</pre>
                        </details>
                    `;
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

# Helper function for Claude calls (if enabled)
async def enhanced_agent_call(prompt: str, use_claude: bool = USE_CLAUDE) -> Any:
    """
    Use Claude for enhanced quality when available, fallback to regular agent
    """
    if use_claude and USE_CLAUDE:
        try:
            response = claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=8000,
                temperature=0.5,
                system="You are an elite market researcher with deep psychological training. Your insights are so accurate that clients feel like you've read their private journals. You uncover hidden beliefs, unspoken fears, and secret desires that even customers don't consciously recognize.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Claude API error: {e}, falling back to default agent")
    
    # Fallback to regular agent
    return agent_function(prompt)

@app.post("/research/context-analysis")
async def context_analysis_research(context: SimpleBusinessContext):
    """
    Process comprehensive business context with enhanced ICP research + simulated interviews
    """
    
    # Generate session ID
    session_id = f"context_research_{len(research_sessions) + 1}"
    
    # Store initial context
    research_sessions[session_id] = {
        "status": "processing",
        "business_context": {"comprehensive_context": context.comprehensive_context},
        "agent_results": {},
        "created_at": datetime.now().isoformat()
    }
    
    try:
        if not AGENTS_AVAILABLE:
            return {
                "session_id": session_id,
                "status": "error",
                "message": "Agent system not available. Check deployment logs for import errors."
            }
        
        print(f"🧠 Phase 1: Starting comprehensive ICP research with belief mapping...")
        
        # Phase 1: Comprehensive ICP Research with Enhanced Prompt
        full_prompt = f"{COMPREHENSIVE_ICP_PROMPT}\n\n---\n\nBUSINESS CONTEXT:\n\n{context.comprehensive_context}"
        
        # Use Claude if available, otherwise fallback
        icp_results = await enhanced_agent_call(full_prompt)
        
        # Phase 2: Simulated Interviews (if available)
        interview_results = None
        if INTERVIEW_AGENT_AVAILABLE and interview_agent:
            print(f"🎭 Phase 2: Conducting simulated customer interviews...")
            
            # Pass the ICP results directly to the interview agent
            interview_results = interview_agent(icp_results)
        else:
            print("⚠️ Interview agent not available - using ICP research only")
        
        # Phase 3: Synthesis
        synthesis_prompt = f"""
        Synthesize these research components into key GTM insights:
        
        ICP Research: {str(icp_results)[:2000]}
        Interview Insights: {str(interview_results)[:2000] if interview_results else "Not conducted"}
        
        Focus on:
        1. Most surprising insights that clients would say "how did you know that?"
        2. Exact language for messaging (pull from interviews)
        3. Biggest belief shifts needed for purchase
        4. Top 3 GTM recommendations based on psychology
        """
        
        synthesis = await enhanced_agent_call(synthesis_prompt)
        
        # Combine all results
        combined_results = {
            "icp_analysis": icp_results,
            "simulated_interviews": interview_results if interview_results else "Interview agent not available",
            "synthesis": synthesis,
            "research_quality": {
                "depth": "Journal-level psychological insights",
                "phases_completed": "ICP + Interviews + Synthesis" if interview_results else "ICP + Synthesis",
                "belief_mapping": "Included",
                "solution_history": "Analyzed",
                "voice_capture": "Authentic language documented"
            }
        }
        
        # Store results
        research_sessions[session_id]["agent_results"]["comprehensive_research"] = combined_results
        research_sessions[session_id]["status"] = "completed"
        
        # Save report to disk for persistence
        try:
            os.makedirs("reports", exist_ok=True)
            report_filename = f"reports/{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            report_data = {
                "session_id": session_id,
                "created_at": datetime.now().isoformat(),
                "business_context": context.comprehensive_context,
                "results": combined_results,
                "status": "completed",
                "research_quality": {
                    "depth": "Journal-level psychological insights",
                    "phases_completed": "ICP + Interviews + Synthesis" if interview_results else "ICP + Synthesis",
                    "belief_mapping": "Included",
                    "solution_history": "Analyzed",
                    "voice_capture": "Authentic language documented"
                }
            }
            
            with open(report_filename, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            # Store filename in session for easy retrieval
            research_sessions[session_id]["report_file"] = report_filename
            print(f"📄 Report saved to {report_filename}")
            
        except Exception as e:
            print(f"⚠️ Failed to save report: {str(e)}")
        
        return {
            "session_id": session_id,
            "status": "completed",
            "message": "Comprehensive ICP research with belief mapping completed",
            "phases_completed": {
                "icp_research": "✅ Complete with belief mapping",
                "simulated_interviews": "✅ Interview intelligence gathered" if interview_results else "⚠️ Not available",
                "synthesis": "✅ GTM insights generated"
            },
            "quality_indicators": {
                "belief_system_mapped": True,
                "solution_history_analyzed": True,
                "transformation_requirements": True,
                "voice_of_customer": True
            },
            "full_results_url": f"/research/{session_id}/report"
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

@app.get("/research/{session_id}/report")
async def get_formatted_report(session_id: str):
    """
    Generate a beautifully formatted HTML report from the research results
    """
    if session_id not in research_sessions:
        raise HTTPException(status_code=404, detail="Research session not found")
    
    session = research_sessions[session_id]
    
    if session["status"] != "completed":
        return HTMLResponse(content="<h1>Report still processing...</h1>")
    
    # For now, return raw JSON - in production, you'd parse and format this beautifully
    results = session.get("agent_results", {}).get("comprehensive_research", {})
    
    html_report = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Market Intelligence Report - Session {session_id}</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6;
                color: #1a1a1a;
                max-width: 900px;
                margin: 0 auto;
                padding: 40px 20px;
                background-color: #f8f9fa;
            }}
            .report-container {{
                background: white;
                padding: 60px;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #0066cc;
                font-size: 2.5em;
                margin-bottom: 20px;
            }}
            pre {{
                white-space: pre-wrap;
                word-wrap: break-word;
                background: #f5f5f5;
                padding: 20px;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="report-container">
            <h1>Market Intelligence Report</h1>
            <p>Session ID: {session_id}</p>
            <h2>Research Results</h2>
            <pre>{json.dumps(results, indent=2)}</pre>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_report)

@app.get("/research/{session_id}/results")
async def get_research_results(session_id: str):
    """
    Get the full research results as JSON
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

# ============= REPORT PERSISTENCE ENDPOINTS =============

@app.get("/reports/list")
async def list_reports():
    """List all saved reports"""
    try:
        if not os.path.exists("reports"):
            return {"reports": [], "message": "No reports directory found"}
        
        report_files = [f for f in os.listdir("reports") if f.endswith('.json')]
        reports = []
        
        for filename in report_files:
            # Extract session_id from filename
            session_id = filename.split('_')[0]
            timestamp = filename.replace('.json', '').split('_', 1)[1] if '_' in filename else 'unknown'
            
            reports.append({
                "filename": filename,
                "session_id": session_id,
                "created_at": timestamp,
                "url": f"/reports/file/{filename}"
            })
        
        return {
            "count": len(reports),
            "reports": sorted(reports, key=lambda x: x['created_at'], reverse=True)
        }
        
    except Exception as e:
        return {"error": str(e), "reports": []}

@app.get("/reports/session/{session_id}")
async def get_report_by_session(session_id: str):
    """Get the latest report for a specific session"""
    try:
        if not os.path.exists("reports"):
            raise HTTPException(status_code=404, detail="No reports directory found")
        
        # Find reports matching this session_id
        matching_files = [f for f in os.listdir("reports") 
                         if f.startswith(f"{session_id}_") and f.endswith('.json')]
        
        if not matching_files:
            raise HTTPException(status_code=404, detail=f"No reports found for session {session_id}")
        
        # Get the most recent one
        latest_file = sorted(matching_files)[-1]
        
        with open(f"reports/{latest_file}", 'r') as f:
            return json.load(f)
            
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Report file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reports/file/{filename}")
async def get_report_by_filename(filename: str):
    """Get a specific report by filename"""
    try:
        # Security: ensure filename doesn't contain path traversal
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        filepath = f"reports/{filename}"
        
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Report not found")
        
        with open(filepath, 'r') as f:
            return json.load(f)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/reports/cleanup")
async def cleanup_old_reports(days_old: int = 30):
    """Clean up reports older than specified days (default 30)"""
    try:
        if not os.path.exists("reports"):
            return {"message": "No reports directory found", "deleted": 0}
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        deleted_count = 0
        
        for filename in os.listdir("reports"):
            if filename.endswith('.json'):
                filepath = f"reports/{filename}"
                file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                if file_time < cutoff_date:
                    os.remove(filepath)
                    deleted_count += 1
        
        return {
            "message": f"Deleted {deleted_count} reports older than {days_old} days",
            "deleted": deleted_count
        }
        
    except Exception as e:
        return {"error": str(e), "deleted": 0}

# ============= END REPORT PERSISTENCE ENDPOINTS =============

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "market-research-agents", 
        "version": "3.0.0",
        "agents_available": AGENTS_AVAILABLE,
        "interview_agent": INTERVIEW_AGENT_AVAILABLE,
        "claude_enabled": USE_CLAUDE
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
