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
            role="ICP Intelligence Specialist",
            goal="Conduct deep research on ideal customer profiles to uncover problems, pains, desires, and beliefs",
            backstory="""You are an expert market researcher with a psychology background. 
            You excel at finding the emotional and rational drivers behind customer behavior. 
            You dig deep into forums, social media, and online communities to understand 
            what people really think and feel about their problems. You're particularly 
            skilled at understanding what solutions people have tried and why they failed.""",
            
            tools=[self.web_search, self.website_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def create_research_task(self, business_context):
        return Task(
            description=f"""
            Research the ideal customer profile for this business context:
            
            BUSINESS: {business_context['company_name']}
            INDUSTRY: {business_context['industry']}
            TARGET_MARKET: {business_context['target_market']}
            CURRENT_CHALLENGES: {business_context['current_challenges']}
            
            Your research should uncover:
            
            1. PROBLEMS & PAINS:
               - What specific problems does this target market face?
               - What are their daily frustrations and challenges?
               - What keeps them up at 3am worrying?
               - What have they tried that didn't work?
            
            2. DESIRES & GOALS:
               - What do they ultimately want to achieve?
               - What would success look like to them?
               - What aspirations drive their decisions?
            
            3. CURRENT BELIEFS:
               - What do they believe about available solutions?
               - What misconceptions or biases do they have?
               - What are their objections to getting help?
            
            4. LANGUAGE & EMOTIONS:
               - How do they describe their problems in their own words?
               - What emotional language do they use?
               - What phrases and terminology are common?
            
            RESEARCH SOURCES:
            - Reddit discussions and comments
            - Industry forums and communities
            - Social media conversations
            - Review sites and complaint forums
            - Blog comments and discussions
            
            DELIVERABLE:
            Comprehensive ICP profile with specific quotes, examples, and emotional insights.
            Include confidence scores for each major finding.
            """,
            
            expected_output="""
            A detailed ICP research report containing:
            
            1. EXECUTIVE SUMMARY
               - Top 3 problems this market faces
               - Primary emotional drivers
               - Key opportunity areas
            
            2. PROBLEMS & PAIN POINTS
               - Detailed list of specific problems
               - Emotional impact of each problem
               - Failed solution attempts
               - Direct quotes from research
            
            3. DESIRES & ASPIRATIONS  
               - What they want to achieve
               - Success definitions
               - Motivational drivers
            
            4. CURRENT BELIEFS & OBJECTIONS
               - Existing beliefs about solutions
               - Common objections and concerns
               - Trust and credibility factors
            
            5. VOICE OF CUSTOMER
               - Actual language and phrases used
               - Emotional expressions
               - Common terminology
            
            6. CONFIDENCE SCORES
               - Research quality indicators
               - Source reliability assessment
               - Recommendation confidence levels
            """,
            
            agent=self.create_agent()
        )

# Example usage function
def run_icp_research(business_context):
    """
    Run ICP research for a given business context
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
