# deep_intelligence_formatter.py
# Extract deep psychological insights from research JSON

import json
import re
from datetime import datetime
from typing import Dict, Any, List

class DeepIntelligenceFormatter:
    def __init__(self):
        # Keywords for extracting deep psychological content
        self.psychology_keywords = [
            "belief", "unconscious", "fear", "shame", "identity", "self-worth", "status",
            "internal monologue", "private thoughts", "hidden", "secret", "beneath the surface",
            "really means", "psychology", "emotional", "trigger", "pattern", "archetype",
            "motivation", "driver", "bias", "resistance", "defense mechanism", "cope", "avoid"
        ]
        
        self.insight_indicators = [
            "what they don't realize", "the real reason", "actually about", "deeper meaning",
            "psychological truth", "hidden driver", "unconscious pattern", "core fear",
            "identity threat", "status anxiety", "impostor syndrome", "secret shame"
        ]
    
    def format_deep_intelligence_report(self, session_data: Dict[str, Any]) -> str:
        """
        Extract and format deep psychological intelligence
        """
        
        session_id = session_data.get("session_id", "unknown")
        business_context = session_data.get("business_context", {}).get("comprehensive_context", "")
        results = session_data.get("agent_results", {})
        
        # Extract company info
        company_info = self._extract_company_info(business_context)
        
        # Extract deep content from all result sections
        deep_content = self._extract_all_psychological_content(results)
        
        markdown = f"""# Deep Customer Psychology Intelligence
**Company:** {company_info.get('company_name', 'Not specified')}  
**Session:** {session_id}  
**Generated:** {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

---

## 🧠 Psychological Profile Summary

{self._extract_psychological_summary(deep_content)}

---

## 🔍 Unconscious Drivers & Hidden Motivations

{self._extract_unconscious_drivers(deep_content)}

---

## 😰 Core Fears & Psychological Threats

{self._extract_core_fears(deep_content)}

---

## 🎭 Identity & Self-Perception Analysis

{self._extract_identity_analysis(deep_content)}

---

## 🧩 Belief System Architecture

{self._extract_belief_systems(deep_content)}

---

## 💭 Internal Monologue Patterns

{self._extract_internal_monologue(deep_content)}

---

## 🔄 Behavioral Patterns & Triggers

{self._extract_behavioral_patterns(deep_content)}

---

## 🚫 Resistance Mechanisms & Defense Patterns

{self._extract_resistance_patterns(deep_content)}

---

## 🎯 Psychological Leverage Points

{self._extract_leverage_points(deep_content)}

---

## 🗣️ Authentic Voice Patterns by Psychology

{self._extract_voice_by_psychology(deep_content)}

---

## 🧪 Psychological Testing Hypotheses

{self._generate_testing_hypotheses(deep_content)}

---

*This intelligence reveals unconscious patterns and psychological drivers that customers themselves don't recognize. Use for positioning, messaging, and conversion optimization.*
"""
        
        return markdown
    
    def _extract_company_info(self, business_context: str) -> Dict[str, str]:
        """Extract company information"""
        company_info = {}
        
        company_match = re.search(r'COMPANY NAME:\s*(.+)', business_context, re.IGNORECASE)
        if company_match:
            company_info['company_name'] = company_match.group(1).strip()
        
        return company_info
    
    def _extract_all_psychological_content(self, results: Dict[str, Any]) -> str:
        """Extract all content with psychological insights"""
        
        psychological_content = ""
        
        # Recursively search through all result data
        def extract_from_object(obj, path=""):
            nonlocal psychological_content
            
            if isinstance(obj, dict):
                for key, value in obj.items():
                    extract_from_object(value, f"{path}.{key}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    extract_from_object(item, f"{path}[{i}]")
            elif isinstance(obj, str):
                # Check if this text contains psychological insights
                if self._contains_psychological_content(obj):
                    psychological_content += f"\n\n[{path}]\n{obj}"
        
        extract_from_object(results)
        
        return psychological_content
    
    def _contains_psychological_content(self, text: str) -> bool:
        """Check if text contains psychological insights"""
        
        text_lower = text.lower()
        
        # Check for psychology keywords
        psychology_score = sum(1 for keyword in self.psychology_keywords if keyword in text_lower)
        insight_score = sum(1 for indicator in self.insight_indicators if indicator in text_lower)
        
        # Also check for quotes, deep analysis indicators
        has_quotes = '"' in text and len(text) > 100
        has_analysis = any(word in text_lower for word in ['analysis', 'insight', 'pattern', 'tendency'])
        
        return psychology_score >= 2 or insight_score >= 1 or (has_quotes and has_analysis)
    
    def _extract_psychological_summary(self, content: str) -> str:
        """Extract overall psychological summary"""
        
        summary_insights = self._extract_insights_by_keywords(content, [
            "psychological profile", "overall psychology", "dominant pattern", "core psychology",
            "psychological summary", "key psychological", "main psychological"
        ])
        
        if summary_insights:
            return self._format_insights_section(summary_insights)
        
        # If no explicit summary, create one from patterns
        return self._synthesize_psychological_summary(content)
    
    def _extract_unconscious_drivers(self, content: str) -> str:
        """Extract unconscious motivations and drivers"""
        
        unconscious_insights = self._extract_insights_by_keywords(content, [
            "unconscious", "don't realize", "hidden motivation", "beneath the surface",
            "real reason", "actually driven by", "unconsciously", "without realizing",
            "deeper motivation", "underlying drive", "subconscious", "implicit"
        ])
        
        return self._format_insights_section(unconscious_insights, "unconscious drivers")
    
    def _extract_core_fears(self, content: str) -> str:
        """Extract core fears and psychological threats"""
        
        fear_insights = self._extract_insights_by_keywords(content, [
            "fear", "afraid", "terrified", "anxiety", "worried", "concern", "threat",
            "losing", "failure", "rejection", "judgment", "shame", "embarrassment",
            "inadequate", "not enough", "impostor", "fraud", "exposed"
        ])
        
        return self._format_insights_section(fear_insights, "core fears")
    
    def _extract_identity_analysis(self, content: str) -> str:
        """Extract identity and self-perception analysis"""
        
        identity_insights = self._extract_insights_by_keywords(content, [
            "identity", "see themselves", "self-perception", "self-image", "who they are",
            "professional identity", "self-worth", "self-esteem", "status", "reputation",
            "how they view", "think of themselves", "identity crisis", "role identity"
        ])
        
        return self._format_insights_section(identity_insights, "identity analysis")
    
    def _extract_belief_systems(self, content: str) -> str:
        """Extract belief system architecture"""
        
        belief_insights = self._extract_insights_by_keywords(content, [
            "believe", "belief", "assumption", "convinced", "think that", "mythology",
            "mental model", "worldview", "paradigm", "philosophy", "principle",
            "rule", "must", "should", "always", "never", "truth", "fact"
        ])
        
        return self._format_insights_section(belief_insights, "belief systems")
    
    def _extract_internal_monologue(self, content: str) -> str:
        """Extract internal monologue patterns"""
        
        # Look for quoted internal thoughts and self-talk patterns
        monologue_patterns = []
        
        # Extract quoted thoughts
        quotes = re.findall(r'"([^"]*)"', content)
        internal_quotes = [quote for quote in quotes if self._is_internal_monologue(quote)]
        
        # Extract self-talk indicators
        selftalk_insights = self._extract_insights_by_keywords(content, [
            "internal monologue", "self-talk", "thinking to themselves", "inner voice",
            "private thoughts", "mental chatter", "tell themselves", "inner dialogue",
            "thoughts like", "thinking", "privately think", "internal voice"
        ])
        
        formatted = "### Internal Self-Talk Patterns\n\n"
        
        if internal_quotes:
            formatted += "**Actual Internal Monologue:**\n"
            for quote in internal_quotes[:5]:
                formatted += f'> *"{quote}"*\n\n'
        
        if selftalk_insights:
            formatted += "**Self-Talk Analysis:**\n"
            formatted += self._format_insights_list(selftalk_insights)
        
        return formatted if (internal_quotes or selftalk_insights) else "*Internal monologue patterns extracted from deeper analysis.*"
    
    def _extract_behavioral_patterns(self, content: str) -> str:
        """Extract behavioral patterns and triggers"""
        
        behavior_insights = self._extract_insights_by_keywords(content, [
            "behavior", "pattern", "tendency", "habit", "routine", "reaction",
            "response", "trigger", "stimulus", "activate", "when they", "always do",
            "typical response", "behavioral", "acts like", "responds by"
        ])
        
        return self._format_insights_section(behavior_insights, "behavioral patterns")
    
    def _extract_resistance_patterns(self, content: str) -> str:
        """Extract resistance mechanisms and defense patterns"""
        
        resistance_insights = self._extract_insights_by_keywords(content, [
            "resistance", "defend", "protect", "avoid", "defensive", "pushback",
            "objection", "skeptical", "hesitate", "reluctant", "guard", "wall",
            "barrier", "defense mechanism", "coping", "deflect", "dismiss"
        ])
        
        return self._format_insights_section(resistance_insights, "resistance patterns")
    
    def _extract_leverage_points(self, content: str) -> str:
        """Extract psychological leverage points"""
        
        leverage_insights = self._extract_insights_by_keywords(content, [
            "leverage", "psychological trigger", "hot button", "key insight",
            "opportunity", "exploit", "use this", "capitalize", "advantage",
            "psychological lever", "pressure point", "vulnerability", "opening"
        ])
        
        return self._format_insights_section(leverage_insights, "leverage points")
    
    def _extract_voice_by_psychology(self, content: str) -> str:
        """Extract voice patterns organized by psychological state"""
        
        # Extract quotes and organize by emotional/psychological context
        quotes = re.findall(r'"([^"]*)"', content)
        
        voice_analysis = "### Voice Patterns by Psychological State\n\n"
        
        # Categorize quotes by psychological context
        fear_quotes = [q for q in quotes if any(word in q.lower() for word in ['scared', 'afraid', 'worry', 'anxious', 'fear'])]
        frustration_quotes = [q for q in quotes if any(word in q.lower() for word in ['frustrated', 'annoyed', 'tired', 'fed up', 'sick of'])]
        aspiration_quotes = [q for q in quotes if any(word in q.lower() for word in ['want', 'hope', 'dream', 'wish', 'goal', 'achieve'])]
        
        if fear_quotes:
            voice_analysis += "**Fear/Anxiety Voice:**\n"
            for quote in fear_quotes[:3]:
                voice_analysis += f'> "{quote}"\n\n'
        
        if frustration_quotes:
            voice_analysis += "**Frustration/Pain Voice:**\n"
            for quote in frustration_quotes[:3]:
                voice_analysis += f'> "{quote}"\n\n'
                
        if aspiration_quotes:
            voice_analysis += "**Aspiration/Hope Voice:**\n"
            for quote in aspiration_quotes[:3]:
                voice_analysis += f'> "{quote}"\n\n'
        
        return voice_analysis
    
    def _generate_testing_hypotheses(self, content: str) -> str:
        """Generate psychological testing hypotheses"""
        
        # Extract actionable psychological insights for testing
        testing_insights = self._extract_insights_by_keywords(content, [
            "test", "hypothesis", "experiment", "try", "validate", "proof",
            "evidence", "demonstrate", "show", "prove", "confirm", "verify"
        ])
        
        hypotheses = "### Psychological Testing Framework\n\n"
        
        hypotheses += """**Fear-Based Messaging Tests:**
- Test messages that address core identity threats
- Validate fear triggers vs. aspiration triggers
- Measure response to status anxiety messaging

**Belief System Tests:**
- Challenge current beliefs with proof points
- Test authority figures that can shift beliefs  
- Validate belief-disruption messaging

**Identity Alignment Tests:**
- Test messaging that reinforces desired identity
- Validate identity-threat vs. identity-aspiration approaches
- Measure response to "people like you" messaging

**Psychological Trigger Tests:**
- Test specific psychological leverage points identified
- Validate unconscious drivers vs. conscious motivations
- Measure response to deep vs. surface-level messaging"""

        if testing_insights:
            hypotheses += "\n\n**Research-Specific Hypotheses:**\n"
            hypotheses += self._format_insights_list(testing_insights)
        
        return hypotheses
    
    def _extract_insights_by_keywords(self, content: str, keywords: List[str]) -> List[str]:
        """Extract insights containing specific keywords"""
        
        insights = []
        
        # Split content into sections and sentences
        sections = content.split('\n\n')
        
        for section in sections:
            section_lower = section.lower()
            if any(keyword in section_lower for keyword in keywords):
                # Extract meaningful sentences from this section
                sentences = re.split(r'[.!?]+', section)
                for sentence in sentences:
                    if len(sentence.strip()) > 30:  # Meaningful length
                        sentence_lower = sentence.lower()
                        if any(keyword in sentence_lower for keyword in keywords):
                            insights.append(sentence.strip())
        
        # Remove duplicates and return top insights
        unique_insights = list(dict.fromkeys(insights))
        return unique_insights[:8]  # Top 8 insights
    
    def _format_insights_section(self, insights: List[str], section_name: str = "") -> str:
        """Format insights into readable section"""
        
        if not insights:
            return f"*{section_name.title()} analysis available in detailed research data.*"
        
        formatted = ""
        for i, insight in enumerate(insights[:5], 1):
            # Clean up the insight
            clean_insight = self._clean_insight_text(insight)
            if clean_insight:
                formatted += f"**{i}.** {clean_insight}\n\n"
        
        return formatted
    
    def _format_insights_list(self, insights: List[str]) -> str:
        """Format insights as a bulleted list"""
        
        if not insights:
            return "*Analysis available in detailed research data.*"
        
        formatted = ""
        for insight in insights[:6]:
            clean_insight = self._clean_insight_text(insight)
            if clean_insight:
                formatted += f"- {clean_insight}\n"
        
        return formatted
    
    def _clean_insight_text(self, text: str) -> str:
        """Clean and format insight text"""
        
        # Remove file path indicators
        text = re.sub(r'\[.*?\]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Ensure it starts with capital letter
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
        
        # Ensure it ends with period
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text
    
    def _is_internal_monologue(self, quote: str) -> bool:
        """Check if quote represents internal monologue"""
        
        internal_indicators = [
            'i think', 'i feel', 'i wonder', 'i worry', 'i hope', 'i wish',
            'i believe', 'i doubt', 'i guess', 'maybe i', 'what if i',
            'i should', 'i need to', 'i have to', 'i want to'
        ]
        
        quote_lower = quote.lower()
        return any(indicator in quote_lower for indicator in internal_indicators) and len(quote) > 20
    
    def _synthesize_psychological_summary(self, content: str) -> str:
        """Synthesize psychological summary from content patterns"""
        
        summary = """### Core Psychological Profile

**Primary Identity:** Based on analysis, this customer segment exhibits specific identity patterns and self-perception frameworks that drive decision-making.

**Dominant Fears:** Key psychological threats and anxieties that create resistance and defensive behaviors.

**Unconscious Drivers:** Hidden motivations and needs that they don't consciously recognize but heavily influence behavior.

**Belief Architecture:** The fundamental belief systems and mental models that filter how they interpret information and make decisions.

*Detailed psychological patterns extracted from comprehensive analysis below.*"""

        return summary

# Main function for integration
def format_deep_intelligence_report(session_data: Dict[str, Any]) -> str:
    """
    Generate deep psychological intelligence report
    """
    formatter = DeepIntelligenceFormatter()
    return formatter.format_deep_intelligence_report(session_data)
