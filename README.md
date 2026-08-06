# SPY Implied Volatility (IV) Surface Visualizer

A Python application that fetches real-time SPY (S&P 500 ETF) option chain data from Yahoo Finance, processes Out-of-The-Money (OTM) option implied volatilities across various expiration dates, and renders a dynamic 3D Implied Volatility Surface using SciPy grid interpolation and Matplotlib.

---

## 📌 Features

- **Real-Time Market Data**: Retrieves option chains directly from Yahoo Finance via the `yfinance` API.
- **OTM Volatility Filtering**: Constructs a true volatility surface by dynamically selecting Out-of-the-Money (OTM) options relative to current spot price:
  - **Puts** for strikes below current spot price ($0.95 \times \text{Spot}$).
  - **Calls** for strikes above current spot price ($1.20 \times \text{Spot}$).
- **Targeted Expiration Window**: Filters for short-to-mid term expirations ($10 < \text{DTE} \le 60$ days) to capture the most liquid section of the volatility curve.
- **Efficient Chain Batching**: Caches full option chains per expiration date to minimize redundant network calls.
- **3D Grid Interpolation**: Leverages `scipy.interpolate.griddata` with linear interpolation to convert irregularly sampled market data into a clean 3D surface mesh.
- **Dark-Theme Visualization**: High-contrast dark background (`#0b0d0f`) styling rendered with Matplotlib's `magma` colormap.

---

## 🛠️ Prerequisites & Installation

Ensure you have Python 3.8 or higher installed on your system.

Install the required dependencies via `pip`:

```bash
pip install yfinance matplotlib numpy scipy
