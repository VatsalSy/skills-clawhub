# Stocks and Financial Data CLI

**Description:** Provides access to real-time financial data from Yahoo Finance. Handles stock prices, fundamentals, earnings, dividends, options, cryptocurrency, forex, commodities, and news using a comprehensive set of tools.

---

## AI Agent Usage

This section describes how AI agents can programmatically use the stock skill's functions.

**Prerequisites:**
*   Python 3 must be installed and accessible.
*   The `yfinance_ai` Python library must be installed in the virtual environment.

**Invocation Guidance:**

The stock skill executes a Python script (`scripts/yfinance_ai.py`) which relies on a virtual environment. The exact commands for invocation depend on your operating system and how the virtual environment and scripts are configured.

Refer to your `skill.json` file for the precise paths to the virtual environment and script directory. The `venv` field in `skill.json` specifies the virtual environment path, and the `invocation` field provides a command template.

Below is a conceptual example of how to invoke a function. You will need to adapt the paths to match your system configuration.

**Example: Fetching Apple Stock Price**

1.  **Identify Paths:**
    *   Find the path to your Python interpreter within the virtual environment (e.g., check `skill.json`'s `venv` field).
    *   Locate the `scripts` directory for this skill (e.g., relative to the skill's workspace folder).

2.  **Construct Command:**
    Use the following structure, replacing placeholder paths with your actual system paths:

    ```bash
    # Example command structure (adjust paths as needed for your OS and setup):
    # cd <path_to_skill_scripts_directory> && <path_to_venv_python> -c "
    # import asyncio, sys
    # sys.path.insert(0, '.') # Add current directory (scripts) to Python path
    # from yfinance_ai import Tools
    # t = Tools()
    # async def main():
    #     # Replace 'method' with the desired function (e.g., get_stock_price)
    #     # Replace '{args}' with function parameters (e.g., ticker='AAPL')
    #     result = await t.method({args})
    #     print(result)
    # asyncio.run(main())
    # " 2>/dev/null

    # Specific example for AAPL using placeholder paths:
    # cd /path/to/your/workspace/skills/stocks/scripts && /path/to/your/venv/stocks/bin/python3 -c "
    # import asyncio, sys
    # sys.path.insert(0, '.')
    # from yfinance_ai import Tools
    # t = Tools()
    # async def main():
    #     result = await t.get_stock_price(ticker='AAPL')
    #     print(result)
    # asyncio.run(main())
    # " 2>/dev/null
    ```

**Available Functions:**
Consult `skill.json` for a complete list of functions, parameters, and triggers. Common functions include:
*   `get_stock_price(ticker: str)`: Retrieves current stock price and key metrics.
*   `get_complete_analysis(ticker: str)`: Provides comprehensive analysis (price, fundamentals, earnings, ratings, news).
*   `compare_stocks(tickers: str)`: Compares multiple stocks side-by-side.
*   `get_crypto_price(symbol: str)`: Fetches cryptocurrency data.
*   `get_forex_rate(pair: str)`: Provides foreign exchange rates.

---

## Human User Usage

Welcome! This skill provides easy access to financial information.

**How to Use:**

Ask questions about stocks, cryptocurrencies, forex, or commodities using natural language.

Examples:
*   "What is the price of Apple stock (AAPL)?"
*   "Show me UnitedHealth Group's (UNH) analysis."
*   "Compare Google (GOOGL) and Microsoft (MSFT)."
*   "What is the current price of Bitcoin?"
*   "What is the EUR to USD exchange rate?"

The skill will interpret your request and fetch the relevant data.

**Key Features:**
*   Real-time market data
*   Company profiles and financial summaries
*   Analyst recommendations and price targets
*   Earnings information
*   Cryptocurrency, Forex, and Commodity prices

**Notes:**
*   Financial data is sourced from Yahoo Finance.
*   There may be slight delays in real-time data.
*   For technical invocation guidance, refer to the AI Agent Usage section.
