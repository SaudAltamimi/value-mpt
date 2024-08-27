import numpy as np
import cvxpy as cp
from valuempt.src.value_mpt.data.ticker import Ticker


class Optimizer:
    def __init__(self, tickers, years, risk_tolerance):
        self.tickers = tickers
        self.years = years
        self.risk_tolerance = risk_tolerance
        self.ticker_data = Ticker(tickers, years)
        self.returns = self.ticker_data.get_returns().mean() * 252
        self.cov_matrix = self.ticker_data.get_returns().cov() * 252

    def optimal_portfolio_selector(self):
        num_assets = len(self.tickers)
        returns = self.returns.values
        cov_matrix = self.cov_matrix.values

        # Define the optimization variables
        weights = cp.Variable(num_assets)
        portfolio_return = cp.sum(cp.multiply(returns, weights))
        portfolio_risk = cp.quad_form(weights, cov_matrix)

        # The sum of the first two weights is less than or equal to 0.6
        constraints = [cp.sum(weights) == 1, weights >= 0, cp.sum(weights[:2]) <= 0.6]

        # To encourage diversification in the portfolio
        regularization = cp.sum_squares(weights - (1 / num_assets))

        # # Objective function, maximize return while minimizing risk and encouraging diversification (After testing 0.5 was the closest to the optimal)
        objective = cp.Maximize(portfolio_return - self.risk_tolerance * portfolio_risk - 0.5 * regularization)


        prob = cp.Problem(objective, constraints)
        prob.solve()

        optimal_weights = weights.value
        optimal_return = portfolio_return.value
        optimal_risk = np.sqrt(portfolio_risk.value)

        return optimal_return, optimal_weights, optimal_risk
    

    def get_returns(self):
        return self.returns
    
    def get_cov_matrix(self):
        return self.cov_matrix