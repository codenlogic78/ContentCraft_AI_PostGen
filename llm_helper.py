from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from config import Config

load_dotenv()
config = Config()

# Validate configuration before initializing LLM
try:
    config.validate_config()
    llm = ChatGroq(groq_api_key=config.GROQ_API_KEY, model_name=config.MODEL_NAME)
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please ensure your .env file contains a valid GROQ_API_KEY")
    llm = None


if __name__ == "__main__":
    if llm:
        response = llm.invoke("What are the key benefits of AI-powered content generation?")
        print(response.content)
    else:
        print("LLM not initialized. Please check your configuration.")





