from imports import *
from classes import RiskAnalyzer, stock_ticker, market_ticker

# Generate risk assessment report
def generate_report():
    analyzer = RiskAnalyzer(stock_ticker, market_ticker)
    beta = analyzer.calculate_beta()
    systematic_risk = analyzer.calculate_systematic_risk()
    unsystematic_risk = analyzer.calculate_unsystematic_risk()

    report = (
        f"""
    Risk Assessment Report
    ----------------------
    Date: {datetime.now().strftime('%Y-%m-%d')}
    
    Stock: {stock_ticker}
    Market Index: {market_ticker}
    
    Beta: {beta:.4f}
    Systematic Risk: {systematic_risk:.7f}
    Unsystematic Risk: {unsystematic_risk:.7f}
    
    Summary:
    - The beta value of {beta:.4f} indicates that the stock is {'more' if beta > 1 else 'less'} volatile compared to the market.
    - Systematic risk represents the risk that cannot be diversified away, influenced by market factors.
    - Unsystematic risk, at {unsystematic_risk:.4f}, is the portion of risk specific to {stock_ticker}, which can be mitigated through diversification.
    """
    )
    return report


report = generate_report()
print(report)