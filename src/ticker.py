import yfinance as yf

class Ticker:
    def __init__(self, tickers, years):
        self.tickers = tickers
        self.years = years
        self.data = self.download_data()

    def download_data(self):
        data = yf.download(self.tickers, period=f'{self.years}y')
        return data

    def get_returns(self):
        if 'Adj Close' in self.data.columns:
            data = self.data['Adj Close']
        else:
            data = self.data['Close']
        returns = data.pct_change().dropna()
        return returns