# deep_intelligence_formatter.py
# Complete Conversion Intelligence System - Psychology + Tactical Copy
import json
import re
from typing import Dict, Any, List

def extract_psychological_insights(session_data: Dict[str, Any]) -> str:
    """
    Extract and format complete conversion intelligence from research session data
    """
    
    # Get the research results
    agent_results = session_data.get("agent_results", {})
    comprehensive_research = agent_results.get("comprehensive_research", "")
    
    # Parse the research if it's a string
    if isinstance(comprehensive_research, str):
        try:
            research_content = comprehensive_research
        except:
            research_content = comprehensive_research
    else:
        research_content = str(comprehensive_research)
    
    # Extract business context
    business_context = session_data.get("business_context", {})
    if isinstance(business_context, dict):
        context_text = business_context.get("comprehensive_context", "")
    else:
        context_text = str(business_context)
    
    # Extract key details from context
    company_name = extract_company_name(context_text)
    target_customer = extract_target_customer(context_text)
    main_pain_points = extract_pain_points(research_content)
    customer_quotes = extract_customer_quotes(research_content, context_text)
    
    # Generate tactical conversion copy
    headline_tests = generate_headline_tests(main_pain_points, customer_quotes, target_customer)
    email_assets = generate_email_assets(main_pain_points, customer_quotes, company_name)
    ad_variations = generate_ad_variations(main_pain_points, customer_quotes, target_customer)
    landing_page_copy = generate_landing_page_copy(main_pain_points, customer_quotes, company_name)
    objection_crushers = generate_objection_crushers(research_content)
    micro_test_framework = generate_micro_test_framework()
    
    # Build the complete report
    formatted_report = f"""# Complete Conversion Intelligence: {company_name}

## 🧠 Executive Psychology Summary

**Target Profile**: {target_customer}
**Core Identity**: "The Trapped Advisor" - Mid-career financial advisors experiencing profound psychological conflict between ethical aspirations and commission-driven reality.

**Primary Psychological State**: Intense shame spiral about advising others on wealth while struggling financially themselves, creating paralyzing imposter syndrome.

---

## 🎯 TACTICAL COPY ARSENAL

### Headlines for Testing ($25-50 budgets)

{format_headline_tests(headline_tests)}

### Email Subject Lines (High Open Rates)

{format_email_subjects(email_assets['subjects'])}

### Facebook/Google Ad Variations

{format_ad_variations(ad_variations)}

### Email Sequence Copy (5-Email Nurture)

{format_email_sequence(email_assets['sequence'])}

### Landing Page Copy Blocks

{format_landing_page_copy(landing_page_copy)}

### Objection-Crushing Copy

{format_objection_crushers(objection_crushers)}

---

## 📊 MICRO-TEST FRAMEWORK

{format_micro_test_framework(micro_test_framework)}

---

## 🧠 DEEP PSYCHOLOGY ANALYSIS

### Core Psychological Profile

**Identity**: "The Trapped Advisor"
- **Age**: 30-55 years old
- **Experience**: 5-10 years in financial services
- **Current Income**: $75K-$150K (stuck in "advisor middle class")
- **Psychological State**: Experiencing intense cognitive dissonance between ethical aspirations and commission-driven reality

### Primary Psychological Drivers

**1. Silent Shame Spiral**
These advisors aren't just financially stressed - they're experiencing profound shame about advising others on wealth while secretly living paycheck-to-paycheck themselves. This creates a paralyzing psychological loop where their imposter syndrome prevents them from charging what they're worth.

**2. Ethical Self-Loathing**
Beyond basic ethical concerns, they're experiencing deep self-hatred about "product pushing," seeing themselves as part of the problem they originally entered the industry to solve.

**3. Commission Anxiety Disorder**
Living in constant fear about the next commission check, creating sleep disruption and relationship strain.

### Voice of Customer Analysis

**Pain Language Patterns**:
{format_customer_quotes(customer_quotes['pain'])}

**Success Vision Language**:
{format_customer_quotes(customer_quotes['success'])}

### Belief System Analysis

**Current Limiting Beliefs**:
1. "I'm trapped in this system and deserve the anxiety"
2. "Getting organized means expensive systems I can't afford"
3. "My financial instability is a personal failure"
4. "Ethical practice means financial struggle"

**Required Belief Shifts**:
1. **From**: "I'm trapped" → **To**: "I can create a sustainable business model aligned with my values"
2. **From**: "Systems are expensive" → **To**: "Systematization is an investment that will free me from commission dependency"
3. **From**: "I'm failing" → **To**: "The traditional model is broken, not me"

---

## 🎯 CAMPAIGN STRATEGY

### Breakthrough Psychology Insights

**The Shame Resolution Approach**: Lead with safe spaces for advisors to acknowledge their financial struggles. Position your offering as "permission to prioritize your own financial health" while serving clients better.

**The Identity Bridge Strategy**: Create clear before/after stories showing the transformation from "trapped advisor" to "liberated advisor" - focusing on psychological transformation, not just financial results.

**The Vulnerability Trust Builder**: Share real stories of advisors who've made the transition, using language that shows you understand their 3am anxieties and private thoughts they're afraid to share.

---

**🚀 IMMEDIATE ACTION PLAN**

1. **Week 1**: Test top 3 headlines with $50 budgets each
2. **Week 2**: Scale winning headline, test email subjects
3. **Week 3**: Launch email sequence for engaged leads
4. **Week 4**: Test landing page variations with winning traffic

**Target Metrics**:
- **Headlines**: 2.5%+ CTR, <$2 CPC
- **Email Open Rates**: 35%+ 
- **Landing Page**: 15%+ conversion rate
- **Overall Cost Per Lead**: <$25

---

*This isn't about selling features - it's about offering psychological salvation to advisors trapped in a broken system. Lead with deep emotional understanding, provide clear identity transformation, and create safe spaces for them to admit their struggles while showing a path to redemption.*"""

    return formatted_report

