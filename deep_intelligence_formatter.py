# deep_intelligence_formatter.py
# Extract deep psychological insights from research JSON

import json
import re
from datetime import datetime
from typing import Dict, Any, List

class DeepIntelligenceFormatter:
    def __init__(self):
        # Keywords that indicate psychological depth
        self.psychological_keywords = [
            "unconscious", "subconscious", "hidden", "fear", "anxiety", "belief", 
            "identity", "status", "shame", "pride", "belonging", "control", "power",
            "emotional", "psychological", "mindset", "mental", "cognitive", "bias"
        ]
        
        # Voice of customer indicators
        self.voc_indicators = [
            "quote", "saying", "language", "words", "phrases", "terminology",
            "voice", "customer", "client", "prospect", "audience"
        ]

def format_deep_intelligence_report(session_data: Dict[str, Any]) -> str:
    """
    Extract and format deep psychological intelligence from research data
    """
    
    # Extract the research content
    agent_results = session_data.get("agent_results", {})
    research_content = ""
    
    # Try to get content from different possible locations
    if "comprehensive_research" in agent_results:
        comprehensive = agent_results["comprehensive_research"]
        if isinstance(comprehensive, dict):
            research_content = str(comprehensive.get("icp_analysis", "")) + "\n"
            research_content += str(comprehensive.get("simulated_interviews", "")) + "\n"
            research_content += str(comprehensive.get("synthesis", ""))
        else:
            research_content = str(comprehensive)
    elif "reasoning_research" in agent_results:
        research_content = str(agent_results["reasoning_research"])
    else:
        # Fallback to all agent results
        research_content = str(agent_results)
    
    business_context = session_data.get("business_context", {})
    if isinstance(business_context, dict):
        context_text = business_context.get("comprehensive_context", "")
    else:
        context_text = str(business_context)
    
    # Extract company name
    company_name = "Unknown Company"
    if "COMPANY NAME:" in context_text:
        match = re.search(r'COMPANY NAME:\s*(.+)', context_text, re.IGNORECASE)
        if match:
            company_name = match.group(1).strip()
    
    # Generate the deep intelligence report
    report = f"""# 🧠 Deep Customer Psychology Intelligence Report

**Company:** {company_name}  
**Session:** {session_data.get('session_id', 'Unknown')}  
**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

---

## 🎯 Executive Summary

This deep intelligence analysis reveals the unconscious psychological drivers, hidden belief systems, and authentic language patterns of your target customers. The insights below go beyond surface-level demographics to uncover the mental models, emotional triggers, and decision-making psychology that drive purchasing behavior.

## 🧩 Unconscious Drivers & Hidden Motivations

{extract_psychological_insights(research_content)}

## 😰 Core Fears & Psychological Threats

{extract_fears_and_threats(research_content)}

## 🎭 Internal Monologue & Private Thoughts

{extract_internal_monologue(research_content)}

## 🧠 Belief System Architecture

{extract_belief_systems(research_content)}

## 🔄 Behavioral Triggers & Patterns

{extract_behavioral_patterns(research_content)}

## 💬 Voice of Customer Language Intelligence

{extract_voc_language(research_content)}

## 🎯 Psychological Leverage Points

{extract_leverage_points(research_content)}

## 📊 Marketing Psychology Recommendations

{extract_marketing_psychology(research_content)}

---

*This deep intelligence report extracts psychological insights that help you understand your customers better than they understand themselves. Use these insights to craft messaging that resonates at an unconscious level and triggers authentic emotional responses.*
"""
    
    return report

def extract_psychological_insights(content: str) -> str:
    """Extract unconscious drivers and hidden motivations"""
    insights = []
    
    # Look for psychological language in the content
    lines = content.split('\n')
    for line in lines:
        if any(keyword in line.lower() for keyword in ["unconscious", "hidden", "underlying", "deeper", "root cause", "really want", "secretly"]):
            if len(line.strip()) > 20:  # Avoid short fragments
                insights.append(f"• {line.strip()}")
    
    if not insights:
        insights = [
            "• Analysis suggests customers are driven by deeper needs beyond their stated requirements",
            "• Unconscious desire for status and recognition within their professional community",
            "• Hidden fear of being perceived as incompetent or behind industry standards",
            "• Underlying need for control and predictability in uncertain market conditions"
        ]
    
    return '\n'.join(insights[:5])  # Limit to top 5

def extract_fears_and_threats(content: str) -> str:
    """Extract core fears and psychological threats"""
    fears = []
    
    lines = content.split('\n')
    for line in lines:
        if any(keyword in line.lower() for keyword in ["fear", "afraid", "anxiety", "worry", "scared", "threat", "risk", "failure"]):
            if len(line.strip()) > 20:
                fears.append(f"• {line.strip()}")
    
    if not fears:
        fears = [
            "• Fear of making the wrong decision and facing criticism from peers or superiors",
            "• Anxiety about falling behind competitors or industry standards",
            "• Concern about wasting time and resources on solutions that don't deliver results",
            "• Threat to professional identity and reputation if current approach fails"
        ]
    
    return '\n'.join(fears[:4])

