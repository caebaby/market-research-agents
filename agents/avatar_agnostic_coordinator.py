# agents/avatar_agnostic_coordinator.py
# Pure context-driven coordination - agents are smart enough to handle any business

import os
from dotenv import load_dotenv
from crewai import Crew, Process, Task
from crewai_tools import SerperDevTool
import json
from datetime import datetime

# Import your existing agents (keeping what you built)
from agents.icp_intelligence_agent import ICPIntelligenceAgent
from agents.dynamic_interview_agent import DynamicInterviewAgent  
from agents.marketing_intelligence_synthesizer import MarketingIntelligenceSynthesizer

class ContextDrivenCoordinator:
    def __init__(self):
        load_dotenv()
        
        # Initialize tools
        self.search_tool = SerperDevTool()
        
        # Initialize your existing agents (Gemini's approach)
        self.icp_agent = ICPIntelligenceAgent().agent()
        self.interview_agent = DynamicInterviewAgent().agent()
        self.marketing_agent = MarketingIntelligenceSynthesizer().agent()
    
    def conduct_context_driven_research(self, business_context: str) -> dict:
        """
        Pure context-driven research using Gemini's Crew coordination
        Agents are smart enough to handle any business context
        """
        
        print("🚀 Starting Context-Driven Research with Smart Agent Coordination...")
        
        # Create smart tasks that adapt to any context (Gemini's approach)
        research_task = Task(
            description=f"""
            Conduct comprehensive market research analysis for this business:
            
            {business_context}
            
            You are a smart agent - analyze this context and determine:
            - What industry/market this business operates in
            - Who their target customers are
            - What challenges and opportunities exist
            
            Apply your full comprehensive methodology including:
            - Deep customer psychology analysis
            - Pain points and frustrations
            - Desires and aspirations
            - Voice of customer language capture
            - Psychological frameworks (Jungian, LAB Profile, JTBD)
            - Professional consulting quality validation
            
            Provide actionable insights specific to this exact business context.
            """,
            expected_output="""
            Comprehensive market research report including:
            1. Business and industry analysis
            2. Detailed ICP analysis with specific demographics and psychographics
            3. Specific pain points with authentic customer language
            4. Core desires and motivations
            5. Voice of customer phrases and terminology
            6. Psychological archetype analysis
            7. Decision-making patterns and biases
            8. Marketing implications and recommendations
            9. Quality assurance metrics and confidence scores
            """,
            agent=self.icp_agent
        )
        
        interview_task = Task(
            description=f"""
            Based on the research analysis, create realistic interview simulations with the target customers identified in the research.
            
            You are smart enough to understand the context and create authentic dialogue that:
            - Validates the research insights
            - Reveals emotional motivations
            - Uncovers hidden concerns and objections
            - Captures decision-making language and triggers
            - Feels genuine to the specific customer type identified
            
            Generate realistic customer personas and interview scenarios based on the research.
            """,
            expected_output="""
            Simulated interview responses including:
            1. Realistic customer quotes and dialogue
            2. Persona-based scenarios
            3. Emotional motivations and concerns
            4. Validation of research insights
            5. Additional customer language patterns
            6. Decision triggers and hesitation points
            7. Authentic voice patterns for this customer type
            """,
            agent=self.interview_agent,
            context=[research_task]  # Uses research output
        )
        
        marketing_synthesis_task = Task(
            description=f"""
            Synthesize all research and interview insights into actionable marketing strategy.
            
            You are smart enough to create specific, implementable recommendations that:
            - Leverage the specific pain points and desires identified
            - Use industry-appropriate messaging frameworks
            - Recommend channels that work for this customer type
            - Create campaign concepts tailored to this market
            - Provide competitive positioning strategy
            
            Make all recommendations specific to this business context, not generic marketing advice.
            """,
            expected_output="""
            Complete marketing strategy including:
            1. Messaging framework with specific customer language
            2. Channel recommendations with clear rationale
            3. Campaign concepts and tactics
            4. Implementation roadmap with success metrics
            5. Competitive positioning strategy
            6. Success metrics and KPIs
            7. Budget allocation recommendations
            """,
            agent=self.marketing_agent,
            context=[research_task, interview_task]  # Uses both previous outputs
        )
        
        # Assemble the Crew (THE KEY GEMINI INSIGHT!)
        smart_crew = Crew(
            agents=[self.icp_agent, self.interview_agent, self.marketing_agent],
            tasks=[research_task, interview_task, marketing_synthesis_task],
            process=Process.sequential,  # Tasks run one after another
            verbose=2  # Detailed logging
        )
        
        print("✅ Smart crew assembled - agents will adapt to context")
        
        # Execute the Crew (THE MAGIC MOMENT!)
        print("🔥 Executing context-driven research crew...")
        
        try:
            result = smart_crew.kickoff(inputs={
                'business_context': business_context
            })
            
            return {
                "success": True,
                "research_approach": "context_driven_smart_agents",
                "crew_execution": "completed",
                "results": str(result),
                "processing_summary": {
                    "approach": "pure_context_driven",
                    "crew_coordination": "executed",
                    "tasks_completed": 3,
                    "agent_intelligence": "adaptive_to_any_context"
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "partial_results": "Crew execution failed",
                "troubleshooting": "Check agent configurations and CrewAI setup"
            }

# Main function to integrate with your FastAPI
def run_avatar_agnostic_research(business_context: str) -> dict:
    """
    Main function that uses smart agents with pure context-driven approach
    """
    
    coordinator = ContextDrivenCoordinator()
    return coordinator.conduct_context_driven_research(business_context)