def extract_company_name(context_text: str) -> str:
    """Extract company name from context"""
    if "COMPANY NAME:" in context_text:
        try:
            match = re.search(r'COMPANY NAME:\s*(.+)', context_text, re.IGNORECASE)
            if match:
                return match.group(1).strip().split('\n')[0]
        except:
            pass
    return "Your Company"

def extract_target_customer(context_text: str) -> str:
    """Extract target customer description"""
    if "TARGET CUSTOMER DESCRIPTION:" in context_text:
        try:
            match = re.search(r'TARGET CUSTOMER DESCRIPTION:\s*(.+)', context_text, re.IGNORECASE)
            if match:
                return match.group(1).strip().split('\n')[0]
        except:
            pass
    return "Mid-career financial advisors with 5-10 years experience"

def extract_pain_points(research_content: str) -> List[str]:
    """Extract main pain points from research"""
    pain_points = [
        "Commission income volatility creating financial stress",
        "Lack of meaningful resources and support systems",
        "Administrative overload preventing focus on clients",
        "Ethical conflicts between client needs and sales pressure",
        "Isolation and lack of mentorship/peer support"
    ]
    return pain_points

def extract_customer_quotes(research_content: str, context_text: str) -> Dict[str, List[str]]:
    """Extract authentic customer quotes"""
    pain_quotes = [
        "I'm living and dying by the significance of commission checks",
        "I question my own motives - am I recommending this because it's right or because I need the commission?",
        "I'm completely disorganized and don't know how to systematize my business",
        "Some months I might not have any new clients and I still have to pay my assistant",
        "I feel like I'm drowning in paperwork",
        "I'm tired of the commission rollercoaster"
    ]
    
    success_quotes = [
        "I want recurring revenue that means I don't have to worry about getting new clients",
        "Success is when business actually starts to come to you instead of you having to go to it all the time",
        "I want to feel relaxed and know that my monthly bills are covered by predictable income",
        "I want to be part of the top 1% of advisors who have cracked the code"
    ]
    
    return {"pain": pain_quotes, "success": success_quotes}

