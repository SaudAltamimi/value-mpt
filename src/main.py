import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from MPT import calculate_expected_return, calculate_standard_deviation, calculate_correlation_matrix, generate_efficient_frontier, optimal_portfolio_selector

# Load data
df = pd.read_csv('../data/stocks.csv')
df.dropna(inplace=True)
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)


daily_returns = df.pct_change().dropna()
expected_annual_returns = calculate_expected_return(daily_returns)
cov_matrix = daily_returns.cov() * 252

# Calculate Standard Deviation
annualized_std_dev = calculate_standard_deviation(daily_returns)
print("Annualized Standard Deviations:")
print(annualized_std_dev)

# Calculate Correlation Matrix
correlation_matrix = calculate_correlation_matrix(daily_returns)
print("Correlation Matrix:")
print(correlation_matrix)

# Generate Efficient Frontier
returns, risks = generate_efficient_frontier(expected_annual_returns.values, cov_matrix)

# Plot Efficient Frontier
plt.figure(figsize=(10, 7))
plt.plot(risks, returns, marker='o', linestyle='-')
plt.title('Efficient Frontier')
plt.xlabel('Volatility (Risk)')
plt.ylabel('Return')
plt.grid(True)
plt.show()


# Implement Optimal Portfolio Selector
risk_tolerance = 1  # 1 being the highest risk tolerance
optimal_weights = optimal_portfolio_selector(expected_annual_returns.values, cov_matrix, risk_tolerance)

# Display the optimal weights with stock names
stock_names = daily_returns.columns
optimal_weights_with_names = dict(zip(stock_names, optimal_weights))
print(optimal_weights_with_names)

max_weight_stock = max(optimal_weights_with_names, key=optimal_weights_with_names.get)
print(f"The most optimal stock with the highest weight is: {max_weight_stock}")