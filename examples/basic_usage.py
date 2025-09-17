#!/usr/bin/env python3
"""
Basic usage example for ContentCraft AI PostGen
"""
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from post_generator import generate_post
from few_shot import FewShotPosts

def main():
    """Demonstrate basic usage of ContentCraft AI PostGen"""
    print("🚀 ContentCraft AI PostGen - Basic Usage Example\n")
    
    # Initialize the few-shot posts handler
    fs = FewShotPosts()
    
    # Get available tags
    tags = fs.get_tags()
    print(f"Available topics: {', '.join(tags[:5])}...")
    
    # Example 1: Generate a short English post about Career
    print("\n📝 Example 1: Short Career Post in English")
    print("-" * 50)
    
    topic = "Career" if "Career" in tags else tags[0]
    post = generate_post("Short", "English", topic)
    print(f"Topic: {topic}")
    print(f"Generated Post:\n{post}\n")
    
    # Example 2: Generate a medium Hinglish post
    print("📝 Example 2: Medium Post in Hinglish")
    print("-" * 50)
    
    topic = "Technology" if "Technology" in tags else tags[0]
    post = generate_post("Medium", "Hinglish", topic)
    print(f"Topic: {topic}")
    print(f"Generated Post:\n{post}\n")
    
    # Example 3: Generate a long post
    print("📝 Example 3: Long Post")
    print("-" * 50)
    
    topic = "Business" if "Business" in tags else tags[0]
    post = generate_post("Long", "English", topic)
    print(f"Topic: {topic}")
    print(f"Generated Post:\n{post}\n")
    
    print("✅ Examples completed! Try running the Streamlit app with: streamlit run main.py")

if __name__ == "__main__":
    main()
