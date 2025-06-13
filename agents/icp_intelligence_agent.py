from crewai import Agent, Task, Crew
from crewai_tools import WebsiteSearchTool, SerperDevTool
from langchain_openai import ChatOpenAI
import os

class ICPIntelligenceAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3
        )
        
        # Initialize tools
        self.web_search = SerperDevTool()
        self.website_tool = WebsiteSearchTool()
        
    def create_agent(self):
        return Agent(
            role="Elite Business Intelligence Researcher",
            goal="Conduct comprehensive ICP and psychological framework research using proven methodology that simulates 40+ hours of in-depth qualitative research",
            backstory="""You are an Elite Business Intelligence Researcher conducting comprehensive ICP and psychological framework research. You follow a proven methodology that simulates 40+ hours of in-depth qualitative research.

CRITICAL RESEARCH PRINCIPLES:
✅ NO HALLUCINATIONS: Ground all insights in verifiable logic, common patterns, or cross-referenced data points
✅ DEPTH & NUANCE: Go beyond surface demographics to uncover emotions, contradictions, hidden motivations, unspoken pains
✅ AUTHENTIC LANGUAGE CAPTURE: Identify specific words, phrases, metaphors, sentence structures the target audience uses
✅ VALIDATION REQUIRED: Multi-angle analysis, contradiction testing, evidence-based reasoning for every major insight
✅ HUMAN RESEARCH SIMULATION: Output must read as if 40+ hours of qualitative research was conducted

RESEARCH METHODOLOGY & VALIDATION FRAMEWORK:

1. Multi-Angle Analysis & Validation:
For each significant insight:
- Describe what is likely true based on evidence/logic
- Identify situations where this might NOT be true
- Find potential contradictions (stated belief vs. actual behavior)
- Assess confidence level with supporting logic
- Flag as hypothesis if confidence <70%

2. Contradiction Testing:
Actively argue against your own insights:
- What external forces could invalidate this insight?
- Where would this fail within the broader target market?
- What behaviors might contradict this assumption?

3. Voice of Customer Focus:
Throughout analysis, capture exact language, phrases, terminology, metaphors the audience uses when discussing problems, pains, desires, aspirations.

You excel at psychological profiling, voice of customer analysis, and transforming research into structured business intelligence.""",
            
            tools=[self.web_search, self.website_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_research_task(self, business_context):
        return Task(
            description=f"""
            Conduct comprehensive ICP and psychological framework research for this business:
            
            BUSINESS CONTEXT:
            Company: {business_context['company_name']}
            Industry: {business_context['industry']}
            Offering: {business_context.get('product_service', 'Not specified')}
            Target Market: {business_context['target_market']}
            Current Challenges: {business_context['current_challenges']}
            Marketing Goal: Generate qualified leads and improve messaging
            
            ICP HYPOTHESIS:
            Role/Title: To be determined through research
            Assumed Pains: {business_context['current_challenges']}
            Assumed Desires: {business_context.get('assumptions', 'To be researched')}
            
            COMPREHENSIVE RESEARCH EXECUTION:
            
            PART A: FOUNDATIONAL ICP DEVELOPMENT
            Step 1: Refine & Expand Baseline Profile
            - Refine ICP definition (Role, Demographics, Psychographics) based on input + knowledge
            - Identify common assumptions about this profile within their industry
            - Analyze how they perceive themselves vs. how outsiders perceive them
            - Apply validation & contradiction testing
            
            Step 2: Deep Dive - Pains, Problems & Frustrations
            Identify pains relevant to the offering in layers:
            - Surface-level/day-to-day operational struggles
            - Deeper, unstated emotional or strategic pains
            - Pains they deny or downplay but still feel
            - Root causes and consequences in their context
            - Specific words/phrases they use to describe pains
            
            Step 3: Deep Dive - Desires, Aspirations & Motivations
            Analyze motivations/desires relevant to offering in layers:
            - Stated goals/what they say they want
            - Actual underlying desires/what they really want
            - Potential latent needs/what they need but don't realize
            - Core psychological drivers behind desires
            - Specific language they use for aspirations/goals
            
            Step 4: Voice of Customer Language Synthesis
            - Key language patterns: keywords, jargon, metaphors, sentence structures
            - Pain Language Lexicon: words/phrases for frustration, challenges, problems
            - Desire Language Lexicon: words/phrases for aspirations, goals, outcomes
            - Tone & Style: typical tone and communication style
            
            PART B: PSYCHOLOGICAL FRAMEWORK ANALYSIS
            Step 5: Jungian Archetype Analysis
            - Identity & Self-Perception
            - Dominant Archetypes
            - Language reflecting archetypes
            
            Step 6: LAB Profile Analysis
            - Motivation Direction, Source, Mode, Process, Proactivity, Communication Style
            - Language revealing LAB preferences
            
            Step 7: Deep Desires & Motivational Drivers
            - Analysis across Significance, Connection, Power/Control, Growth, Security, Variety, Contribution
            - Dominant desires and conflicts
            - Language expressing desires
            
            Step 8: Jobs-To-Be-Done Purchase Psychology
            - Core Job Analysis (Functional, Social, Emotional)
            - Competition/Current Solution Analysis
            - Triggers & Purchase Commitment Factors
            - Objection & Hesitation Analysis
            - Language for JTBD, frustrations, readiness
            
            Step 9: Cognitive Biases & Decision Shortcuts
            - Authority, Social Proof, Scarcity/Loss Aversion, Anchoring, Confirmation, Status Quo biases
            - Language revealing biases
            
            Step 10: Influence & Authority Triggers
            - Authority & Compliance Analysis
            - Resistance & Trust-Building Factors
            - Language indicating trust, resistance, action
            
            PART C: VOICE OF CUSTOMER LANGUAGE MAPS
            Step 11: Funnel Stage Language Patterns
            
            11A: TOFU - Attention & Awareness
            - Problem Recognition Language
            - Pain Point Articulation
            - Initial Solution Seeking
            - Language Map: quotes, terms, questions, tone/urgency
            
            11B: MOFU - Consideration & Evaluation
            - Solution Evaluation Language
            - Comparison Terminology
            - Objection Articulation
            - Language Map: quotes, criteria, objections, trust indicators
            
            11C: BOFU - Decision & Action
            - Decision Trigger Language
            - Commitment Terminology
            - Final Hesitation Language
            - Language Map: quotes, action terms, reassurance needs
            """,
            
            expected_output="""
            A comprehensive JSON-structured research report containing:
            
            {
              "research_summary": {
                "methodology_applied": "Comprehensive ICP & Psychological Framework Research (40+ hours simulated)",
                "overall_confidence": [0-100],
                "validation_approach": "Multi-angle analysis, contradiction testing, evidence-based reasoning",
                "research_depth": "Surface + Deep + Hidden layers analyzed"
              },
              
              "foundational_icp": {
                "refined_profile": {
                  "role_title": "Specific role with context",
                  "demographics": {
                    "age_range": "X-Y years",
                    "location": "Geographic focus", 
                    "company_size": "Employee/revenue range",
                    "experience": "Years in role/industry",
                    "data_basis": "Based on industry patterns and role requirements",
                    "confidence": [0-100]
                  },
                  "psychographics": {
                    "self_perception": "How they see themselves",
                    "external_perception": "How others see them", 
                    "identity_contradictions": "Gaps between perceptions",
                    "confidence": [0-100]
                  }
                }
              },

              "pain_analysis": {
                "surface_pains": [
                  {
                    "pain_description": "Day-to-day operational struggle",
                    "customer_language": ["specific phrases they use"],
                    "frequency": "How often experienced",
                    "intensity": "High/Medium/Low impact",
                    "confidence": [0-100]
                  }
                ],
                "deeper_pains": [
                  {
                    "pain_description": "Unstated emotional/strategic pain",
                    "customer_language": ["how they express this subtly"],
                    "root_cause": "Underlying driver",
                    "consequences": "What happens if unresolved",
                    "confidence": [0-100]
                  }
                ],
                "pain_language_lexicon": {
                  "frustration_words": ["waste", "constantly", "struggling"],
                  "problem_phrases": ["can't seem to", "always having to"],
                  "intensity_indicators": ["overwhelming", "exhausting", "frustrated"],
                  "confidence": [0-100]
                }
              },

              "desire_analysis": {
                "stated_goals": [
                  {
                    "goal_description": "What they publicly say they want",
                    "customer_language": ["exact phrases used"],
                    "context": "When/where they express this",
                    "confidence": [0-100]
                  }
                ],
                "underlying_desires": [
                  {
                    "desire_description": "What they really want underneath",
                    "connection_to_stated": "How it relates to public goals",
                    "customer_language": ["subtle expressions"],
                    "psychological_driver": "Core human need being met",
                    "confidence": [0-100]
                  }
                ]
              },

              "psychological_frameworks": {
                "jungian_archetypes": {
                  "dominant_archetype": {
                    "archetype": "The Achiever",
                    "evidence": "Language patterns and behavioral indicators",
                    "customer_language": ["achievement-focused phrases"],
                    "business_implications": "How this affects purchasing decisions",
                    "confidence": [0-100]
                  }
                },
                "cognitive_biases": [
                  {
                    "bias": "Authority Bias",
                    "strength": "Strong/Medium/Weak",
                    "evidence": "Behavioral indicators",
                    "customer_language": ["authority-seeking phrases"],
                    "business_application": "How to leverage this",
                    "confidence": [0-100]
                  }
                ]
              },

              "voice_of_customer_maps": {
                "tofu_language": {
                  "problem_recognition": {
                    "phrases": ["starting to realize", "noticing that"],
                    "questions": ["Is there a better way to", "Why do I keep"],
                    "tone": "Frustrated, seeking, uncertain",
                    "confidence": [0-100]
                  }
                },
                "mofu_language": {
                  "evaluation_criteria": {
                    "must_haves": ["has to integrate with", "needs to handle"],
                    "comparison_terms": ["better than", "unlike X"],
                    "confidence": [0-100]
                  }
                },
                "bofu_language": {
                  "decision_triggers": {
                    "commitment_phrases": ["ready to move forward", "let's do this"],
                    "urgency_indicators": ["need this now", "can't wait"],
                    "confidence": [0-100]
                  }
                }
              },

              "research_validation": {
                "confidence_by_section": {
                  "foundational_icp": [0-100],
                  "pain_analysis": [0-100],
                  "desire_analysis": [0-100],
                  "psychological_frameworks": [0-100],
                  "voice_of_customer": [0-100]
                },
                "research_gaps": [
                  "Areas needing additional validation"
                ],
                "quality_flags": [
                  "Insights flagged for additional research"
                ]
              }
            }
            
            Provide specific, detailed insights with authentic customer language throughout. Include confidence scores for every major insight. Focus on business-actionable intelligence, not generic market research.
            """,
            
            agent=self.create_agent()
        )

# Example usage function  
def run_icp_research(business_context):
    """
    Run comprehensive ICP research for a given business context using enhanced methodology
    """
    icp_agent = ICPIntelligenceAgent()
    
    # Create the research task
    research_task = icp_agent.create_research_task(business_context)
    
    # Create and run the crew
    crew = Crew(
        agents=[icp_agent.create_agent()],
        tasks=[research_task],
        verbose=True
    )
    
    # Execute the research
    result = crew.kickoff()
    return result
