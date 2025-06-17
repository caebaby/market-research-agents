from crewai import Agent, Task, Crew
from crewai_tools import WebsiteSearchTool, SerperDevTool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import json
import os

class DynamicInterviewAgent:
    def __init__(self):
        # GPT-4 for structured interviews
        self.interview_llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.3
        )
        
        # Claude for persona creation (better at character development)
        try:
            self.persona_llm = ChatAnthropic(
                model="claude-3-5-sonnet-20241022",
                temperature=0.4
            )
        except:
            # Fallback to GPT-4 if Claude not available
            self.persona_llm = ChatOpenAI(
                model="gpt-4",
                temperature=0.4
            )
        
        # Tools (if needed)
        self.web_search = SerperDevTool()
        self.website_tool = WebsiteSearchTool()
        
        # Base template questions
        self.base_questions = {
            "current_situation": [
                "Tell me about your biggest frustration with {CONTEXT} right now.",
                "Walk me through your worst day dealing with {CONTEXT} recently.",
                "What about {CONTEXT} keeps you up at night or worries you most?",
                "When you talk to others about {CONTEXT}, what do you complain about?",
                "What's the gap between where you are and where you want to be with {CONTEXT}?"
            ],
            "aspirations": [
                "What would your ideal {CONTEXT} situation look like?",
                "If you could wave a magic wand and fix one thing about {CONTEXT}, what would it be?",
                "What would make you feel like you've achieved your {CONTEXT} goals?",
                "What are you hoping to achieve with {CONTEXT} that you're not getting now?"
            ],
            "decision_psychology": [
                "Tell me about the last time you invested money in {CONTEXT} solutions.",
                "What made you finally decide to spend money on that {CONTEXT} solution?",
                "What almost stopped you from moving forward with that purchase?",
                "Who do you turn to for advice when making {CONTEXT} decisions?"
            ],
            "emotional_dynamics": [
                "How do you feel when you think about your current {CONTEXT} situation?",
                "What would your family/colleagues say about your {CONTEXT} challenges?",
                "When you succeed with {CONTEXT}, who do you want to share that with?"
            ]
        }
    
    def extract_context_from_research(self, research_results):
        """Extract context from research results using AI"""
        try:
            extraction_prompt = f"""
            Analyze this research data and extract the key context for follow-up interviews:
            
            RESEARCH DATA:
            {json.dumps(research_results, indent=2) if isinstance(research_results, dict) else str(research_results)}
            
            Extract and return ONLY a valid JSON object:
            {{
                "business_type": "B2B or B2C",
                "target_customer": "Primary customer description",
                "industry": "Industry context",
                "customer_context": "What defines the customer (professional context for B2B, lifestyle for B2C)",
                "company_offering": "What the company offers",
                "key_challenges": ["Top 3 challenges customers face"],
                "psychological_drivers": ["Top 3 psychological motivations"],
                "decision_context": "How customers make decisions"
            }}
            
            Use exact language from the research data.
            """
            
            context_response = self.interview_llm.invoke(extraction_prompt)
            
            if hasattr(context_response, 'content'):
                context_text = context_response.content
            else:
                context_text = str(context_response)
            
            # Extract JSON from response
            try:
                import re
                json_match = re.search(r'\{.*\}', context_text, re.DOTALL)
                if json_match:
                    context = json.loads(json_match.group())
                else:
                    context = json.loads(context_text)
                
                return context
                
            except json.JSONDecodeError:
                print(f"Failed to parse context extraction: {context_text}")
                return self._create_fallback_context()
            
        except Exception as e:
            print(f"Error extracting context: {e}")
            return self._create_fallback_context()
    
    def _create_fallback_context(self):
        """Create fallback context if extraction fails"""
        return {
            "business_type": "B2B",
            "target_customer": "Professional",
            "industry": "Business Services",
            "customer_context": "professional work",
            "company_offering": "business solutions",
            "key_challenges": ["operational challenges", "growth challenges", "efficiency challenges"],
            "psychological_drivers": ["professional success", "security", "recognition"],
            "decision_context": "professional purchasing decisions"
        }
    
    def contextualize_questions(self, context):
        """Adapt questions to the specific business context"""
        contextualized = {}
        
        # Determine the context placeholder replacement
        if context.get('business_type') == 'B2C':
            context_replacement = context.get('customer_context', 'your situation')
        else:
            context_replacement = context.get('customer_context', 'your work')
        
        for category, questions in self.base_questions.items():
            contextualized[category] = []
            for question in questions:
                contextualized_question = question.replace('{CONTEXT}', context_replacement)
                contextualized[category].append(contextualized_question)
        
        return contextualized
    
    def create_persona_generator(self, context):
        """Create agent to generate realistic personas based on context"""
        return Agent(
            role="Expert Customer Persona Generator",
            goal=f"Create 6-8 realistic {context['target_customer']} personas for interview simulation",
            backstory=f"""You are an expert at creating realistic customer personas for {context.get('industry', 'business')} companies.

CONTEXT:
• Target Customer: {context['target_customer']}
• Industry: {context.get('industry', 'Business')}
• Customer Context: {context['customer_context']}
• Key Challenges: {context['key_challenges']}
• Psychological Drivers: {context['psychological_drivers']}

Create personas that feel like real people with genuine complexity and authentic motivations. Each persona should be someone who would realistically be a customer and would provide unique insights in interviews.""",
            
            llm=self.persona_llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_interview_conductor(self, context):
        """Create agent to conduct interviews"""
        return Agent(
            role="Expert Interview Researcher",
            goal=f"Conduct insightful interviews with {context['target_customer']} personas to extract marketing intelligence",
            backstory=f"""You are an expert interviewer who specializes in {context.get('industry', 'business')} customer research.

INTERVIEW MISSION:
Extract deep insights about {context['target_customer']}s for marketing intelligence including:
• Authentic emotional language and expressions
• Real objections and concerns about solutions
• Decision-making psychology and triggers
• Trust-building requirements

You conduct natural conversations that reveal genuine insights about customer psychology, pain points, and buying behavior.""",
            
            llm=self.interview_llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_persona_simulator(self, context):
        """Create agent to simulate customer personas in interviews"""
        return Agent(
            role=f"Authentic {context['target_customer']} Persona Simulator",
            goal=f"Authentically embody {context['target_customer']} personas during interviews",
            backstory=f"""You are a master at embodying {context['target_customer']} personas in the {context.get('industry', 'business')} space.

When given a persona profile, you become that person completely:
• Use their authentic voice and communication style
• Express their genuine emotions and concerns about {context['customer_context']}
• Show realistic human complexity and contradictions
• Respond based on their specific psychology and situation

You make interviews feel like conversations with real people, revealing authentic insights about customer psychology.""",
            
            llm=self.interview_llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_persona_task(self, context):
        """Create task for persona generation"""
        return Task(
            description=f"""
            CREATE 6-8 REALISTIC {context['target_customer']} PERSONAS for interview simulation
            
            CONTEXT:
            • Target Customer: {context['target_customer']}
            • Industry: {context.get('industry', 'Business')}
            • Customer Context: {context['customer_context']}
            • Key Challenges: {context['key_challenges']}
            • Psychological Drivers: {context['psychological_drivers']}
            
            CREATE DIVERSE PERSONA TYPES:
            1. **Struggling {context['target_customer']}** (High frustration, seeking solutions)
            2. **Ambitious {context['target_customer']}** (Growth-focused, impatient for results)
            3. **Experienced {context['target_customer']}** (Veteran, skeptical of new solutions)
            4. **Overwhelmed {context['target_customer']}** (Stressed, needs simplification)
            5. **Successful but Plateaued {context['target_customer']}** (Doing well but stuck)
            6. **Cautious {context['target_customer']}** (Risk-averse, needs proof)
            7. **Tech-Savvy {context['target_customer']}** (Embraces new solutions)
            8. **Traditional {context['target_customer']}** (Prefers established approaches)
            
            FOR EACH PERSONA:
            • Detailed demographics and background
            • Current situation and challenges
            • Psychological profile and motivations
            • Communication style and preferences
            • Decision-making approach
            • Likely objections and concerns
            • Trust-building requirements
            """,
            
            expected_output=f"""
            Detailed persona profiles in JSON format:
            
            {{
              "context": {{
                "target_customer": "{context['target_customer']}",
                "industry": "{context.get('industry', 'Business')}",
                "customer_context": "{context['customer_context']}"
              }},
              "personas": [
                {{
                  "persona_id": "persona_001",
                  "persona_type": "Struggling {context['target_customer']}",
                  "name": "[First name + Last initial]",
                  "demographics": {{
                    "age": "[Specific age]",
                    "background": "[Relevant background info]",
                    "situation": "[Current life/work situation]"
                  }},
                  "psychology": {{
                    "primary_motivations": ["[Top motivational drivers]"],
                    "main_concerns": ["[Key worries and fears]"],
                    "decision_style": "[How they make decisions]",
                    "communication_style": "[How they communicate]"
                  }},
                  "challenges": {{
                    "current_problems": ["[Specific problems they face]"],
                    "frustration_level": "[1-10 with description]",
                    "impact_on_life": "[How problems affect them]"
                  }},
                  "solution_experience": {{
                    "past_attempts": ["[Previous solutions tried]"],
                    "typical_objections": ["[Common concerns they raise]"],
                    "trust_requirements": ["[What they need to trust a solution]"],
                    "decision_factors": ["[What influences their choices]"
                  }},
                  "interview_profile": {{
                    "communication_style": "[How they speak in interviews]",
                    "openness_level": "[How forthcoming they are]",
                    "emotional_triggers": ["[Topics that get strong reactions]"],
                    "likely_quotes": ["[Phrases they might use]"]
                  }}
                }}
              ]
            }}
            """,
            
            agent=self.create_persona_generator(context)
        )
    
    def create_interview_task(self, context, personas_data, contextualized_questions):
        """Create task for conducting multiple interviews"""
        return Task(
            description=f"""
            CONDUCT MULTIPLE INTERVIEW SESSIONS with {context['target_customer']} personas
            
            INTERVIEW MISSION:
            Extract marketing intelligence through natural conversations that reveal:
            • Authentic emotional language and pain expressions
            • Real objections and decision-making psychology  
            • Trust-building requirements and credibility factors
            • Buying triggers and timing considerations
            
            PERSONAS TO INTERVIEW:
            {personas_data}
            
            INTERVIEW APPROACH:
            For each persona, conduct 2-3 different interview sessions:
            
            **Session A: Problem-Focused** (Emotional, frustrated state)
            - Focus on pain points and frustrations
            - Explore emotional impact and stress
            - Uncover hidden struggles they don't usually admit
            
            **Session B: Solution-Oriented** (Analytical, evaluative state)  
            - Focus on what they want and need in solutions
            - Explore decision criteria and evaluation process
            - Understand their requirements and deal-breakers
            
            **Session C: Experience-Based** (Reflective, storytelling state)
            - Focus on past experiences with similar solutions
            - Learn from their successes and disappointments
            - Understand what creates trust vs. skepticism
            
            INTERVIEW QUESTIONS TO USE:
            {json.dumps(contextualized_questions, indent=2)}
            
            INSIGHT EXTRACTION REQUIREMENTS:
            For each interview, capture:
            ✅ Exact quotes and authentic language patterns
            ✅ Emotional expressions and intensity levels  
            ✅ Specific objections and concerns raised
            ✅ Decision-making factors and timing
            ✅ Trust-building elements that resonate
            ✅ Competitive positioning opportunities
            """,
            
            expected_output=f"""
            Complete interview intelligence in JSON format:
            
            {{
              "interview_summary": {{
                "total_personas": "[Number of personas interviewed]",
                "sessions_per_persona": "2-3 different interview sessions",
                "total_interviews": "[Total interview sessions conducted]",
                "insight_quality": "[Assessment of insights gathered]"
              }},
              
              "persona_interviews": [
                {{
                  "persona_id": "persona_001",
                  "persona_summary": "[Brief persona description]",
                  
                  "interview_sessions": [
                    {{
                      "session_type": "Problem-Focused",
                      "emotional_state": "Frustrated, stressed, seeking relief",
                      "key_insights": {{
                        "pain_language": ["[Exact phrases used to describe problems]"],
                        "emotional_expressions": ["[How they express frustration/stress]"],
                        "hidden_struggles": ["[Problems they admit when vulnerable]"],
                        "impact_statements": ["[How problems affect their life/work]"]
                      }},
                      "interview_highlights": [
                        {{
                          "question": "[Question asked]",
                          "response": "[Authentic response with exact language]",
                          "insight": "[Marketing insight from this exchange]",
                          "emotional_intensity": "[1-10 scale]"
                        }}
                      ]
                    }},
                    {{
                      "session_type": "Solution-Oriented", 
                      "emotional_state": "Analytical, hopeful, evaluative",
                      "key_insights": {{
                        "solution_criteria": ["[What they look for in solutions]"],
                        "decision_factors": ["[How they evaluate options]"],
                        "deal_breakers": ["[What would make them say no]"],
                        "success_metrics": ["[How they measure solution success]"]
                      }}
                    }},
                    {{
                      "session_type": "Experience-Based",
                      "emotional_state": "Reflective, cautious, wise",  
                      "key_insights": {{
                        "past_experiences": ["[Stories about previous solutions]"],
                        "trust_builders": ["[What creates credibility]"],
                        "red_flags": ["[Warning signs they watch for]"],
                        "buying_lessons": ["[What experience taught them]"]
                      }}
                    }}
                  ],
                  
                  "persona_intelligence": {{
                    "consistent_patterns": ["[What they said across all sessions]"],
                    "emotional_variations": ["[How mood affected responses]"],
                    "objection_evolution": ["[How objections emerged and changed]"],
                    "authentic_voice": ["[Most genuine language captured]"],
                    "marketing_angles": ["[Best approaches for this persona type]"]
                  }}
                }}
              ],
              
              "marketing_intelligence": {{
                "universal_pain_language": ["[Pain expressions used by multiple personas]"],
                "common_objections": ["[Objections shared across personas]"],
                "decision_triggers": ["[Factors that drive action across segments]"],
                "trust_requirements": ["[Universal credibility builders]"],
                "segment_differences": ["[How different persona types vary]"],
                "campaign_opportunities": ["[Marketing angles revealed through interviews]"]
              }},
              
              "campaign_ready_insights": {{
                "headline_concepts": ["[Headlines using authentic customer language]"],
                "pain_point_messaging": ["[Problem descriptions in their voice]"],
                "solution_positioning": ["[How to position offering based on insights]"],
                "objection_handling": ["[Responses to specific concerns raised]"],
                "trust_building_strategy": ["[How to establish credibility quickly]"],
                "call_to_action_approaches": ["[CTA styles that match decision psychology]"]
              }}
            }}
            """,
            
            agent=self.create_interview_conductor(context)
        )
    
    def execute_interview_intelligence(self, research_results):
        """Execute the complete interview intelligence process"""
        
        print("🎭 Starting Interview Intelligence Process...")
        
        # Step 1: Extract context from research
        print("📋 Step 1: Extracting context from research findings...")
        context = self.extract_context_from_research(research_results)
        print(f"   Target Customer: {context['target_customer']}")
        print(f"   Industry: {context.get('industry', 'Business')}")
        print(f"   Context: {context['customer_context']}")
        
        # Step 2: Contextualize interview questions
        print("❓ Step 2: Adapting interview questions...")
        contextualized_questions = self.contextualize_questions(context)
        
        # Step 3: Generate personas
        print("👥 Step 3: Creating realistic customer personas...")
        persona_task = self.create_persona_task(context)
        persona_crew = Crew(
            agents=[self.create_persona_generator(context)],
            tasks=[persona_task],
            verbose=True
        )
        personas_result = persona_crew.kickoff()
        
        # Step 4: Conduct interviews
        print("🎤 Step 4: Conducting multiple interview sessions...")
        interview_task = self.create_interview_task(context, personas_result, contextualized_questions)
        interview_crew = Crew(
            agents=[
                self.create_interview_conductor(context),
                self.create_persona_simulator(context)
            ],
            tasks=[interview_task],
            verbose=True
        )
        interview_results = interview_crew.kickoff()
        
        return {
            "context_extracted": context,
            "personas_created": personas_result,
            "interview_intelligence": interview_results,
            "process_summary": f"Interview intelligence for {context['target_customer']} in {context.get('industry', 'business')}",
            "methodology": "Multiple sessions per persona with different emotional states and focuses",
            "marketing_readiness": "Authentic language and objection handling insights ready for campaigns"
        }

# Main function for integration
def dynamic_interview_intelligence(research_results):
    """
    Execute interview intelligence based on research results
    """
    agent = DynamicInterviewAgent()
    result = agent.execute_interview_intelligence(research_results)
    return result
