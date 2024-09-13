from src.agents.api.api import ClaudeAgent


def sentiment_analysis(self):
        
        ticker = self.financial_data
        news_text = ticker.news
        agent = ClaudeAgent(f"You are a sentiment analysis assistant. Analyze the sentiment of the given news articles for {ticker.name} and provide a summary of the overall sentiment and any notable changes over time. Be measured and discerning. You are a skeptical investor.",
                       f"News articles for {ticker.name}:\n{news_text}\n\n----\n\nProvide a summary of the overall sentiment and any notable changes over time. give me a score in percentage wise on how good the news is looking and why."
                         )
        print(f'Complete Analysis for {ticker.name}')
        return agent.send_request()
    
    