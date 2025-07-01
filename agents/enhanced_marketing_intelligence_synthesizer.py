# enhanced_marketing_intelligence_synthesizer.py
# Tactical framework generator with high-intent conversion focus

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import json

class TacticalMarketingSynthesizer:
    def __init__(self):
        self.strategy_llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.6
        )
        
        self.tactical_llm = ChatOpenAI(
            model="gpt-4o-mini", 
            temperature=0.7
        )
    
    def execute_tactical_synthesis(self, research_results, interview_results, business_context):
        """
        Execute tactical marketing synthesis focused on high-intent conversion
        """
        
        print("🎯 Executing Tactical Marketing Synthesis...")
        
        # Phase 1: High-Intent Strategy Development
        strategy_results = self.create_high_intent_strategy(research_results, interview_results, business_context)
        
        # Phase 2: Conversion Framework Creation
        framework_results = self.create_conversion_frameworks(strategy_results, research_results)
        
        return {
            "high_intent_strategy": strategy_results,
            "conversion_frameworks": framework_results,
            "synthesis_method": "tactical_high_intent_approach"
        }
    
    def create_high_intent_strategy(self, research_results, interview_results, business_context):
        """
        Create strategy focused on highest-intent engagement and conversions
        """
        
        strategy_agent = Agent(
            role="Elite High-Intent Marketing Strategist",
            goal="Identify and create strategies that attract the highest-intent prospects and convert them at maximum rates",
            backstory="""You are an elite marketing strategist who specializes in high-intent marketing. You don't chase vanity metrics - you focus on strategies that attract ready-to-buy prospects and convert them at premium rates.

You understand behavioral triggers that indicate buying intent. You know how to position offers so that only serious prospects respond. You create campaigns that competitors can't replicate because they're based on deep psychological insights.

Your strategies consistently achieve 3-5x higher conversion rates than industry averages because you target intent, not just interest.""",
            llm=self.strategy_llm,
            verbose=True,
            allow_delegation=False
        )
        
        strategy_task = Task(
            description=f"""
            Create HIGH-INTENT marketing strategy from research:
            
            RESEARCH DATA: {str(research_results)[:2000]}
            INTERVIEW DATA: {str(interview_results)[:2000]} 
            BUSINESS CONTEXT: {business_context}
            
            DEVELOP HIGH-INTENT STRATEGY:
            
            1. HIGH-INTENT PROSPECT IDENTIFICATION
            - Behavioral signals that indicate buying readiness
            - Psychographic triggers that separate browsers from buyers  
            - Timing indicators (when they're most likely to buy)
            - Qualification criteria to pre-filter prospects
            
            2. MAXIMUM CONVERSION POSITIONING
            - Unique positioning that attracts serious prospects only
            - Value proposition that justifies premium pricing
            - Authority positioning that eliminates price shopping
            - Differentiation that makes competitors irrelevant
            
            3. INTENT-BASED TARGETING STRATEGY
            - Specific targeting criteria for highest-intent prospects
            - Channel strategy focused on where serious buyers are
            - Messaging that repels tire-kickers and attracts buyers
            - Timing strategy for maximum buying intent
            
            4. CONVERSION RATE OPTIMIZATION FRAMEWORK
            - Specific tactics to achieve 5-15% conversion rates
            - Psychological triggers for each funnel stage
            - Optimization priorities ranked by impact
            - Success metrics focused on quality over quantity
            
            5. PREMIUM POSITIONING STRATEGY
            - How to position as the premium solution
            - Pricing strategy that attracts serious buyers
            - Social proof that eliminates price objections
            - Exclusivity elements that create desire
            
            Focus on strategies that get the HIGHEST INTENT engagement.
            """,
            
            expected_output="""
            High-intent marketing strategy in JSON format:
            
            {
              "high_intent_identification": {
                "behavioral_signals": [
                  {
                    "signal": "[Specific behavior]",
                    "intent_level": "[High/Medium/Low]",
                    "targeting_implication": "[How to target this]"
                  }
                ],
                "psychographic_triggers": [
                  {
                    "trigger": "[Psychological indicator]", 
                    "buyer_readiness": "[Why this indicates readiness]",
                    "messaging_angle": "[How to appeal to this]"
                  }
                ],
                "timing_indicators": [
                  {
                    "timing": "[When they're ready]",
                    "context": "[Situational trigger]",
                    "opportunity": "[How to capitalize]"
                  }
                ]
              },
              "maximum_conversion_positioning": {
                "unique_position": "[Differentiated positioning]",
                "value_proposition": "[Premium value prop]",
                "authority_elements": "[Credibility builders]",
                "competitive_moat": "[Why competitors can't copy]"
              },
              "intent_targeting_strategy": {
                "targeting_criteria": "[Specific audience definition]",
                "channel_strategy": "[Where serious buyers are]",
                "message_filtering": "[Copy that repels tire-kickers]",
                "timing_optimization": "[When to reach them]"
              },
              "conversion_optimization": {
                "target_conversion_rates": {
                  "tofu_to_mofu": "[%]",
                  "mofu_to_bofu": "[%]",
                  "bofu_to_customer": "[%]"
                },
                "psychological_triggers": [
                  {
                    "stage": "[TOFU/MOFU/BOFU]",
                    "trigger": "[Specific psychological lever]",
                    "implementation": "[How to use this]"
                  }
                ],
                "optimization_priorities": [
                  {
                    "priority": 1,
                    "tactic": "[Highest impact optimization]",
                    "expected_lift": "[% improvement]"
                  }
                ]
              }
            }
            """,
            agent=strategy_agent
        )
        
        strategy_crew = Crew(
            agents=[strategy_agent],
            tasks=[strategy_task],
            verbose=True
        )
        
        return strategy_crew.kickoff()
    
    def create_conversion_frameworks(self, strategy_results, research_results):
        """
        Create tactical conversion frameworks based on strategy
        """
        
        framework_agent = Agent(
            role="Elite Conversion Framework Architect",
            goal="Create proven conversion frameworks that turn strategy into high-converting tactical implementations",
            backstory="""You are a conversion framework specialist who translates strategy into tactical frameworks that consistently convert at 3-5x industry averages.

You understand that frameworks are the bridge between strategy and execution. You create systematic approaches that ensure every piece of copy, every funnel stage, and every touchpoint is optimized for maximum conversion.

Your frameworks have been tested across thousands of campaigns and consistently produce predictable, scalable results.""",
            llm=self.tactical_llm,
            verbose=True,
            allow_delegation=False
        )
        
        framework_task = Task(
            description=f"""
            Create TACTICAL CONVERSION FRAMEWORKS from strategy:
            
            STRATEGY: {str(strategy_results)[:2000]}
            RESEARCH INSIGHTS: {str(research_results)[:2000]}
            
            CREATE TACTICAL FRAMEWORKS:
            
            1. MICRO-TESTING FRAMEWORK (MintCRO Style)
            - Specific test variations with success criteria
            - Budget allocation for maximum learning
            - Success metrics and kill/scale criteria
            - Testing sequence for optimal results
            
            2. FUNNEL CONVERSION FRAMEWORK
            - TOFU: Pattern interrupt and curiosity creation
            - MOFU: Value demonstration and trust building  
            - BOFU: Objection handling and closing
            - Specific conversion rate targets for each stage
            
            3. OFFER CREATION FRAMEWORK
            - Core offer structure that maximizes perceived value
            - Bonus stacking strategy for irresistible offers
            - Risk reversal framework that eliminates fear
            - Pricing psychology for premium positioning
            
            4. CONTENT MARKETING FRAMEWORK
            - Authority-building content that attracts high-intent prospects
            - Educational content that pre-qualifies prospects
            - Case study framework that proves results
            - Social proof collection and deployment
            
            5. SALES PROCESS FRAMEWORK
            - Discovery questions that reveal buying intent
            - Presentation structure that builds irresistible desire
            - Objection handling system for common concerns
            - Closing techniques for different prospect types
            
            Each framework should include:
            - Step-by-step implementation
            - Success metrics and benchmarks
            - Common mistakes to avoid
            - Optimization opportunities
            """,
            
            expected_output="""
            Tactical conversion frameworks in JSON format:
            
            {
              "micro_testing_framework": {
                "test_variations": [
                  {
                    "test_type": "[Headline/Hook/Offer/etc]",
                    "variations": [
                      {
                        "variation": "[Specific test copy]",
                        "hypothesis": "[Why this should work]",
                        "success_criteria": "[What constitutes success]"
                      }
                    ],
                    "budget_allocation": "[$X per variation]",
                    "testing_duration": "[Days]",
                    "kill_criteria": "[When to stop test]",
                    "scale_criteria": "[When to scale winner]"
                  }
                ],
                "testing_sequence": "[Order to run tests]",
                "learning_objectives": "[What each test teaches]"
              },
              "funnel_conversion_framework": {
                "tofu_framework": {
                  "objective": "[Pattern interrupt and curiosity]",
                  "tactics": [
                    {
                      "tactic": "[Specific TOFU tactic]",
                      "implementation": "[How to execute]",
                      "success_metric": "[Target CTR/engagement]"
                    }
                  ],
                  "target_conversion": "[TOFU to MOFU %]"
                },
                "mofu_framework": {
                  "objective": "[Value demo and trust building]",
                  "tactics": [
                    {
                      "tactic": "[Specific MOFU tactic]",
                      "implementation": "[How to execute]",
                      "success_metric": "[Target engagement/opt-in]"
                    }
                  ],
                  "target_conversion": "[MOFU to BOFU %]"
                },
                "bofu_framework": {
                  "objective": "[Objection handling and closing]",
                  "tactics": [
                    {
                      "tactic": "[Specific BOFU tactic]",
                      "implementation": "[How to execute]",
                      "success_metric": "[Target conversion %]"
                    }
                  ],
                  "target_conversion": "[BOFU to customer %]"
                }
              },
              "offer_creation_framework": {
                "core_offer_structure": {
                  "main_deliverable": "[Primary product/service]",
                  "value_proposition": "[Specific value]",
                  "pricing_psychology": "[Why this price point]"
                },
                "bonus_stacking": [
                  {
                    "bonus": "[Specific bonus]",
                    "value": "[$XXX]",
                    "relevance": "[Why this adds value]"
                  }
                ],
                "risk_reversal": {
                  "guarantee_type": "[Money-back/Performance/etc]",
                  "guarantee_copy": "[Exact guarantee language]",
                  "credibility_elements": "[What makes guarantee believable]"
                }
              },
              "implementation_priorities": [
                {
                  "priority": 1,
                  "framework": "[Which framework to implement first]",
                  "timeline": "[Implementation timeframe]",
                  "resources_needed": "[Team/budget requirements]",
                  "expected_impact": "[Projected results]"
                }
              ]
            }
            """,
            agent=framework_agent
        )
        
        framework_crew = Crew(
            agents=[framework_agent],
            tasks=[framework_task],
            verbose=True
        )
        
        return framework_crew.kickoff()

# Main function for integration
def synthesize_tactical_marketing_intelligence(research_results, interview_results, business_context):
    """
    Tactical marketing synthesis focused on high-intent conversion
    """
    synthesizer = TacticalMarketingSynthesizer()
    return synthesizer.execute_tactical_synthesis(
        research_results, 
        interview_results, 
        business_context
    )
