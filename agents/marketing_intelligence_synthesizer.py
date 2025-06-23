from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import json

class MarketingIntelligenceSynthesizer:
    def __init__(self):
        # Use same model as your other successful agents
        self.marketing_llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7  # Balanced for strategic thinking
        )
        
        self.copy_llm = ChatOpenAI(
            model="gpt-4o-mini", 
            temperature=0.8  # Higher for creative copy
        )
        
        # Marketing frameworks
        self.frameworks = {
            "PAS": "Problem-Agitate-Solve",
            "AIDA": "Attention-Interest-Desire-Action",
            "BAB": "Before-After-Bridge",
            "4Ps": "Promise-Picture-Proof-Push",
            "PASTOR": "Problem-Amplify-Story-Transformation-Offer-Response"
        }
        
        # Priority assets (optimized for token limits)
        self.priority_assets = {
            "headlines": 5,
            "ad_copy": 3,
            "email_sequence": 1,
            "landing_page": 1,
            "social_hooks": 3
        }
    
    def extract_marketing_intelligence(self, research_results, interview_results):
        """Extract key marketing data from research and interviews"""
        extraction_prompt = f"""
        Analyze this research and interview data to extract KEY marketing intelligence:
        
        RESEARCH DATA:
        {json.dumps(research_results, indent=2) if isinstance(research_results, dict) else str(research_results)[:3000]}
        
        INTERVIEW DATA:
        {json.dumps(interview_results, indent=2) if isinstance(interview_results, dict) else str(interview_results)[:3000]}
        
        Extract and return ONLY a valid JSON object with:
        {{
            "core_message": "The single most powerful message",
            "primary_pain_points": ["Top 3 pain points in customer language"],
            "primary_desires": ["Top 3 desires in customer language"],
            "emotional_triggers": ["Key emotional drivers"],
            "trust_factors": ["What builds trust"],
            "objections": ["Main objections to handle"],
            "transformation": {{
                "from": "Current painful state",
                "to": "Desired outcome state"
            }},
            "unique_value": "What makes this solution different",
            "urgency_factors": ["Why act now"],
            "social_proof_needs": ["Types of proof that matter"]
        }}
        """
        
        response = self.marketing_llm.invoke(extraction_prompt)
        
        try:
            if hasattr(response, 'content'):
                content = response.content
            else:
                content = str(response)
            
            # Extract JSON
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(content)
            
        except Exception as e:
            print(f"Error extracting intelligence: {e}")
            return self._get_fallback_intelligence()
    
    def _get_fallback_intelligence(self):
        """Fallback if extraction fails"""
        return {
            "core_message": "Transform your business",
            "primary_pain_points": ["Struggling with growth", "Feeling overwhelmed", "Lacking clarity"],
            "primary_desires": ["Achieve success", "Find balance", "Gain confidence"],
            "emotional_triggers": ["Frustration", "Hope", "Ambition"],
            "trust_factors": ["Proven results", "Expert guidance", "Peer success"],
            "objections": ["Cost concerns", "Time investment", "Will it work"],
            "transformation": {
                "from": "Struggling and overwhelmed",
                "to": "Confident and successful"
            },
            "unique_value": "Comprehensive solution",
            "urgency_factors": ["Limited time", "Competition growing", "Opportunity cost"],
            "social_proof_needs": ["Testimonials", "Case studies", "Results data"]
        }
    
    def create_strategy_synthesizer(self):
        """Agent that creates the overall marketing strategy"""
        return Agent(
            role="Master Marketing Strategist",
            goal="Synthesize research insights into a coherent marketing strategy with clear messaging hierarchy",
            backstory="""You are a world-class marketing strategist who has created campaigns for hundreds of successful companies.

STRATEGIC EXPERTISE:
✅ Message Architecture: You create clear messaging hierarchies that guide all marketing
✅ Positioning Mastery: You find unique market positions that differentiate offerings
✅ Psychological Insight: You understand what drives purchase decisions
✅ Campaign Integration: You ensure all assets work together cohesively

You excel at transforming complex research into simple, powerful marketing strategies that convert.""",
            
            llm=self.marketing_llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_copywriting_specialist(self):
        """Agent that writes all marketing copy"""
        return Agent(
            role="Elite Direct Response Copywriter",
            goal="Transform marketing strategy into high-converting copy that uses authentic customer language",
            backstory="""You are an elite direct response copywriter trained by the legends: 
Gary Halbert, Eugene Schwartz, David Ogilvy, and Clayton Makepeace.

COPYWRITING MASTERY:
✅ Headlines: You write headlines that stop scrollers and demand attention
✅ Emotional Resonance: You write copy that touches deep emotional drivers
✅ Voice Matching: You mirror the exact language customers use
✅ Conversion Focus: Every word drives toward the desired action

You've written copy that has generated millions in revenue. You know that great copy 
enters the conversation already happening in the customer's mind.""",
            
            llm=self.copy_llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_strategy_task(self, marketing_intelligence, business_context):
        """Create task for marketing strategy development"""
        return Task(
            description=f"""
            Create a MASTER MARKETING STRATEGY based on deep customer insights
            
            MARKETING INTELLIGENCE:
            {json.dumps(marketing_intelligence, indent=2)}
            
            BUSINESS CONTEXT:
            {business_context}
            
            DEVELOP COMPREHENSIVE STRATEGY:
            
            1. CORE POSITIONING
               - Unique value proposition using their language
               - Market position that's defensible
               - Key differentiators that matter
            
            2. MESSAGE ARCHITECTURE
               - Primary message (one clear point)
               - Supporting messages (3-5 pillars)
               - Proof points for each message
            
            3. CUSTOMER JOURNEY MESSAGING
               - Awareness stage: What grabs attention
               - Consideration: What builds interest
               - Decision: What triggers action
               - Retention: What creates loyalty
            
            4. EMOTIONAL JOURNEY MAP
               - Current emotional state
               - Emotional transitions needed
               - Desired emotional outcome
            
            5. CAMPAIGN THEMES
               - 3 powerful campaign angles
               - Why each will resonate
               - How to execute each
            """,
            
            expected_output="""
            Complete marketing strategy in JSON format:
            
            {
              "core_positioning": {
                "value_proposition": "Clear, compelling statement",
                "market_position": "How we're different",
                "key_differentiators": ["Differentiator 1", "Differentiator 2", "Differentiator 3"]
              },
              
              "message_architecture": {
                "primary_message": "The one thing to remember",
                "supporting_pillars": [
                  {
                    "pillar": "Pillar name",
                    "message": "Key message",
                    "proof": "Evidence/support"
                  }
                ],
                "tagline_options": ["Option 1", "Option 2", "Option 3"]
              },
              
              "customer_journey": {
                "awareness": {
                  "hook": "What stops them scrolling",
                  "message": "First thing they need to know"
                },
                "consideration": {
                  "message": "What makes them lean in",
                  "content_themes": ["Theme 1", "Theme 2"]
                },
                "decision": {
                  "trigger": "What makes them buy",
                  "urgency": "Why now"
                }
              },
              
              "campaign_angles": [
                {
                  "name": "Campaign angle name",
                  "hook": "Core hook",
                  "why_it_works": "Psychological reason",
                  "execution": "How to run it"
                }
              ]
            }
            """,
            
            agent=self.create_strategy_synthesizer()
        )
    
    def create_copywriting_task(self, strategy, marketing_intelligence):
        """Create task for copywriting"""
        return Task(
            description=f"""
            Write HIGH-CONVERTING MARKETING COPY based on strategy and customer insights
            
            MARKETING STRATEGY:
            {strategy}
            
            CUSTOMER INTELLIGENCE:
            {json.dumps(marketing_intelligence, indent=2)}
            
            CREATE THESE PRIORITY ASSETS:
            
            1. HEADLINES (5 Variants)
               - Use their exact pain language
               - Promise the transformation they want
               - Create curiosity or urgency
               - Test different emotional angles
            
            2. FACEBOOK AD COPY (3 Variants)
               - Hook: Stop the scroll
               - Story: Relate to their pain
               - Offer: Clear next step
               - Use PAS or AIDA framework
            
            3. EMAIL SEQUENCE (3-Part Welcome Series)
               - Email 1: Welcome & Quick Win
               - Email 2: Transformation Story
               - Email 3: Irresistible Offer
            
            4. LANDING PAGE HERO SECTION
               - Headline (benefit-focused)
               - Subheadline (expand/clarify)
               - Bullet benefits (3-5)
               - CTA button text
            
            5. SOCIAL MEDIA HOOKS (3 Variants)
               - Pattern interrupt openings
               - Native to platform style
               - Drive to next action
            
            COPYWRITING RULES:
            ✅ Use THEIR words, not yours
            ✅ Benefits before features
            ✅ Emotion drives logic justifies
            ✅ Specific beats generic
            ✅ Show transformation, not information
            """,
            
            expected_output="""
            Marketing copy assets in JSON format:
            
            {
              "headlines": [
                {
                  "headline": "Headline text",
                  "angle": "Emotional angle used",
                  "framework": "PAS/AIDA/etc"
                }
              ],
              
              "facebook_ads": [
                {
                  "variant": "A",
                  "hook": "Opening line",
                  "body": "Main ad copy",
                  "cta": "Call to action",
                  "emoji_enhanced": "Version with strategic emojis"
                }
              ],
              
              "email_sequence": [
                {
                  "email": 1,
                  "subject": "Subject line",
                  "preview": "Preview text",
                  "body": "Full email copy with formatting",
                  "cta": "Primary call to action"
                }
              ],
              
              "landing_page": {
                "headline": "Main headline",
                "subheadline": "Supporting subheadline",
                "bullets": [
                  "Benefit 1",
                  "Benefit 2",
                  "Benefit 3"
                ],
                "cta_button": "Button text",
                "above_fold": "Complete hero section copy"
              },
              
              "social_hooks": [
                {
                  "platform": "Instagram/Facebook/LinkedIn",
                  "hook": "Opening line",
                  "cta": "What to do next"
                }
              ]
            }
            """,
            
            agent=self.create_copywriting_specialist()
        )
    
    def synthesize_marketing_campaign(self, research_results, interview_results, business_context):
        """Main method to create complete marketing campaign"""
        
        print("🎯 Starting Marketing Intelligence Synthesis...")
        
        # Step 1: Extract marketing intelligence
        print("📊 Extracting marketing intelligence from research...")
        marketing_intelligence = self.extract_marketing_intelligence(
            research_results, 
            interview_results
        )
        
        # Step 2: Create marketing strategy
        print("🧠 Developing marketing strategy...")
        strategy_task = self.create_strategy_task(marketing_intelligence, business_context)
        strategy_crew = Crew(
            agents=[self.create_strategy_synthesizer()],
            tasks=[strategy_task],
            verbose=True
        )
        strategy_results = strategy_crew.kickoff()
        
        # Step 3: Create marketing copy
        print("✍️ Writing high-converting copy...")
        copy_task = self.create_copywriting_task(strategy_results, marketing_intelligence)
        copy_crew = Crew(
            agents=[self.create_copywriting_specialist()],
            tasks=[copy_task],
            verbose=True
        )
        copy_results = copy_crew.kickoff()
        
        return {
            "marketing_intelligence": marketing_intelligence,
            "marketing_strategy": strategy_results,
            "marketing_copy": copy_results,
            "synthesis_complete": True,
            "assets_created": [
                "5 Headlines",
                "3 Facebook Ads",
                "3-Email Welcome Series",
                "Landing Page Copy",
                "3 Social Media Hooks"
            ]
        }

# Main function for integration
def synthesize_marketing_intelligence(research_results, interview_results, business_context):
    """
    Create complete marketing campaign from research insights
    """
    synthesizer = MarketingIntelligenceSynthesizer()
    result = synthesizer.synthesize_marketing_campaign(
        research_results,
        interview_results, 
        business_context
    )
    return result