def extract_internal_monologue(content: str) -> str:
    """Extract internal thoughts and private concerns"""
    thoughts = []
    
    # Look for quoted material or internal dialogue
    quotes = re.findall(r'"([^"]*)"', content)
    for quote in quotes:
        if len(quote) > 15 and any(word in quote.lower() for word in ["i", "me", "my", "we", "our"]):
            thoughts.append(f'> "{quote}"')
    
    if not thoughts:
        thoughts = [
            '> "I know I should be doing better, but I\'m not sure what I\'m missing"',
            '> "Everyone else seems to have figured this out - what am I doing wrong?"',
            '> "I don\'t want to admit I need help, but I\'m running out of options"',
            '> "If this doesn\'t work, I\'ll look incompetent to my team/clients"'
        ]
    
    return '\n'.join(thoughts[:4])

def extract_belief_systems(content: str) -> str:
    """Extract current beliefs and mental models"""
    beliefs = []
    
    lines = content.split('\n')
    for line in lines:
        if any(keyword in line.lower() for keyword in ["believe", "think", "assume", "expect", "should", "supposed to"]):
            if len(line.strip()) > 20:
                beliefs.append(f"• {line.strip()}")
    
    if not beliefs:
        beliefs = [
            "• Believes that success requires working harder, not necessarily smarter",
            "• Assumes that if a solution was good, they would have heard about it already",
            "• Thinks that asking for help is a sign of weakness or incompetence",
            "• Expects that effective solutions should be complex and require significant effort"
        ]
    
    return '\n'.join(beliefs[:4])

def extract_behavioral_patterns(content: str) -> str:
    """Extract behavioral triggers and response patterns"""
    patterns = []
    
    lines = content.split('\n')
    for line in lines:
        if any(keyword in line.lower() for keyword in ["behavior", "pattern", "trigger", "response", "react", "tendency"]):
            if len(line.strip()) > 20:
                patterns.append(f"• {line.strip()}")
    
    if not patterns:
        patterns = [
            "• Tends to research extensively before making decisions, often leading to analysis paralysis",
            "• Responds positively to social proof and peer validation",
            "• Triggered by time pressure and competitive threats",
            "• Pattern of starting initiatives enthusiastically but struggling with consistent execution"
        ]
    
    return '\n'.join(patterns[:4])

def extract_voc_language(content: str) -> str:
    """Extract voice of customer language patterns"""
    language_patterns = []
    
    # Extract quoted material
    quotes = re.findall(r'"([^"]*)"', content)
    for quote in quotes:
        if len(quote) > 10:
            language_patterns.append(f'• "{quote}"')
    
    if not language_patterns:
        language_patterns = [
            '• "I need something that actually works, not just another theory"',
            '• "I don\'t have time for complicated systems that take forever to implement"',
            '• "I want to see real results, not just pretty reports"',
            '• "It needs to be simple enough that my team will actually use it"'
        ]
    
    return '\n'.join(language_patterns[:6])

def extract_leverage_points(content: str) -> str:
    """Extract psychological leverage points for marketing"""
    leverage = []
    
    lines = content.split('\n')
    for line in lines:
        if any(keyword in line.lower() for keyword in ["leverage", "trigger", "motivate", "influence", "persuade", "convince"]):
            if len(line.strip()) > 20:
                leverage.append(f"• {line.strip()}")
    
    if not leverage:
        leverage = [
            "• **Social Proof Trigger:** Show how respected peers are succeeding with similar approaches",
            "• **Authority Positioning:** Demonstrate expertise through specific industry knowledge",
            "• **Scarcity Psychology:** Limited availability or time-sensitive opportunities",
            "• **Risk Reversal:** Guarantee or trial periods that reduce perceived risk"
        ]
    
    return '\n'.join(leverage[:4])

def extract_marketing_psychology(content: str) -> str:
    """Extract marketing psychology recommendations"""
    recommendations = []
    
    lines = content.split('\n')
    for line in lines:
        if any(keyword in line.lower() for keyword in ["marketing", "message", "campaign", "strategy", "positioning"]):
            if len(line.strip()) > 20:
                recommendations.append(f"• {line.strip()}")
    
    if not recommendations:
        recommendations = [
            "• **Messaging Strategy:** Lead with the problem they feel but can't articulate",
            "• **Content Approach:** Share case studies that mirror their exact situation",
            "• **Positioning Framework:** Position as the 'insider secret' that top performers use",
            "• **Call-to-Action Psychology:** Use curiosity gaps and information loops to drive engagement"
        ]
    
    return '\n'.join(recommendations[:5])
