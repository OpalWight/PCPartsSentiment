import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'PCPartsSentiment/1.0')
    REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
    REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')
    
    MAX_POSTS = int(os.getenv('MAX_POSTS', '100'))
    RATE_LIMIT_DELAY = int(os.getenv('RATE_LIMIT_DELAY', '2'))
    
    SUBREDDIT = 'pcbuilds'
    BRANDS_FILE = 'brands.json'
    
    @classmethod
    def validate_reddit_config(cls):
        if not cls.REDDIT_CLIENT_ID or not cls.REDDIT_CLIENT_SECRET:
            raise ValueError("Reddit API credentials are required. Please check your .env file.")
        return True