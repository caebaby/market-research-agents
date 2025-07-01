from crewai import Agent, Task, Crew
from crewai_tools import WebsiteSearchTool, SerperDevTool
from langchain_openai import ChatOpenAI
import json
import os

class ChunkedReasoningAgent:
    def __init__(self):
        self.reasoning_llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2
        )
        
        # Tools
        self.web_search = SerperDevTool()
        self.website_tool = WebsiteSearchTool()
        
        # Industry frameworks (same as before)
        self.reasoning_frameworks = {
            "financial_services": {
                "psychology_drivers": [
                    "Status and recognition needs",
                    "Financial security anxiety", 
                    "Professional competence validation",
                    "Client trust and relationship dynamics",
                    "Regulatory compliance stress"
                ],
                "business_challenges": [
                    "Client acquisition cost vs lifetime value",
                    "Commission volatility vs recurring revenue",
                    "Compliance overhead vs growth focus",
                    "Market commoditization pressure"
                ]
            },
            "general_business": {
                "psychology_drivers": [
                    "Achievement and growth motivation",
                    "Status and market position",
                    "Security and risk management",
                    "Autonomy and control needs"
                ]
            }
        }
        
    def detect_industry_context(self, business_context):
        """Detect industry to apply appropriate reasoning framework"""
        context_text = str(business_context).lower()
        
        if any(term in context_text for term in ["financial", "advisor", "commission", "finra", "investment"]):
            return "financial_services"
        else:
            return "general_business"
    
    def create_chunked_analysis_agent(self, industry_context, chunk_focus):
        """Create agent focused on specific analysis chunk"""
        
        framework = self.reasoning_frameworks.get(industry_context, self.reasoning_frameworks["general_business"])
        
        return Agent(
            role=f"Precision Intelligence Researcher - {chunk_focus} Specialist",
            goal=f"Conduct deep {chunk_focus.lower()} analysis using structured reasoning chains and Schwartz frameworks",
            backstory=f"""You are a specialist in {chunk_focus.lower()} analysis for {industry_context}. 
            You use 5-step reasoning chains and Eugene Schwartz frameworks to extract deep insights.

REASONING METHODOLOGY:
1. OBSERVATION: What specific evidence do I see?
2. PATTERN RECOGNITION: What patterns does this connect to?
3. ROOT CAUSE ANALYSIS: What deeper drivers explain this?
4. CONTRADICTION TESTING: What evidence would contradict this?
5. CONFIDENCE ASSESSMENT: How certain am I and why?

SCHWARTZ FRAMEWORKS:
- Awareness Levels (Unaware → Problem → Solution → Product → Most Aware)
- Belief Systems (Surface → Private → Unconscious)
- Market Sophistication (Virgin → Cynical stages)

DOMAIN EXPERTISE: {framework['psychology_drivers']}

FOCUS AREA: {chunk_focus}
You must stay focused ONLY on your specialty area to ensure depth within token limits.""",
            
            tools=[self.web_search, self.website_tool],
            llm=self.reasoning_llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_chunk_task(self, business_context, industry_context, chunk_focus):
        """Create focused task for specific analysis chunk"""
        
        chunk_prompts = {
            "Awareness_Analysis": f"""
            AWARENESS LEVEL & BELIEF SYSTEM ANALYSIS ONLY
            
            BUSINESS CONTEXT: {json.dumps(business_context, indent=2)}
            
            FOCUS: Analyze ONLY awareness levels and belief systems
            
            SCHWARTZ AWARENESS ANALYSIS:
            For each awareness level, provide 2-3 key insights with complete reasoning chains:
            
            LEVEL 1 - UNAWARE:
            - What problems don't they recognize? (with reasoning chain)
            - What pain do they accept as normal? (with reasoning chain)
            - Customer voice examples
            
            LEVEL 2 - PROBLEM AWARE:
            - How do they describe pain? (with reasoning chain)
            - What do they blame problems on? (with reasoning chain)
            - Customer voice examples
            
            LEVEL 3 - SOLUTION AWARE:
            - What solutions have they tried? (with reasoning chain)
            - What solution prejudices exist? (with reasoning chain)
            - Customer voice examples
            
            LEVEL 4 - PRODUCT AWARE:
            - What false beliefs about your category? (with reasoning chain)
            - What preemptive objections? (with reasoning chain)
            - Customer voice examples
            
            LEVEL 5 - MOST AWARE:
            - What prevents final action? (with reasoning chain)
            - Customer voice examples
            
            BELIEF SYSTEM ARCHAEOLOGY:
            
            SURFACE BELIEFS (3-4 key beliefs with reasoning chains)
            PRIVATE BELIEFS (3-4 key beliefs with reasoning chains)  
            UNCONSCIOUS BELIEFS (3-4 key beliefs with reasoning chains)
            
            Each belief must include:
            - Complete 5-step reasoning chain
            - Customer voice quote
            - Copy strategy implication
            """,
            
            "Psychology_Analysis": f"""
            CUSTOMER PSYCHOLOGY & DECISION ANALYSIS ONLY
            
            BUSINESS CONTEXT: {json.dumps(business_context, indent=2)}
            
            FOCUS: Deep psychological drivers and decision psychology
            
            CORE IDENTITY ANALYSIS:
            - How do they see themselves? (with reasoning chain)
            - What threatens their identity? (with reasoning chain)
            - Customer voice examples
            
            EMOTIONAL DRIVERS:
            Analyze 4-5 key emotional drivers:
            - Specific driver (with reasoning chain)
            - How it manifests in behavior
            - Customer voice examples
            - Marketing implication
            
            DECISION PSYCHOLOGY:
            - What triggers action? (with reasoning chain)
            - What creates resistance? (with reasoning chain)
            - How do they evaluate options? (with reasoning chain)
            - What builds trust? (with reasoning chain)
            
            PAIN ANALYSIS:
            - Surface pains (3-4 with reasoning chains)
            - Deep emotional pains (3-4 with reasoning chains)
            - Hidden pains they deny (2-3 with reasoning chains)
            
            DESIRE MAPPING:
            - Stated desires (3-4 with reasoning chains)
            - Underlying desires (3-4 with reasoning chains)
            - Latent needs (2-3 with reasoning chains)
            """,
            
            "Market_Strategy": f"""
            MARKET SOPHISTICATION & COPY STRATEGY ONLY
            
            BUSINESS CONTEXT: {json.dumps(business_context, indent=2)}
            
            FOCUS: Market sophistication assessment and copy strategy
            
            MARKET SOPHISTICATION ASSESSMENT:
            - Current stage (1-5) with reasoning chain
            - Competitive landscape analysis
            - Message fatigue indicators
            - Required differentiation mechanism
            
            COPY STRATEGY INTELLIGENCE:
            
            AWARENESS PROGRESSION STRATEGY:
            - How to move Level 1→2 (with reasoning chain)
            - How to move Level 2→3 (with reasoning chain)
            - How to move Level 3→4 (with reasoning chain)
            - How to move Level 4→5 (with reasoning chain)
            
            BELIEF DISRUPTION STRATEGY:
            - Top 3 beliefs to disrupt (with reasoning chains)
            - Disruption methods for each
            - New beliefs to install
            - Proof required for each
            
            VOICE OF CUSTOMER BY LEVEL:
            - Unaware language patterns (5-7 phrases)
            - Problem aware language (5-7 phrases)
            - Solution aware language (5-7 phrases)
            - Product aware language (5-7 phrases)
            - Most aware language (5-7 phrases)
            
            CAMPAIGN IMPLICATIONS:
            - TOFU messaging strategy (with reasoning)
            - MOFU messaging strategy (with reasoning)
            - BOFU messaging strategy (with reasoning)
            - Objection handling strategy (with reasoning)
            """
        }
        
        return Task(
            description=chunk_prompts[chunk_focus],
            expected_output=f"""
            Focused {chunk_focus.replace('_', ' ')} analysis in JSON format:
            
            {{
              "analysis_type": "{chunk_focus}",
              "industry_context": "{industry_context}",
              "chunk_summary": "[Summary of key findings]",
              
              [Specific output structure for {chunk_focus}]
              
              "reasoning_quality": {{
                "total_reasoning_chains": "[Count]",
                "average_confidence": "[0-100]",
                "customer_voice_authenticity": "[Assessment]"
              }}
            }}
            """,
            agent=self.create_chunked_analysis_agent(industry_context, chunk_focus)
        )
    
    def execute_chunked_analysis(self, business_context):
        """Execute analysis in chunks to stay within token limits"""
        
        print("🧠 Executing Chunked Reasoning Analysis...")
        
        # Detect industry context
        industry_context = self.detect_industry_context(business_context)
        print(f"📊 Industry Context: {industry_context}")
        
        # Define analysis chunks
        chunks = [
            "Awareness_Analysis",    # Awareness levels + belief systems
            "Psychology_Analysis",   # Customer psychology + decision analysis  
            "Market_Strategy"        # Market sophistication + copy strategy
        ]
        
        results = {}
        
        # Execute each chunk separately
        for chunk in chunks:
            print(f"🔍 Processing {chunk.replace('_', ' ')}...")
            
            # Create focused task
            task = self.create_chunk_task(business_context, industry_context, chunk)
            
            # Execute chunk analysis
            crew = Crew(
                agents=[self.create_chunked_analysis_agent(industry_context, chunk)],
                tasks=[task],
                verbose=True
            )
            
            chunk_result = crew.kickoff()
            results[chunk] = chunk_result
            
            print(f"✅ {chunk.replace('_', ' ')} completed")
        
        # Synthesize results
        synthesized_results = self.synthesize_chunked_results(results, industry_context)
        
        return synthesized_results
    
    def synthesize_chunked_results(self, chunk_results, industry_context):
        """Synthesize chunked results into coherent analysis"""
        
        return {
            "analysis_summary": {
                "methodology": "Chunked Analysis with Schwartz Intelligence",
                "industry_context": industry_context,
                "chunks_completed": list(chunk_results.keys()),
                "total_analysis": "Complete market sophistication analysis"
            },
            
            "awareness_and_beliefs": chunk_results.get("Awareness_Analysis", {}),
            "customer_psychology": chunk_results.get("Psychology_Analysis", {}), 
            "market_strategy": chunk_results.get("Market_Strategy", {}),
            
            "integrated_insights": {
                "key_findings": "Top insights from all chunks",
                "copy_recommendations": "Synthesized copywriting strategy",
                "campaign_strategy": "Integrated campaign approach"
            },
            
            "implementation_roadmap": {
                "immediate_actions": "What to implement first",
                "testing_framework": "How to test insights",
                "success_metrics": "How to measure results"
            }
        }

# Drop-in replacement for your existing function
def reasoning_agent_call(business_context):
    """
    Chunked reasoning agent that respects token limits while providing deep analysis
    """
    agent = ChunkedReasoningAgent()
    
    # Handle different input formats
    if isinstance(business_context, str):
        context_dict = {
            "company_name": "Analysis Request",
            "comprehensive_context": business_context,
            "industry": "To be determined",
            "target_market": "To be analyzed"
        }
    else:
        context_dict = business_context
    
    # Execute chunked analysis
    result = agent.execute_chunked_analysis(context_dict)
    
    return result
