from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download VADER (only needed once)
nltk.download('vader_lexicon')

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """Analyzes sentiment and returns Positive, Negative, or Neutral labels."""
    sentiment_score = sia.polarity_scores(text)['compound']
    
    if sentiment_score >= 0.05:
        return "Positive"
    elif sentiment_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Test function
if __name__ == "__main__":
    sample_text = "Google just launched an amazing new AI product!"
    print(f"Sentiment: {analyze_sentiment(sample_text)}")
