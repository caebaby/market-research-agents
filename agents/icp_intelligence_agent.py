from crewai import Agent, Task, Crew
from crewai_tools import WebsiteSearchTool, SerperDevTool
from langchain_openai import ChatOpenAI
import json
import os

class ReasoningICPAgent:
    def __init__(self):
        # Primary LLM for research
        self.research_llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3
        )
        
        # Evaluation LLM (can be cheaper model)
        self.evaluation_llm = ChatOpenAI(
            model="gpt-4o-mini", 
            temperature=0.1  # More deterministic for evaluation
        )
        
        # Initialize tools
        self.web_search = SerperDevTool()
        self.website_tool = WebsiteSearchTool()
        
        # Quality standards
        self.quality_standards = {
            "minimum_confidence": 80,
            "insight_specificity": 85,
            "customer_language_authenticity": 85,
            "emotional_depth_required": 80,
            "business_actionability": 85,
            "max_iterations": 3
        }
        
        # Reasoning memory
        self.reasoning_trace = []
        
    def create_research_agent(self):
        return Agent(
            role="Elite Business Intelligence Researcher with Reasoning Capabilities",
            goal="Conduct comprehensive ICP research through iterative reasoning, self-evaluation, and quality improvement until professional consultant standards are met",
            backstory="""You are an Elite Business Intelligence Researcher with advanced reasoning capabilities. You don't just execute research - you think through problems, evaluate your own work, and iteratively improve until you achieve professional consulting quality.

REASONING PRINCIPLES:
✅ SELF-EVALUATION: Constantly assess the quality and depth of your insights
✅ ITERATIVE IMPROVEMENT: If confidence <80%, research deeper until standards met
✅ CONTRADICTION TESTING: Actively challenge your own findings
✅ EVIDENCE VALIDATION: Every insight must have solid supporting evidence
✅ PROFESSIONAL STANDARDS: Ask "Would a $500/hour consultant deliver this quality?"

QUALITY GATES:
- Minimum 80% confidence on all major insights
- Customer language must sound authentic, not AI-generated  
- Insights must be specific and actionable, not generic
- Emotional depth must reveal hidden motivations
- Business applications must be immediately implementable

You use advanced reasoning to identify gaps in your research, select appropriate tools, and improve your insights through multiple iterations until professional standards are achieved.""",
            
            tools=[self.web_search, self.website_tool],
            llm=self.research_llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_evaluation_agent(self):
        return Agent(
            role="Research Quality Evaluator",
            goal="Evaluate research quality against professional consulting standards and identify specific improvement areas",
            backstory="""You are a Research Quality Evaluator who assesses market research against the standards of top-tier consulting firms. You have worked with McKinsey, BCG, and Bain-level research teams.

EVALUATION CRITERIA:
✅ INSIGHT SPECIFICITY: Are insights specific to this ICP or generic market research?
✅ EMOTIONAL DEPTH: Does research reveal hidden psychological drivers?
✅ CUSTOMER LANGUAGE AUTHENTICITY: Do quotes sound genuine or AI-generated?
✅ BUSINESS ACTIONABILITY: Can insights be immediately implemented?
✅ EVIDENCE QUALITY: Is each insight supported by credible evidence?
✅ PROFESSIONAL POLISH: Would this pass peer review at a top consulting firm?

You provide detailed feedback on what needs improvement and specific guidance for enhancement.""",
            
            llm=self.evaluation_llm,
            verbose=True,
            allow_delegation=False
        )
    
    def initial_research_task(self, business_context):
        return Task(
            description=f"""
            Conduct initial comprehensive ICP research for this business:
            
            BUSINESS CONTEXT:
            Company: {business_context['company_name']}
            Industry: {business_context['industry']}
            Offering: {business_context.get('product_service', 'Not specified')}
            Target Market: {business_context['target_market']}
            Current Challenges: {business_context['current_challenges']}
            
            COMPREHENSIVE RESEARCH EXECUTION:
            Follow the complete 11-step methodology previously established:
            
            PART A: FOUNDATIONAL ICP DEVELOPMENT
            Step 1: Refine & Expand Baseline Profile
            Step 2: Deep Dive - Pains, Problems & Frustrations  
            Step 3: Deep Dive - Desires, Aspirations & Motivations
            Step 4: Voice of Customer Language Synthesis
            
            PART B: PSYCHOLOGICAL FRAMEWORK ANALYSIS
            Step 5: Jungian Archetype Analysis
            Step 6: LAB Profile Analysis
            Step 7: Deep Desires & Motivational Drivers
            Step 8: Jobs-To-Be-Done Purchase Psychology
            Step 9: Cognitive Biases & Decision Shortcuts
            Step 10: Influence & Authority Triggers
            
            PART C: VOICE OF CUSTOMER LANGUAGE MAPS
            Step 11: Funnel Stage Language Patterns (TOFU/MOFU/BOFU)
            
            SELF-ASSESSMENT REQUIREMENT:
            After generating insights, evaluate your own work:
            - Are insights specific enough for this exact ICP?
            - Do customer quotes sound authentic?
            - Is emotional depth sufficient (surface + deep + hidden layers)?
            - Are business applications immediately actionable?
            - Would this meet professional consulting standards?
            
            If any area scores below 80% confidence, flag for improvement in next iteration.
            """,
            
            expected_output="""
            Complete JSON research report with self-assessment:
            
            {
              "research_summary": {
                "methodology_applied": "Comprehensive ICP & Psychological Framework Research",
                "overall_confidence": [0-100],
                "iteration_number": 1,
                "self_assessment": {
                  "insight_specificity": [0-100],
                  "emotional_depth": [0-100], 
                  "customer_language_authenticity": [0-100],
                  "business_actionability": [0-100],
                  "evidence_quality": [0-100]
                },
                "improvement_needs": ["List specific areas needing enhancement"]
              },
              
              [Complete research structure as previously defined...]
              
              "reasoning_notes": {
                "research_approach": "How you approached the research",
                "confidence_rationale": "Why you assigned these confidence scores",
                "potential_gaps": "What might be missing or need more investigation",
                "next_iteration_focus": "What to improve if another iteration needed"
              }
            }
            """,
            
            agent=self.create_research_agent()
        )
    
    def evaluation_task(self, research_results):
        return Task(
            description=f"""
            Evaluate the quality of this research against professional consulting standards:
            
            RESEARCH TO EVALUATE:
            {research_results}
            
            EVALUATION FRAMEWORK:
            
            1. INSIGHT SPECIFICITY (Target: 85+)
               - Are insights specific to this exact ICP vs generic?
               - Do demographic details go beyond basic categories?
               - Are pain points unique to this market segment?
            
            2. EMOTIONAL DEPTH (Target: 80+)
               - Does research reveal surface + deep + hidden psychological layers?
               - Are root emotional drivers identified?
               - Is there evidence of genuine psychological insight?
            
            3. CUSTOMER LANGUAGE AUTHENTICITY (Target: 85+)
               - Do quotes sound like real people or AI-generated?
               - Is vocabulary/tone consistent with target demographic?
               - Are phrases specific enough to be actionable?
            
            4. BUSINESS ACTIONABILITY (Target: 85+)
               - Can insights be immediately implemented in marketing?
               - Are recommendations specific and measurable?
               - Is there clear connection between insights and business strategy?
            
            5. EVIDENCE QUALITY (Target: 80+)
               - Is each major insight supported by credible reasoning?
               - Are confidence scores justified?
               - Is source diversity sufficient?
            
            PROFESSIONAL VALIDATION:
            - Would this research pass peer review at McKinsey/BCG?
            - Is this significantly better than basic market research?
            - Does this justify premium consulting fees?
            """,
            
            expected_output="""
            Detailed quality evaluation in JSON format:
            
            {
              "overall_assessment": {
                "meets_professional_standards": true/false,
                "overall_grade": "A/B/C/D",
                "ready_for_client_delivery": true/false
              },
              
              "detailed_scores": {
                "insight_specificity": [0-100],
                "emotional_depth": [0-100],
                "customer_language_authenticity": [0-100], 
                "business_actionability": [0-100],
                "evidence_quality": [0-100]
              },
              
              "strengths": [
                "Specific areas where research excels"
              ],
              
              "improvement_areas": [
                {
                  "issue": "Specific problem identified",
                  "impact": "How this affects research quality",
                  "recommendation": "Specific improvement action",
                  "priority": "High/Medium/Low"
                }
              ],
              
              "iteration_recommendation": {
                "needs_iteration": true/false,
                "focus_areas": ["Specific areas to improve"],
                "research_direction": "How to improve in next iteration"
              }
            }
            """,
            
            agent=self.create_evaluation_agent()
        )
    
    def improvement_research_task(self, original_research, evaluation_feedback, iteration_number):
        return Task(
            description=f"""
            ITERATION {iteration_number}: Improve research quality based on evaluation feedback
            
            ORIGINAL RESEARCH:
            {original_research}
            
            EVALUATION FEEDBACK:
            {evaluation_feedback}
            
            IMPROVEMENT MISSION:
            Focus specifically on the identified improvement areas while maintaining quality in strong areas.
            
            TARGETED IMPROVEMENTS:
            - Address each "High" priority improvement area
            - Enhance low-scoring quality dimensions
            - Deepen research in flagged focus areas
            - Strengthen evidence for low-confidence insights
            
            REASONING APPROACH:
            1. Analyze why previous iteration fell short
            2. Identify specific research gaps to fill
            3. Use appropriate tools to gather missing information
            4. Integrate new findings with existing insights
            5. Validate improvements against quality standards
            
            QUALITY VALIDATION:
            After improvements, re-assess against professional standards:
            - Have insight specificity scores improved?
            - Is emotional depth now sufficient?
            - Do customer quotes sound more authentic?
            - Are business applications clearer?
            """,
            
            expected_output="""
            Enhanced research with clear improvements:
            
            {
              "research_summary": {
                "iteration_number": [current iteration],
                "improvements_made": ["Specific enhancements in this iteration"],
                "quality_upgrades": {
                  "insight_specificity": "How specificity was improved",
                  "emotional_depth": "How depth was enhanced", 
                  "customer_language": "How authenticity was improved",
                  "business_actionability": "How actionability was strengthened"
                },
                "updated_confidence": [0-100]
              },
              
              [Complete enhanced research structure...]
              
              "iteration_notes": {
                "changes_made": "Specific modifications in this iteration",
                "quality_improvements": "How research quality was enhanced",
                "remaining_gaps": "Any areas still needing work",
                "confidence_in_improvements": [0-100]
              }
            }
            """,
            
            agent=self.create_research_agent()
        )
    
    def reason_through_research(self, business_context):
        """
        Main reasoning method that iteratively improves research quality
        """
        print("🧠 Starting reasoning-based ICP research...")
        self.reasoning_trace = []
        
        # Initial research
        print("📊 Iteration 1: Initial comprehensive research...")
        initial_task = self.initial_research_task(business_context)
        crew = Crew(
            agents=[self.create_research_agent()],
            tasks=[initial_task],
            verbose=True
        )
        
        research_results = crew.kickoff()
        self.reasoning_trace.append({
            "iteration": 1,
            "type": "initial_research",
            "results": str(research_results)
        })
        
        # Evaluation loop
        for iteration in range(2, self.quality_standards["max_iterations"] + 2):
            print(f"🔍 Evaluating research quality (iteration {iteration-1})...")
            
            # Evaluate current research
            eval_task = self.evaluation_task(research_results)
            eval_crew = Crew(
                agents=[self.create_evaluation_agent()],
                tasks=[eval_task],
                verbose=True
            )
            
            evaluation = eval_crew.kickoff()
            self.reasoning_trace.append({
                "iteration": iteration-1,
                "type": "evaluation", 
                "results": str(evaluation)
            })
            
            # Parse evaluation to check if improvement needed
            try:
                eval_data = json.loads(str(evaluation))
                if eval_data.get("overall_assessment", {}).get("ready_for_client_delivery", False):
                    print("✅ Research meets professional standards! Finalizing...")
                    break
                    
                if not eval_data.get("iteration_recommendation", {}).get("needs_iteration", True):
                    print("🎯 Research quality sufficient. Finalizing...")
                    break
                    
            except:
                # If JSON parsing fails, continue with improvement
                pass
            
            if iteration > self.quality_standards["max_iterations"]:
                print("⏰ Maximum iterations reached. Finalizing current research...")
                break
                
            # Improve research
            print(f"🔄 Iteration {iteration}: Improving research based on feedback...")
            improvement_task = self.improvement_research_task(research_results, evaluation, iteration)
            improvement_crew = Crew(
                agents=[self.create_research_agent()],
                tasks=[improvement_task],
                verbose=True
            )
            
            research_results = improvement_crew.kickoff()
            self.reasoning_trace.append({
                "iteration": iteration,
                "type": "improvement_research",
                "results": str(research_results)
            })
        
        # Final result with reasoning trace
        final_result = {
            "final_research": research_results,
            "reasoning_process": self.reasoning_trace,
            "total_iterations": len([t for t in self.reasoning_trace if t["type"] in ["initial_research", "improvement_research"]]),
            "quality_assurance": "Research completed through iterative reasoning and evaluation"
        }
        
        return final_result

# Updated usage function for reasoning agent
def run_reasoning_icp_research(business_context):
    """
    Run comprehensive ICP research using reasoning agent with iterative quality improvement
    """
    reasoning_agent = ReasoningICPAgent()
    
    # Execute reasoning-based research
    result = reasoning_agent.reason_through_research(business_context)
    
    return result