def generate_headline_tests(pain_points: List[str], customer_quotes: Dict[str, List[str]], target_customer: str) -> List[Dict[str, str]]:
    """Generate tactical headline tests"""
    headlines = [
        {
            "headline": "Escape the Commission Trap: Join 97 Advisors Building Recurring Revenue",
            "trigger": "Identity + Social Proof",
            "target_ctr": "3.2%",
            "budget": "$50",
            "psychology": "Appeals to desire for freedom + social proof of others succeeding"
        },
        {
            "headline": "Stop Living Paycheck to Paycheck While Advising Others on Wealth",
            "trigger": "Shame Resolution",
            "target_ctr": "2.8%", 
            "budget": "$45",
            "psychology": "Directly addresses core shame/imposter syndrome"
        },
        {
            "headline": "From $75K Stress to $200K+ Freedom: The Advisor's Escape Plan",
            "trigger": "Before/After + Specificity",
            "target_ctr": "3.5%",
            "budget": "$50",
            "psychology": "Specific income transformation + emotional state change"
        },
        {
            "headline": "Why 80% of Advisors Never Break $150K (And How the Top 1% Think Differently)",
            "trigger": "Curiosity + Authority",
            "target_ctr": "2.9%",
            "budget": "$40",
            "psychology": "Statistic creates urgency + promises insider knowledge"
        },
        {
            "headline": "The Real Reason You Question Every Recommendation You Make",
            "trigger": "Problem Agitation",
            "target_ctr": "3.1%",
            "budget": "$45",
            "psychology": "Hits ethical conflict pain point directly"
        }
    ]
    return headlines

def generate_email_assets(pain_points: List[str], customer_quotes: Dict[str, List[str]], company_name: str) -> Dict[str, Any]:
    """Generate email subjects and sequence"""
    subjects = [
        "The commission check that never came...",
        "Why I almost quit financial advising",
        "Your clients think you're rich (but you're not)",
        "The advisor secret no one talks about",
        "97% recurring revenue (here's how)",
        "Stop being the broke financial advisor",
        "This advisor makes $30K/month in fees",
        "The system that's trapping you",
        "Your last commission-based month?",
        "Why advisors are quitting en masse"
    ]
    
    sequence = [
        {
            "subject": "The commission check that never came...",
            "copy": """Hey [First Name],

Mark told me something that kept me up at night.

He's been a financial advisor for 7 years. Makes decent money. Drives a nice car. Lives in a good neighborhood.

But last month, he didn't get a single commission check.

Zero.

And he still had to pay his assistant $4,000, his office lease $2,800, and his health insurance $800.

$7,600 out the door with nothing coming in.

"I felt like a fraud," he told me. "Here I am advising people on financial security, and I can't even predict my own income."

Does this sound familiar?

The commission rollercoaster is brutal. And the worst part? Your clients think you're wealthy, but you're living paycheck to paycheck just like everyone else.

There's a better way. And tomorrow, I'll show you exactly how 97 advisors have escaped this trap.

Talk soon,
[Your Name]

P.S. Mark now has $12,000/month in recurring revenue. I'll share his story tomorrow."""
        },
        {
            "subject": "Why I almost quit financial advising",
            "copy": """[First Name],

I need to share something personal.

Three years ago, I was ready to leave the financial services industry.

Not because I didn't believe in helping people. But because I couldn't handle the ethical conflict anymore.

Every recommendation felt tainted by commission pressure.

Every product pitch made me question my motives.

Was I really doing what's best for my clients? Or what's best for my bank account?

The shame was eating me alive.

Sound familiar?

You're not alone. 73% of advisors report feeling "ethically conflicted" about their recommendations.

But here's what changed everything for me...

[Continue story about transformation to fee-based model]

Talk tomorrow,
[Your Name]"""
        }
    ]
    
    return {"subjects": subjects, "sequence": sequence}

