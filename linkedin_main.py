import streamlit as st
import json
import os
from datetime import datetime, timedelta
import time
import random

# LinkedIn-focused configuration
class LinkedInConfig:
    APP_NAME = "ContentCraft AI - LinkedIn Post Generator"
    VERSION = "2.0.0"
    
    # LinkedIn-specific settings
    MAX_CHARS = 3000
    OPTIMAL_LENGTH = {
        "Short": "1-5 lines (125-300 chars)",
        "Medium": "6-10 lines (300-600 chars)", 
        "Long": "11-15 lines (600-1300 chars)"
    }
    
    # LinkedIn content types
    CONTENT_TYPES = [
        "Professional Update", "Thought Leadership", "Industry Insights", 
        "Personal Story", "Career Advice", "Company News", 
        "Achievement/Milestone", "Question/Poll", "Tips & Best Practices",
        "Behind the Scenes", "Team Spotlight", "Learning & Development"
    ]
    
    # LinkedIn-specific topics
    TOPICS = [
        "Leadership", "Career Growth", "Technology", "Innovation", 
        "Entrepreneurship", "Team Building", "Professional Development",
        "Industry Trends", "Networking", "Work-Life Balance",
        "Digital Transformation", "Remote Work", "Mentorship"
    ]
    
    # Professional tones for LinkedIn
    TONES = [
        "Professional", "Inspirational", "Educational", "Conversational",
        "Authoritative", "Humble", "Motivational", "Analytical"
    ]
    
    # Industries
    INDUSTRIES = [
        "Technology", "Finance", "Healthcare", "Education", "Marketing",
        "Sales", "Consulting", "Manufacturing", "Real Estate", "Legal",
        "HR & Recruiting", "Non-Profit", "Government", "Retail"
    ]
    
    # LinkedIn engagement elements
    ENGAGEMENT_ELEMENTS = {
        "Call-to-Action": ["What's your experience?", "Share your thoughts", "Tag someone who needs to see this"],
        "Questions": ["What would you add?", "How do you handle this?", "What's worked for you?"],
        "Hashtags": ["#Leadership", "#CareerGrowth", "#Innovation", "#ProfessionalDevelopment"]
    }

config = LinkedInConfig()

