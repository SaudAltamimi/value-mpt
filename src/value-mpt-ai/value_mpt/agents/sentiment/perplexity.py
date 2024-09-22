import requests
import os

class PerplexitySentimentAnalyzer:
    def __init__(self):
        self.api_key = os.environ.get("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY environment variable not set")
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def analyze_sentiment(self, stock_symbol):
        prompt = f"Analyze the current market sentiment for the stock {stock_symbol}. Provide a brief summary and categorize the sentiment as positive, negative, or neutral. Base your analysis on recent news, financial reports, and market trends."

        data = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {"role": "system", "content": "You are a financial analyst specializing in stock market sentiment analysis."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(self.base_url, headers=self.headers, json=data)
        response.raise_for_status()

        result = response.json()
        sentiment_analysis = result['choices'][0]['message']['content']

        return sentiment_analysis

    def extract_sentiment_category(self, analysis):
        lower_analysis = analysis.lower()
        if "positive" in lower_analysis:
            return "Positive"
        elif "negative" in lower_analysis:
            return "Negative"
        else:
            return "Neutral"

if __name__ == "__main__":
    analyzer = PerplexitySentimentAnalyzer()
    
    stock_symbol = input("Enter the stock symbol to analyze: ")
    
    try:
        sentiment_analysis = analyzer.analyze_sentiment(stock_symbol)
        sentiment_category = analyzer.extract_sentiment_category(sentiment_analysis)
        
        print(f"\nSentiment Analysis for {stock_symbol}:")
        print(sentiment_analysis)
        print(f"\nOverall Sentiment: {sentiment_category}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")