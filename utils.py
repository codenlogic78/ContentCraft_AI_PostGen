"""
Utility functions for ContentCraft AI PostGen
"""
import os
import json
from typing import List, Dict, Any

def ensure_directory_exists(directory_path: str) -> None:
    """Ensure that a directory exists, create if it doesn't"""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load JSON data from file with error handling"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: File {file_path} not found")
        return {}
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in {file_path}")
        return {}

def save_json_file(data: Dict[str, Any], file_path: str) -> bool:
    """Save data to JSON file with error handling"""
    try:
        ensure_directory_exists(os.path.dirname(file_path))
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving to {file_path}: {e}")
        return False

def validate_post_data(post: Dict[str, Any]) -> bool:
    """Validate that a post contains required fields"""
    required_fields = ['text', 'tags', 'language', 'line_count']
    return all(field in post for field in required_fields)

def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    if not isinstance(text, str):
        return ""
    
    # Remove extra whitespace and normalize line endings
    text = text.strip()
    text = '\n'.join(line.strip() for line in text.split('\n'))
    
    return text

def count_lines(text: str) -> int:
    """Count the number of lines in text"""
    if not text:
        return 0
    return len([line for line in text.split('\n') if line.strip()])

def format_post_preview(post: str, max_length: int = 100) -> str:
    """Format post for preview display"""
    if len(post) <= max_length:
        return post
    return post[:max_length] + "..."