# Advanced LinkedIn post generator
class LinkedInPostGenerator:
    def __init__(self):
        self.templates = self._load_templates()
        self.engagement_boosters = self._load_engagement_boosters()
    
    def _load_templates(self):
        return {
            "Professional Update": {
                "structure": "Hook → Context → Insight → Call-to-Action",
                "templates": {
                    "Short": "🚀 {hook}\n\n{insight}\n\n{cta}",
                    "Medium": "🚀 {hook}\n\n{context}\n\nKey takeaway: {insight}\n\n{cta}",
                    "Long": "🚀 {hook}\n\n{context}\n\nHere's what I learned:\n• {point1}\n• {point2}\n• {point3}\n\n{insight}\n\n{cta}"
                }
            },
            "Thought Leadership": {
                "structure": "Bold Statement → Evidence → Analysis → Future Outlook",
                "templates": {
                    "Short": "💡 {bold_statement}\n\n{evidence}\n\nThoughts?",
                    "Medium": "💡 {bold_statement}\n\n{evidence}\n\n{analysis}\n\nWhat's your take?",
                    "Long": "💡 {bold_statement}\n\n{evidence}\n\n{analysis}\n\nLooking ahead: {future_outlook}\n\nHow do you see this evolving?"
                }
            },
            "Career Advice": {
                "structure": "Problem → Solution → Example → Actionable Tip",
                "templates": {
                    "Short": "💼 {problem}\n\n{solution}\n\nTry this: {tip}",
                    "Medium": "💼 {problem}\n\n{solution}\n\nExample: {example}\n\nActionable tip: {tip}",
                    "Long": "💼 {problem}\n\n{solution}\n\nReal example: {example}\n\nHere's how to apply this:\n1. {step1}\n2. {step2}\n3. {step3}\n\nWhat's worked for you?"
                }
            }
        }
    
    def _load_engagement_boosters(self):
        return {
            "hooks": [
                "Here's what nobody tells you about {topic}:",
                "I made a mistake that cost me {impact}. Here's what I learned:",
                "After {timeframe} in {industry}, here's my biggest insight:",
                "The best advice I ever received about {topic}:",
                "This simple change increased my {metric} by {percentage}:"
            ],
            "storytelling": [
                "Let me tell you about a conversation that changed everything...",
                "Three years ago, I was struggling with {challenge}...",
                "I'll never forget the day when...",
                "Here's a story that perfectly illustrates why {topic} matters:"
            ],
            "statistics": [
                "Did you know that {percentage}% of professionals struggle with {topic}?",
                "Recent studies show that {statistic}...",
                "The data is clear: {finding}..."
            ]
        }
    
    def generate_post(self, content_type, topic, length, tone, industry, include_hashtags=True, include_cta=True):
        template = self.templates.get(content_type, self.templates["Professional Update"])
        post_template = template["templates"][length]
        
        # Generate content based on inputs
        content_vars = self._generate_content_variables(content_type, topic, tone, industry)
        
        # Fill template
        try:
            post = post_template.format(**content_vars)
        except KeyError:
            # Fallback if template variables don't match
            post = self._generate_fallback_post(content_type, topic, length, tone, industry)
        
        # Add hashtags if requested
        if include_hashtags:
            hashtags = self._generate_hashtags(topic, industry)
            post += f"\n\n{' '.join(hashtags[:5])}"
        
        # Ensure within LinkedIn character limit
        if len(post) > config.MAX_CHARS:
            post = post[:config.MAX_CHARS-3] + "..."
        
        return post
    
    def _generate_content_variables(self, content_type, topic, tone, industry):
        # Generate contextual content based on inputs
        hooks = [
            f"The {industry.lower()} industry is evolving rapidly, especially around {topic.lower()}.",
            f"After years in {industry.lower()}, I've learned something crucial about {topic.lower()}.",
            f"Here's an unpopular opinion about {topic.lower()} in {industry.lower()}:",
        ]
        
        contexts = [
            f"Working in {industry.lower()}, I've seen how {topic.lower()} impacts everything we do.",
            f"The conversation around {topic.lower()} has shifted dramatically in {industry.lower()}.",
            f"Every {industry.lower()} professional should understand {topic.lower()}."
        ]
        
        insights = [
            f"The key to success in {topic.lower()} isn't what most people think.",
            f"Sustainable {topic.lower()} requires a {tone.lower()} approach.",
            f"The future of {topic.lower()} in {industry.lower()} depends on how we adapt today."
        ]
        
        ctas = [
            "What's been your experience with this?",
            f"How do you approach {topic.lower()} in your role?",
            "I'd love to hear your thoughts in the comments.",
            f"What would you add to this {topic.lower()} discussion?"
        ]
        
        return {
            "hook": random.choice(hooks),
            "context": random.choice(contexts),
            "insight": random.choice(insights),
            "cta": random.choice(ctas),
            "bold_statement": f"{topic} is fundamentally changing how we work in {industry.lower()}.",
            "evidence": f"Recent trends in {industry.lower()} show a 40% increase in {topic.lower()}-related initiatives.",
            "analysis": f"This shift represents more than just a trend—it's a fundamental change in how {industry.lower()} operates.",
            "future_outlook": f"I predict {topic.lower()} will become the standard in {industry.lower()} within 3 years.",
            "problem": f"Many {industry.lower()} professionals struggle with {topic.lower()}.",
            "solution": f"The solution isn't more tools—it's a {tone.lower()} mindset shift.",
            "example": f"Last month, I helped a {industry.lower()} team improve their {topic.lower()} approach by 60%.",
            "tip": f"Start small: focus on one aspect of {topic.lower()} and master it first.",
            "step1": f"Assess your current {topic.lower()} strategy",
            "step2": f"Identify the biggest gap in your {topic.lower()} approach",
            "step3": f"Implement one small change and measure the impact",
            "point1": f"{topic} requires consistent effort, not perfection",
            "point2": f"The best {topic.lower()} strategies are simple and sustainable",
            "point3": f"Success in {topic.lower()} comes from helping others succeed too"
        }
    
    def _generate_fallback_post(self, content_type, topic, length, tone, industry):
        if length == "Short":
            return f"💼 Reflecting on {topic.lower()} in {industry.lower()} today.\n\nThe key insight? A {tone.lower()} approach always wins.\n\nWhat's your experience been?"
        elif length == "Medium":
            return f"💼 {topic} continues to evolve in the {industry.lower()} space.\n\nAfter working in this field, I've learned that success comes from maintaining a {tone.lower()} perspective while staying adaptable.\n\nThe companies thriving today are those that embrace change while staying true to their values.\n\nWhat trends are you seeing in your industry?"
        else:
            return f"💼 The landscape of {topic.lower()} in {industry.lower()} has changed dramatically.\n\nWhen I started my career, the approach was very different. Today, success requires:\n\n• A {tone.lower()} mindset that embraces continuous learning\n• The ability to adapt quickly to new challenges\n• Strong relationships built on trust and mutual respect\n\nThe professionals who thrive are those who view every challenge as an opportunity to grow.\n\nLooking ahead, I believe {topic.lower()} will become even more critical to success in {industry.lower()}.\n\nWhat's one lesson that's shaped your approach to {topic.lower()}?"
    
    def _generate_hashtags(self, topic, industry):
        topic_hashtags = {
            "Leadership": ["#Leadership", "#Management", "#TeamBuilding", "#ExecutiveCoaching"],
            "Career Growth": ["#CareerGrowth", "#ProfessionalDevelopment", "#CareerAdvice", "#Success"],
            "Technology": ["#Technology", "#Innovation", "#DigitalTransformation", "#TechTrends"],
            "Entrepreneurship": ["#Entrepreneurship", "#Startup", "#Business", "#Innovation"],
            "Networking": ["#Networking", "#Relationships", "#ProfessionalNetworking", "#Career"]
        }
        
        industry_hashtags = {
            "Technology": ["#Tech", "#Software", "#AI", "#Cloud"],
            "Finance": ["#Finance", "#Banking", "#FinTech", "#Investment"],
            "Healthcare": ["#Healthcare", "#MedTech", "#PatientCare", "#HealthInnovation"],
            "Marketing": ["#Marketing", "#DigitalMarketing", "#ContentMarketing", "#Branding"]
        }
        
        base_hashtags = topic_hashtags.get(topic, ["#Professional", "#Growth", "#Success"])
        industry_tags = industry_hashtags.get(industry, [f"#{industry.replace(' ', '')}"])
        
        return base_hashtags + industry_tags + ["#LinkedIn", "#Networking"]
    
    def get_optimization_suggestions(self, post_content):
        suggestions = []
        
        # Length analysis
        char_count = len(post_content)
        if char_count < 100:
            suggestions.append("💡 Consider adding more context - posts with 150+ characters get better engagement")
        elif char_count > 1300:
            suggestions.append("⚠️ Consider shortening - very long posts may lose reader attention")
        
        # Engagement elements
        if "?" not in post_content:
            suggestions.append("❓ Add a question to encourage comments and engagement")
        
        if not any(emoji in post_content for emoji in ["🚀", "💼", "💡", "🌟", "📈"]):
            suggestions.append("😊 Add relevant emojis to make your post more visually appealing")
        
        # Hashtag analysis
        hashtag_count = post_content.count("#")
        if hashtag_count == 0:
            suggestions.append("#️⃣ Add 3-5 relevant hashtags to increase discoverability")
        elif hashtag_count > 10:
            suggestions.append("#️⃣ Consider reducing hashtags - 3-5 is optimal for LinkedIn")
        
        return suggestions

