from collections import Counter

def generate_sentiment_report(news_list):
    """Generates a summary of sentiment distribution."""
    
    # Count occurrences of each sentiment
    sentiment_counts = Counter(news['sentiment'] for news in news_list)
    
    # Calculate total articles
    total = sum(sentiment_counts.values())

    # Determine overall sentiment trend
    overall_sentiment = determine_overall_sentiment(sentiment_counts)

    # Create sentiment summary report
    report = {
        "Positive": sentiment_counts.get("Positive", 0),
        "Negative": sentiment_counts.get("Negative", 0),
        "Neutral": sentiment_counts.get("Neutral", 0),
        "Total Articles": total,
        "Overall Sentiment": overall_sentiment
    }

    return report

def determine_overall_sentiment(sentiment_counts):
    """Determines the dominant sentiment trend."""
    positive = sentiment_counts.get("Positive", 0)
    negative = sentiment_counts.get("Negative", 0)

    if positive > negative:
        return "Mostly Positive"
    elif negative > positive:
        return "Mostly Negative"
    else:
        return "Balanced Sentiment"

# Test function
if __name__ == "__main__":
    sample_news = [
        {"title": "Stock Market Up", "sentiment": "Positive"},
        {"title": "Economy Declines", "sentiment": "Negative"},
        {"title": "Tech Industry Steady", "sentiment": "Neutral"},
        {"title": "New AI Breakthrough", "sentiment": "Positive"},
    ]
    
    report = generate_sentiment_report(sample_news)
    print(report)
