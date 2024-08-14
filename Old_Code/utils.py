from imports import *
from classes import ModernPortfolioOptimizationTheory,TickerClass, ClaudeAgent, api_key


def get_article_text (url: str) -> str:
    """Gets output from links that are in the news
    section within the articles"""



    try:
        response=  requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        article_text = ' '.join([p.get_text() for p in soup.find_all('p')])
        return article_text
    except:
        return 'Error retrieving article text'
    
def get_stock_data(ticker: str, years: int=10) -> tuple:
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days = years*365)


    stock = yf.Ticker(ticker)
    
    info = stock.info
    hist_data = stock.history(start= start_date, end = end_date)
    balance_sheet = stock.balance_sheet
    financials = stock.financials
    news = stock.news
    return info,hist_data, balance_sheet, financials, news

def get_current_price (ticker: str) -> float:
    stock= yf.Ticker(ticker)
    data = stock.history(period='1d')
    return data


def get_saudi_stock_ticker():
    stocks = pd.read_csv('Tadawul_stocks_data.csv')
    tickers_unprocessed = stocks['symbol'].drop_duplicates()
    tickers_unprocessed = tickers_unprocessed.apply(str)
    tickers = tickers_unprocessed + '.SR'
    tickers_active = [active for active in tickers if get_is_stock_active(active)]
    return tickers_active


def get_is_stock_active(ticker, days_to_check = 5):
    stock = yf.Ticker(ticker)
    data_is_listed_today = stock.history(period='1d')
    
    if data_is_listed_today.empty:
        print('Data for today is unavailable, checking for last 5 days.... \n')
        historic_data = stock.history(period = f'{days_to_check}d')
        if (historic_data.empty):
            print('Data is delisted: ', ticker,'\n\n')
            return False
        else:
            return True
        
    else: 
        return True





def get_sentiment_analysis_agent(ticker: TickerClass) -> None:
    print(f'analyzing sentiment for {ticker.name}')

    news_text = ''
    for article in ticker.news:
        article_text= get_article_text(article['link'])
        timestamp = datetime.fromtimestamp(article['providerPublishTime']).strftime('%Y-%m-%d')
        news_text += f"\n\n---\n\nDate: {timestamp}\nTitle: {article['title']}\nText: {article_text}"

    agent = ClaudeAgent(f"You are a sentiment analysis assistant. Analyze the sentiment of the given news articles for {ticker.name} and provide a summary of the overall sentiment and any notable changes over time. Be measured and discerning. You are a skeptical investor.",
                       f"News articles for {ticker.name}:\n{news_text}\n\n----\n\nProvide a summary of the overall sentiment and any notable changes over time.",
                        api_key )
    print(f'Complete Analysis for {ticker.name}')
    return agent.send_request()


def get_filtered_fundamental_analysis_graham_agent() -> None:
    ticker_list = get_saudi_stock_data_before_graham_analysis()
    
    criteria_graham = []
    for i in range(len(ticker_list)):
        
        agent = ClaudeAgent(f"""
You are tasked as an expert financial analyst to evaluate stock symbols based on Graham's criteria.
For each stock symbol provided, check if it meets Graham's investment criteria.
Output only the stock symbol if it meets the criteria; otherwise, output nothing.

Your only task is to output the symbol of the stock if it fits graham's principles and criteria, if it doesn't fit the criteria then do not output anything.
for example: if it fits, you output the stock symbol,
            if it doesn't fit you output nothing,
            do not even give an explanation, you are only to give the symbol if it fits, nothing else.
""",f"""Only output the ticker name which is the 
        symbol if it fits grahams criteria, this is the data: {ticker_list[i]}. only ouput the ticker symbol if it fits the criteria of graham principles, don't output anything else. and if it doesn't fit graham criteria, don't output anything.""",api_key)
        
        graham_filtered_tickers =agent.send_request()
        print(graham_filtered_tickers)
        criteria_graham.append(graham_filtered_tickers)
        
    print(criteria_graham)
    
    return get_saudi_stock_data_after_graham_analysis(criteria_graham)



def get_saudi_stock_data_before_graham_analysis():
    
    ticker_info_list = get_saudi_stock_ticker()
    tickers_info = []
    for ticker in ticker_info_list:
        temp_ticker_info = TickerClass(name = ticker)
        temp_ticker_info.info,temp_ticker_info.hist_data, temp_ticker_info.balance_sheet, temp_ticker_info.financials, _ = get_stock_data(ticker, years=1)

        temp_ticker_info.price =get_current_price(ticker)
        
        
        tickers_info.append(temp_ticker_info)
        
    
    
    return tickers_info



def get_saudi_stock_data_after_graham_analysis(ticker_info_list):

    tickers_info = []
    for ticker in ticker_info_list:
        temp_ticker_info = TickerClass(name = ticker)
        temp_ticker_info.info,temp_ticker_info.hist_data, temp_ticker_info.balance_sheet, temp_ticker_info.financials, temp_ticker_info.news = get_stock_data(ticker, years=1)

        temp_ticker_info.price =get_current_price(ticker)
        
        
        tickers_info.append(temp_ticker_info)
        
    
    
    return tickers_info

