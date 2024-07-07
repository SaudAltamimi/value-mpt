
<p align="center">
  <img src="docs/images/technology-disruption.svg" width="200" title="Technology Disruption">
</p>

# ValueMPT: Value Stock Selection with MPT Portfolio Optimization

ValueMPT is an intelligent multi-agent system that combines Benjamin Graham's value investing principles for stock selection with Modern Portfolio Theory (MPT) for portfolio optimization.

## Project Overview

This system implements a two-stage approach to investment:

1. Stock selection using Graham's value investing principles
2. Portfolio optimization of selected stocks using Modern Portfolio Theory

The system consists of several AI agents working in two main phases:

### Phase 1: Value Stock Selection
1. Fundamental Analysis Agent
2. Margin of Safety Calculator
3. Market Sentiment Analyzer

### Phase 2: Portfolio Optimization
1. Modern Portfolio Theory Optimization Agent
2. Risk Management Agent
3. Portfolio Rebalancing Agent

## Features

- Fundamental stock analysis using key financial ratios
- Margin of safety calculations for potential investments
- Market sentiment analysis for contrarian opportunities
- Portfolio optimization based on MPT principles
- Risk assessment and management
- Automated portfolio rebalancing suggestions


## To-Do List

### Phase 1: Value Stock Selection
- [ ] Implement data fetching and preprocessing for financial ratios
- [ ] Develop Fundamental Analysis Agent
  - [ ] Implement ratio calculations (P/E, P/B, Debt-to-Equity, ROE, etc.)
  - [ ] Create stock screening based on Graham's criteria
- [ ] Create Margin of Safety Calculator
  - [ ] Implement intrinsic value estimation
  - [ ] Develop margin of safety calculation
- [ ] Implement Market Sentiment Analyzer
  - [ ] Develop sentiment analysis algorithm
  - [ ] Create contrarian opportunity identifier

### Phase 2: Portfolio Optimization
- [ ] Develop Modern Portfolio Theory Optimization Agent
  - [ ] Implement expected return and standard deviation calculations
  - [ ] Create efficient frontier generator
  - [ ] Develop optimal portfolio selector
- [ ] Implement Risk Management Agent
  - [ ] Develop systematic risk analysis
  - [ ] Implement unsystematic risk identification
- [ ] Develop Portfolio Rebalancing Agent
  - [ ] Implement portfolio tracking
  - [ ] Create rebalancing suggestion algorithm

### General Tasks
- [ ] Set up project structure and environment 
- [ ] Integrate all agents into a cohesive system [multi-agent-workflows](https://blog.langchain.dev/langgraph-multi-agent-workflows/)
- [ ] Develop user interface for interacting with the system [chainlit](https://docs.chainlit.io/)
- [ ] Write comprehensive documentation [mkdocs](https://www.mkdocs.org/)
- [ ] Implement unit tests and integration tests
- [ ] Perform system testing and optimization
- [ ] Create user guide and API documentation [fastapi](https://fastapi.tiangolo.com/#interactive-api-docs)

## Disclaimer

This project is for educational purposes only. It is not financial advice. Always conduct your own research and consult with a qualified financial advisor before making investment decisions.

## Approach

1. The Value Stock Selection phase uses Graham's principles to identify fundamentally sound, potentially undervalued stocks.
2. The Portfolio Optimization phase then applies MPT to optimize the allocation among these selected stocks for a given risk tolerance.

This approach aims to combine the strengths of value investing in stock selection with the portfolio-level insights of MPT, providing a more robust investment strategy.