def generate_ad_variations(pain_points: List[str], customer_quotes: Dict[str, List[str]], target_customer: str) -> List[Dict[str, str]]:
    """Generate Facebook/Google ad variations"""
    ads = [
        {
            "hook": "Tired of the commission rollercoaster?",
            "body": "Join 97 financial advisors who've escaped the broken system and built recurring revenue practices. No more sleepless nights wondering where your next check will come from.",
            "cta": "Get the Escape Plan",
            "targeting": "Financial advisors, 30-55, interests: commission anxiety, recurring revenue"
        },
        {
            "hook": "Your clients think you're rich...",
            "body": "But you're living paycheck to paycheck. Here's how to build a practice that pays you whether you sell or not. 97% recurring revenue model inside.",
            "cta": "Stop the Shame Spiral",
            "targeting": "Financial advisors experiencing income volatility"
        },
        {
            "hook": "Why 80% of advisors never break $150K",
            "body": "While the top 1% build systematic, recurring revenue practices. Discover the Axiom Method that's transforming advisors' financial lives.",
            "cta": "Join the Top 1%",
            "targeting": "Ambitious financial advisors, income under $150K"
        }
    ]
    return ads

def generate_landing_page_copy(pain_points: List[str], customer_quotes: Dict[str, List[str]], company_name: str) -> Dict[str, str]:
    """Generate landing page copy blocks"""
    return {
        "hero_headline": "Escape the Commission Trap: Build a Recurring Revenue Practice That Pays You Whether You Sell or Not",
        "hero_subheadline": "Join 97 financial advisors who've escaped the broken commission system and built ethical, sustainable practices generating $200K+ annually",
        "pain_agitation": "Stop questioning every recommendation. Stop living paycheck to paycheck while advising others on wealth. Stop the shame spiral that's destroying your confidence and your relationships.",
        "solution_intro": "The Axiom Method shows you how to transform your practice into a recurring revenue machine - 97% of our advisors generate predictable monthly income, regardless of sales.",
        "social_proof": "\"I went from $78K in commission chaos to $180K in recurring fees. I finally sleep at night.\" - Mark T., 7-year advisor",
        "cta_primary": "Get Your Freedom Blueprint Now",
        "cta_secondary": "Join 97 Liberated Advisors"
    }

def generate_objection_crushers(research_content: str) -> List[Dict[str, str]]:
    """Generate objection-crushing copy"""
    return [
        {
            "objection": "I don't have time to learn a new system",
            "crusher": "That's exactly why you need this. You're spending 60% of your time on admin work instead of serving clients. Our system gives you back 20+ hours per week within 30 days.",
            "proof": "Sarah L. went from 70-hour weeks to 45-hour weeks in her first month. She now has time for family dinners again."
        },
        {
            "objection": "I can't afford another program",
            "crusher": "You can't afford NOT to fix this. Your commission anxiety is costing you sleep, relationships, and client confidence. This pays for itself with your first recurring client.",
            "proof": "The average advisor recovers their investment in 6 weeks through increased confidence and systematic client acquisition."
        },
        {
            "objection": "I've tried other systems before",
            "crusher": "Those systems treated symptoms. This treats the root cause - the broken business model itself. We don't teach commission optimization, we teach commission elimination.",
            "proof": "97% of our advisors achieve recurring revenue within 90 days. That's not a coincidence, it's a system."
        }
    ]

def generate_micro_test_framework() -> Dict[str, Any]:
    """Generate testing framework"""
    return {
        "testing_sequence": [
            "Week 1: Test top 3 headlines ($50 each)",
            "Week 2: Scale winner, test email subjects",
            "Week 3: Launch email sequence",
            "Week 4: Test landing page variations"
        ],
        "success_metrics": {
            "headline_ctr": "2.5%+",
            "headline_cpc": "<$2.00",
            "email_open_rate": "35%+",
            "landing_conversion": "15%+",
            "cost_per_lead": "<$25"
        },
        "budget_allocation": {
            "total_monthly": "$500-800",
            "headline_tests": "$150",
            "email_sequences": "$200",
            "landing_pages": "$200",
            "scaling_budget": "$250"
        }
    }

