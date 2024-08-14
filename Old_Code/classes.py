from imports import *


#Getting API Key
load_dotenv('api_key.env')
api_key = os.getenv('API_KEY')

@dataclass
class TickerClass:
    name: str
    info : Optional[str] = field(default = None)
    hist_data: Optional[pd.DataFrame] = field(default = None)
    balance_sheet: Optional[pd.DataFrame] = field(default=None)
    financials: Optional[pd.DataFrame] = field(default=None)
    news: Optional[Dict] = field(default=None)
    price: float = field(default=None)
    ######
    sentiment_analysis_agent: str = field(default=None)
    margin_of_saftey_analysis_agent: str = field (default = None)
    overall_agent_analysis: str = field(default = None)


class ClaudeAgent:
    def __init__(self, prompt,message, api_key):
        self.prompt = prompt
        self.message = message
        self.api_key = api_key
        self.headers = {
        'x-api-key': self.api_key,
        'anthropic-version' : '2023-06-01',
        'Content-Type' :'application/json'
        }
    
    def send_request(self):

        messages = [
                {'role': 'user', 'content':self.message}

            ]

        data = {
            "model": "claude-3-5-sonnet-20240620",
            "max_tokens": 3000,
            "temperature": 0.5,
            "messages": messages,
            'system' : self.prompt,
            }
        
        response = requests.post("https://api.anthropic.com/v1/messages", headers=self.headers, json=data)
    
        if response.status_code == 200:
            response_json = response.json()
            #print("Response JSON:", response_json)  # For debugging
            if 'content' in response_json and response_json['content']:
                
                if 'text' in response_json['content'][0] and response_json['content'][0]['text']:
                    return response_json['content'][0]['text']
                else:
                    return None
            else:
                return f"Error: 'content' not found in response. Response: {response_json}"
        else:
            return f"Error: Request failed with status code {response.status_code}. Response: {response.text}"
        
        


class ModernPortfolioOptimizationTheory:
    def __init__(self, tickers, years,risk_tolerance):
        self.tickers = tickers
        self.years = years
        self.risk_tolerance= risk_tolerance
        self.data = self._download_data()

    def _download_data(self):
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=self.years * 365)
        return yf.download(self.tickers, start=start_date, end=end_date)['Adj Close']

    def fetch_history(self):
        return self.data.pct_change()

    def get_covariance_matrix(self):
        return self.fetch_history().cov() * 252  # Annualizing

    def get_correlation_matrix(self):
        return self.fetch_history().corr()

    def generate_efficient_frontier(self, num_portfolios=10000):
        returns = self.fetch_history().mean() * 252
        covariance = self.get_covariance_matrix()
        num_assets = len(self.tickers)
        # Separate arrays for numerical results and weights
        results = np.zeros((num_portfolios, 3))  # Only for Volatility, Returns, Sharpe Ratio
        weights_record = []

        for i in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            weights_record.append(weights)
            portfolio_return = np.dot(weights, returns)
            portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(covariance, weights)))
            sharpe_ratio = portfolio_return / portfolio_volatility
            results[i] = [portfolio_volatility, portfolio_return, sharpe_ratio]

        return pd.DataFrame(results, columns=['Volatility', 'Returns', 'Sharpe Ratio']), weights_record
    
    def find_optimal_portfolio(self, num_portfolios):
        results, weights = self.generate_efficient_frontier(num_portfolios)
        # Utility is defined as return minus risk scaled by tolerance
        results['Utility'] = results['Returns'] - self.risk_tolerance * results['Volatility']
        max_utility_idx = results['Utility'].idxmax()
        optimal_weights = weights[max_utility_idx]
        optimal_portfolio = results.iloc[max_utility_idx]
        return optimal_portfolio, optimal_weights
    
    
    def plot_efficient_frontier_with_tolerance(self, num_portfolios):
        results, weights = self.generate_efficient_frontier(num_portfolios)
        results['Utility'] = results['Returns'] - self.risk_tolerance * results['Volatility']
        max_utility_idx = results['Utility'].idxmax()

        plt.figure(figsize=(10, 6))
        plt.scatter(results['Volatility'], results['Returns'], c=results['Sharpe Ratio'], cmap='viridis')
        plt.colorbar(label='Sharpe Ratio')
        plt.scatter(results.iloc[max_utility_idx]['Volatility'], results.iloc[max_utility_idx]['Returns'], color='red')  # Highlight optimal portfolio
        plt.xlabel('Volatility (Standard Deviation)')
        plt.ylabel('Expected Returns')
        plt.title('Efficient Frontier with Risk Tolerance')
        plt.show()




class Backtest:
    def __init__(self, portfolio, start_date, end_date):
        self.portfolio = portfolio
        self.start_date = start_date
        self.end_date = end_date
        self.data = self.get_historical_data()
        self.results = None
    
    def get_historical_data(self):
        tickers = list(self.portfolio.keys())
        data = yf.download(tickers, start=self.start_date, end=self.end_date)['Adj Close']
        return data

    def simulate_trades(self):
        initial_investment = 100000  # Example starting amount
        weights = np.array(list(self.portfolio.values()))
        self.data = self.data.pct_change().dropna()
        returns = self.data.dot(weights)
        self.results = (returns + 1).cumprod() * initial_investment
    
    def calculate_performance_metrics(self):
        if self.results is None:
            raise ValueError("Run simulate_trades() before calculating performance metrics.")
        
        total_return = self.results[-1] / self.results[0] - 1
        annualized_return = (1 + total_return) ** (252 / len(self.results)) - 1
        volatility = self.results.pct_change().std() * np.sqrt(252)
        sharpe_ratio = annualized_return / volatility
        
        rolling_max = self.results.cummax()
        daily_drawdown = self.results / rolling_max - 1.0
        max_drawdown = daily_drawdown.cummin().min()
        
        performance = {
            "Total Return": total_return,
            "Annualized Return": annualized_return,
            "Volatility": volatility,
            "Sharpe Ratio": sharpe_ratio,
            "Max Drawdown": max_drawdown
        }
        
        return performance



