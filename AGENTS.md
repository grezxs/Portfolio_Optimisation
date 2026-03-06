# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a collection of 3 standalone Python scripts for stock analysis and Markowitz portfolio optimization targeting the Indonesian stock market (Jakarta Stock Exchange, `.JK` tickers). There are no web services, databases, or test suites.

### Scripts

| Script | Purpose | Interactive Inputs |
|---|---|---|
| `Portfolio Optimisation.py` | Markowitz optimal portfolio (Sharpe ratio maximization) | Tickers, time horizon, risk-free rate |
| `Stock Cumulative Returns.py` | Cumulative log-return plotting | Time horizon, tickers |
| `Alpha Beta.py` | OLS regression for alpha/beta across ~90 financial stocks, exports to Excel | None (hardcoded tickers) |

### Running scripts

All scripts use `input()` for interactive prompts. To run non-interactively, pipe inputs:
```
echo -e "BBCA,BBRI,BMRI\n1\n0.05" | python3 "Portfolio Optimisation.py"
echo -e "1\nBBCA,BBRI" | MPLBACKEND=Agg python3 "Stock Cumulative Returns.py"
MPLBACKEND=Agg python3 "Alpha Beta.py"
```

Use `MPLBACKEND=Agg` for scripts that call `plt.show()` in headless environments.

### Known compatibility gotchas

- **yfinance `Adj Close` removal**: yfinance >= 0.2.43 defaults to `auto_adjust=True`, removing the `Adj Close` column. A `usercustomize.py` monkey-patch in user site-packages sets `auto_adjust=False` and `multi_level_index=False` by default so the scripts work unchanged with yfinance 1.x.
- **pandas_datareader**: Imported in `Stock Cumulative Returns.py` but never used. Requires pandas < 3.0 (currently pinned to 2.2.x) for a compatible `deprecate_kwarg` API.
- **Hardcoded output path in `Alpha Beta.py`**: Line 75 writes to `/Users/gracechandra/Documents/Python for Finance_Learning`. This directory must exist; in the cloud VM it is created via `sudo mkdir -p`.
- **No requirements.txt**: Dependencies are inferred from imports. The update script installs them explicitly.
- **No automated tests or linter configuration** exist in the repository.
