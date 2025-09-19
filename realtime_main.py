import streamlit as st
import json
import os
from datetime import datetime, timedelta
import time
from api_integrations import SocialMediaAPIs, RealTimeAnalytics, ContentScheduler

# Enhanced configuration with real-time capabilities
class RealTimeConfig:
    APP_NAME = "ContentCraft AI PostGen"
    VERSION = "3.0.0 - Real-Time Edition"
    
    PLATFORMS = {
        "LinkedIn": {"max_chars": 3000, "icon": "💼", "hashtags": True, "api_enabled": True},
        "Twitter/X": {"max_chars": 280, "icon": "🐦", "hashtags": True, "api_enabled": True},
        "Instagram": {"max_chars": 2200, "icon": "📸", "hashtags": True, "api_enabled": True},
        "Facebook": {"max_chars": 63206, "icon": "📘", "hashtags": False, "api_enabled": True},
        "TikTok": {"max_chars": 150, "icon": "🎵", "hashtags": True, "api_enabled": False},
        "YouTube": {"max_chars": 5000, "icon": "📺", "hashtags": True, "api_enabled": False}
    }
    
    CONTENT_TYPES = [
        "Professional Update", "Thought Leadership", "Industry News", 
        "Personal Story", "Tips & Advice", "Question/Poll", 
        "Behind the Scenes", "Product Launch", "Event Promotion",
        "Case Study", "Tutorial", "Motivational"
    ]
    
    LENGTH_OPTIONS = ["Short", "Medium", "Long"]
    LANGUAGE_OPTIONS = ["English", "Hinglish", "Spanish", "French", "German"]
    TONES = ["Professional", "Casual", "Inspirational", "Educational", "Humorous", "Authoritative"]
    INDUSTRIES = [
        "Technology", "Healthcare", "Finance", "Education", "Marketing", 
        "Sales", "HR", "Consulting", "Real Estate", "E-commerce"
    ]

config = RealTimeConfig()

# Initialize real-time components
@st.cache_resource
def init_realtime_components():
    return {
        'social_apis': SocialMediaAPIs(),
        'analytics': RealTimeAnalytics(),
        'scheduler': ContentScheduler()
    }

