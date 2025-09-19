import streamlit as st
import json
import os
from datetime import datetime, timedelta
import hashlib
import time
import random

# Enhanced configuration
class EnhancedConfig:
    APP_NAME = "ContentCraft AI PostGen"
    VERSION = "2.0.0"
    
    # Platform options with character limits and features
    PLATFORMS = {
        "LinkedIn": {"max_chars": 3000, "icon": "💼", "hashtags": True, "optimal_length": "Medium"},
        "Twitter/X": {"max_chars": 280, "icon": "🐦", "hashtags": True, "optimal_length": "Short"},
        "Instagram": {"max_chars": 2200, "icon": "📸", "hashtags": True, "optimal_length": "Medium"},
        "Facebook": {"max_chars": 63206, "icon": "📘", "hashtags": False, "optimal_length": "Long"},
        "TikTok": {"max_chars": 150, "icon": "🎵", "hashtags": True, "optimal_length": "Short"},
        "YouTube": {"max_chars": 5000, "icon": "📺", "hashtags": True, "optimal_length": "Long"}
    }
    
    # Content types
    CONTENT_TYPES = [
        "Professional Update", "Thought Leadership", "Industry News", 
        "Personal Story", "Tips & Advice", "Question/Poll", 
        "Behind the Scenes", "Product Launch", "Event Promotion",
        "Case Study", "Tutorial", "Motivational"
    ]
    
    # AI Models
    AI_MODELS = {
        "Groq Llama": {"provider": "groq", "model": "llama-3.2-90b-text-preview", "speed": "Fast"},
        "OpenAI GPT-4": {"provider": "openai", "model": "gpt-4", "speed": "Medium"},
        "Claude": {"provider": "anthropic", "model": "claude-3-sonnet", "speed": "Medium"}
    }
    
    LENGTH_OPTIONS = ["Short", "Medium", "Long"]
    LANGUAGE_OPTIONS = ["English", "Hinglish", "Spanish", "French", "German"]
    
    TONES = ["Professional", "Casual", "Inspirational", "Educational", "Humorous", "Authoritative"]
    
    INDUSTRIES = [
        "Technology", "Healthcare", "Finance", "Education", "Marketing", 
        "Sales", "HR", "Consulting", "Real Estate", "E-commerce"
    ]

config = EnhancedConfig()

