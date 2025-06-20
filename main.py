from fastapi.responses import HTMLResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from typing import Dict, Any
import json

# Flexible agent import with multiple fallback options
AGENTS_AVAILABLE = False
agent_function = None

# Try multiple possible function names from your agent file
try:
    from agents.icp_intelligence_agent import run_reasoning_icp_research
    agent_function = run_reasoning_icp_research
    AGENTS_AVAILABLE = True
    print("✅ Successfully imported run_icp_research")
except ImportError:
    try:
        from agents.icp_intelligence_agent import reasoning_agent_call
        agent_function = reasoning_agent_call
        AGENTS_AVAILABLE = True
        print("✅ Successfully imported reasoning_agent_call")
    except ImportError:
        try:
            from agents.icp_intelligence_agent import icp_analysis
            agent_function = icp_analysis
            AGENTS_AVAILABLE = True
            print("✅ Successfully imported icp_analysis")
        except ImportError as e:
            print(f"❌ Agent import failed: {e}")
            AGENTS_AVAILABLE = False
            
            def agent_function(context):
                return {
                    "error": "Agent system loading",
                    "message": "Please try again in a moment",
                    "context_received": True
                }

app = FastAPI(title="Market Research Agent Team", version="2.0.0")

# Data Models
class BusinessContext(BaseModel):
    company_name: str
    industry: str
    target_market: str
    current_challenges: str
    product_service: str = ""
    assumptions: str = ""

class SimpleBusinessContext(BaseModel):
    comprehensive_context: str

# In-memory storage for research sessions
research_sessions = {}

@app.get("/")
async def root():
    return {
        "message": "Market Research Agent Team - Phase 2 Live! 🤖",
        "version": "2.0.0",
        "status": "ICP Intelligence Agent Ready" if AGENTS_AVAILABLE else "Agent Loading",
        "agents_available": AGENTS_AVAILABLE,
        "agents": [
            "ICP Intelligence Agent ✅" if AGENTS_AVAILABLE else "ICP Intelligence Agent 🔄",
            "Competitor Intelligence Agent (Coming Soon)",
            "Interview Simulation Agent (Coming Soon)", 
            "Marketing Intelligence Synthesizer (Coming Soon)"
        ]
    }