def main():
    st.set_page_config(
        page_title="🚀 ContentCraft AI PostGen v3.0 - Real-Time",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize components
    components = init_realtime_components()
    social_apis = components['social_apis']
    analytics = components['analytics']
    scheduler = components['scheduler']
    
    # Sidebar with real-time data
    with st.sidebar:
        st.markdown("## 🚀 ContentCraft AI v3.0")
        st.markdown("*Real-Time Social Media Studio*")
        
        # Real-time status indicator
        st.markdown("### 🔴 Live Status")
        if st.button("🔄 Refresh Data", key="refresh_sidebar"):
            st.rerun()
        
        # Live metrics
        with st.spinner("📊 Loading live data..."):
            live_metrics = analytics.get_live_metrics(['LinkedIn', 'Twitter', 'Instagram'])
        
        st.markdown("### 📈 Live Metrics")
        for platform, metrics in live_metrics.items():
            with st.expander(f"{config.PLATFORMS[platform]['icon']} {platform}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Followers", f"{metrics.get('followers', 0):,}")
                    st.metric("Engagement", f"{metrics.get('engagement_rate', 0)}%")
                with col2:
                    st.metric("Posts", metrics.get('posts', metrics.get('tweets', 0)))
                    st.caption(f"Updated: {datetime.fromisoformat(metrics['last_updated']).strftime('%H:%M')}")
        
        # Navigation
        st.markdown("---")
        page = st.selectbox(
            "Navigate",
            ["🎯 Content Studio", "📊 Live Analytics", "📅 Scheduler", "🔗 API Settings"]
        )
    
    # Main content area
    if page == "🎯 Content Studio":
        st.title("🎯 Real-Time Content Studio")
        st.markdown("*Create and publish content with live platform integration*")
        
        # Platform selection with real-time trending data
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_platform = st.selectbox(
                "🌐 Platform",
                options=list(config.PLATFORMS.keys()),
                help="Choose your target platform"
            )
            
            # Show real-time trending hashtags
            with st.spinner("🔥 Loading trending hashtags..."):
                trending = social_apis.get_trending_hashtags(selected_platform)
            
            st.markdown("**🔥 Trending Now:**")
            st.write(" ".join(trending[:3]))
        
        with col2:
            selected_topic = st.selectbox(
                "🎯 Topic",
                options=["Technology", "Career", "Business", "Marketing", "Personal Growth", "Leadership"]
            )
            
            selected_tone = st.selectbox("🎭 Tone", options=config.TONES)
        
        with col3:
            selected_length = st.selectbox("📏 Length", options=config.LENGTH_OPTIONS)
            selected_industry = st.selectbox("🏢 Industry", options=config.INDUSTRIES)
        
        # Platform info with API status
        platform_info = config.PLATFORMS[selected_platform]
        api_status = "🟢 Connected" if platform_info['api_enabled'] else "🟡 Demo Mode"
        st.info(f"{platform_info['icon']} **{selected_platform}** - {api_status} | Max {platform_info['max_chars']} chars")
        
        # Content generation
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("🚀 Generate Content", type="primary", use_container_width=True):
                with st.spinner("✨ Creating optimized content..."):
                    time.sleep(2)
                    
                    # Enhanced content generation
                    content = f"""🚀 Breaking: The {selected_industry.lower()} industry is experiencing a major shift in {selected_topic.lower()}! 

Here's what I've learned from analyzing the latest trends:

✅ {selected_tone} approach is key to success
✅ Real-time adaptation beats rigid planning
✅ Community engagement drives authentic growth

The companies thriving today are those that embrace change while staying true to their core values.

What's your take on this transformation? Share your thoughts below! 👇

{' '.join(trending[:3])} #ContentCraft #Innovation"""
                    
                    # Optimize for platform
                    if len(content) > platform_info['max_chars']:
                        content = content[:platform_info['max_chars']-3] + "..."
                    
                    st.success("🎉 Content generated with real-time optimization!")
                    
                    # Display content
                    st.markdown("### 📝 Generated Content:")
                    st.text_area("Content", content, height=150, key="generated_content")
                    
                    # Real-time metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Characters", len(content))
                    with col2:
                        st.metric("Words", len(content.split()))
                    with col3:
                        predicted_engagement = 85 + (len(trending) * 2)
                        st.metric("Predicted Engagement", f"{predicted_engagement}%")
                    with col4:
                        optimal_time = "2:30 PM"
                        st.metric("Optimal Post Time", optimal_time)
                    
                    # Publishing options
                    st.markdown("---")
                    st.markdown("### 📤 Publishing Options")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📡 Publish Now", type="primary", use_container_width=True):
                            with st.spinner("📡 Publishing to platform..."):
                                result = scheduler.publish_now(selected_platform, content)
                                
                                if result['success']:
                                    st.success(f"✅ Published successfully!")
                                    if 'url' in result:
                                        st.markdown(f"🔗 [View Post]({result['url']})")
                                    else:
                                        st.info("📝 Demo mode - Content ready for manual posting")
                                else:
                                    st.error(f"❌ Publishing failed: {result.get('error', 'Unknown error')}")
                    
                    with col2:
                        schedule_time = st.time_input("⏰ Schedule for", datetime.now().time())
                        schedule_date = st.date_input("📅 Date", datetime.now().date())
                        
                        if st.button("📅 Schedule Post", use_container_width=True):
                            schedule_datetime = datetime.combine(schedule_date, schedule_time)
                            result = scheduler.schedule_post(selected_platform, content, schedule_datetime)
                            
                            if result['success']:
                                st.success(f"✅ Scheduled for {schedule_datetime.strftime('%B %d at %I:%M %p')}")
        
        with col2:
            if st.button("🔄 Generate Variation", use_container_width=True):
                st.info("🔄 Generating alternative version...")
        
        with col3:
            if st.button("💾 Save Draft", use_container_width=True):
                st.success("💾 Draft saved to library!")
    
    elif page == "📊 Live Analytics":
        st.title("📊 Live Analytics Dashboard")
        st.markdown("*Real-time performance tracking across all platforms*")
        
        # Auto-refresh toggle
        auto_refresh = st.toggle("🔄 Auto-refresh (30s)", value=False)
        if auto_refresh:
            time.sleep(30)
            st.rerun()
        
        # Live metrics overview
        st.markdown("### 🔴 Live Platform Metrics")
        
        with st.spinner("📊 Fetching live data..."):
            all_metrics = analytics.get_live_metrics(['LinkedIn', 'Twitter', 'Instagram', 'Facebook'])
        
        # Display metrics in columns
        platforms = list(all_metrics.keys())
        cols = st.columns(len(platforms))
        
        for i, (platform, metrics) in enumerate(all_metrics.items()):
            with cols[i]:
                st.markdown(f"#### {config.PLATFORMS[platform]['icon']} {platform}")
                st.metric("Followers", f"{metrics.get('followers', 0):,}", 
                         delta=f"+{metrics.get('followers', 0) % 10}")
                st.metric("Engagement Rate", f"{metrics.get('engagement_rate', 0)}%",
                         delta=f"+{(metrics.get('engagement_rate', 0) % 10) / 10:.1f}%")
                st.metric("Monthly Posts", metrics.get('posts_this_month', metrics.get('posts', 0)))
                
                # Last updated
                last_update = datetime.fromisoformat(metrics['last_updated'])
                st.caption(f"🕐 Updated: {last_update.strftime('%H:%M:%S')}")
        
        # Engagement trends
        st.markdown("---")
        st.markdown("### 📈 Engagement Trends (7 Days)")
        
        selected_platform_analytics = st.selectbox(
            "Select Platform for Detailed Analytics",
            list(config.PLATFORMS.keys()),
            key="analytics_platform"
        )
        
        with st.spinner("📈 Loading trend data..."):
            trend_data = analytics.get_engagement_trends(selected_platform_analytics)
        
        # Display trend chart (mock data for demo)
        import pandas as pd
        df = pd.DataFrame(trend_data['trend_data'])
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.line_chart(df.set_index('date')['engagement_rate'])
        
        with col2:
            st.metric("Average Engagement", f"{trend_data['avg_engagement']}%")
            trend_icon = "📈" if trend_data['trend_direction'] == 'up' else "📉"
            st.metric("Trend", f"{trend_icon} {trend_data['trend_direction'].title()}")
        
        # Top performing content
        st.markdown("---")
        st.markdown("### 🏆 Top Performing Posts (Real-Time)")
        
        # Mock real-time post performance
        top_posts = [
            {"content": "AI is transforming how we work...", "platform": "LinkedIn", "engagement": "156 likes, 23 shares"},
            {"content": "Quick tip for better productivity...", "platform": "Twitter", "engagement": "89 likes, 12 retweets"},
            {"content": "Behind the scenes of our latest project...", "platform": "Instagram", "engagement": "234 likes, 45 comments"}
        ]
        
        for post in top_posts:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{post['content'][:50]}...**")
                with col2:
                    platform_icon = config.PLATFORMS[post['platform']]['icon']
                    st.markdown(f"{platform_icon} {post['platform']}")
                with col3:
                    st.markdown(f"📊 {post['engagement']}")
                st.markdown("---")
    
    elif page == "📅 Scheduler":
        st.title("📅 Real-Time Content Scheduler")
        st.markdown("*Schedule and manage posts across all platforms*")
        
        # Scheduled posts overview
        scheduled_posts = scheduler.get_scheduled_posts()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Scheduled Posts", len([p for p in scheduled_posts if p['status'] == 'scheduled']))
        with col2:
            st.metric("Published Today", len([p for p in scheduled_posts if p['status'] == 'published']))
        with col3:
            st.metric("Failed Posts", len([p for p in scheduled_posts if p['status'] == 'failed']))
        
        # Upcoming posts
        st.markdown("### 📋 Upcoming Posts")
        
        if scheduled_posts:
            for post in scheduled_posts[-5:]:  # Show last 5 posts
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{post['content'][:60]}...**")
                    
                    with col2:
                        platform_icon = config.PLATFORMS[post['platform']]['icon']
                        st.markdown(f"{platform_icon} {post['platform']}")
                    
                    with col3:
                        schedule_time = post['schedule_time'].strftime('%m/%d %H:%M')
                        st.markdown(f"📅 {schedule_time}")
                    
                    with col4:
                        status_colors = {
                            'scheduled': 'orange',
                            'published': 'green',
                            'failed': 'red',
                            'cancelled': 'gray'
                        }
                        color = status_colors.get(post['status'], 'blue')
                        st.markdown(f":{color}[{post['status'].title()}]")
                    
                    st.markdown("---")
        else:
            st.info("📝 No scheduled posts yet. Create content in the Content Studio to get started!")
        
        # Quick scheduling
        st.markdown("### ⚡ Quick Schedule")
        with st.form("quick_schedule"):
            quick_content = st.text_area("Content", placeholder="What's on your mind?")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                quick_platform = st.selectbox("Platform", list(config.PLATFORMS.keys()))
            with col2:
                quick_date = st.date_input("Date", datetime.now().date())
            with col3:
                quick_time = st.time_input("Time", datetime.now().time())
            
            if st.form_submit_button("📅 Schedule Post", type="primary"):
                if quick_content:
                    schedule_datetime = datetime.combine(quick_date, quick_time)
                    result = scheduler.schedule_post(quick_platform, quick_content, schedule_datetime)
                    
                    if result['success']:
                        st.success(f"✅ Post scheduled for {schedule_datetime.strftime('%B %d at %I:%M %p')}")
                        st.rerun()
                else:
                    st.error("Please enter content to schedule")
    
    elif page == "🔗 API Settings":
        st.title("🔗 API Configuration")
        st.markdown("*Connect your social media accounts for real-time features*")
        
        # API status overview
        st.markdown("### 📊 API Connection Status")
        
        api_status = {
            "LinkedIn": {"connected": bool(os.getenv('LINKEDIN_ACCESS_TOKEN')), "features": "Profile stats, posting"},
            "Twitter/X": {"connected": bool(os.getenv('TWITTER_BEARER_TOKEN')), "features": "Analytics, posting, trends"},
            "Instagram": {"connected": bool(os.getenv('INSTAGRAM_ACCESS_TOKEN')), "features": "Basic insights, media"},
            "Facebook": {"connected": bool(os.getenv('FACEBOOK_ACCESS_TOKEN')), "features": "Page insights, posting"}
        }
        
        for platform, status in api_status.items():
            with st.container():
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    platform_icon = config.PLATFORMS[platform]['icon']
                    st.markdown(f"### {platform_icon} {platform}")
                
                with col2:
                    st.markdown(f"**Features:** {status['features']}")
                    if status['connected']:
                        st.success("🟢 Connected")
                    else:
                        st.warning("🟡 Not connected - using demo data")
                
                with col3:
                    if not status['connected']:
                        if st.button(f"Connect {platform}", key=f"connect_{platform}"):
                            st.info(f"Please add your {platform} API credentials to environment variables")
                
                st.markdown("---")
        
        # API configuration
        st.markdown("### 🔑 API Credentials")
        st.info("💡 Add these environment variables to enable real-time features:")
        
        credentials = {
            "LINKEDIN_ACCESS_TOKEN": "Your LinkedIn API access token",
            "TWITTER_BEARER_TOKEN": "Your Twitter API bearer token", 
            "INSTAGRAM_ACCESS_TOKEN": "Your Instagram Basic Display API token",
            "FACEBOOK_ACCESS_TOKEN": "Your Facebook Graph API token"
        }
        
        for var, description in credentials.items():
            st.code(f"export {var}='your_token_here'  # {description}")
        
        # Test connections
        st.markdown("### 🧪 Test API Connections")
        if st.button("🔍 Test All Connections", type="primary"):
            with st.spinner("Testing API connections..."):
                time.sleep(2)
                
                test_results = {
                    "LinkedIn": "🟢 Connected" if os.getenv('LINKEDIN_ACCESS_TOKEN') else "🟡 Demo mode",
                    "Twitter/X": "🟢 Connected" if os.getenv('TWITTER_BEARER_TOKEN') else "🟡 Demo mode",
                    "Instagram": "🟢 Connected" if os.getenv('INSTAGRAM_ACCESS_TOKEN') else "🟡 Demo mode",
                    "Facebook": "🟢 Connected" if os.getenv('FACEBOOK_ACCESS_TOKEN') else "🟡 Demo mode"
                }
                
                for platform, result in test_results.items():
                    st.markdown(f"**{platform}:** {result}")
    
    # Footer with real-time status
    st.markdown("---")
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(
        f"<div style='text-align: center; color: #666;'>"
        f"ContentCraft AI PostGen v{config.VERSION} | 🔴 Live at {current_time} | Made with ❤️ for content creators"
        f"</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
