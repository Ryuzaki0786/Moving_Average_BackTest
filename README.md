# Moving_Average_BackTest

# Moving Average Backtesting App

This Streamlit application allows users to perform a simple moving average crossover backtest on any stock using historical price data fetched via Yahoo Finance. The app generates buy/sell signals based on short-term and long-term moving average crossover strategy and visualizes both the signals and the resulting equity curve.

---

## Features

- Input any stock ticker (e.g., AAPL, TSLA, INFY, etc.)
- Select custom date range for historical data
- Adjust short-term and long-term moving averages via sliders
- Input starting capital to simulate your portfolio
- View:
  - Price chart with MA crossovers
  - Buy/Sell signals
  - Simulated equity curve
  - Recent output data in a table

---

## Requirements

Install all required packages using:

```bash
pip install -r requirements.txt

## License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

##Acknowledgements
- This project served as a practical deep-dive into quantitative finance and technical indicators.
- Conceptual Learning: I utilized ChatGPT and Claude as instructional tools to bridge the gap between financial theory (specifically Short vs. Long Moving Averages) and implementation logic.
- Development: While AI assisted with debugging and optimization, I manually wrote the core backtesting engine to ensure a first-principles understanding of the code.
- Transparency & Reproducibility: I have included detailed documentation and inline comments at every crucial step. This ensures the project is easy to follow, reproducible for other developers, and serves as a clear foundation for my future quantitative work.


