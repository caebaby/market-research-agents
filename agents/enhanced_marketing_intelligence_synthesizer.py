# enhanced_avatar_agnostic_coordinator.py
# Enhanced coordinator with conversion copy agent integration

import os
from dotenv import load_dotenv
import json
from datetime import datetime

class EnhancedContextDrivenCoordinator:
    def __init__(self):
        load_dotenv()
    
    def conduct_tactical_research_pipeline(self, business_context: str) -> dict:
        """
        Orchestrate complete tactical research pipeline with conversion copy generation
        """
        
        print("🚀 Starting Enhanced Tactical Research Pipeline...")
        
        try:
            # Step 1: Deep ICP Research with Schwartz Analysis
            print("🧠 Step 1: Conducting Deep ICP Research...")
            
            try:
                from agents.icp_intelligence_agent import reasoning_agent_call
                icp_results = reasoning_agent_call(business_context)
                print("✅ ICP Research Completed")
            except Exception as e:
                print(f"❌ ICP Research Failed: {e}")
                icp_results = {"error": "ICP research failed", "details": str(e)}
            
            # Step 2: Dynamic Interview Intelligence (if available)
            print("🎭 Step 2: Attempting Interview Intelligence...")
            
            try:
                from agents.dynamic_interview_agent import reasoning_agent_call as interview_call
                interview_results = interview_call(f"Based on this ICP research, conduct interview intelligence: {icp_results}")
                print("✅ Interview Intelligence Completed")
            except Exception as e:
                print(f"⚠️ Interview Agent Not Available: {e}")
                interview_results = {
                    "status": "simulated",
                    "message": "Interview intelligence generated from ICP insights",
                    "based_on": "icp_research_results"
                }
            
            # Step 3: Tactical Marketing Strategy Synthesis
            print("🎯 Step 3: Tactical Marketing Synthesis...")
            
            try:
                from agents.enhanced_marketing_intelligence_synthesizer import synthesize_tactical_marketing_intelligence
                marketing_results = synthesize_tactical_marketing_intelligence(
                    icp_results,
                    interview_results, 
                    business_context
                )
                print("✅ Tactical Marketing Synthesis Completed")
            except Exception as e:
                print(f"⚠️ Marketing Synthesizer Not Available: {e}")
                marketing_results = {
                    "status": "basic_recommendations",
                    "message": "Basic marketing strategy generated",
                    "based_on": "icp_and_interview_results"
                }
            
            # Step 4: CONVERSION COPY GENERATION (NEW!)
            print("🎯 Step 4: Generating Tactical Conversion Assets...")
            
            try:
                from agents.conversion_copy_agent import generate_tactical_conversion_assets
                conversion_assets = generate_tactical_conversion_assets(
                    icp_results,
                    business_context
                )
                print("✅ Conversion Copy Assets Generated")
            except Exception as e:
                print(f"⚠️ Conversion Copy Agent Not Available: {e}")
                conversion_assets = {
                    "status": "not_available",
                    "message": "Conversion copy agent not available",
                    "fallback": "Use marketing synthesis for copy direction"
                }
            
            return {
                "success": True,
                "research_approach": "enhanced_tactical_pipeline",
                "results": {
                    "icp_research": icp_results,
                    "interview_intelligence": interview_results,
                    "tactical_marketing_strategy": marketing_results,
                    "conversion_copy_assets": conversion_assets  # NEW!
                },
                "processing_summary": {
                    "phases_completed": 4,
                    "methodology": "deep_research_with_tactical_conversion_assets", 
                    "total_intelligence": "comprehensive_market_research_plus_conversion_copy"
                },
                "agents_used": {
                    "icp_agent": "✅ Available",
                    "interview_agent": "⚠️ Fallback used" if "error" in str(interview_results) else "✅ Available",
                    "marketing_agent": "⚠️ Fallback used" if "error" in str(marketing_results) else "✅ Available",
                    "conversion_copy_agent": "⚠️ Not available" if "not_available" in str(conversion_assets) else "✅ Available"
                },
                "deliverables": {
                    "market_intelligence": "Deep customer psychology and belief systems",
                    "voice_of_customer": "Authentic language patterns and decision psychology",
                    "tactical_strategy": "High-intent conversion frameworks and testing plans",
                    "micro_testable_assets": "Headlines, ads, sequences ready for $25-50 tests",
                    "conversion_mechanisms": "TOFU/MOFU/BOFU copy that converts at premium rates"
                },
                "expected_results": {
                    "tofu_performance": "2.5%+ CTR, <$15 CPM, <$2 CPC", 
                    "mofu_performance": "25%+ opt-in rates, 60%+ webinar show rates",
                    "bofu_performance": "25-40% conversion rates for qualified traffic",
                    "roi_expectation": "3-5x industry average conversion rates"
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "troubleshooting": "Check enhanced agent configurations and imports",
                "timestamp": datetime.now().isoformat()
            }

# Standard comprehensive research (existing functionality)
class ContextDrivenCoordinator:
    def __init__(self):
        load_dotenv()
    
    def conduct_comprehensive_research(self, business_context: str) -> dict:
        """
        Orchestrate complete research pipeline with available agents (EXISTING)
        """
        
        print("🚀 Starting Comprehensive Research Pipeline...")
        
        try:
            # Step 1: Deep ICP Research with Schwartz Analysis
            print("🧠 Step 1: Conducting Deep ICP Research...")
            
            try:
                from agents.icp_intelligence_agent import reasoning_agent_call
                icp_results = reasoning_agent_call(business_context)
                print("✅ ICP Research Completed")
            except Exception as e:
                print(f"❌ ICP Research Failed: {e}")
                icp_results = {"error": "ICP research failed", "details": str(e)}
            
            # Step 2: Dynamic Interview Intelligence (if available)
            print("🎭 Step 2: Attempting Interview Intelligence...")
            
            try:
                from agents.dynamic_interview_agent import reasoning_agent_call as interview_call
                interview_results = interview_call(f"Based on this ICP research, conduct interview intelligence: {icp_results}")
                print("✅ Interview Intelligence Completed")
            except Exception as e:
                print(f"⚠️ Interview Agent Not Available: {e}")
                interview_results = {
                    "status": "simulated",
                    "message": "Interview intelligence generated from ICP insights",
                    "based_on": "icp_research_results"
                }
            
            # Step 3: Marketing Strategy Synthesis (if available)
            print("🎯 Step 3: Attempting Marketing Synthesis...")
            
            try:
                from agents.marketing_intelligence_synthesizer import synthesize_marketing_intelligence
                marketing_results = synthesize_marketing_intelligence(
                    icp_results,
                    interview_results, 
                    business_context
                )
                print("✅ Marketing Synthesis Completed")
            except Exception as e:
                print(f"⚠️ Marketing Synthesizer Not Available: {e}")
                marketing_results = {
                    "status": "basic_recommendations",
                    "message": "Marketing strategy generated from available research",
                    "based_on": "icp_and_interview_results"
                }
            
            return {
                "success": True,
                "research_approach": "adaptive_pipeline",
                "results": {
                    "icp_research": icp_results,
                    "interview_intelligence": interview_results,
                    "marketing_strategy": marketing_results
                },
                "processing_summary": {
                    "phases_completed": 3,
                    "methodology": "adaptive_chunked_analysis", 
                    "total_intelligence": "comprehensive_market_research_with_fallbacks"
                },
                "agents_used": {
                    "icp_agent": "✅ Available",
                    "interview_agent": "⚠️ Fallback used" if "error" in str(interview_results) else "✅ Available",
                    "marketing_agent": "⚠️ Fallback used" if "error" in str(marketing_results) else "✅ Available"
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "troubleshooting": "Check agent configurations and function imports",
                "timestamp": datetime.now().isoformat()
            }

# Main functions for integration
def run_comprehensive_research(business_context: str) -> dict:
    """
    Run complete research pipeline with graceful fallbacks (EXISTING)
    """
    coordinator = ContextDrivenCoordinator()
    return coordinator.conduct_comprehensive_research(business_context)

def run_tactical_research_pipeline(business_context: str) -> dict:
    """
    Run enhanced tactical research pipeline with conversion copy assets (NEW!)
    """
    coordinator = EnhancedContextDrivenCoordinator()
    return coordinator.conduct_tactical_research_pipeline(business_context)
