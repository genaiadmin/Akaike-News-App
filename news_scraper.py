import feedparser
import logging
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from gtts import gTTS
import time
from tenacity import retry, stop_after_attempt, wait_exponential
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_news_rss(company_name):
    company_name = company_name.replace(" ", "+")  # Replace spaces with '+' for URL encoding
    url = f'https://news.google.com/rss/search?q={company_name}&hl=en-IN&gl=IN&ceid=IN:en'
    feed = feedparser.parse(url)
    
    if not feed.entries:
        logging.warning("कोई समाचार नहीं मिला।")
        return []
    
    news_list = []
    for entry in feed.entries[:10]:
        title = entry.title
        link = entry.link
        content = entry.summary if 'summary' in entry else "कोई सामग्री उपलब्ध नहीं।"
        news_list.append({"title": title, "content": content, "link": link})
    
    return news_list

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_news_bs4(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text() for p in paragraphs])
        return content if content else "कोई सामग्री उपलब्ध नहीं।"
    except requests.RequestException as e:
        logging.error(f"वेब स्क्रैपिंग विफल: {e}")
        return ""

def translate_to_hindi(text):
    if not text.strip():
        return text  
    try:
        translated_text = GoogleTranslator(source='auto', target='hi').translate(text)
        return translated_text if translated_text else text
    except Exception as e:
        logging.error(f"अनुवाद में त्रुटि: {e}")
        return text

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)
    if sentiment_score['compound'] > 0.05:
        return "Positive"
    elif sentiment_score['compound'] < -0.05:
        return "Negative"
    else:
        return "Neutral"

def generate_tts(text):
    try:
        filename = f"tts_{int(time.time())}.mp3"
        tts = gTTS(text=text, lang='hi')
        tts.save(filename)
        return filename
    except Exception as e:
        logging.error(f"TTS त्रुटि: {e}")
        return None

def get_translated_news(company_name):
    setup_logging()
    try:
        news_articles = fetch_news_rss(company_name)
    except Exception as e:
        logging.error(f"समाचार प्राप्त करने में असफल: {e}")
        return []
    
    if not news_articles:
        return []
    
    translated_news = []
    for article in news_articles:
        full_content = fetch_news_bs4(article["link"]) if article["content"] == "कोई सामग्री उपलब्ध नहीं।" else article["content"]
        sentiment = analyze_sentiment(full_content)
        translated_title = translate_to_hindi(article["title"])
        translated_content = translate_to_hindi(full_content)
        audio_file = generate_tts(translated_content)
        
        translated_news.append({
            "title": translated_title,
            "content": translated_content,
            "link": article["link"],
            "sentiment": sentiment,
            "audio": audio_file
        })
    
    return translated_news
