# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a collection of three standalone Python scripts for Markowitz Portfolio Optimisation targeting Jakarta Stock Exchange (IDX) tickers. There are no services, databases, or build systems — just Python scripts run from the command line.

**Scripts:**
- `Portfolio Optimisation.py` — Mean-variance optimisation (maximises Sharpe ratio via `scipy.optimize.minimize`)
- `Stock Cumulative Returns.py` — Downloads historical prices and plots cumulative log returns
- `Alpha Beta.py` — Computes alpha/beta via OLS regression for ~100 IDX financial-sector stocks, exports to Excel

### Dependencies

Install with: `pip install yfinance pandas numpy scipy matplotlib statsmodels pandas_datareader openpyxl`

### Known issues

1. **yfinance API changes:** The scripts were written for an older yfinance version that returned flat DataFrame columns with an `Adj Close` field. Modern yfinance (>=0.2.44) returns a MultiIndex DataFrame and defaults `auto_adjust=True` (removing `Adj Close`). To get the original behavior, pass `auto_adjust=False, multi_level_index=False` to `yf.download()`.
2. **pandas_datareader incompatibility:** `pandas_datareader` 0.10.0 is incompatible with pandas >= 2.0 (broken `deprecate_kwarg` import). The import in `Stock Cumulative Returns.py` will fail at runtime. The library is imported but never actually used — `yf.download()` handles all data fetching.
3. **Hardcoded output path:** `Alpha Beta.py` writes to `/Users/gracechandra/Documents/Python for Finance_Learning/`. Change this path before running.
4. **Interactive input:** All scripts use `input()` prompts. For non-interactive execution, pipe input via stdin (e.g., `echo -e "BBCA,BBRI\n3\n0.06" | python3 "Portfolio Optimisation.py"`).
5. **Yahoo Finance rate limiting:** Rapid successive calls to `yf.download()` may trigger rate limiting. Add delays between runs if needed.

### Running scripts

Since scripts use `input()`, they require interactive terminal or piped stdin. Use `matplotlib.use('Agg')` backend or `MPLBACKEND=Agg` env var when running headless (no display server).

### Linting / Testing

There are no test suites, linters, or build tools configured in this repository.
