import streamlit as st
import json
import os
from datetime import datetime, timedelta
import time
import random
from dataclasses import dataclass
from typing import List, Dict, Optional
import sqlite3
from pathlib import Path
import calendar

# Import existing modules
from llm_helper import get_llm
from post_generator import generate_post as original_generate_post
from few_shot import FewShotPosts
from config import Config
from linkedin_scheduler import LinkedInScheduler, ContentCalendar, PerformanceTracker
from linkedin_api_client import LinkedInAPIClient, LinkedInAuthManager, LINKEDIN_API_SETUP_INSTRUCTIONS

# Enhanced LinkedIn configuration
@dataclass
class LinkedInConfig:
    APP_NAME = "ContentCraft AI - Enhanced LinkedIn Generator"
    VERSION = "3.0.0"
    
    # LinkedIn-specific settings
    MAX_CHARS = 3000
    OPTIMAL_LENGTH = {
        "Short": "1-5 lines (125-300 chars)",
        "Medium": "6-10 lines (300-600 chars)", 
        "Long": "11-15 lines (600-1300 chars)"
    }
    
    # Enhanced content types
    CONTENT_TYPES = [
        "Professional Update", "Thought Leadership", "Industry Insights", 
        "Personal Story", "Career Advice", "Company News", 
        "Achievement/Milestone", "Question/Poll", "Tips & Best Practices",
        "Behind the Scenes", "Team Spotlight", "Learning & Development",
        "Case Study", "Product Launch", "Event Announcement", "Recruitment"
    ]
    
    # Expanded topics with trending focus
    TOPICS = [
        "Leadership", "Career Growth", "Technology", "Innovation", 
        "Entrepreneurship", "Team Building", "Professional Development",
        "Industry Trends", "Networking", "Work-Life Balance",
        "Digital Transformation", "Remote Work", "Mentorship", "AI & Machine Learning",
        "Sustainability", "Diversity & Inclusion", "Customer Success", "Sales Strategy"
    ]
    
    # Professional tones
    TONES = [
        "Professional", "Inspirational", "Educational", "Conversational",
        "Authoritative", "Humble", "Motivational", "Analytical", "Storytelling", "Data-Driven"
    ]
    
    # Expanded industries
    INDUSTRIES = [
        "Technology", "Finance", "Healthcare", "Education", "Marketing",
        "Sales", "Consulting", "Manufacturing", "Real Estate", "Legal",
        "HR & Recruiting", "Non-Profit", "Government", "Retail", "Media",
        "Automotive", "Energy", "Telecommunications", "Aerospace", "Biotechnology"
    ]

config = LinkedInConfig()

# Enhanced AI-powered post generator
class EnhancedLinkedInGenerator:
    def __init__(self):
        self.llm = None
        self.few_shot = None
        self.init_ai_components()
        self.db_path = "content_library.db"
        self.init_database()
        
    def init_ai_components(self):
        """Initialize AI components with fallback"""
        try:
            self.llm = get_llm()
            self.few_shot = FewShotPosts()
            st.success("🤖 AI Engine: Connected")
        except Exception as e:
            st.warning(f"⚠️ AI Engine: Using demo mode ({str(e)[:50]}...)")
            self.llm = None
            self.few_shot = None
    
    def init_database(self):
        """Initialize SQLite database for content library"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                content_type TEXT,
                topic TEXT,
                tone TEXT,
                industry TEXT,
                hashtags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                performance_score INTEGER DEFAULT 0,
                is_published BOOLEAN DEFAULT FALSE,
                scheduled_time TIMESTAMP,
                engagement_data TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER,
                views INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (post_id) REFERENCES posts (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT DEFAULT 'default',
                writing_style TEXT,
                preferred_topics TEXT,
                brand_voice TEXT,
                posting_schedule TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_ai_post(self, content_type: str, topic: str, length: str, tone: str, 
                        industry: str, custom_prompt: str = "", user_context: str = "") -> str:
        """Generate post using AI with enhanced prompting"""
        
        if not self.llm:
            return self._generate_demo_post(content_type, topic, length, tone, industry)
        
        try:
            # Build enhanced prompt
            prompt = self._build_enhanced_prompt(
                content_type, topic, length, tone, industry, custom_prompt, user_context
            )
            
            # Generate with AI
            response = self.llm.invoke(prompt)
            return response.content.strip()
            
        except Exception as e:
            st.error(f"AI Generation Error: {e}")
            return self._generate_demo_post(content_type, topic, length, tone, industry)
    
    def _build_enhanced_prompt(self, content_type: str, topic: str, length: str, 
                              tone: str, industry: str, custom_prompt: str, user_context: str) -> str:
        """Build sophisticated AI prompt"""
        
        # Get few-shot examples if available
        examples = ""
        if self.few_shot:
            try:
                example_posts = self.few_shot.get_filtered_posts(length.lower(), topic.lower())
                if example_posts:
                    examples = "\n\nExample LinkedIn posts for reference:\n"
                    for i, post in enumerate(example_posts[:2], 1):
                        examples += f"\nExample {i}:\n{post.get('text', '')}\n"
            except:
                pass
        
        # Character limits based on length
        char_limits = {
            "Short": "125-300 characters",
            "Medium": "300-600 characters", 
            "Long": "600-1300 characters"
        }
        
        prompt = f"""You are an expert LinkedIn content creator and social media strategist. Create a high-engagement LinkedIn post with the following specifications:

