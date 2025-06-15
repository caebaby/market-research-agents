from crewai import Agent, Task, Crew
from crewai_tools import WebsiteSearchTool, SerperDevTool
from langchain_openai import ChatOpenAI
import json
import os

class HighQualityReasoningAgent:
    def __init__(self):
        # CRITICAL: Use proper models for reasoning tasks
        self.reasoning_llm = ChatOpenAI(
            model="gpt-4",  # Changed from gpt-4o-mini
            temperature=0.2  # Lower for more focused reasoning
        )
        
        self.validation_llm = ChatOpenAI(
            model="gpt-4", 
            temperature=0.1
        )
        
        # Tools
        self.web_search = SerperDevTool()
        self.website_tool = WebsiteSearchTool()
        
        # Domain-specific reasoning frameworks
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
    
    def create_precision_reasoning_agent(self, industry_context):
        """Create agent with precision reasoning prompts based on industry"""
        
        framework = self.reasoning_frameworks.get(industry_context, self.reasoning_frameworks["general_business"])
        
        return Agent(
            role="Precision Business Intelligence Researcher with Chain-of-Thought Reasoning",
            goal="Conduct deep customer psychology analysis using structured reasoning chains and domain expertise",
            backstory=f"""You are an expert business intelligence researcher specializing in {industry_context} who uses structured reasoning chains to uncover deep customer insights.

REASONING METHODOLOGY:
You follow a precise 5-step reasoning chain for every insight:

1. OBSERVATION: What specific evidence do I see in the business context?
2. PATTERN RECOGNITION: What psychological or business patterns does this connect to?
3. ROOT CAUSE ANALYSIS: What deeper drivers explain this pattern?
4. CONTRADICTION TESTING: What evidence would contradict this insight?
5. CONFIDENCE ASSESSMENT: How certain am I and what could improve certainty?

DOMAIN EXPERTISE ({industry_context}):
Key Psychology Drivers: {framework['psychology_drivers']}
{f"Business Challenge Patterns: {framework.get('business_challenges', [])}" if 'business_challenges' in framework else ""}

QUALITY STANDARDS:
- Every insight must follow the 5-step reasoning chain
- Customer language must be specific, not generic ("I'm drowning in compliance paperwork" not "I have challenges")
- Confidence scores must be justified with explicit reasoning
- Contradictions must be actively identified and addressed

You produce insights that would pass peer review at McKinsey, BCG, or Bain.""",
            
            tools=[self.web_search, self.website_tool],
            llm=self.reasoning_llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_structured_reasoning_task(self, business_context, industry_context):
        """Create task with structured reasoning requirements"""
        
        framework = self.reasoning_frameworks.get(industry_context, self.reasoning_frameworks["general_business"])
        
        return Task(
            description=f"""
            STRUCTURED REASONING ANALYSIS FOR: {business_context.get('company_name', 'Business')}
            
            BUSINESS CONTEXT TO ANALYZE:
            {json.dumps(business_context, indent=2)}
            
            REASONING CHAIN REQUIREMENTS:
            For each major insight, you must follow this exact structure:
            
            INSIGHT: [Clear, specific insight statement]
            
            REASONING CHAIN:
            1. OBSERVATION: [Specific evidence from context that led to this insight]
            2. PATTERN: [What known psychological/business pattern this connects to]
            3. ROOT CAUSE: [Deeper psychological or business driver explaining this pattern]
            4. CONTRADICTION TEST: [What evidence would contradict this? Where might this not apply?]
            5. CONFIDENCE: [0-100 score with explicit justification]
            
            CUSTOMER VOICE: [Specific quote showing how they would express this - must sound authentic]
            
            REQUIRED ANALYSIS AREAS:
            
            A. TARGET CUSTOMER PSYCHOLOGY
            Apply reasoning chains to analyze:
            - Core identity and self-perception
            - Primary emotional drivers from domain framework: {framework['psychology_drivers']}
            - Hidden psychological conflicts or tensions
            - Decision-making triggers and barriers
            
            B. BUSINESS PAIN ANALYSIS  
            Apply reasoning chains to uncover:
            - Surface-level operational frustrations
            - Deeper strategic or emotional pains
            - Pains they deny or minimize but still feel
            - Root causes of each pain pattern
            
            C. DESIRE AND ASPIRATION MAPPING
            Apply reasoning chains to identify:
            - Stated goals vs actual underlying desires
            - Status and achievement motivations
            - Security and control needs
            - Latent needs they don't recognize yet
            
            D. VOICE OF CUSTOMER LANGUAGE
            For each insight area, provide:
            - Exact phrases they use (not generic marketing speak)
            - Emotional tone and urgency level
            - Industry-specific terminology and metaphors
            - Questions they ask when seeking solutions
            
            E. ACTIONABLE INTELLIGENCE
            Synthesize reasoning into:
            - 3 highest-confidence insights with business implications
            - 2 biggest reasoning gaps requiring additional research
            - 5 specific marketing/positioning recommendations
            
            CRITICAL QUALITY REQUIREMENT:
            Every single insight must include the complete 5-step reasoning chain. No exceptions.
            Generic insights without reasoning chains will be rejected.
            """,
            
            expected_output="""
            Structured JSON analysis with complete reasoning chains:
            
            {
              "analysis_summary": {
                "target_customer": "[Specific customer description]",
                "industry_context": "[Industry-specific factors identified]",
                "confidence_overview": "[Overall confidence in analysis with justification]"
              },
              
              "customer_psychology": {
                "core_identity": {
                  "insight": "[Specific insight about how they see themselves]",
                  "reasoning_chain": {
                    "observation": "[Evidence from context]",
                    "pattern": "[Psychological pattern identified]", 
                    "root_cause": "[Deeper driver]",
                    "contradiction_test": "[What could contradict this]",
                    "confidence": "[0-100 with justification]"
                  },
                  "customer_voice": "[Authentic quote showing this psychology]"
                },
                "emotional_drivers": [
                  {
                    "driver": "[Specific emotional driver]",
                    "reasoning_chain": { [Complete 5-step chain] },
                    "customer_voice": "[How they express this]"
                  }
                ],
                "decision_psychology": {
                  "triggers": "[What motivates action with reasoning chain]",
                  "barriers": "[What prevents action with reasoning chain]"
                }
              },
              
              "pain_analysis": [
                {
                  "pain_category": "[Surface/Deep/Hidden]",
                  "specific_pain": "[Exact pain description]",
                  "reasoning_chain": { [Complete 5-step chain] },
                  "customer_voice": "[How they describe this pain]",
                  "business_impact": "[Why this matters for marketing]"
                }
              ],
              
              "desire_mapping": [
                {
                  "desire_type": "[Stated/Underlying/Latent]", 
                  "specific_desire": "[Exact desire description]",
                  "reasoning_chain": { [Complete 5-step chain] },
                  "customer_voice": "[How they express this desire]"
                }
              ],
              
              "voice_of_customer": {
                "pain_language": ["[5-7 authentic phrases for pains]"],
                "desire_language": ["[5-7 authentic phrases for desires]"],
                "decision_language": ["[5-7 phrases showing readiness to buy]"],
                "tone_analysis": "[Overall communication style and emotional tone]"
              },
              
              "actionable_intelligence": {
                "top_insights": [
                  {
                    "insight": "[High-confidence insight]",
                    "confidence": "[Score with justification]",
                    "business_application": "[How to use this in marketing]"
                  }
                ],
                "research_gaps": ["[What needs more investigation]"],
                "marketing_recommendations": [
                  {
                    "recommendation": "[Specific marketing action]",
                    "reasoning": "[Why this will work based on psychology]",
                    "implementation": "[How to execute this]"
                  }
                ]
              },
              
              "reasoning_quality_check": {
                "insights_with_complete_chains": "[Count]",
                "average_confidence": "[0-100]",
                "contradiction_tests_performed": "[Count]",
                "authenticity_assessment": "[How authentic does customer voice sound]"
              }
            }
            """,
            
            agent=self.create_precision_reasoning_agent(industry_context)
        )
    
    def execute_precision_reasoning(self, business_context):
        """Execute precision reasoning analysis with quality controls"""
        
        print("🧠 Executing Precision Reasoning Analysis...")
        
        # Detect industry context for domain-specific reasoning
        industry_context = self.detect_industry_context(business_context)
        print(f"📊 Industry Context Detected: {industry_context}")
        
        # Create reasoning task
        reasoning_task = self.create_structured_reasoning_task(business_context, industry_context)
        
        # Execute analysis
        crew = Crew(
            agents=[self.create_precision_reasoning_agent(industry_context)],
            tasks=[reasoning_task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Quality validation
        quality_score = self.validate_reasoning_quality(result)
        
        return {
            "reasoning_analysis": result,
            "industry_context": industry_context,
            "quality_assessment": quality_score,
            "methodology": "Structured Chain-of-Thought Reasoning with Domain Expertise"
        }
    
    def validate_reasoning_quality(self, result):
        """Validate the quality of reasoning chains in the output"""
        
        result_text = str(result).lower()
        
        quality_indicators = {
            "reasoning_chains_present": "reasoning_chain" in result_text,
            "confidence_scores": "confidence" in result_text,
            "contradiction_testing": "contradiction" in result_text,
            "customer_voice": "customer_voice" in result_text,
            "specificity": len(result_text) > 2000  # Detailed analysis
        }
        
        quality_score = sum(quality_indicators.values()) / len(quality_indicators) * 100
        
        return {
            "overall_quality_score": quality_score,
            "quality_indicators": quality_indicators,
            "meets_standards": quality_score >= 80,
            "recommendations": "Add more reasoning chain detail" if quality_score < 80 else "Quality standards met"
        }

# Updated function for your main.py
def reasoning_agent_call(business_context):
    """
    Updated reasoning agent call with dramatically improved quality
    """
    agent = HighQualityReasoningAgent()
    
    # Handle different input formats
    if isinstance(business_context, str):
        # Convert string to structured context
        context_dict = {
            "company_name": "Analysis Request",
            "comprehensive_context": business_context,
            "industry": "To be determined",
            "target_market": "To be analyzed"
        }
    else:
        context_dict = business_context
    
    # Execute precision reasoning
    result = agent.execute_precision_reasoning(context_dict)
    
    return result