# LinkedIn analytics simulator
class LinkedInAnalytics:
    def __init__(self):
        self.sample_data = self._generate_sample_analytics()
    
    def _generate_sample_analytics(self):
        return {
            "profile_views": 1250 + random.randint(0, 100),
            "post_impressions": 5600 + random.randint(0, 500),
            "engagement_rate": round(7.2 + random.uniform(-1, 2), 1),
            "connection_requests": 15 + random.randint(0, 10),
            "best_performing_content": "Thought Leadership",
            "optimal_posting_time": "9:00 AM - 11:00 AM",
            "top_hashtags": ["#Leadership", "#Innovation", "#CareerGrowth", "#Technology", "#ProfessionalDevelopment"]
        }
    
    def get_content_performance_prediction(self, content_type, topic, length):
        base_score = 75
        
        # Content type impact
        type_multipliers = {
            "Thought Leadership": 1.2,
            "Personal Story": 1.15,
            "Career Advice": 1.1,
            "Professional Update": 1.0,
            "Industry Insights": 1.05
        }
        
        # Topic impact
        topic_multipliers = {
            "Leadership": 1.15,
            "Career Growth": 1.1,
            "Innovation": 1.08,
            "Technology": 1.05
        }
        
        # Length impact
        length_multipliers = {
            "Short": 0.9,
            "Medium": 1.1,
            "Long": 1.0
        }
        
        score = base_score * type_multipliers.get(content_type, 1.0)
        score *= topic_multipliers.get(topic, 1.0)
        score *= length_multipliers.get(length, 1.0)
        
        return min(100, int(score + random.uniform(-5, 5)))