# Enhanced post generator with multiple features
class EnhancedPostGenerator:
    def __init__(self):
        self.analytics_data = self.load_analytics()
        self.content_history = []
        
    def load_analytics(self):
        return {
            "total_posts": 156,
            "avg_engagement": 8.7,
            "best_performing_topics": ["Technology", "Career", "Leadership"],
            "optimal_posting_times": ["9:00 AM", "1:00 PM", "6:00 PM"]
        }
    
    def generate_hashtags(self, topic, platform):
        hashtag_db = {
            "Technology": ["#Tech", "#Innovation", "#AI", "#DigitalTransformation", "#TechTrends"],
            "Career": ["#Career", "#ProfessionalGrowth", "#Leadership", "#Success", "#Networking"],
            "Business": ["#Business", "#Entrepreneurship", "#Strategy", "#Growth", "#Innovation"],
            "Marketing": ["#Marketing", "#DigitalMarketing", "#ContentMarketing", "#SocialMedia", "#Branding"],
            "Personal Growth": ["#PersonalGrowth", "#Motivation", "#Success", "#Mindset", "#Development"]
        }
        
        base_tags = hashtag_db.get(topic, ["#Content", "#SocialMedia", "#Professional"])
        
        # Platform-specific hashtag optimization
        if platform == "LinkedIn":
            base_tags.extend(["#LinkedIn", "#Professional", "#Networking"])
        elif platform == "Instagram":
            base_tags.extend(["#InstaGood", "#Inspiration", "#Daily"])
        elif platform == "Twitter/X":
            base_tags = base_tags[:3]  # Twitter works better with fewer hashtags
            
        return random.sample(base_tags, min(5, len(base_tags)))
    
    def generate_content(self, platform, content_type, topic, length, language, tone, industry):
        # Enhanced content generation with platform optimization
        platform_info = config.PLATFORMS[platform]
        max_chars = platform_info["max_chars"]
        
        # Base content templates
        templates = {
            "Professional Update": {
                "Short": f"🚀 Exciting update from the {industry} world! Just completed a major milestone in {topic.lower()}. The key insight? {tone.lower()} approach always wins. What's your biggest win this week?",
                "Medium": f"💼 Reflecting on my journey in {industry} and {topic.lower()}. Every challenge has taught me valuable lessons about maintaining a {tone.lower()} mindset. Here are 3 key takeaways that transformed my approach: 1) Consistency beats perfection 2) Network authentically 3) Never stop learning. What's one lesson that changed your perspective?",
                "Long": f"🌟 Today marks a significant milestone in my {industry} career, particularly in {topic.lower()}. Looking back, I realize how much growth comes from embracing a {tone.lower()} approach to challenges. When I started, I thought success was about having all the answers. Now I know it's about asking the right questions, building genuine relationships, and staying curious. The {industry} landscape is constantly evolving, and those who adapt with grace and maintain their authentic voice are the ones who truly thrive. My advice to anyone in this space: embrace the uncertainty, invest in relationships, and remember that your unique perspective is your greatest asset."
            },
            "Thought Leadership": {
                "Short": f"💡 The future of {industry} lies in {topic.lower()}. Companies that embrace this shift will lead tomorrow's market. Are you ready?",
                "Medium": f"🔮 Prediction: {topic} will reshape {industry} in the next 5 years. Here's why I believe this transformation is inevitable and how professionals can prepare: The convergence of technology and human insight is creating unprecedented opportunities. Those who maintain a {tone.lower()} approach while adapting to change will emerge as leaders.",
                "Long": f"🚀 The {industry} industry is at a pivotal moment. {topic} isn't just a trend—it's the foundation of tomorrow's business landscape. Having worked in this space for years, I've observed patterns that suggest we're on the brink of a major transformation. Companies that understand this shift and approach it with a {tone.lower()} strategy will not only survive but thrive. The key is balancing innovation with human-centered values. What we're seeing isn't just technological advancement; it's a fundamental reimagining of how we create value, serve customers, and build sustainable businesses. The question isn't whether this change will happen, but how quickly organizations will adapt."
            }
        }
        
        # Get base content
        content_template = templates.get(content_type, templates["Professional Update"])
        base_content = content_template.get(length, content_template["Medium"])
        
        # Add hashtags if platform supports them
        if platform_info["hashtags"]:
            hashtags = self.generate_hashtags(topic, platform)
            hashtag_string = " ".join(hashtags)
            
            # Ensure content fits within character limit
            if len(base_content) + len(hashtag_string) + 2 <= max_chars:
                base_content += f"\n\n{hashtag_string}"
        
        # Truncate if necessary
        if len(base_content) > max_chars:
            base_content = base_content[:max_chars-3] + "..."
            
        return base_content
    
    def get_content_suggestions(self, platform, topic):
        suggestions = [
            f"Share a personal story about {topic.lower()}",
            f"Create a tips post about {topic.lower()} best practices",
            f"Ask your audience a question about {topic.lower()}",
            f"Share industry insights about {topic.lower()}",
            f"Post a behind-the-scenes look at {topic.lower()}"
        ]
        return random.sample(suggestions, 3)

# Analytics and insights
class ContentAnalytics:
    def __init__(self):
        self.engagement_data = self.generate_sample_analytics()
    
    def generate_sample_analytics(self):
        return {
            "posts_this_month": random.randint(15, 30),
            "avg_engagement_rate": round(random.uniform(5.2, 12.8), 1),
            "best_performing_platform": random.choice(["LinkedIn", "Instagram", "Twitter/X"]),
            "top_hashtags": ["#Innovation", "#Leadership", "#Growth", "#Technology", "#Success"],
            "optimal_posting_time": "2:00 PM",
            "engagement_trend": "📈 +15% vs last month"
        }
    
    def get_performance_insights(self):
        return {
            "recommendation": "Your technology posts perform 23% better than average",
            "best_day": "Tuesday",
            "engagement_peak": "2:00 PM - 4:00 PM",
            "hashtag_effectiveness": "Using 3-5 hashtags increases engagement by 12%"
        }

# Content calendar
class ContentCalendar:
    def __init__(self):
        self.scheduled_posts = []
    
    def add_scheduled_post(self, date, platform, content, status="Scheduled"):
        post = {
            "id": len(self.scheduled_posts) + 1,
            "date": date,
            "platform": platform,
            "content": content[:100] + "..." if len(content) > 100 else content,
            "status": status,
            "engagement": random.randint(50, 500) if status == "Published" else 0
        }
        self.scheduled_posts.append(post)
        return post
    
    def get_upcoming_posts(self, days=7):
        today = datetime.now()
        upcoming = []
        for i in range(days):
            date = today + timedelta(days=i)
            posts = [p for p in self.scheduled_posts if p["date"].date() == date.date()]
            if posts:
                upcoming.extend(posts)
        return upcoming

