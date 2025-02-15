import requests
import pandas as pd
import io


def retrieve_news_articles(FINVIZ_API_KEY):
    url = f"https://elite.finviz.com/news_export.ashx?v=3&auth={FINVIZ_API_KEY}"
    response = requests.get(url)
    data = io.StringIO(response.text)
    df = pd.read_csv(data)

    # If we are getting a key error for 'Url', then it is most likely an issue with the api key.
    # In this case generate new api key.

    # print("Retrieved Columns:", df.columns.tolist())
    # print("First few rows:\n", df.head())
    expected_columns = {"Title", "Url", "Ticker", "Date", "Category"}
    if not expected_columns.issubset(df.columns):
        raise KeyError("One or more expected columns are missing. Check API Key.")

    # Filter only finance.yahoo articles
    filtered_df = df[df["Url"].str.contains("finance.yahoo", na=False)]

    # Extract individual lists
    titles = filtered_df["Title"].tolist()
    urls = filtered_df["Url"].tolist()
    tickers = filtered_df["Ticker"].tolist()
    dates = filtered_df["Date"].tolist()
    categories = filtered_df["Category"].tolist()

    return titles, urls, tickers, dates, categories