def main():
    st.set_page_config(
        page_title="🚀 ContentCraft AI - LinkedIn Post Generator",
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize components
    generator = LinkedInPostGenerator()
    analytics = LinkedInAnalytics()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 💼 ContentCraft AI")
        st.markdown("*LinkedIn Post Generator*")
        st.markdown(f"**Version:** {config.VERSION}")
        
        st.markdown("---")
        st.markdown("### 📊 Your LinkedIn Stats")
        stats = analytics.sample_data
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Profile Views", f"{stats['profile_views']:,}")
            st.metric("Engagement Rate", f"{stats['engagement_rate']}%")
        with col2:
            st.metric("Post Impressions", f"{stats['post_impressions']:,}")
            st.metric("New Connections", stats['connection_requests'])
        
        st.markdown("---")
        st.markdown("### 💡 Quick Tips")
        st.info("🕘 **Best time to post:** 9-11 AM on weekdays")
        st.success("📈 **Top performing:** Thought Leadership posts")
        st.warning("🎯 **Optimal length:** 150-300 characters for max engagement")
    
    # Main content
    st.title("💼 LinkedIn Post Generator")
    st.markdown("*Create engaging LinkedIn content that drives professional growth*")
    
    # Input controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        content_type = st.selectbox(
            "📝 Content Type",
            options=config.CONTENT_TYPES,
            help="Choose the type of LinkedIn post you want to create"
        )
        
        topic = st.selectbox(
            "🎯 Topic",
            options=config.TOPICS,
            help="Select the main topic for your post"
        )
    
    with col2:
        length = st.selectbox(
            "📏 Post Length",
            options=list(config.OPTIMAL_LENGTH.keys()),
            help="Choose your preferred post length"
        )
        st.caption(config.OPTIMAL_LENGTH[length])
        
        tone = st.selectbox(
            "🎭 Tone",
            options=config.TONES,
            help="Select the tone that matches your brand voice"
        )
    
    with col3:
        industry = st.selectbox(
            "🏢 Industry",
            options=config.INDUSTRIES,
            help="Your industry context"
        )
        
        # Advanced options
        with st.expander("⚙️ Advanced Options"):
            include_hashtags = st.checkbox("Include hashtags", value=True)
            include_cta = st.checkbox("Include call-to-action", value=True)
            optimize_engagement = st.checkbox("Optimize for engagement", value=True)
    
    # Generate button
    st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("🚀 Generate LinkedIn Post", type="primary", use_container_width=True):
            with st.spinner("✨ Crafting your professional content..."):
                time.sleep(2)
                
                # Generate post
                post_content = generator.generate_post(
                    content_type, topic, length, tone, industry, 
                    include_hashtags, include_cta
                )
                
                st.success("🎉 Your LinkedIn post is ready!")
                
                # Display post
                st.markdown("### 📝 Generated Post:")
                st.text_area("", post_content, height=200, key="generated_post")
                
                # Post analytics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Characters", len(post_content))
                with col2:
                    st.metric("Words", len(post_content.split()))
                with col3:
                    predicted_score = analytics.get_content_performance_prediction(content_type, topic, length)
                    st.metric("Engagement Score", f"{predicted_score}%")
                with col4:
                    hashtag_count = post_content.count("#")
                    st.metric("Hashtags", hashtag_count)
                
                # Optimization suggestions
                suggestions = generator.get_optimization_suggestions(post_content)
                if suggestions:
                    st.markdown("### 💡 Optimization Suggestions:")
                    for suggestion in suggestions:
                        st.markdown(f"• {suggestion}")
                
                # Copy to clipboard helper
                st.markdown("---")
                st.info("💡 **Tip:** Copy the post above and paste it directly into LinkedIn!")
    
    with col2:
        if st.button("🔄 Generate Variation", use_container_width=True):
            st.info("🔄 Creating alternative version...")
    
    with col3:
        if st.button("💾 Save to Library", use_container_width=True):
            st.success("💾 Saved to your content library!")
    
    # Content templates section
    st.markdown("---")
    st.markdown("### 📚 Content Templates & Examples")
    
    template_tab1, template_tab2, template_tab3 = st.tabs(["🎯 Professional Update", "💡 Thought Leadership", "💼 Career Advice"])
    
    with template_tab1:
        st.markdown("**Structure:** Hook → Context → Insight → Call-to-Action")
        st.code("""🚀 Just completed a game-changing project...

Working with an incredible team, I learned that the best solutions come from diverse perspectives.

Key takeaway: Innovation happens when we combine different viewpoints and expertise.

What's been your experience with cross-functional collaboration?""")
    
    with template_tab2:
        st.markdown("**Structure:** Bold Statement → Evidence → Analysis → Future Outlook")
        st.code("""💡 Remote work isn't just a trend—it's the future of professional collaboration.

Recent data shows 85% of companies plan to maintain hybrid models post-pandemic.

This shift represents a fundamental change in how we define workplace productivity and culture.

Looking ahead: Companies that master remote collaboration will have a significant competitive advantage.

How is your organization adapting to this new reality?""")
    
    with template_tab3:
        st.markdown("**Structure:** Problem → Solution → Example → Actionable Tip")
        st.code("""💼 Many professionals struggle with imposter syndrome early in their careers.

The solution isn't more confidence—it's reframing your perspective on learning and growth.

Example: I once felt overwhelmed in a senior meeting, but realized everyone was there to solve problems together, not judge each other.

Actionable tip: Before your next challenging situation, remind yourself that you were invited because you bring value.

What strategies have helped you overcome self-doubt?""")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        f"ContentCraft AI - LinkedIn Post Generator v{config.VERSION} | 💼 Built for LinkedIn professionals"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
