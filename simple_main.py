import streamlit as st
import json
import os

# Simple configuration
class SimpleConfig:
    APP_NAME = "ContentCraft AI PostGen"
    LENGTH_OPTIONS = ["Short", "Medium", "Long"]
    LANGUAGE_OPTIONS = ["English", "Hinglish"]
    
    LENGTH_MAPPING = {
        "Short": "1 to 5 lines",
        "Medium": "6 to 10 lines", 
        "Long": "11 to 15 lines"
    }

config = SimpleConfig()

# Simple post data handler
class SimplePosts:
    def __init__(self):
        self.posts_data = []
        self.unique_tags = ["Career", "Technology", "Business", "Personal Growth", "Leadership", "Innovation"]
        self.load_sample_data()
    
    def load_sample_data(self):
        # Sample data for demonstration
        self.posts_data = [
            {
                "text": "Just completed an amazing project! The key to success is persistence and continuous learning. #Career #Growth",
                "tags": ["Career", "Personal Growth"],
                "language": "English",
                "line_count": 2,
                "length": "Short"
            },
            {
                "text": "Technology is reshaping our world every day. From AI to blockchain, we're witnessing unprecedented innovation. The future belongs to those who adapt and embrace change. What's your take on the latest tech trends?",
                "tags": ["Technology", "Innovation"],
                "language": "English", 
                "line_count": 4,
                "length": "Short"
            }
        ]
    
    def get_tags(self):
        return self.unique_tags
    
    def get_filtered_posts(self, length, language, tag):
        filtered = []
        for post in self.posts_data:
            if (tag in post.get('tags', []) and 
                post.get('language') == language and 
                post.get('length') == length):
                filtered.append(post)
        return filtered

# Simple post generator (mock for now)
def generate_mock_post(length, language, tag):
    length_str = config.LENGTH_MAPPING.get(length, "6 to 10 lines")
    
    sample_posts = {
        "Career": {
            "Short": f"🚀 Just achieved a major milestone in my {tag.lower()} journey! The key is consistent effort and never giving up. What's your biggest career win this year?",
            "Medium": f"💼 Reflecting on my {tag.lower()} path today. Every challenge has been a stepping stone to growth. From late nights to breakthrough moments, the journey shapes us. Remember: your current position is not your final destination. Keep pushing forward! What's one lesson you've learned recently?",
            "Long": f"🌟 Today marks an important moment in my {tag.lower()} journey. Looking back, I realize how much I've grown from facing challenges head-on. Each obstacle taught me resilience, each failure showed me new paths, and each success reminded me why I started. The corporate world can be tough, but it's also full of opportunities for those willing to learn and adapt. My advice to anyone starting out: embrace the uncertainty, build genuine relationships, stay curious, and never stop learning. Your {tag.lower()} is a marathon, not a sprint. What's one piece of advice that changed your professional life?"
        },
        "Technology": {
            "Short": f"🔥 The future of {tag.lower()} is here! AI and automation are reshaping industries. Are you ready for what's coming next?",
            "Medium": f"💻 {tag.lower()} continues to amaze me every day. From machine learning breakthroughs to quantum computing advances, we're living in extraordinary times. The pace of innovation is accelerating, and those who adapt will thrive. What tech trend excites you the most?",
            "Long": f"🚀 The {tag.lower()} landscape is evolving at breakneck speed. Artificial intelligence, blockchain, IoT, and quantum computing are no longer futuristic concepts – they're today's reality. As professionals, we must stay ahead of the curve by continuously learning and adapting. The companies that will succeed are those that embrace digital transformation and put innovation at their core. But remember, technology is just a tool – it's how we use it to solve real problems that matters. What's one way you're leveraging technology to make a difference in your field?"
        },
        "Business": {
            "Short": f"📈 {tag} success isn't just about profits – it's about creating value and building lasting relationships. What's your definition of success?",
            "Medium": f"💼 In today's {tag.lower()} world, adaptability is everything. Markets change, customer needs evolve, and new competitors emerge constantly. The key is staying agile while maintaining your core values. How is your organization staying competitive?",
            "Long": f"🏢 Running a {tag.lower()} in today's world requires more than just a good product or service. It demands vision, adaptability, and genuine care for your customers and team. I've learned that sustainable growth comes from building trust, delivering consistent value, and always being willing to evolve. The most successful companies are those that view challenges as opportunities and treat their employees as their greatest asset. Remember: {tag.lower()} is ultimately about people – understanding their needs, solving their problems, and creating meaningful connections. What's one lesson that transformed your approach to {tag.lower()}?"
        }
    }
    
    # Get sample post or create a generic one
    category_posts = sample_posts.get(tag, sample_posts["Career"])
    return category_posts.get(length, f"Here's a {length.lower()} post about {tag} in {language}. This is a sample generated post that demonstrates the ContentCraft AI PostGen functionality!")

# Main Streamlit app
def main():
    st.set_page_config(
        page_title="🚀 ContentCraft AI PostGen",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.title("🚀 ContentCraft AI PostGen")
    st.subheader("Your AI-Powered Social Media Content Generator")
    
    # Add sidebar with information
    with st.sidebar:
        st.markdown("## About ContentCraft AI")
        st.markdown(
            "ContentCraft AI PostGen analyzes your writing style "
            "and generates authentic social media content that "
            "matches your unique voice."
        )
        st.markdown("---")
        st.markdown("### Features:")
        st.markdown("• 🎯 Style-matched content generation")
        st.markdown("• 📏 Flexible post lengths")
        st.markdown("• 🌐 Multi-language support")
        st.markdown("• 🤖 AI-powered topic analysis")
        st.markdown("---")
        st.markdown("**Made with ❤️ for content creators**")
    
    # Create three columns for the dropdowns
    col1, col2, col3 = st.columns(3)
    
    fs = SimplePosts()
    tags = fs.get_tags()
    
    with col1:
        selected_tag = st.selectbox("Topic", options=tags)
    
    with col2:
        selected_length = st.selectbox("Length", options=config.LENGTH_OPTIONS)
    
    with col3:
        selected_language = st.selectbox("Language", options=config.LANGUAGE_OPTIONS)
    
    # Add some spacing and styling
    st.markdown("---")
    st.markdown("### 📝 Generate Your Content")
    
    # Generate Button with enhanced styling
    if st.button("🚀 Generate Post", type="primary"):
        with st.spinner("✨ Crafting your personalized content..."):
            post = generate_mock_post(selected_length, selected_language, selected_tag)
        
        st.success("🎉 Your content is ready!")
        st.markdown("### Generated Post:")
        st.markdown(f"```\n{post}\n```")
        
        # Add copy to clipboard functionality
        st.markdown("---")
        st.info("💡 **Tip:** Copy the generated post and customize it further to match your personal touch!")
        
        # Show configuration note
        st.warning("🔧 **Note:** This is running in demo mode with sample content. To use AI generation, add your GROQ_API_KEY to the .env file.")

if __name__ == "__main__":
    main()
