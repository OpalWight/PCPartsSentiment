import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from typing import Dict, List, Tuple
import os

class SentimentAnalyzer:
    def __init__(self):
        self._download_vader_lexicon()
        self.analyzer = SentimentIntensityAnalyzer()
    
    def _download_vader_lexicon(self):
        try:
            nltk.data.find('vader_lexicon')
        except LookupError:
            print("Downloading VADER lexicon...")
            nltk.download('vader_lexicon', quiet=True)
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        scores = self.analyzer.polarity_scores(text)
        return scores
    
    def classify_sentiment(self, compound_score: float) -> str:
        if compound_score >= 0.05:
            return "Positive"
        elif compound_score <= -0.05:
            return "Negative"
        else:
            return "Neutral"
    
    def analyze_brand_mentions(self, brand_mentions: Dict[str, List[str]]) -> Dict[str, Dict]:
        results = {}
        
        for brand, texts in brand_mentions.items():
            total_compound = 0.0
            mention_count = 0
            sentiment_scores = []
            
            for text in texts:
                scores = self.analyze_sentiment(text)
                sentiment_scores.append(scores)
                total_compound += scores['compound']
                mention_count += 1
            
            if mention_count > 0:
                avg_compound = total_compound / mention_count
                sentiment_classification = self.classify_sentiment(avg_compound)
                
                results[brand] = {
                    'mention_count': mention_count,
                    'avg_compound_score': round(avg_compound, 3),
                    'sentiment': sentiment_classification,
                    'individual_scores': sentiment_scores
                }
        
        return results
    
    def get_sentiment_summary(self, results: Dict[str, Dict]) -> Dict[str, int]:
        summary = {"Positive": 0, "Neutral": 0, "Negative": 0}
        
        for brand_data in results.values():
            sentiment = brand_data['sentiment']
            summary[sentiment] += 1
        
        return summary