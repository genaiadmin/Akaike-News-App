import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from sentiment_analysis import analyze_sentiment  # Import Sentiment Analysis
from comparative_analysis import generate_sentiment_report  # Import Comparative Analysis
from hindi_tts import generate_hindi_tts  # Import Hindi Text-to-Speech
from IPython.display import Audio, display  # ✅ FIXED: Import `display`

# Load AI-powered summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def get_news(company):
    """Fetches the latest 10 news articles for a given company and analyzes sentiment."""
    url = f"https://www.bing.com/news/search?q={company}&form=QBNH"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": f"Unable to fetch news (Status Code: {response.status_code})"}
    
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("a", class_="title")[:10]  # Adjust selector if needed
    
    news_list = []
    for article in articles:
        title = article.text.strip()
        link = article["href"]
        summary = summarize_text(title)  # Summarize the news headline
        sentiment = analyze_sentiment(summary)  # Analyze sentiment

        news_list.append({
            "title": title,
            "link": link,
            "summary": summary,
            "sentiment": sentiment  # Store sentiment label
        })
    
    return news_list

def summarize_text(text):
    """Summarizes text using a Transformer model with optimized length settings."""
    words = len(text.split())  # Count words
    max_length = max(15, min(30, words - 5))  # Optimize summarization length
    
    if words < 10:  # Skip summarization for very short text
        return text  
    
    summary = summarizer(text, max_length=max_length, min_length=10, do_sample=False)
    return summary[0]['summary_text']

if __name__ == "__main__":
    company_name = input("Enter the company name: ")
    news_results = get_news(company_name)

    print("\nLatest News Articles with Sentiment Analysis:")
    if news_results and "error" not in news_results:
        for idx, news in enumerate(news_results, 1):
            print(f"{idx}. {news['title']}")
            print(f"   Summary: {news['summary']}")
            print(f"   Sentiment: {news['sentiment']}")  
            print(f"   Link: {news['link']}\n")

        # ✅ Generate and Display Comparative Sentiment Analysis Report
        sentiment_report = generate_sentiment_report(news_results)
        print("\n📊 Sentiment Analysis Report:")
        print(f"   Positive: {sentiment_report['Positive']}")
        print(f"   Negative: {sentiment_report['Negative']}")
        print(f"   Neutral: {sentiment_report['Neutral']}")
        print(f"   Total Articles: {sentiment_report['Total Articles']}")
        print(f"   Overall Sentiment: {sentiment_report['Overall Sentiment']}")

        # ✅ Generate and Play Hindi Text-to-Speech
        generate_hindi_tts(sentiment_report)
        print("\n🔊 Playing Sentiment Report in Hindi...")
        
        # ✅ FIXED: Play the Hindi speech file correctly
        display(Audio("sentiment_report.mp3"))

    else:
        print("No news articles found or an error occurred.")
