import pandas as pd
import numpy as np
import cvxpy as cp

def calculate_expected_return(daily_returns):
    return daily_returns.mean() * 252

def calculate_standard_deviation(daily_returns):
    return daily_returns.std() * np.sqrt(252)

def calculate_correlation_matrix(daily_returns):
    return daily_returns.corr()

def generate_efficient_frontier(expected_returns, cov_matrix, num_points=100):
    num_assets = len(expected_returns)
    returns = np.linspace(expected_returns.min(), expected_returns.max(), num_points)
    risks = []

    for return_target in returns:
        weights = cp.Variable(num_assets)
        portfolio_return = expected_returns @ weights
        portfolio_variance = cp.quad_form(weights, cov_matrix)
        objective = cp.Minimize(portfolio_variance)
        constraints = [cp.sum(weights) == 1, weights >= 0, portfolio_return >= return_target]
        problem = cp.Problem(objective, constraints)
        problem.solve()
        risks.append(np.sqrt(portfolio_variance.value))

    return returns, risks

def optimal_portfolio_selector(expected_returns, cov_matrix, risk_tolerance):
    num_assets = len(expected_returns)
    weights = cp.Variable(num_assets)
    portfolio_return = expected_returns @ weights
    portfolio_variance = cp.quad_form(weights, cov_matrix)
    objective = cp.Maximize(portfolio_return - risk_tolerance * portfolio_variance)
    constraints = [cp.sum(weights) == 1, weights >= 0]
    problem = cp.Problem(objective, constraints)
    problem.solve()
    
    return weights.value