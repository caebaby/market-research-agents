# conversion_copy_agent.py
# Tactical conversion copy generator based on deep market research

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import json

class ConversionCopyAgent:
    def __init__(self):
        # Use different temperatures for different copy types
        self.tofu_llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.8  # Higher creativity for hooks/headlines
        )
        
        self.mofu_llm = ChatOpenAI(
            model="gpt-4o-mini", 
            temperature=0.6  # Balanced for persuasion
        )
        
        self.bofu_llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.4  # Lower for conversion precision
        )
    
    def generate_conversion_assets(self, research_data, business_context):
        """
        Generate micro-testable conversion assets from research insights
        """
        
        print("🎯 Generating Tactical Conversion Assets...")
        
        # Phase 1: TOFU Micro-Test Assets (MintCRO Style)
        tofu_assets = self.create_tofu_microtests(research_data, business_context)
        
        # Phase 2: MOFU Conversion Mechanisms
        mofu_assets = self.create_mofu_conversion_mechanisms(research_data, tofu_assets)
        
        # Phase 3: BOFU High-Converting Copy
        bofu_assets = self.create_bofu_conversion_copy(research_data, mofu_assets)
        
        return {
            "tofu_microtests": tofu_assets,
            "mofu_mechanisms": mofu_assets, 
            "bofu_conversion_copy": bofu_assets,
            "testing_framework": "micro_budget_tactical_approach"
        }
    
    def create_tofu_microtests(self, research_data, business_context):
        """
        Create MintCRO/Curt Maly style micro-budget test assets
        """
        
        tofu_agent = Agent(
            role="Elite TOFU Conversion Specialist",
            goal="Create micro-testable ad assets using MintCRO methodology for maximum engagement",
            backstory="""You are an elite direct response advertiser who specializes in micro-budget testing like MintCRO and Curt Maly. You create ad variations that get stopped-scroll attention and drive high-intent clicks for under $50 test budgets. 

Every headline you write is a testable hypothesis based on psychological triggers. You understand that TOFU is about interrupting patterns and creating curiosity gaps that compel clicks from high-intent prospects.

You write hooks that feel like the prospect's internal monologue, headlines that challenge assumptions, and angles that make competitors' approaches look amateur.""",
            llm=self.tofu_llm,
            verbose=True,
            allow_delegation=False
        )
        
        tofu_task = Task(
            description=f"""
            Create MICRO-TESTABLE TOFU assets using this research:
            
            RESEARCH INSIGHTS: {str(research_data)[:2000]}
            BUSINESS CONTEXT: {business_context}
            
            TACTICAL REQUIREMENTS:
            
            1. HEADLINE TEST VARIATIONS (8 different angles)
            For each headline provide:
            - The headline copy
            - Psychological trigger used
            - Target audience segment 
            - Success hypothesis (what response you expect)
            - Test budget recommendation ($25-50)
            - Success metrics (CTR%, CPM targets)
            
            2. HOOK-STORY-OFFER MICRO-TESTS (5 variations)
            For each provide:
            - Pattern interrupt hook (first 3 seconds)
            - Relatable story setup (seconds 4-8)
            - Clear offer/CTA (seconds 9-15)
            - Audience targeting suggestion
            - Expected cost per result
            
            3. SCROLL-STOPPING ANGLES (6 variations)
            Test these psychological angles:
            - Authority contradiction ("Everyone says X, but...")
            - Social proof specificity ("87% of [specific group]...")
            - Future pacing ("Imagine if...")
            - Problem agitation ("The real reason you...")
            - Curiosity gap ("What [industry] doesn't want you to know...")
            - Identity alignment ("If you're [specific identity]...")
            
            4. MICRO-TEST SUCCESS FRAMEWORK
            - Target CTR: 2.5%+ for cold traffic
            - Target CPM: Under $15
            - Target CPC: Under $2
            - Conversion rate expectation: 3-8%
            - Budget per test: $25-50
            - Test duration: 3-5 days
            
            Use exact customer language from research. Make each test hypothesis crystal clear.
            """,
            
            expected_output="""
            Tactical TOFU micro-test assets in JSON format:
            
            {
              "headline_tests": [
                {
                  "headline": "[Exact headline copy]",
                  "psychological_trigger": "[Fear/Curiosity/Authority/etc]",
                  "target_segment": "[Specific audience description]",
                  "success_hypothesis": "[What response we expect and why]",
                  "test_budget": "[Recommended $25-50]",
                  "success_metrics": {
                    "target_ctr": "[%]",
                    "target_cpm": "[$X]",
                    "target_cpc": "[$X]"
                  },
                  "customer_language_basis": "[Research insight this is based on]"
                }
              ],
              "hook_story_offer_tests": [
                {
                  "hook": "[First 3 seconds - pattern interrupt]",
                  "story": "[Seconds 4-8 - relatable setup]", 
                  "offer": "[Seconds 9-15 - clear CTA]",
                  "targeting": "[Audience suggestion]",
                  "expected_cost_per_result": "[$X]",
                  "psychological_flow": "[Why this sequence works]"
                }
              ],
              "scroll_stopping_angles": [
                {
                  "angle_type": "[Authority/Social/Curiosity/etc]",
                  "headline": "[Scroll-stopping headline]",
                  "subtext": "[Supporting copy]",
                  "cta": "[Action to take]",
                  "target_emotion": "[Fear/Desire/Curiosity]",
                  "test_hypothesis": "[Why this will work]"
                }
              ],
              "micro_test_framework": {
                "success_criteria": "Detailed success metrics",
                "testing_sequence": "Order to test these variations",
                "budget_allocation": "How to split $200-300 across tests",
                "winning_criteria": "When to scale vs kill tests"
              }
            }
            """,
            agent=tofu_agent
        )
        
        tofu_crew = Crew(
            agents=[tofu_agent],
            tasks=[tofu_task],
            verbose=True
        )
        
        return tofu_crew.kickoff()
    
    def create_mofu_conversion_mechanisms(self, research_data, tofu_results):
        """
        Create MOFU conversion mechanisms for engaged prospects
        """
        
        mofu_agent = Agent(
            role="Elite MOFU Conversion Architect", 
            goal="Design conversion mechanisms that transform interest into buying intent",
            backstory="""You are a master of middle-funnel conversion psychology. You understand that MOFU prospects are educated but skeptical. They need proof, specificity, and risk reversal.

You design conversion mechanisms like Eugene Schwartz and Gary Halbert - understanding that MOFU is about belief transformation. You create sequences that address skepticism, provide proof, and build irresistible desire.

Your mechanisms don't just educate - they systematically dismantle objections while building emotional commitment to the solution.""",
            llm=self.mofu_llm,
            verbose=True,
            allow_delegation=False
        )
        
        mofu_task = Task(
            description=f"""
            Design MOFU conversion mechanisms based on:
            
            RESEARCH DATA: {str(research_data)[:2000]}
            TOFU RESULTS: {str(tofu_results)[:1000]}
            
            CREATE HIGH-CONVERTING MOFU ASSETS:
            
            1. LEAD MAGNET CONVERSION MECHANISMS (3 options)
            - High-value, specific lead magnets
            - Opt-in page copy that converts 25%+
            - Email sequences for immediate nurturing
            
            2. WEBINAR/VSL CONVERSION FRAMEWORKS (2 options)
            - Hook that gets 60%+ show-up rates
            - Content that builds massive value and desire
            - Pitch sequence that converts 15-25%
            
            3. CASE STUDY/PROOF MECHANISMS (4 variations)
            - Specific, believable case studies
            - Social proof that overcomes skepticism  
            - Transformation stories that create desire
            
            4. OBJECTION-CRUSHING SEQUENCES (5 main objections)
            - Identify top 5 objections from research
            - Create content that dismantles each objection
            - Provide irrefutable proof points
            
            5. DESIRE-BUILDING MECHANISMS
            - Future state visualization content
            - Before/after transformation content
            - Identity shift positioning
            
            Each mechanism should include:
            - Exact copy/scripts
            - Psychological reasoning
            - Expected conversion rates
            - Success metrics
            """,
            
            expected_output="""
            MOFU conversion mechanisms in JSON format:
            
            {
              "lead_magnets": [
                {
                  "magnet_title": "[Specific, valuable title]",
                  "opt_in_headline": "[25%+ converting headline]",
                  "opt_in_copy": "[Complete opt-in page copy]",
                  "email_sequence": [
                    {
                      "email_number": 1,
                      "subject": "[Subject line]",
                      "copy": "[Full email copy]",
                      "goal": "[What this email achieves]"
                    }
                  ],
                  "conversion_psychology": "[Why this works]",
                  "expected_opt_in_rate": "[%]"
                }
              ],
              "webinar_vsl_frameworks": [
                {
                  "hook": "[60%+ show-up hook]",
                  "content_outline": "[Value-building content structure]",
                  "pitch_sequence": "[15-25% converting pitch]",
                  "psychological_flow": "[Why this converts]",
                  "expected_show_rate": "[%]",
                  "expected_conversion_rate": "[%]"
                }
              ],
              "proof_mechanisms": [
                {
                  "case_study_headline": "[Believable, specific result]",
                  "story_structure": "[Complete case study]",
                  "proof_points": "[Specific evidence]",
                  "emotional_triggers": "[Why this creates desire]"
                }
              ],
              "objection_crushing": [
                {
                  "objection": "[Specific objection from research]",
                  "dismantling_content": "[How to overcome this objection]",
                  "proof_points": "[Evidence to support position]",
                  "reframe": "[New way to think about this]"
                }
              ]
            }
            """,
            agent=mofu_agent
        )
        
        mofu_crew = Crew(
            agents=[mofu_agent],
            tasks=[mofu_task],
            verbose=True
        )
        
        return mofu_crew.kickoff()
    
    def create_bofu_conversion_copy(self, research_data, mofu_results):
        """
        Create BOFU high-converting copy for ready-to-buy prospects
        """
        
        bofu_agent = Agent(
            role="Elite BOFU Conversion Closer",
            goal="Write conversion copy that closes high-intent prospects at maximum rates",
            backstory="""You are a master closer who writes copy that converts ready-to-buy prospects at 25-40% rates. You understand that BOFU prospects have buying intent but need the final push.

You write like the greatest closers in history - David Ogilvy's precision, Gary Halbert's psychology, and Dan Kennedy's urgency. Your copy doesn't just ask for the sale - it makes NOT buying feel impossible.

You create offers so compelling and risk-free that prospects feel foolish not to take action immediately.""",
            llm=self.bofu_llm,
            verbose=True,
            allow_delegation=False
        )
        
        bofu_task = Task(
            description=f"""
            Create BOFU high-converting copy based on:
            
            RESEARCH INSIGHTS: {str(research_data)[:2000]}
            MOFU MECHANISMS: {str(mofu_results)[:1000]}
            
            WRITE CONVERSION COPY THAT CLOSES:
            
            1. SALES PAGE SECTIONS (Complete sales page)
            - Headline that pre-qualifies buyers
            - Subheadline that agitates core pain
            - Benefits that create irresistible desire
            - Social proof that eliminates doubt
            - Offer that's impossible to refuse
            - Risk reversal that removes all fear
            - Urgency that compels immediate action
            - CTA that gets 25-40% conversion
            
            2. EMAIL SALES SEQUENCES (5-email sequence)
            - Email 1: Reactivation and curiosity
            - Email 2: Problem agitation and consequences  
            - Email 3: Solution presentation and social proof
            - Email 4: Objection handling and risk reversal
            - Email 5: Final urgency and last chance
            
            3. IRRESISTIBLE OFFER STRUCTURES (3 variations)
            - Core offer with massive value
            - Bonuses that double perceived value
            - Risk reversal that removes all fear
            - Urgency that creates immediate action
            
            4. OBJECTION-CRUSHING COPY BLOCKS
            - "I don't have time" objection
            - "I can't afford it" objection  
            - "I've tried everything" objection
            - "It won't work for me" objection
            - "I need to think about it" objection
            
            5. CLOSING MECHANISMS
            - Assumptive close copy
            - Alternative choice close
            - Urgency-based close
            - Risk reversal close
            - Social proof close
            
            Expected conversion rates: 25-40% for qualified traffic
            """,
            
            expected_output="""
            BOFU conversion copy in JSON format:
            
            {
              "sales_page": {
                "headline": "[Pre-qualifying headline]",
                "subheadline": "[Pain agitation]", 
                "benefits_section": "[Irresistible benefits copy]",
                "social_proof_section": "[Doubt-eliminating proof]",
                "offer_section": "[Impossible to refuse offer]",
                "risk_reversal": "[Fear-removing guarantee]",
                "urgency_section": "[Action-compelling urgency]",
                "cta": "[25-40% converting call-to-action]",
                "psychological_flow": "[Why this structure converts]"
              },
              "email_sequences": [
                {
                  "email_number": 1,
                  "subject": "[High open rate subject]",
                  "copy": "[Complete email copy]",
                  "goal": "[Psychological objective]",
                  "cta": "[Specific action]"
                }
              ],
              "offer_structures": [
                {
                  "core_offer": "[Main product/service]",
                  "value_stack": "[Itemized value breakdown]",
                  "bonuses": "[Value-doubling bonuses]",
                  "total_value": "[$X,XXX]",
                  "your_investment": "[$XXX]",
                  "risk_reversal": "[Complete guarantee]",
                  "urgency_element": "[Scarcity/urgency]"
                }
              ],
              "objection_crushers": [
                {
                  "objection": "[Specific objection]",
                  "crushing_copy": "[Copy that destroys objection]",
                  "proof_points": "[Supporting evidence]",
                  "reframe": "[New perspective]"
                }
              ],
              "closing_mechanisms": [
                {
                  "close_type": "[Assumptive/Alternative/etc]",
                  "copy": "[Exact closing copy]",
                  "psychology": "[Why this works]",
                  "when_to_use": "[Optimal timing]"
                }
              ]
            }
            """,
            agent=bofu_agent
        )
        
        bofu_crew = Crew(
            agents=[bofu_agent],
            tasks=[bofu_task],
            verbose=True
        )
        
        return bofu_crew.kickoff()

# Main function for integration
def generate_tactical_conversion_assets(research_data, business_context):
    """
    Generate micro-testable conversion assets from research insights
    """
    conversion_agent = ConversionCopyAgent()
    return conversion_agent.generate_conversion_assets(research_data, business_context)