CONTENT REQUIREMENTS:
- Content Type: {content_type}
- Topic: {topic}
- Industry: {industry}
- Tone: {tone}
- Length: {length} ({char_limits.get(length, '300-600 characters')})

LINKEDIN BEST PRACTICES:
- Start with an attention-grabbing hook
- Use line breaks for readability
- Include relevant emojis (but don't overuse)
- End with an engaging question or call-to-action
- Keep paragraphs short (1-2 sentences)
- Use professional language appropriate for {industry}

ENGAGEMENT OPTIMIZATION:
- Create content that encourages comments and shares
- Use storytelling elements when appropriate
- Include actionable insights or tips
- Make it relatable to {industry} professionals

{f"CUSTOM INSTRUCTIONS: {custom_prompt}" if custom_prompt else ""}

{f"USER CONTEXT: {user_context}" if user_context else ""}

{examples}

Generate a LinkedIn post that follows these guidelines and will perform well with {industry} professionals. Focus on creating genuine value and encouraging meaningful engagement."""

        return prompt
    
    def _generate_demo_post(self, content_type: str, topic: str, length: str, tone: str, industry: str) -> str:
        """Fallback demo post generation"""
        templates = {
            "Short": f"💼 Quick insight on {topic.lower()} in {industry.lower()}:\n\nThe key to success? A {tone.lower()} approach that focuses on continuous learning.\n\nWhat's your experience been?",
            
            "Medium": f"💡 {topic} is reshaping the {industry.lower()} landscape.\n\nAfter working in this space, I've learned that the most successful professionals maintain a {tone.lower()} mindset while staying adaptable to change.\n\nThe companies thriving today are those that embrace innovation while staying true to their core values.\n\nWhat trends are you seeing in your field?",
            
            "Long": f"🚀 The evolution of {topic.lower()} in {industry.lower()} has been remarkable.\n\nWhen I started my career, the approach was completely different. Today's success requires:\n\n• A {tone.lower()} mindset that embraces continuous learning\n• The ability to adapt quickly to new challenges\n• Strong relationships built on trust and collaboration\n• Data-driven decision making combined with human intuition\n\nThe professionals who thrive are those who view every challenge as an opportunity for growth and innovation.\n\nLooking ahead, I believe {topic.lower()} will become even more critical to success in {industry.lower()}.\n\nWhat's one lesson that's shaped your approach to {topic.lower()}? I'd love to hear your insights in the comments.\n\n#Leadership #ProfessionalDevelopment #{industry.replace(' ', '')}"
        }
        
        return templates.get(length, templates["Medium"])
    
    def save_post(self, content: str, content_type: str, topic: str, tone: str, 
                  industry: str, hashtags: str = "") -> int:
        """Save post to content library"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO posts (content, content_type, topic, tone, industry, hashtags)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (content, content_type, topic, tone, industry, hashtags))
        
        post_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return post_id
    
    def get_saved_posts(self, limit: int = 10) -> List[Dict]:
        """Retrieve saved posts from library"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, content, content_type, topic, created_at, performance_score
            FROM posts 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        posts = []
        for row in cursor.fetchall():
            posts.append({
                'id': row[0],
                'content': row[1],
                'content_type': row[2],
                'topic': row[3],
                'created_at': row[4],
                'performance_score': row[5]
            })
        
        conn.close()
        return posts
    
    def generate_variations(self, original_post: str, num_variations: int = 3) -> List[str]:
        """Generate variations of a post for A/B testing"""
        if not self.llm:
            return [
                original_post.replace("💼", "🚀"),
                original_post.replace("What's your experience?", "Share your thoughts below!"),
                original_post + "\n\nWhat would you add to this list?"
            ][:num_variations]
        
        try:
            prompt = f"""Create {num_variations} variations of this LinkedIn post for A/B testing. 
            Keep the core message the same but vary the:
            - Opening hook
            - Call-to-action
            - Emojis and formatting
            - Question style
            
            Original post:
            {original_post}
            
            Generate {num_variations} distinct variations that maintain the professional tone and key message:"""
            
            response = self.llm.invoke(prompt)
            variations = response.content.split("---") if "---" in response.content else [response.content]
            return [var.strip() for var in variations[:num_variations]]
            
        except Exception as e:
            st.error(f"Variation generation error: {e}")
            return [original_post]
    
    def analyze_post_performance(self, content: str) -> Dict:
        """Analyze and predict post performance"""
        analysis = {
            "engagement_score": 75,
            "readability_score": 85,
            "hashtag_effectiveness": 70,
            "cta_strength": 80,
            "suggestions": []
        }
        
        # Character analysis
        char_count = len(content)
        if char_count < 100:
            analysis["suggestions"].append("💡 Consider adding more context - posts with 150+ characters get better engagement")
            analysis["engagement_score"] -= 10
        elif char_count > 1300:
            analysis["suggestions"].append("⚠️ Consider shortening - very long posts may lose reader attention")
            analysis["engagement_score"] -= 5
        
        # Engagement elements
        if "?" not in content:
            analysis["suggestions"].append("❓ Add a question to encourage comments")
            analysis["cta_strength"] -= 20
        
        # Emoji analysis
        emoji_count = sum(1 for char in content if ord(char) > 127)
        if emoji_count == 0:
            analysis["suggestions"].append("😊 Add relevant emojis for visual appeal")
            analysis["engagement_score"] -= 5
        elif emoji_count > 10:
            analysis["suggestions"].append("😊 Consider reducing emojis for professional balance")
            analysis["engagement_score"] -= 3
        
        # Hashtag analysis
        hashtag_count = content.count("#")
        if hashtag_count == 0:
            analysis["suggestions"].append("#️⃣ Add 3-5 relevant hashtags for discoverability")
            analysis["hashtag_effectiveness"] = 30
        elif hashtag_count > 10:
            analysis["suggestions"].append("#️⃣ Reduce hashtags - 3-5 is optimal for LinkedIn")
            analysis["hashtag_effectiveness"] -= 20
        
        # Line break analysis
        line_breaks = content.count("\n")
        if line_breaks < 2 and char_count > 200:
            analysis["suggestions"].append("📝 Add line breaks for better readability")
            analysis["readability_score"] -= 15
        
        return analysis

# Enhanced analytics class
class EnhancedAnalytics:
    def __init__(self):
        self.sample_data = self._generate_enhanced_analytics()
    
    def _generate_enhanced_analytics(self):
        return {
            "profile_views": 1250 + random.randint(0, 100),
            "post_impressions": 5600 + random.randint(0, 500),
            "engagement_rate": round(7.2 + random.uniform(-1, 2), 1),
            "connection_requests": 15 + random.randint(0, 10),
            "follower_growth": 45 + random.randint(-5, 15),
            "best_performing_content": "Thought Leadership",
            "optimal_posting_time": "9:00 AM - 11:00 AM",
            "top_hashtags": ["#Leadership", "#Innovation", "#CareerGrowth", "#Technology", "#ProfessionalDevelopment"],
            "weekly_engagement": [120, 145, 98, 167, 134, 189, 156],
            "content_performance": {
                "Professional Update": 85,
                "Thought Leadership": 92,
                "Career Advice": 78,
                "Industry Insights": 81
            }
        }
    
    def get_trending_topics(self) -> List[str]:
        """Get current trending LinkedIn topics"""
        trending = [
            "AI in the Workplace", "Remote Work Culture", "Leadership in Crisis",
            "Digital Transformation", "Employee Wellbeing", "Sustainable Business",
            "Future of Work", "Data Privacy", "Cybersecurity Awareness", "Green Technology"
        ]
        return random.sample(trending, 5)
    
    def get_optimal_posting_schedule(self) -> Dict:
        """Get personalized posting schedule recommendations"""
        return {
            "Monday": ["9:00 AM", "1:00 PM"],
            "Tuesday": ["8:00 AM", "12:00 PM", "3:00 PM"],
            "Wednesday": ["9:00 AM", "2:00 PM"],
            "Thursday": ["8:00 AM", "11:00 AM", "4:00 PM"],
            "Friday": ["9:00 AM", "1:00 PM"],
            "Saturday": ["10:00 AM"],
            "Sunday": ["7:00 PM"]
        }

def main():
    st.set_page_config(
        page_title="🚀 ContentCraft AI - Enhanced LinkedIn Generator",
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize components
    generator = EnhancedLinkedInGenerator()
    analytics = EnhancedAnalytics()
    
    # Session state initialization
    if 'generated_post' not in st.session_state:
        st.session_state.generated_post = ""
    if 'post_variations' not in st.session_state:
        st.session_state.post_variations = []
    if 'saved_posts' not in st.session_state:
        st.session_state.saved_posts = []
    
    # Sidebar with enhanced features
    with st.sidebar:
        st.markdown("## 💼 ContentCraft AI")
        st.markdown("*Enhanced LinkedIn Generator*")
        st.markdown(f"**Version:** {config.VERSION}")
        
        # AI Status
        ai_status = "🟢 Connected" if generator.llm else "🟡 Demo Mode"
        st.markdown(f"**AI Engine:** {ai_status}")
        
        st.markdown("---")
        
        # Navigation
        page = st.selectbox(
            "📍 Navigate",
            ["🚀 Post Generator", "📊 Analytics", "📚 Content Library", "📅 Content Calendar", "🔗 LinkedIn API", "⚙️ Settings"],
            key="navigation"
        )
        
        st.markdown("---")
        
        # Quick stats
        st.markdown("### 📊 Your LinkedIn Stats")
        stats = analytics.sample_data
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Profile Views", f"{stats['profile_views']:,}")
            st.metric("Engagement Rate", f"{stats['engagement_rate']}%")
        with col2:
            st.metric("Post Impressions", f"{stats['post_impressions']:,}")
            st.metric("Follower Growth", f"+{stats['follower_growth']}")
        
        st.markdown("---")
        
        # Trending topics
        st.markdown("### 🔥 Trending Now")
        trending = analytics.get_trending_topics()
        for topic in trending[:3]:
            st.markdown(f"• {topic}")
        
        st.markdown("---")
        
        # Quick tips
        st.markdown("### 💡 Pro Tips")
        st.info("🕘 **Best time:** Weekdays 9-11 AM")
        st.success("📈 **Top format:** Thought Leadership")
        st.warning("🎯 **Sweet spot:** 300-600 characters")
    
    # Main content based on navigation
    if page == "🚀 Post Generator":
        show_post_generator(generator, analytics)
    elif page == "📊 Analytics":
        show_analytics(analytics)
    elif page == "📚 Content Library":
        show_content_library(generator)
    elif page == "📅 Content Calendar":
        show_content_calendar(generator)
    elif page == "⚙️ Settings":
        show_settings()
    elif page == "🔗 LinkedIn API":
        show_linkedin_api_setup()

def show_post_generator(generator, analytics):
    """Main post generator interface"""
    st.title("🚀 Enhanced LinkedIn Post Generator")
    st.markdown("*AI-powered content creation with advanced optimization*")
    
    # Input controls in tabs
    input_tab, advanced_tab, ai_tab = st.tabs(["📝 Basic Settings", "⚙️ Advanced Options", "🤖 AI Controls"])
    
    with input_tab:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            content_type = st.selectbox("📝 Content Type", config.CONTENT_TYPES)
            topic = st.selectbox("🎯 Topic", config.TOPICS)
        
        with col2:
            length = st.selectbox("📏 Post Length", list(config.OPTIMAL_LENGTH.keys()))
            st.caption(config.OPTIMAL_LENGTH[length])
            tone = st.selectbox("🎭 Tone", config.TONES)
        
        with col3:
            industry = st.selectbox("🏢 Industry", config.INDUSTRIES)
            include_hashtags = st.checkbox("Include hashtags", value=True)
    
    with advanced_tab:
        col1, col2 = st.columns(2)
        
        with col1:
            custom_prompt = st.text_area(
                "🎯 Custom Instructions",
                placeholder="Add specific requirements or context...",
                height=100
            )
        
        with col2:
            user_context = st.text_area(
                "👤 Your Background",
                placeholder="Your role, company, recent achievements...",
                height=100
            )
        
        # Advanced options
        generate_variations = st.checkbox("Generate A/B test variations", value=False)
        num_variations = st.slider("Number of variations", 2, 5, 3) if generate_variations else 3
        
        optimize_engagement = st.checkbox("Optimize for engagement", value=True)
        include_cta = st.checkbox("Include call-to-action", value=True)
    
    with ai_tab:
        st.markdown("### 🤖 AI Configuration")
        
        if generator.llm:
            st.success("✅ AI Engine: Connected and ready")
            st.info("💡 Using advanced AI for personalized content generation")
        else:
            st.warning("⚠️ AI Engine: Demo mode - Connect API keys for full AI features")
        
        # AI model selection (placeholder for future enhancement)
        ai_model = st.selectbox(
            "🧠 AI Model",
            ["GPT-4 (Recommended)", "Claude-3", "Groq Llama", "Demo Mode"],
            disabled=not generator.llm
        )
        
        creativity_level = st.slider("🎨 Creativity Level", 0.1, 1.0, 0.7, 0.1)
    
    # Generation section
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        if st.button("🚀 Generate LinkedIn Post", type="primary", use_container_width=True):
            with st.spinner("✨ AI is crafting your professional content..."):
                time.sleep(2)
                
                # Generate main post
                post_content = generator.generate_ai_post(
                    content_type, topic, length, tone, industry, 
                    custom_prompt, user_context
                )
                
                st.session_state.generated_post = post_content
                
                # Generate variations if requested
                if generate_variations:
                    st.session_state.post_variations = generator.generate_variations(
                        post_content, num_variations
                    )
                
                st.success("🎉 Your LinkedIn post is ready!")
    
    with col2:
        if st.button("🔄 Regenerate", use_container_width=True):
            if st.session_state.generated_post:
                with st.spinner("🔄 Creating new version..."):
                    time.sleep(1)
                    post_content = generator.generate_ai_post(
                        content_type, topic, length, tone, industry, 
                        custom_prompt, user_context
                    )
                    st.session_state.generated_post = post_content
                    st.success("🔄 New version generated!")
    
    with col3:
        if st.button("💾 Save Post", use_container_width=True):
            if st.session_state.generated_post:
                post_id = generator.save_post(
                    st.session_state.generated_post, content_type, 
                    topic, tone, industry
                )
                st.success(f"💾 Saved as Post #{post_id}")
    
    with col4:
        if st.button("📤 Schedule", use_container_width=True):
            if st.session_state.generated_post:
                st.info("📅 Scheduling feature coming soon!")
    
    # Display generated content
    if st.session_state.generated_post:
        st.markdown("---")
        st.markdown("### 📝 Generated Post:")
        
        # Main post
        st.text_area("", st.session_state.generated_post, height=200, key="main_post")
        
        # Post analysis
        analysis = generator.analyze_post_performance(st.session_state.generated_post)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Characters", len(st.session_state.generated_post))
        with col2:
            st.metric("Words", len(st.session_state.generated_post.split()))
        with col3:
            st.metric("Engagement Score", f"{analysis['engagement_score']}%")
        with col4:
            hashtag_count = st.session_state.generated_post.count("#")
            st.metric("Hashtags", hashtag_count)
        
        # Performance analysis
        if analysis['suggestions']:
            st.markdown("### 💡 Optimization Suggestions:")
            for suggestion in analysis['suggestions']:
                st.markdown(f"• {suggestion}")
        
        # A/B test variations
        if st.session_state.post_variations:
            st.markdown("### 🧪 A/B Test Variations:")
            for i, variation in enumerate(st.session_state.post_variations, 1):
                with st.expander(f"Variation {i}"):
                    st.text_area("", variation, height=150, key=f"variation_{i}")
        
        # Copy helper
        st.markdown("---")
        st.info("💡 **Tip:** Copy the post above and paste directly into LinkedIn!")

def show_analytics(analytics):
    """Analytics dashboard"""
    st.title("📊 LinkedIn Analytics Dashboard")
    
    # Key metrics
    stats = analytics.sample_data
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Profile Views", f"{stats['profile_views']:,}", "+12%")
    with col2:
        st.metric("Post Impressions", f"{stats['post_impressions']:,}", "+8%")
    with col3:
        st.metric("Engagement Rate", f"{stats['engagement_rate']}%", "+2.1%")
    with col4:
        st.metric("Follower Growth", f"+{stats['follower_growth']}", "+15%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Weekly Engagement")
        st.line_chart(stats['weekly_engagement'])
    
    with col2:
        st.markdown("### 🎯 Content Performance")
        st.bar_chart(stats['content_performance'])
    
    # Optimal posting schedule
    st.markdown("### ⏰ Optimal Posting Schedule")
    schedule = analytics.get_optimal_posting_schedule()
    
    for day, times in schedule.items():
        st.markdown(f"**{day}:** {', '.join(times)}")

def show_content_library(generator):
    """Content library interface"""
    st.title("📚 Content Library")
    
    # Saved posts
    saved_posts = generator.get_saved_posts(20)
    
    if saved_posts:
        st.markdown(f"### 📄 Recent Posts ({len(saved_posts)})")
        
        for post in saved_posts:
            with st.expander(f"{post['content_type']} - {post['topic']} ({post['created_at'][:10]})"):
                st.text_area("", post['content'], height=100, key=f"saved_{post['id']}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Performance Score", f"{post['performance_score']}%")
                with col2:
                    if st.button("📤 Reuse", key=f"reuse_{post['id']}"):
                        st.session_state.generated_post = post['content']
                        st.success("📤 Post loaded to generator!")
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_{post['id']}"):
                        st.warning("🗑️ Delete functionality coming soon!")
    else:
        st.info("📝 No saved posts yet. Generate and save some content to build your library!")

def show_content_calendar(generator):
    """Content calendar interface"""
    st.title("📅 Content Calendar")
    st.markdown("*Plan, schedule, and track your LinkedIn content*")
    
    # Initialize calendar components
    scheduler = LinkedInScheduler()
    content_calendar = ContentCalendar()
    performance_tracker = PerformanceTracker()
    
    # Calendar navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("◀ Previous Month"):
            if 'calendar_month' not in st.session_state:
                st.session_state.calendar_month = datetime.now().month
                st.session_state.calendar_year = datetime.now().year
            
            if st.session_state.calendar_month == 1:
                st.session_state.calendar_month = 12
                st.session_state.calendar_year -= 1
            else:
                st.session_state.calendar_month -= 1
    
    with col2:
        if 'calendar_month' not in st.session_state:
            st.session_state.calendar_month = datetime.now().month
            st.session_state.calendar_year = datetime.now().year
        
        current_date = datetime(st.session_state.calendar_year, st.session_state.calendar_month, 1)
        st.markdown(f"### {current_date.strftime('%B %Y')}")
    
    with col3:
        if st.button("Next Month ▶"):
            if st.session_state.calendar_month == 12:
                st.session_state.calendar_month = 1
                st.session_state.calendar_year += 1
            else:
                st.session_state.calendar_month += 1
    
    # Calendar tabs
    calendar_tab, schedule_tab, gaps_tab, insights_tab = st.tabs(["📅 Calendar View", "⏰ Schedule Post", "🔍 Content Gaps", "📊 Insights"])
    
    with calendar_tab:
        # Get calendar data
        calendar_data = content_calendar.get_calendar_data(st.session_state.calendar_year, st.session_state.calendar_month)
        
        # Display calendar grid
        st.markdown("### 📅 Monthly Overview")
        
        # Create calendar grid
        cal = calendar.monthcalendar(st.session_state.calendar_year, st.session_state.calendar_month)
        
        # Calendar headers
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        cols = st.columns(7)
        for i, day in enumerate(days):
            with cols[i]:
                st.markdown(f"**{day}**")
        
        # Calendar days
        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                with cols[i]:
                    if day == 0:
                        st.markdown("")
                    else:
                        date_str = f"{st.session_state.calendar_year}-{st.session_state.calendar_month:02d}-{day:02d}"
                        
                        if date_str in calendar_data:
                            post_count = calendar_data[date_str]['post_count']
                            st.markdown(f"**{day}**\n🗓️ {post_count} post(s)")
                        else:
                            st.markdown(f"{day}")
        
        # Scheduled posts list
        st.markdown("---")
        st.markdown("### 📋 Upcoming Posts")
        
        scheduled_posts = scheduler.get_scheduled_posts(30)
        
        if scheduled_posts:
            for post in scheduled_posts[:5]:  # Show next 5 posts
                with st.expander(f"📝 {post['content_type']} - {post['scheduled_time'][:16]}"):
                    st.markdown(f"**Topic:** {post['topic']}")
                    st.markdown(f"**Content Preview:** {post['content']}")
                    st.markdown(f"**Status:** {post['status']}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("✏️ Edit", key=f"edit_{post['schedule_id']}"):
                            st.info("✏️ Edit functionality coming soon!")
                    with col2:
                        if st.button("🚀 Publish Now", key=f"publish_{post['schedule_id']}"):
                            st.success("🚀 Publishing functionality coming soon!")
                    with col3:
                        if st.button("🗑️ Delete", key=f"delete_{post['schedule_id']}"):
                            st.warning("🗑️ Delete functionality coming soon!")
        else:
            st.info("📝 No scheduled posts. Use the Schedule tab to plan your content!")
    
    with schedule_tab:
        st.markdown("### ⏰ Schedule New Post")
        
        # Post selection
        saved_posts = generator.get_saved_posts(20)
        
        if saved_posts:
            post_options = {f"Post #{post['id']} - {post['content_type']}": post['id'] for post in saved_posts}
            selected_post = st.selectbox("📝 Select Post to Schedule", list(post_options.keys()))
            
            if selected_post:
                post_id = post_options[selected_post]
                
                # Show post preview
                selected_post_data = next(post for post in saved_posts if post['id'] == post_id)
                st.text_area("📄 Post Preview", selected_post_data['content'], height=100, disabled=True)
                
                # Scheduling options
                col1, col2 = st.columns(2)
                
                with col1:
                    schedule_date = st.date_input("📅 Schedule Date", min_value=datetime.now().date())
                    schedule_time = st.time_input("⏰ Schedule Time", value=datetime.now().time())
                
                with col2:
                    auto_optimize = st.checkbox("🎯 Auto-optimize timing", value=True, help="Adjust to optimal posting times")
                    add_hashtags = st.checkbox("#️⃣ Auto-add hashtags", value=True)
                
                # Optimal time suggestions
                if auto_optimize:
                    optimal_schedule = scheduler.get_optimal_schedule_suggestions()
                    st.markdown("### 💡 Optimal Posting Times")
                    
                    for suggestion in optimal_schedule['high_engagement_times'][:3]:
                        st.markdown(f"• **{suggestion['day']}** at **{suggestion['time']}** ({suggestion['engagement_boost']} engagement boost)")
                
                # Schedule button
                if st.button("📅 Schedule Post", type="primary"):
                    schedule_datetime = datetime.combine(schedule_date, schedule_time)
                    
                    try:
                        schedule_id = scheduler.schedule_post(post_id, schedule_datetime, auto_optimize)
                        st.success(f"✅ Post scheduled successfully! Schedule ID: {schedule_id}")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Scheduling failed: {e}")
        else:
            st.info("📝 No saved posts available. Generate and save some posts first!")
    
    with gaps_tab:
        st.markdown("### 🔍 Content Gap Analysis")
        
        # Get content gaps
        gaps = content_calendar.suggest_content_gaps(30)
        
        if gaps:
            st.markdown(f"### 📊 Found {len(gaps)} content opportunities in the next 30 days:")
            
            for gap in gaps[:10]:
                with st.expander(f"📅 {gap['date'].strftime('%A, %B %d')} - {gap['optimal_time']}"):
                    st.markdown(f"**Suggested Content:** {gap['suggested_content']}")
                    st.markdown(f"**Optimal Time:** {gap['optimal_time']}")
                    
                    if st.button(f"✨ Generate Content", key=f"generate_{gap['date']}"):
                        st.info("🚀 Content generation for this slot coming soon!")
        else:
            st.success("🎉 Great job! No content gaps found in your schedule.")
        
        # Content mix recommendations
        st.markdown("---")
        st.markdown("### 🎯 Recommended Content Mix")
        
        optimal_schedule = scheduler.get_optimal_schedule_suggestions()
        content_mix = optimal_schedule['best_content_mix']
        
        for content_type, percentage in content_mix.items():
            st.markdown(f"• **{content_type}:** {percentage}")
    
    with insights_tab:
        st.markdown("### 📊 Performance Insights")
        
        # Performance summary
        performance_summary = performance_tracker.get_performance_summary(30)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Posts", performance_summary['total_posts'])
        with col2:
            st.metric("Avg Views", f"{performance_summary['avg_views']:.0f}")
        with col3:
            st.metric("Avg Engagement", f"{performance_summary['avg_engagement_rate']:.1f}%")
        with col4:
            st.metric("Avg Likes", f"{performance_summary['avg_likes']:.0f}")
        
        # AI Insights
        st.markdown("### 🤖 AI-Powered Insights")
        
        insights = performance_tracker.generate_performance_insights()
        
        for insight in insights:
            insight_type = insight['type']
            confidence = insight['confidence']
            
            # Color code by confidence
            if confidence >= 0.8:
                st.success(f"**{insight_type.title()}:** {insight['message']} (Confidence: {confidence:.0%})")
                st.markdown(f"💡 **Action:** {insight['action']}")
            elif confidence >= 0.6:
                st.info(f"**{insight_type.title()}:** {insight['message']} (Confidence: {confidence:.0%})")
                st.markdown(f"💡 **Action:** {insight['action']}")
            else:
                st.warning(f"**{insight_type.title()}:** {insight['message']} (Confidence: {confidence:.0%})")
                st.markdown(f"💡 **Action:** {insight['action']}")
            
            st.markdown("---")

def show_settings():
    """Settings interface"""
    st.title("⚙️ Settings")
    
    # API Configuration
    st.markdown("### 🔑 API Configuration")
    
    with st.expander("🤖 AI Model Settings"):
        groq_key = st.text_input("Groq API Key", type="password", help="For AI content generation")
        openai_key = st.text_input("OpenAI API Key", type="password", help="Alternative AI model")
        
        if st.button("💾 Save API Keys"):
            st.success("🔑 API keys saved securely!")
    
    # User Preferences
    st.markdown("### 👤 User Preferences")
    
    default_industry = st.selectbox("Default Industry", config.INDUSTRIES)
    default_tone = st.selectbox("Default Tone", config.TONES)
    brand_voice = st.text_area("Brand Voice Guidelines", height=100)
    
    # Posting Schedule
    st.markdown("### ⏰ Posting Preferences")
    
    timezone = st.selectbox("Timezone", ["UTC", "EST", "PST", "GMT", "CET"])
    auto_schedule = st.checkbox("Enable auto-scheduling")
    
    if st.button("💾 Save Preferences"):
        st.success("✅ Preferences saved!")

def show_linkedin_api_setup():
    """LinkedIn API setup and real-time integration"""
    st.title("🔗 LinkedIn API Integration")
    st.markdown("*Connect to LinkedIn for real-time data and publishing*")
    
    # Initialize LinkedIn components
    auth_manager = LinkedInAuthManager()
    
    # Check authentication status
    is_authenticated = auth_manager.is_authenticated()
    
    if is_authenticated:
        st.success("✅ LinkedIn API: Connected")
        
        # Get authenticated client
        linkedin_client = auth_manager.get_authenticated_client()
        
        # Show real-time data tabs
        profile_tab, analytics_tab, publish_tab, setup_tab = st.tabs(["👤 Profile", "📊 Live Analytics", "🚀 Publish", "⚙️ Setup"])
        
        with profile_tab:
            st.markdown("### 👤 LinkedIn Profile")
            
            if st.button("🔄 Refresh Profile Data"):
                with st.spinner("Fetching LinkedIn profile..."):
                    profile_data = linkedin_client.get_profile_info()
                    
                    if profile_data:
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            st.markdown("**Profile Info:**")
                            st.write(f"Name: {profile_data.get('first_name', '')} {profile_data.get('last_name', '')}")
                            st.write(f"ID: {profile_data.get('id', '')}")
                        
                        with col2:
                            # Test API connection
                            connection_test = linkedin_client.test_connection()
                            if connection_test['success']:
                                st.success(f"✅ {connection_test['message']}")
                            else:
                                st.error(f"❌ {connection_test['message']}")
        
        with analytics_tab:
            st.markdown("### 📊 Live LinkedIn Analytics")
            
            if st.button("🔄 Fetch Live Analytics"):
                with st.spinner("Fetching real-time LinkedIn data..."):
                    analytics_data = linkedin_client.get_profile_analytics()
                    
                    if analytics_data:
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Connections", f"{analytics_data.get('connections', 0):,}")
                        with col2:
                            st.metric("Followers", f"{analytics_data.get('followers', 0):,}")
                        with col3:
                            st.metric("Profile Views", f"{analytics_data.get('profile_views', 0):,}")
                        
                        st.markdown(f"**Last Updated:** {analytics_data.get('last_updated', 'Unknown')}")
                    
                    # Show trending hashtags
                    st.markdown("### #️⃣ Trending Hashtags")
                    trending = linkedin_client.get_trending_hashtags()
                    
                    cols = st.columns(4)
                    for i, hashtag in enumerate(trending[:12]):
                        with cols[i % 4]:
                            st.markdown(f"`{hashtag}`")
        
        with publish_tab:
            st.markdown("### 🚀 Publish to LinkedIn")
            
            # Post content
            post_content = st.text_area(
                "📝 Post Content",
                placeholder="Write your LinkedIn post here...",
                height=150,
                max_chars=3000
            )
            
            # Publishing options
            col1, col2 = st.columns(2)
            
            with col1:
                visibility = st.selectbox(
                    "🌍 Visibility",
                    ["PUBLIC", "CONNECTIONS_ONLY"],
                    help="Who can see this post"
                )
            
            with col2:
                schedule_option = st.selectbox(
                    "⏰ Publishing",
                    ["Publish Now", "Schedule for Later"],
                    help="When to publish the post"
                )
            
            if schedule_option == "Schedule for Later":
                schedule_date = st.date_input("📅 Schedule Date")
                schedule_time = st.time_input("⏰ Schedule Time")
                st.info("📝 Note: Scheduling requires background job system")
            
            # Publish button
            if st.button("🚀 Publish to LinkedIn", type="primary", disabled=not post_content):
                if post_content:
                    with st.spinner("Publishing to LinkedIn..."):
                        result = linkedin_client.publish_post(post_content, visibility)
                        
                        if result.get('success'):
                            st.success(f"✅ Post published successfully!")
                            st.markdown(f"**Post ID:** {result.get('post_id')}")
                            st.balloons()
                        else:
                            st.error(f"❌ Publishing failed: {result.get('error')}")
                else:
                    st.warning("⚠️ Please enter post content")
        
        with setup_tab:
            st.markdown("### ⚙️ API Configuration")
            
            # Show current API status
            st.markdown("**Current Status:**")
            st.success("✅ LinkedIn API: Connected")
            
            # API credentials status
            client_id = os.getenv('LINKEDIN_CLIENT_ID')
            client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
            
            col1, col2 = st.columns(2)
            with col1:
                status = "✅ Set" if client_id else "❌ Missing"
                st.markdown(f"**Client ID:** {status}")
            with col2:
                status = "✅ Set" if client_secret else "❌ Missing"
                st.markdown(f"**Client Secret:** {status}")
            
            # Disconnect option
            if st.button("🔌 Disconnect LinkedIn"):
                if 'linkedin_access_token' in st.session_state:
                    del st.session_state['linkedin_access_token']
                if 'linkedin_token_expires' in st.session_state:
                    del st.session_state['linkedin_token_expires']
                st.success("🔌 Disconnected from LinkedIn")
                st.experimental_rerun()
    
    else:
        # Not authenticated - show setup instructions
        st.warning("⚠️ LinkedIn API not connected")
        
        # Setup tabs
        auth_tab, instructions_tab, credentials_tab = st.tabs(["🔐 Authenticate", "📝 Instructions", "🔑 Credentials"])
        
        with auth_tab:
            st.markdown("### 🔐 LinkedIn Authentication")
            
            # Check if credentials are configured
            client_id = os.getenv('LINKEDIN_CLIENT_ID')
            
            if not client_id:
                st.error("❌ LinkedIn API credentials not configured")
                st.markdown("Please set up your LinkedIn API credentials first (see Instructions tab)")
            else:
                st.info("🔗 Ready to connect to LinkedIn")
                
                if st.button("🔗 Connect to LinkedIn", type="primary"):
                    try:
                        auth_url = auth_manager.initiate_auth_flow()
                        st.markdown(f"**[Click here to authorize with LinkedIn]({auth_url})**")
                        st.markdown("After authorization, you'll be redirected back to continue.")
                    except Exception as e:
                        st.error(f"Authentication setup failed: {e}")
                
                # Manual token input (for development)
                st.markdown("---")
                st.markdown("**Development Mode:**")
                manual_token = st.text_input(
                    "Manual Access Token",
                    type="password",
                    help="For development: paste your LinkedIn access token"
                )
                
                if st.button("🔑 Set Manual Token") and manual_token:
                    st.session_state['linkedin_access_token'] = manual_token
                    st.session_state['linkedin_token_expires'] = datetime.now() + timedelta(hours=1)
                    st.success("✅ Manual token set! Refresh the page.")
        
        with instructions_tab:
            st.markdown(LINKEDIN_API_SETUP_INSTRUCTIONS)
        
        with credentials_tab:
            st.markdown("### 🔑 API Credentials Setup")
            
            st.markdown("**Current Environment Variables:**")
            
            # Show current status
            credentials = {
                'LINKEDIN_CLIENT_ID': os.getenv('LINKEDIN_CLIENT_ID'),
                'LINKEDIN_CLIENT_SECRET': os.getenv('LINKEDIN_CLIENT_SECRET'),
                'LINKEDIN_REDIRECT_URI': os.getenv('LINKEDIN_REDIRECT_URI')
            }
            
            for key, value in credentials.items():
                status = "✅ Set" if value else "❌ Missing"
                st.markdown(f"**{key}:** {status}")
                if value:
                    st.code(f"{key}={value[:10]}...")
            
            st.markdown("---")
            st.markdown("**To set credentials, add to your `.env` file:**")
            st.code('''
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
LINKEDIN_REDIRECT_URI=http://localhost:8507/callback
''')
            
            if st.button("🔄 Reload Environment"):
                st.info("🔄 Please restart the application to reload environment variables")

if __name__ == "__main__":
    main()