def get_margin_of_safety_agent(ticker: TickerClass)-> None:
    print(f'Analyzing margin of safety analysis for {ticker.name}')

        
    agent = ClaudeAgent(f"""You are an expert financial analyst assistant. Analyze the financials of the stock: {ticker.name}. 
    analyze the financials: {ticker.financials} and analyze the balance sheet: {ticker.balance_sheet}.
    Your task is to create a margin of safety analysis, by providing the calculation of NVAC (Net current asset value)
    and to calculate EPV (Earnings power value). This is the current price: {ticker.price}""",f"""Show me why this company {ticker.name} is safe to invest in, show me your statistics and output your answer
    if the company is safe to invest in or not.""",api_key)
    
    print(f'Complete analysis for {ticker.name}')

    return agent.send_request()




def get_overall_agent(ticker,sentiment_analysis, margin_of_safety_analysis):
    print(f'\nAnalyzing overall analysis for {ticker.name}')

        
    agent = ClaudeAgent(f"""You are an expert financial analyst. Analyze the given data from your fellow agents
    sentiment analysis: {sentiment_analysis}, margin of safety analysis: {margin_of_safety_analysis}.
    Tell me why you think overall that this is a good investment opportunity or not, and tell me if it is a long term investment or short term.
    You are a skeptical investor.""", f'Tell me if this stock: {ticker.name} is good to invest in or not, specify clearly.', api_key)
    
    print(f'Complete analysis for {ticker.name}\n')

    return agent.send_request()




def get_sentiment_margin_agent_outputs(tickers_info):
    for i in range(len(tickers_info)):
        tickers_info[i].sentiment_analysis_agent=get_sentiment_analysis_agent(tickers_info[i])
        tickers_info[i].margin_of_safety_analysis_agent= get_margin_of_safety_agent(tickers_info[i])
        tickers_info[i].overall_agent_analysis = get_overall_agent(tickers_info[i],tickers_info[i].sentiment_analysis_agent,
        tickers_info[i].margin_of_safety_analysis_agent)
    return tickers_info


def ranking_analysis_agent(tickers_info):
    agent = ClaudeAgent(f"""You are an expert financial analyst, rank these companies based on the given outputs from each agent,
                      sentiment_analysis_agent: found in the file,
                      margin_of_safety_analysis_agent: found in the file, overall_agent_analysis: found in the file.
                      You are a skeptical investor, rank these companies from top to bottom in terms of these given outputs
                      from each agent.
                      These are the companies and the file: {tickers_info}.
                      Rank each company and give me a summary of each agent like this:
                      -Sentiment Analysis Agent Summary:
                      -Margin of Safety Analysis Agent Summary:
                      -Overall Analysis:
                      include in the rankings that the stocks are fit in grahams criteria
                      the rankings will be based on all the results from the agents. also on each ranking give a score out of
                      100%, which the metrics are the graham agent and sentiment analysis and margin of safety analysis
                      
                      """, 'give me top 10 in the Saudi Tadawul Market investments based on all the agents', api_key)
    return agent.send_request()


def fetching_agent_from_ranking_agent(ranking_agent):
    agent= ClaudeAgent(f'You are an agent who does what he is asked to do concisely, if a user askes you to do something you do it without added words.'
                      , f'I want you to fetch the symbols of the stock in this: {ranking_agent} and put it in a list, only the stock symbols nothing else.',api_key)
    
    rankings =agent.send_request()
    list_of_rankings = ''.join(rankings)
    list_of_rankings=list_of_rankings.split()
    return list_of_rankings



def monte_carlo_portfolio_simulation(tickers, years=2, num_portfolios=10000):
    # Download stock data
    end_date = pd.Timestamp.today()
    start_date = end_date - pd.DateOffset(years=years)
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    
    # Calculate daily returns
    returns = data.pct_change().dropna()

    # Calculate mean returns and covariance
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    
    # Results storage
    results = np.zeros((3, num_portfolios))
    weight_array = np.zeros((len(tickers), num_portfolios))

    for i in range(num_portfolios):
        # Generate random weights
        weights = np.random.random(len(tickers))
        weights /= np.sum(weights)
        weight_array[:, i] = weights
        
        # Expected portfolio return
        portfolio_return = np.sum(weights * mean_returns * 252)  # Annualize the return
        # Expected portfolio volatility
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix * 252, weights)))  # Annualize the volatility
        
        # Store results
        results[0,i] = portfolio_volatility
        results[1,i] = portfolio_return
        # Store Sharpe Ratio (assuming risk-free rate = 0 for simplification)
        results[2,i] = portfolio_return / portfolio_volatility
    


        # Plotting the results
        plt.figure(figsize=(10, 6))
        plt.scatter(results[0,:], results[1,:], c=results[2,:], cmap='YlGnBu', marker='o')
        plt.colorbar(label='Sharpe Ratio')
        plt.xlabel('Volatility (Standard Deviation)')
        plt.ylabel('Expected Returns')
        plt.title('Efficient Frontier via Monte Carlo Simulation')
        plt.show()
        return results, weight_array



