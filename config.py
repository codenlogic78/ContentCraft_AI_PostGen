"""
Configuration settings for ContentCraft AI PostGen
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class"""
    
    # API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MODEL_NAME = "llama-3.2-90b-text-preview"
    
    # Data paths
    PROCESSED_POSTS_PATH = "data/processed_posts.json"
    RAW_POSTS_PATH = "data/raw_posts.json"
    
    # Application settings
    APP_NAME = "ContentCraft AI PostGen"
    APP_DESCRIPTION = "Your AI-Powered Social Media Content Generator"
    
    # Post generation settings
    LENGTH_OPTIONS = ["Short", "Medium", "Long"]
    LANGUAGE_OPTIONS = ["English", "Hinglish"]
    
    # Length definitions
    LENGTH_MAPPING = {
        "Short": "1 to 5 lines",
        "Medium": "6 to 10 lines", 
        "Long": "11 to 15 lines"
    }
    
    # UI Configuration
    PAGE_TITLE = "🚀 ContentCraft AI PostGen"
    PAGE_ICON = "🚀"
    
    @classmethod
    def validate_config(cls):
        """Validate required configuration"""
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable is required")
        return True
