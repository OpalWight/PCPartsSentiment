#!/usr/bin/env python3

import sys
import argparse
from datetime import datetime
from reddit_scraper import RedditScraper
from brand_matcher import BrandMatcher
from sentiment_analyzer import SentimentAnalyzer
from config import Config

def print_header():
    print("=" * 60)
    print("PC Parts Brand Sentiment Analyzer")
    print("r/pcbuilds Sentiment Analysis Tool")
    print("=" * 60)
    print()

def print_results(results, sentiment_summary):
    print(f"\n{'='*60}")
    print("SENTIMENT ANALYSIS RESULTS")
    print(f"{'='*60}")
    
    if not results:
        print("No brand mentions found in the analyzed posts.")
        return
    
    sorted_results = sorted(results.items(), key=lambda x: x[1]['avg_compound_score'], reverse=True)
    
    print(f"\n{'Brand':<20} {'Mentions':<10} {'Score':<8} {'Sentiment':<10}")
    print("-" * 60)
    
    for brand, data in sorted_results:
        brand_display = brand.title()
        mentions = data['mention_count']
        score = data['avg_compound_score']
        sentiment = data['sentiment']
        
        sentiment_icon = "😊" if sentiment == "Positive" else "😐" if sentiment == "Neutral" else "😞"
        
        print(f"{brand_display:<20} {mentions:<10} {score:<8} {sentiment:<10} {sentiment_icon}")
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total brands analyzed: {len(results)}")
    print(f"Positive sentiment: {sentiment_summary['Positive']} brands")
    print(f"Neutral sentiment: {sentiment_summary['Neutral']} brands")
    print(f"Negative sentiment: {sentiment_summary['Negative']} brands")
    
    total_mentions = sum(data['mention_count'] for data in results.values())
    print(f"Total mentions: {total_mentions}")
    
    if results:
        avg_sentiment = sum(data['avg_compound_score'] for data in results.values()) / len(results)
        print(f"Overall average sentiment: {avg_sentiment:.3f}")

def main():
    parser = argparse.ArgumentParser(description='Analyze PC part brand sentiment from r/pcbuilds')
    parser.add_argument('--posts', type=int, default=Config.MAX_POSTS,
                        help=f'Number of posts to analyze (default: {Config.MAX_POSTS})')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose output')
    
    args = parser.parse_args()
    
    try:
        print_header()
        
        if args.verbose:
            print(f"Configuration:")
            print(f"  Subreddit: r/{Config.SUBREDDIT}")
            print(f"  Max posts: {args.posts}")
            print(f"  Rate limit delay: {Config.RATE_LIMIT_DELAY}s")
            print()
        
        print("🔍 Initializing Reddit scraper...")
        scraper = RedditScraper()
        
        print("📝 Loading brand database...")
        matcher = BrandMatcher()
        
        print("🧠 Initializing sentiment analyzer...")
        analyzer = SentimentAnalyzer()
        
        print(f"📊 Scraping {args.posts} posts from r/{Config.SUBREDDIT}...")
        posts_data = scraper.scrape_posts(limit=args.posts)
        
        if not posts_data:
            print("❌ No posts found. Please check your Reddit API configuration.")
            sys.exit(1)
        
        print(f"✅ Successfully scraped {len(posts_data)} posts")
        
        print("🔍 Extracting text and matching brands...")
        all_text = scraper.get_all_text(posts_data)
        brand_mentions = matcher.extract_brand_mentions(all_text)
        
        if not brand_mentions:
            print("❌ No brand mentions found in the scraped content.")
            sys.exit(0)
        
        print(f"✅ Found mentions of {len(brand_mentions)} different brands")
        
        print("💭 Analyzing sentiment...")
        results = analyzer.analyze_brand_mentions(brand_mentions)
        sentiment_summary = analyzer.get_sentiment_summary(results)
        
        print_results(results, sentiment_summary)
        
        print(f"\n📅 Analysis completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except KeyboardInterrupt:
        print("\n❌ Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()