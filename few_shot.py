import json
from config import Config

config = Config()

# Try to import pandas, fallback to basic functionality if not available
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: pandas not available, using basic JSON processing")

class FewShotPosts:
    def __init__(self, file_path=None):
        if file_path is None:
            file_path = config.PROCESSED_POSTS_PATH
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        """Load and process posts from JSON file"""
        try:
            with open(file_path, encoding="utf-8") as f:
                posts = json.load(f)
                
                if PANDAS_AVAILABLE:
                    self.df = pd.json_normalize(posts)
                    self.df['length'] = self.df['line_count'].apply(self.categorize_length)
                    # collect unique tags
                    all_tags = self.df['tags'].apply(lambda x: x).sum()
                    self.unique_tags = list(set(all_tags))
                else:
                    # Fallback to basic processing without pandas
                    self.posts_data = posts
                    self.df = None
                    # Process posts manually
                    for post in posts:
                        post['length'] = self.categorize_length(post.get('line_count', 0))
                    
                    # collect unique tags
                    all_tags = []
                    for post in posts:
                        all_tags.extend(post.get('tags', []))
                    self.unique_tags = list(set(all_tags))
                    
        except FileNotFoundError:
            print(f"Warning: Could not find {file_path}. Using empty dataset.")
            if PANDAS_AVAILABLE:
                self.df = pd.DataFrame()
            else:
                self.posts_data = []
                self.df = None
            self.unique_tags = []

    def get_filtered_posts(self, length, language, tag):
        """Filter posts based on length, language, and tag"""
        if PANDAS_AVAILABLE and self.df is not None:
            if self.df.empty:
                return []
                
            df_filtered = self.df[
                (self.df['tags'].apply(lambda tags: tag in tags)) &
                (self.df['language'] == language) &
                (self.df['length'] == length)
            ]
            return df_filtered.to_dict(orient='records')
        else:
            # Fallback manual filtering
            if not hasattr(self, 'posts_data') or not self.posts_data:
                return []
                
            filtered_posts = []
            for post in self.posts_data:
                if (tag in post.get('tags', []) and 
                    post.get('language') == language and 
                    post.get('length') == length):
                    filtered_posts.append(post)
            return filtered_posts

    def categorize_length(self, line_count):
        """Categorize post length based on line count"""
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        """Get list of unique tags from the dataset"""
        return self.unique_tags if self.unique_tags else ["General", "Technology", "Career", "Business"]


if __name__ == "__main__":
    fs = FewShotPosts()
    # print(fs.get_tags())
    posts = fs.get_filtered_posts("Medium","Hinglish","Job Search")
    print(posts)