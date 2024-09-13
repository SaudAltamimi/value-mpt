from typing import Tuple
import pandas as pd
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import yfinance as yf




class FinancialData:
    """
    A class to represent financial data for a stock.

    Attributes:
        ticker (str): The stock ticker symbol.
        info (dict): Stock info
        balance_sheet (pd.DataFrame): Balance sheet data.
        income_statement (pd.DataFrame): Income statement data.
        cash_flow (pd.DataFrame): Cash flow statement data.
        dividends (pd.DataFrame): dividends of stock
        news (str): The stock news period of three months max.

    """

    def __init__(self, ticker: str):
        """
        Initialize FinancialData with a stock ticker.

        Args:
            ticker (str): The stock ticker symbol.
        """
        
        
        
        self.ticker = ticker
        self.balance_sheet,self.income_statement, self.cash_flow, self.info, self.dividends = self._get_financial_data()
        self.news = self._get_financial_news()
        


    def _get_financial_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Fetch financial data from Yahoo Finance.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Balance sheet, income statement, and cash flow data.
        """
        stock = yf.Ticker(self.ticker)
        
        return stock.balance_sheet, stock.financials, stock.cashflow, stock.info, stock.dividends
    

    
    def _get_financial_news(self):
        """Fetch financial news from Yahoo Finance, filtered from the last 3 months.
        
        Returns:
        str: news_text
        """
        
        
        
        stock = yf.Ticker(self.ticker)
        stock_links = stock.news
        
        current_time = datetime.now()
        three_months_ago = current_time - timedelta(days=90)
        
        filtered_news = [news for news in stock_links if datetime.fromtimestamp(news['providerPublishTime']) >= three_months_ago]
        news_text=''
        for news in filtered_news:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                response = requests.get(news['link'], headers=headers)
                if response.status_code == 200:
                    timestamp = datetime.fromtimestamp(news['providerPublishTime']).strftime('%Y-%m-%d')
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_text = ' '.join([p.get_text() for p in soup.find_all('p')])
                    news_text += f"\n\n---\n\nDate: {timestamp}\nTitle: {news['title']}\nText: {article_text}"

                    
                

        return news_text
        