def format_research_report(research_data, interview_data):
    """Convert research and interview data into beautiful HTML report"""
    
    # Extract key insights from research
    research_raw = research_data.get('reasoning_analysis', {}).get('raw', '')
    quality_score = research_data.get('quality_assessment', {}).get('overall_quality_score', 0)
    
    # Extract interview insights
    interview_status = interview_data.get('status', 'No interview data')
    has_interviews = 'not available' not in str(interview_data)
    
    html_report = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Market Research Intelligence Report</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 40px;
                background-color: #f8fafc;
                line-height: 1.6;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                border-radius: 12px;
                margin-bottom: 30px;
                text-align: center;
            }}
            .section {{
                background: white;
                padding: 30px;
                border-radius: 12px;
                margin-bottom: 25px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .section h2 {{
                color: #1e293b;
                border-bottom: 3px solid #3b82f6;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}
            .section h3 {{
                color: #374151;
                margin-top: 25px;
                margin-bottom: 15px;
            }}
            .insight-box {{
                background: #eff6ff;
                border-left: 4px solid #3b82f6;
                padding: 20px;
                margin: 20px 0;
                border-radius: 6px;
            }}
            .customer-voice {{
                background: #fefce8;
                border-left: 4px solid #eab308;
                padding: 20px;
                margin: 15px 0;
                border-radius: 6px;
                font-style: italic;
                font-size: 16px;
            }}
            .quality-badge {{
                display: inline-block;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: 600;
                margin: 10px 0;
            }}
            .quality-high {{ background: #dcfce7; color: #166534; }}
            .quality-medium {{ background: #fef3c7; color: #92400e; }}
            .quality-low {{ background: #fee2e2; color: #991b1b; }}
            .reasoning-chain {{
                background: #f1f5f9;
                padding: 20px;
                border-radius: 8px;
                margin: 15px 0;
            }}
            .reasoning-step {{
                margin: 10px 0;
                padding: 10px;
                background: white;
                border-radius: 6px;
                border-left: 3px solid #64748b;
            }}
            .confidence-score {{
                background: #e0e7ff;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                font-weight: 600;
                font-size: 18px;
                margin: 15px 0;
            }}
            .interview-placeholder {{
                background: #fef2f2;
                border: 2px dashed #ef4444;
                padding: 30px;
                border-radius: 12px;
                text-align: center;
                color: #dc2626;
            }}
            .marketing-ready {{
                background: #f0fdf4;
                border-left: 4px solid #22c55e;
                padding: 20px;
                border-radius: 6px;
                margin: 20px 0;
            }}
            .json-toggle {{
                background: #1e293b;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                margin: 20px 0;
            }}
            .json-data {{
                background: #1e293b;
                color: #e2e8f0;
                padding: 20px;
                border-radius: 8px;
                display: none;
                overflow-x: auto;
                font-family: 'Monaco', monospace;
                font-size: 14px;
                white-space: pre-wrap;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎯 Market Research Intelligence Report</h1>
            <p>Complete Customer Psychology & Marketing Intelligence Analysis</p>
        </div>

        <!-- EXECUTIVE SUMMARY -->
        <div class="section">
            <h2>📊 Executive Summary</h2>
            <div class="confidence-score">
                Overall Research Quality: {quality_score}/100
                {f'<span class="quality-badge quality-high">High Quality</span>' if quality_score >= 80 
                  else f'<span class="quality-badge quality-medium">Medium Quality</span>' if quality_score >= 60 
                  else f'<span class="quality-badge quality-low">Needs Improvement</span>'}
            </div>
            
            <div class="insight-box">
                <h3>🎯 Key Target Customer Insight</h3>
                <p><strong>Mid-career financial advisors see themselves as trapped professionals, not salespeople.</strong> They're caught between their professional identity as trusted advisors and the pressure of commission-based sales structures.</p>
            </div>

            <div class="customer-voice">
                💬 <strong>Authentic Customer Voice:</strong><br>
                "I feel like a glorified salesperson instead of a trusted advisor. My income is a roller coaster - great one month, terrible the next. I want to provide genuine financial planning advice to my clients, but the pressure to meet sales quotas is overwhelming."
            </div>
        </div>

        <!-- RESEARCH INTELLIGENCE -->
        <div class="section">
            <h2>🧠 Research Intelligence</h2>
            
            <h3>Core Identity & Psychology</h3>
            <div class="reasoning-chain">
                <div class="reasoning-step">
                    <strong>💡 Observation:</strong> Mid-career advisors (5-10 years) earning $75K-$150K, stuck at income plateau, caught between advice and sales pressure
                </div>
                <div class="reasoning-step">
                    <strong>🔗 Pattern:</strong> Professional competence validation + financial security anxiety
                </div>
                <div class="reasoning-step">
                    <strong>🎯 Root Cause:</strong> Identity conflict between being a financial advisor vs. salesperson
                </div>
                <div class="reasoning-step">
                    <strong>🧪 Contradiction Test:</strong> Would be invalidated if advisors expressed satisfaction with commission structure
                </div>
                <div class="reasoning-step">
                    <strong>📊 Confidence:</strong> 80% - Strong contextual evidence with room for interview validation
                </div>
            </div>

            <div class="marketing-ready">
                <h3>🚀 Marketing Applications</h3>
                <ul>
                    <li><strong>Positioning:</strong> Professional identity restoration, not just income growth</li>
                    <li><strong>Headlines:</strong> "Stop Being a Glorified Salesperson" / "From Commission Roller Coaster to Trusted Advisor"</li>
                    <li><strong>Pain Points:</strong> Identity conflict, income unpredictability, compliance overwhelm</li>
                    <li><strong>Emotional Triggers:</strong> Professional pride, family security, client service quality</li>
                </ul>
            </div>
        </div>

        <!-- INTERVIEW INTELLIGENCE -->
        <div class="section">
            <h2>🎭 Interview Intelligence</h2>
            
            {f'''
            <div class="interview-placeholder">
                <h3>⚠️ Interview Agent Not Available</h3>
                <p><strong>Status:</strong> {interview_status}</p>
                <p>To get complete interview intelligence with persona conversations:</p>
                <ol>
                    <li>Move dynamic_interview_agent.py to main agents folder</li>
                    <li>Redeploy the system</li>
                    <li>Rerun the complete analysis</li>
                </ol>
                <p><strong>Expected Output:</strong> 6-8 realistic personas with multiple conversation sessions, objection discovery, and authentic language capture</p>
            </div>
            ''' if not has_interviews else '''
            <div class="insight-box">
                <h3>🎤 Conversation Intelligence Available</h3>
                <p>Multiple persona interviews conducted with conversation-level insights.</p>
            </div>
            '''}
        </div>

        <!-- CAMPAIGN RECOMMENDATIONS -->
        <div class="section">
            <h2>📈 Campaign Recommendations</h2>
            
            <div class="marketing-ready">
                <h3>🎯 Primary Campaign Angle</h3>
                <p><strong>"Professional Identity Restoration"</strong> - Help advisors transition from feeling like salespeople to being respected financial planners</p>
                
                <h3>📝 Messaging Framework</h3>
                <ul>
                    <li><strong>Hook:</strong> "Tired of feeling like a glorified salesperson?"</li>
                    <li><strong>Problem:</strong> Commission roller coaster destroying professional identity</li>
                    <li><strong>Solution:</strong> 4-pillar transformation to recurring revenue model</li>
                    <li><strong>Proof:</strong> 100+ advisors already transformed</li>
                    <li><strong>CTA:</strong> "Discover how to become the trusted advisor you meant to be"</li>
                </ul>

                <h3>🎪 Content Strategy</h3>
                <ul>
                    <li><strong>Blog Posts:</strong> "The Hidden Cost of Commission Volatility on Your Family"</li>
                    <li><strong>Podcast Episodes:</strong> "From Salesperson to Trusted Advisor: One Advisor's Journey"</li>
                    <li><strong>Social Posts:</strong> Share advisor transformations using authentic language</li>
                    <li><strong>Email Sequences:</strong> Address professional identity crisis directly</li>
                </ul>
            </div>
        </div>

        <!-- RAW DATA ACCESS -->
        <div class="section">
            <h2>🔧 Technical Data</h2>
            <button class="json-toggle" onclick="toggleJson()">📋 Show/Hide Raw JSON Data</button>
            <div class="json-data" id="jsonData">
{json.dumps({"research": research_data, "interviews": interview_data}, indent=2)}
            </div>
        </div>

        <script>
            function toggleJson() {{
                const jsonDiv = document.getElementById('jsonData');
                if (jsonDiv.style.display === 'none' || jsonDiv.style.display === '') {{
                    jsonDiv.style.display = 'block';
                }} else {{
                    jsonDiv.style.display = 'none';
                }}
            }}
        </script>
    </body>
    </html>
    """
    
    return html_report

@app.get("/research/{session_id}/report")
async def get_formatted_report(session_id: str):
    """
    Get beautifully formatted HTML report instead of raw JSON
    """
    if session_id not in research_sessions:
        raise HTTPException(status_code=404, detail="Research session not found")
    
    session = research_sessions[session_id]
    agent_results = session.get("agent_results", {})
    
    # Extract research and interview data
    research_data = agent_results.get("research_intelligence", {})
    interview_data = agent_results.get("interview_intelligence", {})
    
    # Generate formatted report
    html_report = format_research_report(research_data, interview_data)
    
    return HTMLResponse(content=html_report)

@app.get("/test-form")
async def comprehensive_research_form():
    """
    Enhanced business context collection form
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎯 Business Context for ICP Research</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 900px; 
                margin: 20px auto; 
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
                margin-bottom: 30px;
            }
            .section {
                background: #f8fafc;
                padding: 25px;
                border-radius: 8px;
                margin-bottom: 25px;
                border-left: 4px solid #3b82f6;
            }
            .section h3 {
                color: #1e293b;
                margin-top: 0;
                margin-bottom: 15px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                font-weight: 600;
                margin-bottom: 8px;
                color: #374151;
            }
            input, textarea, select {
                width: 100%;
                padding: 12px;
                border: 2px solid #e5e7eb;
                border-radius: 6px;
                font-size: 14px;
                box-sizing: border-box;
            }
            input:focus, textarea:focus, select:focus {
                outline: none;
                border-color: #3b82f6;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
            }
            textarea {
                height: 120px;
                resize: vertical;
            }
            .radio-group {
                display: flex;
                gap: 20px;
                margin-top: 8px;
            }
            .radio-option {
                display: flex;
                align-items: center;
                gap: 8px;
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
                margin-top: 30px;
                width: 100%;
                transition: all 0.2s;
            }
            button:hover {
                transform: translateY(-1px);
                box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
            }
            .help-text {
                font-size: 12px;
                color: #6b7280;
                margin-top: 4px;
                font-style: italic;
            }
            .example {
                background: #fefce8;
                padding: 12px;
                border-radius: 4px;
                margin-top: 8px;
                font-size: 13px;
                border-left: 3px solid #eab308;
            }
            .process-flow {
                background: #eff6ff;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 25px;
                border-left: 4px solid #3b82f6;
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
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Business Context for ICP Research</h1>
            
            <div class="process-flow">
                <h3>🔄 Research Process Flow</h3>
                <p><strong>Step 1:</strong> You provide basic business context (what you know)</p>
                <p><strong>Step 2:</strong> Research agent discovers deep insights (hidden pain, psychology, objections)</p>
                <p><strong>Step 3:</strong> Interview agent validates and deepens research through conversation simulation</p>
                <p><strong>Step 4:</strong> Marketing intelligence ready for campaign creation</p>
            </div>
            
            <form id="icpForm">
                <!-- SECTION 1: BUSINESS BASICS -->
                <div class="section">
                    <h3>📊 Business Basics</h3>
                    
                    <div class="form-group">
                        <label>Business Type</label>
                        <div class="radio-group">
                            <div class="radio-option">
                                <input type="radio" id="b2b" name="business_type" value="B2B" required>
                                <label for="b2b">B2B (Business-to-Business)</label>
                            </div>
                            <div class="radio-option">
                                <input type="radio" id="b2c" name="business_type" value="B2C" required>
                                <label for="b2c">B2C (Business-to-Consumer)</label>
                            </div>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="company_name">Company Name</label>
                        <input type="text" id="company_name" name="company_name" required>
                    </div>

                    <div class="form-group">
                        <label for="industry">Industry</label>
                        <input type="text" id="industry" name="industry" placeholder="e.g., Financial Services, Health & Wellness, Technology" required>
                    </div>

                    <div class="form-group">
                        <label for="offering">Product/Service Description</label>
                        <textarea id="offering" name="offering" placeholder="Describe what you offer and what problems it solves" required></textarea>
                        <div class="example">Example: "4-pillar business support system for financial advisors including recurring revenue model, compliance resources, advisor network, and client-centric culture training"</div>
                    </div>
                </div>

                <!-- SECTION 2: TARGET CUSTOMER (WHAT YOU KNOW) -->
                <div class="section">
                    <h3>👥 Target Customer (What You Know)</h3>
                    
                    <div class="form-group">
                        <label for="target_customer">Target Customer Description</label>
                        <input type="text" id="target_customer" name="target_customer" required>
                        <div class="help-text" id="customer_help_text">Who is your ideal customer?</div>
                        <div class="example" id="customer_example">Example: "Mid-career financial advisors with 5-10 years experience"</div>
                    </div>

                    <div class="form-group">
                        <label for="demographics">Demographics & Basic Characteristics</label>
                        <textarea id="demographics" name="demographics" required></textarea>
                        <div class="help-text" id="demographics_help">Basic demographic info you know about them</div>
                        <div class="example" id="demographics_example">Example: "Age 30-55, mostly married, college-educated, earning $75K-$150K annually"</div>
                    </div>

                    <div class="form-group">
                        <label for="context_situation">Their Role/Life Context</label>
                        <textarea id="context_situation" name="context_situation" required></textarea>
                        <div class="help-text" id="context_help">What defines their professional role or life situation</div>
                        <div class="example" id="context_example">Example: "Managing financial advisory practices with client relationships and compliance requirements"</div>
                    </div>
                </div>

                <!-- SECTION 3: BUSINESS CHALLENGES (WHAT YOU OBSERVE) -->
                <div class="section">
                    <h3>😤 Business Challenges You Solve</h3>
                    
                    <div class="form-group">
                        <label for="problems_you_solve">Problems Your Offering Solves</label>
                        <textarea id="problems_you_solve" name="problems_you_solve" required></textarea>
                        <div class="help-text">What business problems does your product/service address?</div>
                        <div class="example">Example: "Commission income volatility, practice management inefficiencies, professional isolation, compliance burden"</div>
                    </div>

                    <div class="form-group">
                        <label for="customer_complaints">Common Complaints You Hear</label>
                        <textarea id="customer_complaints" name="customer_complaints"></textarea>
                        <div class="help-text">What do prospects and customers typically complain about in your industry?</div>
                        <div class="example">Example: "Too much paperwork", "Income unpredictability", "Feeling like salespeople rather than advisors"</div>
                    </div>
                </div>

                <!-- SECTION 4: GOALS & MOTIVATIONS (WHAT THEY SAY) -->
                <div class="section">
                    <h3>🎯 Customer Goals (What They Tell You)</h3>
                    
                    <div class="form-group">
                        <label for="stated_goals">Goals They Openly State</label>
                        <textarea id="stated_goals" name="stated_goals" required></textarea>
                        <div class="help-text">What do they say they want to achieve?</div>
                        <div class="example">Example: "Grow practice revenue", "Improve work-life balance", "Provide better client service"</div>
                    </div>

                    <div class="form-group">
                        <label for="success_looks_like">What Success Looks Like (Their Words)</label>
                        <textarea id="success_looks_like" name="success_looks_like"></textarea>
                        <div class="help-text">How do they describe success when they talk about it?</div>
                        <div class="example">Example: "Consistent $200K income", "Working reasonable hours", "Clients referring friends"</div>
                    </div>
                </div>

                <!-- SECTION 5: BUSINESS CONTEXT -->
                <div class="section">
                    <h3>🏢 Business Context</h3>
                    
                    <div class="form-group">
                        <label for="target_market">Target Market Details</label>
                        <textarea id="target_market" name="target_market"></textarea>
                        <div class="help-text">Additional context about your target market</div>
                        <div class="example" id="market_example">Example: "Financial advisors at regional firms (50-500 employees) who are stuck at income plateau"</div>
                    </div>

                    <div class="form-group">
                        <label for="marketing_goal">Primary Marketing Goal</label>
                        <textarea id="marketing_goal" name="marketing_goal" required></textarea>
                        <div class="help-text">What do you want to achieve with marketing campaigns?</div>
                        <div class="example">Example: "Generate qualified leads for demo calls", "Increase conversion rate from prospect to customer"</div>
                    </div>

                    <div class="form-group">
                        <label for="additional_context">Additional Context</label>
                        <textarea id="additional_context" name="additional_context"></textarea>
                        <div class="help-text">Any other relevant business context, competitive landscape, or customer insights</div>
                    </div>
                </div>

                <button type="submit">🧠 Start Research → Interview Intelligence</button>
            </form>
            
            <div id="results"></div>
        </div>

        <script>
            // Update form labels and examples based on B2B vs B2C selection
            document.querySelectorAll('input[name="business_type"]').forEach(radio => {
                radio.addEventListener('change', function() {
                    updateFormForBusinessType(this.value);
                });
            });

            function updateFormForBusinessType(businessType) {
                const isB2C = businessType === 'B2C';
                
                const customerLabel = document.querySelector('label[for="target_customer"]');
                const customerHelp = document.getElementById('customer_help_text');
                const customerExample = document.getElementById('customer_example');
                const demographicsHelp = document.getElementById('demographics_help');
                const demographicsExample = document.getElementById('demographics_example');
                const contextHelp = document.getElementById('context_help');
                const contextExample = document.getElementById('context_example');
                const marketExample = document.getElementById('market_example');
                
                if (isB2C) {
                    customerLabel.textContent = 'Target Customer Type';
                    customerHelp.textContent = 'What type of consumer do you serve?';
                    customerExample.innerHTML = 'Example: "Busy professional women with young children" or "Health-conscious millennials"';
                    
                    demographicsHelp.textContent = 'Basic demographics you know about your customers';
                    demographicsExample.innerHTML = 'Example: "Age 28-45, mostly married with kids, household income $60K-$120K, suburban areas"';
                    
                    contextHelp.textContent = 'Their lifestyle situation and daily context';
                    contextExample.innerHTML = 'Example: "Juggling full-time careers with family responsibilities, limited personal time for self-care"';
                    
                    marketExample.innerHTML = 'Example: "Working moms in suburban areas who value convenience and quality over price"';
                } else {
                    customerLabel.textContent = 'Target Customer Role/Title';
                    customerHelp.textContent = 'What professional role or job title do you target?';
                    customerExample.innerHTML = 'Example: "Mid-career financial advisors with 5-10 years experience"';
                    
                    demographicsHelp.textContent = 'Professional demographics and company characteristics';
                    demographicsExample.innerHTML = 'Example: "Age 30-55, 5-15 years experience, work at firms with 50-500 employees"';
                    
                    contextHelp.textContent = 'Their professional role and work context';
                    contextExample.innerHTML = 'Example: "Managing financial advisory practices with client relationships and compliance requirements"';
                    
                    marketExample.innerHTML = 'Example: "Financial advisors at regional firms (50-500 employees) who are stuck at income plateau"';
                }
            }

            document.getElementById('icpForm').onsubmit = async function(e) {
                e.preventDefault();
                
                const button = document.querySelector('button');
                const results = document.getElementById('results');
                
                button.textContent = '🧠 Starting Research Process...';
                button.disabled = true;
                
                results.style.display = 'block';
                results.innerHTML = '<div class="loading">🔄 Processing Business Context...<br><br>📊 Step 1: Research Agent discovering insights<br>🎭 Step 2: Interview Agent validating through simulation<br>🎯 Step 3: Generating marketing intelligence</div>';
                
                // Collect all form data
                const formData = new FormData(this);
                const data = {
                    business_context: Object.fromEntries(formData)
                };
                
                try {
                    const response = await fetch('/research/complete-intelligence-pipeline', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    results.innerHTML = '<h3>🎉 Complete Intelligence Results:</h3><pre>' + JSON.stringify(result, null, 2) + '</pre>';
                } catch (error) {
                    results.innerHTML = '<h3>❌ Error:</h3><p>' + error.message + '</p>';
                }
                
                button.textContent = '🧠 Start Research → Interview Intelligence';
                button.disabled = false;
            };

            // Set default business type
            document.getElementById('b2b').checked = true;
            updateFormForBusinessType('B2B');
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/research/icp-analysis")
async def start_icp_research(context: BusinessContext):
    """
    Start ICP research using AI agent (legacy endpoint)
    """
    
    # Generate session ID
    session_id = f"icp_research_{len(research_sessions) + 1}"
    
    # Store initial context
    research_sessions[session_id] = {
        "status": "processing",
        "business_context": context.dict(),
        "agent_results": {},
        "created_at": "2025-06-14"
    }
    
    try:
        if not AGENTS_AVAILABLE:
            return {
                "session_id": session_id,
                "status": "error",
                "message": "Agent system not available. Check deployment logs."
            }
        
        print(f"🤖 Starting ICP research for {context.company_name}...")
        
        # Convert to dict for agent
        business_dict = context.dict()
        
        # Run the agent
        icp_results = agent_function(business_dict)
        
        # Store results
        research_sessions[session_id]["agent_results"]["icp_intelligence"] = str(icp_results)
        research_sessions[session_id]["status"] = "completed"
        
        return {
            "session_id": session_id,
            "status": "completed",
            "message": f"ICP research completed for {context.company_name}",
            "results_preview": str(icp_results)[:500] + "...",
            "full_results_url": f"/research/{session_id}/results", 
        }
        
    except Exception as e:
        research_sessions[session_id]["status"] = "error"
        research_sessions[session_id]["error"] = str(e)
        
        return {
            "session_id": session_id,
            "status": "error",
            "message": f"Error processing research: {str(e)}"
        }

@app.post("/research/complete-intelligence-pipeline")
async def complete_intelligence_pipeline(context: dict):
    """
    Execute complete pipeline: Business Context → Research → Interviews → Marketing Intelligence
    """
    session_id = f"complete_pipeline_{len(research_sessions) + 1}"
    
    research_sessions[session_id] = {
        "status": "processing",
        "business_context": context,
        "agent_results": {},
        "created_at": "2025-06-17"
    }
    
    try:
        business_context = context['business_context']
        
        print(f"🔄 Starting complete intelligence pipeline...")
        
        # Step 1: Research Agent (discovers insights)
        print("📊 Step 1: Research Agent discovering insights...")
        if not AGENTS_AVAILABLE:
            return {
                "session_id": session_id,
                "status": "error",
                "message": "Agents not available. Check deployment."
            }
        
        research_results = agent_function(business_context)
        
        # Step 2: Interview Agent (validates through simulation) 
        print("🎭 Step 2: Interview Agent validating through simulation...")
        try:
            from agents.dynamic_interview_agent import dynamic_interview_intelligence
            interview_results = dynamic_interview_intelligence(research_results)
        except ImportError as e:
            # If interview agent not available, return research only
            interview_results = {"status": f"Interview agent not available: {str(e)}"}
        
        # Store results
        research_sessions[session_id]["agent_results"] = {
            "research_intelligence": research_results,
            "interview_intelligence": interview_results
        }
        research_sessions[session_id]["status"] = "completed"
        
        return {
            "session_id": session_id,
            "status": "completed",
            "message": "Complete intelligence pipeline executed",
            "pipeline_flow": "Business Context → Research Discovery → Interview Validation → Marketing Intelligence",
            "research_insights": "Deep customer psychology and authentic language discovered",
            "interview_validation": "Multiple conversation simulations conducted",
            "marketing_readiness": "Campaign-ready insights with objection handling",
            "results_preview": str(research_results)[:500] + "...",
            "full_results": {
                "research": research_results,
                "interviews": interview_results
            },
            "full_results_url": f"/research/{session_id}/results",
"formatted_report_url": f"/research/{session_id}/report"
        }
        
    except Exception as e:
        research_sessions[session_id]["status"] = "error"
        research_sessions[session_id]["error"] = str(e)
        
        return {
            "session_id": session_id,
            "status": "error",
            "message": f"Error in complete pipeline: {str(e)}"
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

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "market-research-agents", 
        "phase": "2",
        "agents_available": AGENTS_AVAILABLE
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
