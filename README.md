# Real-Time Sales & Business Analytics Dashboard

A beginner-friendly, portfolio-ready sales analytics app built with Python, Pandas, Streamlit, and Plotly.

## Features
- Upload a sales CSV and refresh dashboard results from the uploaded file
- KPI cards: revenue, profit, orders, average order value, profit margin
- Date, region, and category filters
- Monthly trends, category comparison, top products, and regional performance
- Cleaned data preview and downloadable filtered results
- Sample dataset included

> The included sample dataset is synthetic. This is a refreshable dashboard, not a live production feed. To call it truly real-time, connect an authorized business API/database and configure scheduled or event-driven refresh.

## Run on Windows 11
1. Install Python 3.11+ from https://www.python.org/downloads/ and select **Add Python to PATH** during installation.
2. Extract this ZIP folder.
3. Open the extracted folder in File Explorer.
4. Click the address bar, type `cmd`, and press Enter.
5. Run:

```bash
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

The dashboard should open in your browser. If it does not, open the local URL printed in the terminal.

## CSV format
Required columns (headers can be in upper/lower case; spaces are converted to underscores):
- `order_date` (YYYY-MM-DD)
- `order_id`
- `product`
- `category`
- `region`
- `quantity`
- `unit_price`
- `unit_cost`

See `sample_sales.csv` for an example.

## Suggested next improvements
1. Connect a real database (PostgreSQL/MySQL/SQL Server) with read-only credentials.
2. Add scheduled refresh or a live API integration.
3. Add SQL queries and tests for data quality.
4. Deploy to Streamlit Community Cloud using a public GitHub repository and `requirements.txt`.

## Resume bullet
**Sales & Business Analytics Dashboard | Python, Pandas, Streamlit, Plotly**
- Built an interactive sales dashboard with CSV ingestion, data cleaning, KPI calculations, date/region/category filters, and downloadable reports.
- Visualized monthly revenue, profit, category performance, top products, and regional trends to support data-driven business decisions.

Only claim live API/database integration after you implement and test it.