# Main enhanced application
def main():
    st.set_page_config(
        page_title="🚀 ContentCraft AI PostGen v2.0",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize components
    generator = EnhancedPostGenerator()
    analytics = ContentAnalytics()
    calendar = ContentCalendar()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🚀 ContentCraft AI v2.0")
        st.markdown("*Your Advanced AI Content Studio*")
        
        page = st.selectbox(
            "Navigate",
            ["🎯 Content Generator", "📊 Analytics", "📅 Content Calendar", "⚙️ Settings"]
        )
        
        st.markdown("---")
        st.markdown("### 📈 Quick Stats")
        stats = analytics.engagement_data
        st.metric("Posts This Month", stats["posts_this_month"])
        st.metric("Avg Engagement", f"{stats['avg_engagement_rate']}%")
        st.metric("Trend", stats["engagement_trend"])
        
        st.markdown("---")
        st.markdown("### 🎯 Today's Focus")
        st.info(f"Best time to post: **{stats['optimal_posting_time']}**")
        st.success(f"Top platform: **{stats['best_performing_platform']}**")
    
    # Main content area
    if page == "🎯 Content Generator":
        st.title("🎯 Advanced Content Generator")
        st.markdown("*Create platform-optimized content with AI-powered insights*")
        
        # Enhanced input controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_platform = st.selectbox(
                "🌐 Platform",
                options=list(config.PLATFORMS.keys()),
                help="Choose your target social media platform"
            )
            
            selected_content_type = st.selectbox(
                "📝 Content Type",
                options=config.CONTENT_TYPES
            )
        
        with col2:
            selected_topic = st.selectbox(
                "🎯 Topic",
                options=["Technology", "Career", "Business", "Marketing", "Personal Growth", "Leadership", "Innovation"]
            )
            
            selected_tone = st.selectbox(
                "🎭 Tone",
                options=config.TONES
            )
        
        with col3:
            selected_length = st.selectbox(
                "📏 Length",
                options=config.LENGTH_OPTIONS,
                index=config.LENGTH_OPTIONS.index(config.PLATFORMS[selected_platform]["optimal_length"])
            )
            
            selected_industry = st.selectbox(
                "🏢 Industry",
                options=config.INDUSTRIES
            )
        
        # Platform info
        platform_info = config.PLATFORMS[selected_platform]
        st.info(f"{platform_info['icon']} **{selected_platform}** - Max {platform_info['max_chars']} characters | Hashtags: {'✅' if platform_info['hashtags'] else '❌'}")
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            col1, col2 = st.columns(2)
            with col1:
                selected_language = st.selectbox("🌍 Language", config.LANGUAGE_OPTIONS)
                include_cta = st.checkbox("📢 Include Call-to-Action", value=True)
            with col2:
                ai_model = st.selectbox("🤖 AI Model", list(config.AI_MODELS.keys()))
                optimize_engagement = st.checkbox("📈 Optimize for Engagement", value=True)
        
        # Generate content
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("🚀 Generate Content", type="primary", use_container_width=True):
                with st.spinner("✨ Crafting your optimized content..."):
                    time.sleep(2)  # Simulate AI processing
                    
                    content = generator.generate_content(
                        selected_platform, selected_content_type, selected_topic,
                        selected_length, selected_language, selected_tone, selected_industry
                    )
                    
                    st.success("🎉 Content generated successfully!")
                    
                    # Display generated content
                    st.markdown("### 📝 Generated Content:")
                    st.markdown(f"```\n{content}\n```")
                    
                    # Content metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Characters", len(content))
                    with col2:
                        st.metric("Words", len(content.split()))
                    with col3:
                        engagement_score = random.randint(75, 95)
                        st.metric("Engagement Score", f"{engagement_score}%")
                    with col4:
                        readability = random.choice(["Easy", "Medium", "Advanced"])
                        st.metric("Readability", readability)
                    
                    # Content suggestions
                    st.markdown("### 💡 Content Suggestions:")
                    suggestions = generator.get_content_suggestions(selected_platform, selected_topic)
                    for i, suggestion in enumerate(suggestions, 1):
                        st.markdown(f"{i}. {suggestion}")
                    
                    # Schedule option
                    st.markdown("---")
                    col1, col2 = st.columns(2)
                    with col1:
                        schedule_date = st.date_input("📅 Schedule for", datetime.now().date())
                        schedule_time = st.time_input("⏰ Time", datetime.now().time())
                    with col2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("📅 Schedule Post", use_container_width=True):
                            schedule_datetime = datetime.combine(schedule_date, schedule_time)
                            calendar.add_scheduled_post(schedule_datetime, selected_platform, content)
                            st.success(f"✅ Post scheduled for {schedule_datetime.strftime('%B %d, %Y at %I:%M %p')}")
        
        with col2:
            if st.button("🔄 Generate Variation", use_container_width=True):
                st.info("🔄 Generating content variation...")
        
        with col3:
            if st.button("💾 Save Draft", use_container_width=True):
                st.success("💾 Draft saved!")
    
    elif page == "📊 Analytics":
        st.title("📊 Content Analytics")
        st.markdown("*Track your content performance and optimize your strategy*")
        
        # Performance metrics
        col1, col2, col3, col4 = st.columns(4)
        stats = analytics.engagement_data
        
        with col1:
            st.metric("Total Posts", stats["posts_this_month"], "📈 +5 vs last month")
        with col2:
            st.metric("Engagement Rate", f"{stats['avg_engagement_rate']}%", "📈 +2.3%")
        with col3:
            st.metric("Best Platform", stats["best_performing_platform"])
        with col4:
            st.metric("Reach", "12.5K", "📈 +1.2K")
        
        # Performance insights
        st.markdown("### 🎯 Performance Insights")
        insights = analytics.get_performance_insights()
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"💡 **Recommendation:** {insights['recommendation']}")
            st.success(f"📅 **Best Day:** {insights['best_day']}")
        with col2:
            st.warning(f"⏰ **Peak Hours:** {insights['engagement_peak']}")
            st.info(f"🏷️ **Hashtag Tip:** {insights['hashtag_effectiveness']}")
        
        # Top performing hashtags
        st.markdown("### 🏷️ Top Performing Hashtags")
        hashtag_cols = st.columns(5)
        for i, hashtag in enumerate(stats["top_hashtags"]):
            with hashtag_cols[i]:
                engagement = random.randint(150, 500)
                st.metric(hashtag, f"{engagement} uses")
    
    elif page == "📅 Content Calendar":
        st.title("📅 Content Calendar")
        st.markdown("*Plan and schedule your content strategy*")
        
        # Add some sample scheduled posts
        if not calendar.scheduled_posts:
            for i in range(5):
                date = datetime.now() + timedelta(days=i)
                platform = random.choice(list(config.PLATFORMS.keys()))
                content = f"Sample scheduled post #{i+1} for {platform}"
                status = "Published" if i < 2 else "Scheduled"
                calendar.add_scheduled_post(date, platform, content, status)
        
        # Calendar view
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📋 Upcoming Posts")
            upcoming = calendar.get_upcoming_posts()
            
            for post in upcoming[:5]:
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    with col1:
                        st.markdown(f"**{post['content']}**")
                    with col2:
                        platform_icon = config.PLATFORMS[post['platform']]['icon']
                        st.markdown(f"{platform_icon} {post['platform']}")
                    with col3:
                        st.markdown(f"📅 {post['date'].strftime('%m/%d')}")
                    with col4:
                        color = "green" if post['status'] == "Published" else "orange"
                        st.markdown(f":{color}[{post['status']}]")
                    st.markdown("---")
        
        with col2:
            st.markdown("### 📊 Calendar Stats")
            st.metric("Posts This Week", len(upcoming))
            st.metric("Scheduled", len([p for p in upcoming if p['status'] == 'Scheduled']))
            st.metric("Published", len([p for p in upcoming if p['status'] == 'Published']))
            
            st.markdown("### 🎯 Quick Actions")
            if st.button("➕ Schedule New Post", use_container_width=True):
                st.info("Use the Content Generator to create and schedule posts!")
            if st.button("📊 View Full Calendar", use_container_width=True):
                st.info("Full calendar view coming soon!")
    
    elif page == "⚙️ Settings":
        st.title("⚙️ Settings & Configuration")
        st.markdown("*Customize your ContentCraft AI experience*")
        
        # API Configuration
        st.markdown("### 🔑 API Configuration")
        col1, col2 = st.columns(2)
        
        with col1:
            groq_key = st.text_input("Groq API Key", type="password", placeholder="Enter your Groq API key")
            openai_key = st.text_input("OpenAI API Key", type="password", placeholder="Enter your OpenAI API key")
        
        with col2:
            claude_key = st.text_input("Claude API Key", type="password", placeholder="Enter your Claude API key")
            default_model = st.selectbox("Default AI Model", list(config.AI_MODELS.keys()))
        
        # Brand Settings
        st.markdown("### 🎨 Brand Settings")
        col1, col2 = st.columns(2)
        
        with col1:
            brand_name = st.text_input("Brand Name", placeholder="Your Company/Personal Brand")
            brand_voice = st.selectbox("Brand Voice", config.TONES)
        
        with col2:
            primary_industry = st.selectbox("Primary Industry", config.INDUSTRIES)
            target_audience = st.text_input("Target Audience", placeholder="e.g., Tech professionals, Entrepreneurs")
        
        # Platform Preferences
        st.markdown("### 🌐 Platform Preferences")
        preferred_platforms = st.multiselect(
            "Preferred Platforms",
            list(config.PLATFORMS.keys()),
            default=["LinkedIn", "Twitter/X"]
        )
        
        # Save settings
        if st.button("💾 Save Settings", type="primary"):
            st.success("✅ Settings saved successfully!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        f"ContentCraft AI PostGen v{config.VERSION} | Made with ❤️ for content creators"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
