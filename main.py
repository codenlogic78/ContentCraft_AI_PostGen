import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post
from config import Config

# Initialize configuration
config = Config()

# Options for length and language
length_options = config.LENGTH_OPTIONS
language_options = config.LANGUAGE_OPTIONS


# Main app layout
def main():
    st.title("🚀 ContentCraft AI PostGen")
    st.subheader("Your AI-Powered Social Media Content Generator")

    # Create three columns for the dropdowns
    col1, col2, col3 = st.columns(3)

    fs = FewShotPosts()
    tags = fs.get_tags()
    with col1:
        # Dropdown for Topic (Tags)
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        # Dropdown for Length
        selected_length = st.selectbox("Length", options=length_options)

    with col3:
        # Dropdown for Language
        selected_language = st.selectbox("Language", options=language_options)



    # Add some spacing and styling
    st.markdown("---")
    st.markdown("### 📝 Generate Your Content")
    
    # Generate Button with enhanced styling
    if st.button("🚀 Generate Post", type="primary"):
        with st.spinner("✨ Crafting your personalized content..."):
            post = generate_post(selected_length, selected_language, selected_tag)
        
        st.success("🎉 Your content is ready!")
        st.markdown("### Generated Post:")
        st.markdown(f"```\n{post}\n```")
        
        # Add copy to clipboard functionality
        st.markdown("---")
        st.info("💡 **Tip:** Copy the generated post and customize it further to match your personal touch!")


# Configure Streamlit page
if __name__ == "__main__":
    st.set_page_config(
        page_title=config.PAGE_TITLE,
        page_icon=config.PAGE_ICON,
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
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
    
    main()
