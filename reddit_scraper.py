import praw
import time
from typing import List, Dict, Optional
from config import Config

class RedditScraper:
    def __init__(self):
        Config.validate_reddit_config()
        
        self.reddit = praw.Reddit(
            client_id=Config.REDDIT_CLIENT_ID,
            client_secret=Config.REDDIT_CLIENT_SECRET,
            user_agent=Config.REDDIT_USER_AGENT,
            username=Config.REDDIT_USERNAME,
            password=Config.REDDIT_PASSWORD
        )
        
        self.subreddit = self.reddit.subreddit(Config.SUBREDDIT)
    
    def scrape_posts(self, limit: int = None) -> List[Dict[str, str]]:
        if limit is None:
            limit = Config.MAX_POSTS
            
        posts_data = []
        
        try:
            for submission in self.subreddit.hot(limit=limit):
                post_data = {
                    'id': submission.id,
                    'title': submission.title,
                    'body': submission.selftext if submission.selftext else '',
                    'score': submission.score,
                    'comments': []
                }
                
                submission.comments.replace_more(limit=0)
                
                for comment in submission.comments.list()[:20]:
                    if hasattr(comment, 'body') and comment.body:
                        post_data['comments'].append({
                            'body': comment.body,
                            'score': comment.score
                        })
                
                posts_data.append(post_data)
                
                time.sleep(Config.RATE_LIMIT_DELAY)
                
        except Exception as e:
            print(f"Error scraping Reddit: {e}")
            raise
            
        return posts_data
    
    def get_all_text(self, posts_data: List[Dict]) -> List[str]:
        all_text = []
        
        for post in posts_data:
            if post['title']:
                all_text.append(post['title'])
            if post['body']:
                all_text.append(post['body'])
            
            for comment in post['comments']:
                if comment['body'] and comment['body'] not in ['[deleted]', '[removed]']:
                    all_text.append(comment['body'])
        
        return all_text