def mpt_agent(ticker_list, num_portfolios, risk_tolerance, years=2):
    mpt = ModernPortfolioOptimizationTheory(tickers=ticker_list, years=years ,risk_tolerance=risk_tolerance)
    
    # Fetch and calculate correlation matrix
    correlation_matrix = mpt.get_correlation_matrix()
    print('Correlation matrix:')
    print(correlation_matrix)
    
    # Plot the efficient frontier
    mpt.plot_efficient_frontier_with_tolerance(num_portfolios)
    
    # Generate and display a sample from the efficient frontier
    efficient_frontier, weights = mpt.generate_efficient_frontier(num_portfolios=10000)
    print('Efficient Frontier Sample:')
    print(efficient_frontier.head())
    
    portfolio = mpt.find_optimal_portfolio(num_portfolios)
    
    results_carlo, weights_carlo = monte_carlo_portfolio_simulation(ticker_list, years=3, num_portfolios=10000)

    # Create a portfolio summary to send to the agent
    portfolio_summary = f"""
    You are a financial analyst who excels in Modern Portfolio Theory. Here is the data you need:
    - Correlation matrix: 
    {correlation_matrix}
    - Efficient Frontier Sample:
    {efficient_frontier.head()}
    Analyze it and determine what is good for the investor.
    
    this is the optimal portfolio: {portfolio}
    
    This is also a montecarlo frontier: 
    results = {results_carlo},
    weights = {weights_carlo}.
    
    """
    # Example placeholder for agent interaction (replace with actual API interaction if applicable)
    # Assume ClaudeAgent is a class you have defined or imported that can handle such requests
    agent = ClaudeAgent(portfolio_summary, f"Advise me on allocations for each stock in {ticker_list} with a portfolio of {num_portfolios} portfolios.", api_key)
    
    return agent.send_request()


def fetching_agent_from_mpt(mpt_agent):
    
    
    agent= ClaudeAgent(f'You are an agent who does what he is asked to do concisely, if a user askes you to do something you do it without added words.'
                      , f'I want you to fetch the symbols and allocation percentage in this: {mpt_agent} and put it in a dictionary, only the stock symbols as a key and allocation as an value (make the value float, like if 10% it should be 0.1), nothing else.',api_key)
    
    allocation =agent.send_request()
    allocation = json.load(allocation)
    return allocation



def calculate_returns(data):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days = 2* 365)
    stock = yf.download(data, start = start_date, end=end_date)

    return stock.pct_change().dropna()

def calculate_beta(stock_returns, market_returns):
    market_returns = sm.add_constant(market_returns)
    model = sm.OLS(stock_returns, market_returns).fit()
    return model.params[1]



def get_systematic_risk_analysis(stock_ticker, market_ticker='^TASI'):

    stock_returns = calculate_returns(stock_ticker)
    market_returns = calculate_returns(market_ticker)

    beta = calculate_beta(stock_returns, market_returns)
    return beta

def get_unsystematic_risk(stock_returns, market_returns):
    market_returns = sm.add_constant(market_returns)
    model = sm.OLS(stock_returns, market_returns.fit())
    residuals = model.resid
    unsystematic_risk = np.var(residuals)

    return unsystematic_risk


def get_unsystematic_risk_analysis(stock_ticker, market_ticker='^TASI'):
    
    stock_returns = calculate_returns(stock_ticker)
    market_returns = calculate_returns(market_ticker)


    unsystematic_risk = get_unsystematic_risk(stock_returns, market_returns)

    return unsystematic_risk


def generate_risk_assessment_report(stock_ticker, market_ticker='^TASI',years=2):
    beta = get_systematic_risk_analysis(stock_ticker, market_ticker)
    unsystematic_risk = get_unsystematic_risk_analysis(stock_ticker, market_ticker)

    report = f"""
    Risk Assessment Report for {stock_ticker}
    ----------------------------------------
    Market: {market_ticker}
    Period: {years} year(s)

    Systematic Risk (Beta):
    {beta}

    Unsystematic Risk (Variance of Residuals):
    {unsystematic_risk}

    Interpretation:
    - A beta greater than 1 indicates the stock is more volatile than the market.
    - A beta less than 1 indicates the stock is less volatile than the market.
    - Unsystematic risk represents the risk inherent to the stock that is not correlated with the market.
    """
    return report




def get_portfolio_rebalancing_agent(portfolio, start_date, end_date):
    message = f"""
Implement portfolio tracking function
Create rebalancing threshold calculator
Develop rebalancing suggestion algorithm

Portfolio: {portfolio}
Start Date: {start_date}
End Date: {end_date}

Implement the functions and run them sequentially to track the portfolio, calculate rebalancing thresholds, and suggest rebalancing adjustments.
"""

    prompt = "You are a financial analyst assistant. The user will provide you with tasks related to portfolio management, and you will execute them efficiently."

    agent = ClaudeAgent(prompt, message,api_key)
    return agent.send_request()
























