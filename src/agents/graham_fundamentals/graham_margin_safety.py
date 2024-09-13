from typing import Dict
import yfinance as yf
from src.data.data_extraction.fetching_data_module import FinancialData

class ValuationMetrics:
    """
    A class to calculate various valuation metrics for a stock.

    Attributes:
        financial_data (FinancialData): Financial data for the stock.
    """

    def __init__(self, financial_data: FinancialData):
        """
        Initialize ValuationMetrics with financial data.

        Args:
            financial_data (FinancialData): Financial data for the stock.
        """
        self.financial_data = financial_data
        self.current_assets = self.financial_data.balance_sheet.loc['Current Assets'].iloc[0]
        self.total_liabilities = self.financial_data.balance_sheet.loc['Total Liabilities Net Minority Interest'].iloc[0]
    
    def calculate_ncav(self) -> float:
        """
        Calculate Net Current Asset Value (NCAV).

        Returns:
            float: The calculated NCAV.
        """
        
        return (self.current_assets - self.total_liabilities)

    def calculate_epv(self, wacc: float = 0.10) -> float:
        """
        Calculate Earnings Power Value (EPV).

        Args:
            wacc (float): Weighted Average Cost of Capital. Defaults to 0.10.

        Returns:
            float: The calculated EPV.
        """
        income_statement = self.financial_data.income_statement
        cash_flow = self.financial_data.cash_flow

        # Calculate average EBIT margin
        ebit = income_statement.loc['EBIT']
        revenue = income_statement.loc['Total Revenue']
        ebit_margins = ebit / revenue
        avg_ebit_margin = ebit_margins.mean()

        # Normalize EBIT
        current_revenue = revenue.iloc[0]
        normalized_ebit = current_revenue * avg_ebit_margin

        # Calculate after-tax normalized EBIT
        tax_rate = income_statement.loc['Tax Provision'].iloc[0] / income_statement.loc['Pretax Income'].iloc[0]
        after_tax_normalized_ebit = normalized_ebit * (1 - tax_rate)

        # Adjust for depreciation
        avg_depreciation = cash_flow.loc['Depreciation'].mean()
        adjusted_depreciation = 0.5 * tax_rate * avg_depreciation

        # Calculate maintenance capex
        capex = cash_flow.loc['Capital Expenditure'].abs()
        income_growth_rate = income_statement.loc['Net Income'].pct_change().mean()
        maintenance_capex = capex.mean() * (1 - income_growth_rate)

        # Calculate adjusted earnings
        adjusted_earnings = after_tax_normalized_ebit + adjusted_depreciation - maintenance_capex

        return adjusted_earnings / wacc

    @staticmethod
    def calculate_margin_of_safety(intrinsic_value: float, current_price: float) -> float:
        """
        Calculate Margin of Safety.

        Args:
            intrinsic_value (float): The estimated intrinsic value of the stock.
            current_price (float): The current market price of the stock.

        Returns:
            float: The calculated Margin of Safety.
        """
        return ((intrinsic_value - current_price)/intrinsic_value) 
    

class StockAnalyzer:
    """
    A class to analyze a stock using various valuation metrics.

    Attributes:
        ticker (str): The stock ticker symbol.
        financial_data (FinancialData): Financial data for the stock.
        valuation_metrics (ValuationMetrics): Valuation metrics calculator for the stock.
    """

    def __init__(self, ticker: str):
        """
        Initialize StockAnalyzer with a stock ticker.

        Args:
            ticker (str): The stock ticker symbol.
        """
        self.ticker = ticker
        self.financial_data = FinancialData(ticker)
        self.valuation_metrics = ValuationMetrics(self.financial_data)
    
    
    def margin_of_safety(self) -> Dict[str,float]:
        """ 
            Perform margin of safety calculation for stocks
        
            Returns calculation of margin of safety
            
        """
        stock = yf.Ticker(self.ticker)
        current_price = stock.info['currentPrice']
        shares_outstanding = stock.info['sharesOutstanding']

        ncav = self.valuation_metrics.calculate_ncav()
        epv = self.valuation_metrics.calculate_epv()

        ncav_per_share = ncav / shares_outstanding
        epv_per_share = epv / shares_outstanding
        
        #Margin of safety

        mos_ncav = self.valuation_metrics.calculate_margin_of_safety(ncav_per_share, current_price)
        mos_epv = self.valuation_metrics.calculate_margin_of_safety(epv_per_share, current_price)
        
        
        return {
            'current_price': current_price,
            'ncav_per_share': ncav_per_share,
            'epv_per_share': epv_per_share,
            'mos_ncav': mos_ncav,
            'mos_epv': mos_epv
            
        }
    
    
    
    def check_graham_criteria_analysis(self):
        """
         Checks if stock fits graham's criteria to undervalued stocks.
         
         
         Returns: dict
        """
        stock = self.financial_data
        info = stock.info
        financials = stock.income_statement
        dividends = stock.dividends
        
        valuation_metrics_stock = self.valuation_metrics
        current_assets = valuation_metrics_stock.current_assets
        current_liabilities = valuation_metrics_stock.total_liabilities
        
        
        current_ratio = current_assets / current_liabilities if current_liabilities else float('inf')
        debt_to_equity = info.get('debtToEquity')
        earnings_stability = (financials.loc['Net Income'].fillna(0) > 0).sum() >=5
        pe_ratio = info.get('trailingPE', float('inf'))
        pb_ratio = info.get('priceToBook',float('inf'))
        
        
        return {
            
            'strong_financial_condition': current_ratio > 1.5 and debt_to_equity < 0.5,
            'earnings': earnings_stability,
            'dividend_record': len(dividends) >=5,
            'moderate_pe_ratio': pe_ratio<15,
            'moderate_pb_ratio': pb_ratio < 1.5
        }
       
    
    
    

    def print_analysis(self):
        """
        Print the stock analysis results.
        """
        
        margin_of_safety = self.margin_of_safety()
        graham_check = self.check_graham_criteria_analysis()
        
        
        print(f"Analysis for {self.ticker}:")
        print(f"\tGraham analysis: ")
        print(f"\t\tStrong Financial Conditions?: {graham_check['strong_financial_condition']}")
        print(f"\t\tEarnings are stable?: {graham_check['earnings']}")
        print(f"\t\tDividend more than 20 years?: {graham_check['dividend_record']}")
        print(f"\t\tModerate Price to equity Ratio?: {graham_check['moderate_pe_ratio']}")
        print(f"\t\tModerate Price to Book Ratio?: {graham_check['moderate_pb_ratio']}")
        
        print('\n\tMargin of Safety: ')
        print(f"\t\tCurrent price of stock: {margin_of_safety['current_price']}")
        print(f"\t\tNet Current Asset Value Per Share: {margin_of_safety['ncav_per_share']}")
        print(f"\t\tEarnings Power Value Per Share: {margin_of_safety['epv_per_share']}")
        print(f"\t\tMargin of Safety (NCAV): {margin_of_safety['mos_ncav']} ")
        print(f"\t\tMargin of Safety (EPV): {margin_of_safety['mos_epv']}")