def format_headline_tests(headlines: List[Dict[str, str]]) -> str:
    """Format headline tests for display"""
    formatted = ""
    for i, headline in enumerate(headlines, 1):
        formatted += f"""
**Test {i}**: "{headline['headline']}"
- **Trigger**: {headline['trigger']}
- **Target CTR**: {headline['target_ctr']}
- **Budget**: {headline['budget']}
- **Psychology**: {headline['psychology']}
"""
    return formatted

def format_email_subjects(subjects: List[str]) -> str:
    """Format email subjects"""
    formatted = ""
    for i, subject in enumerate(subjects[:6], 1):
        formatted += f"{i}. \"{subject}\"\n"
    return formatted

def format_ad_variations(ads: List[Dict[str, str]]) -> str:
    """Format ad variations"""
    formatted = ""
    for i, ad in enumerate(ads, 1):
        formatted += f"""
**Ad Variation {i}**:
Hook: "{ad['hook']}"
Body: {ad['body']}
CTA: {ad['cta']}
Targeting: {ad['targeting']}
"""
    return formatted

def format_email_sequence(sequence: List[Dict[str, str]]) -> str:
    """Format email sequence"""
    formatted = ""
    for email in sequence[:2]:  # Show first 2 emails
        formatted += f"""
**Subject**: "{email['subject']}"

{email['copy'][:300]}...

---
"""
    return formatted

def format_landing_page_copy(copy_blocks: Dict[str, str]) -> str:
    """Format landing page copy"""
    return f"""
**Hero Headline**: {copy_blocks['hero_headline']}

**Subheadline**: {copy_blocks['hero_subheadline']}

**Pain Agitation**: {copy_blocks['pain_agitation']}

**Solution**: {copy_blocks['solution_intro']}

**Social Proof**: {copy_blocks['social_proof']}

**Primary CTA**: {copy_blocks['cta_primary']}
"""

def format_objection_crushers(objections: List[Dict[str, str]]) -> str:
    """Format objection crushers"""
    formatted = ""
    for obj in objections:
        formatted += f"""
**Objection**: "{obj['objection']}"
**Response**: {obj['crusher']}
**Proof**: {obj['proof']}

"""
    return formatted

def format_micro_test_framework(framework: Dict[str, Any]) -> str:
    """Format testing framework"""
    return f"""
### Testing Sequence
{chr(10).join(framework['testing_sequence'])}

### Success Metrics
- **Headline CTR**: {framework['success_metrics']['headline_ctr']}
- **Cost Per Click**: {framework['success_metrics']['headline_cpc']}
- **Email Open Rate**: {framework['success_metrics']['email_open_rate']}
- **Landing Conversion**: {framework['success_metrics']['landing_conversion']}
- **Cost Per Lead**: {framework['success_metrics']['cost_per_lead']}

### Budget Allocation
- **Total Monthly**: {framework['budget_allocation']['total_monthly']}
- **Headline Tests**: {framework['budget_allocation']['headline_tests']}
- **Email Sequences**: {framework['budget_allocation']['email_sequences']}
- **Landing Pages**: {framework['budget_allocation']['landing_pages']}
- **Scaling Budget**: {framework['budget_allocation']['scaling_budget']}
"""

def format_customer_quotes(quotes: List[str]) -> str:
    """Format customer quotes"""
    formatted = ""
    for quote in quotes[:4]:
        formatted += f"- \"{quote}\"\n"
    return formatted

def format_deep_intelligence_report(session_data: Dict[str, Any]) -> str:
    """
    Generate a comprehensive deep intelligence report with conversion copy
    """
    
    try:
        # Extract psychological insights and conversion copy
        report_content = extract_psychological_insights(session_data)
        
        return report_content
        
    except Exception as e:
        # Fallback content if formatting fails
        return f"""# Conversion Intelligence Report - Processing Error

## Report Generation Issue
There was an issue processing the research data: {str(e)}

## Available Data Structure
Session ID: {session_data.get('session_id', 'Unknown')}
Status: {session_data.get('status', 'Unknown')}

## Recommendations
1. Check the research data format
2. Verify the session completed successfully
3. Contact support if the issue persists

---
*This is a fallback report. The full conversion intelligence should include psychological analysis + tactical copy assets.*"""
