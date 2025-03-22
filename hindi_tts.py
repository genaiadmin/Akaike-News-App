from gtts import gTTS
import os

def generate_hindi_tts(sentiment_report):
    """Converts sentiment report into Hindi speech and saves it as an MP3 file."""
    
    # Convert sentiment report into Hindi text
    text = f""" 
    नमस्ते! यहाँ आपकी समाचार भावना विश्लेषण रिपोर्ट है:
    सकारात्मक समाचारों की संख्या: {sentiment_report['Positive']}
    नकारात्मक समाचारों की संख्या: {sentiment_report['Negative']}
    तटस्थ समाचारों की संख्या: {sentiment_report['Neutral']}
    कुल समाचार लेखों की संख्या: {sentiment_report['Total Articles']}
    समग्र भावना: {sentiment_report['Overall Sentiment']}
    धन्यवाद!
    """

    # Generate speech
    tts = gTTS(text=text, lang="hi")
    tts.save("sentiment_report.mp3")
    
    print("✅ हिंदी टेक्स्ट-टू-स्पीच फ़ाइल 'sentiment_report.mp3' बना दी गई है!")

# Test function
if __name__ == "__main__":
    sample_report = {
        "Positive": 3,
        "Negative": 2,
        "Neutral": 5,
        "Total Articles": 10,
        "Overall Sentiment": "Balanced Sentiment"
    }
    
    generate_hindi_tts(sample_report)
    
    # Play the generated speech file (works in Colab)
    os.system("mpg321 sentiment_report.mp3")  # Works in some systems
