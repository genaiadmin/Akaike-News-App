from fastapi import FastAPI
from news_scraper import get_news
from sentiment_analysis import analyze_sentiment
from comparative_analysis import generate_sentiment_report
from hindi_tts import generate_hindi_tts
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class NewsRequest(BaseModel):
    company: str

@app.get("/")
def home():
    return {"message": "Welcome to the News Sentiment API"}

@app.post("/get_news")
def fetch_news(request: NewsRequest):
    news = get_news(request.company)
    return {"articles": news}

@app.post("/analyze_sentiment")
def sentiment_analysis(request: NewsRequest):
    news = get_news(request.company)
    sentiment_report = generate_sentiment_report(news)
    return {"sentiment_report": sentiment_report}

@app.post("/generate_tts")
def generate_hindi_audio(request: NewsRequest):
    news = get_news(request.company)
    sentiment_report = generate_sentiment_report(news)
    generate_hindi_tts(sentiment_report)
    return {"message": "Hindi TTS generated!", "audio_file": "hindi_output.mp3"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
