from utils import *
from classes import *
from imports import *

def run_backend_analysis():
    filtered_graham_saudi_stocks = get_filtered_fundamental_analysis_graham_agent()
    saudi_stock_data = get_sentiment_margin_agent_outputs(filtered_graham_saudi_stocks)
    rankings = ranking_analysis_agent(saudi_stock_data)

    ranking_list = fetching_agent_from_ranking_agent(rankings)
    portfolio = mpt_agent(ranking_list,10000,0.01)

    fetch_allocation_recommendation = fetching_agent_from_mpt(portfolio)
    allocation_recommendation_to_json = json.loads(fetch_allocation_recommendation)


    end_date = datetime.now().date()
    start_date = end_date-timedelta(days=3* 365)
    backtest = Backtest(allocation_recommendation_to_json,start_date, end_date )
    backtest.simulate_trades()
    performance_metrics = backtest.calculate_performance_metrics()
    print(performance_metrics)

def streamlit_run():
    

    return None