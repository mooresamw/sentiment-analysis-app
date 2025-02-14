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
    # filtered_url_list = [url for url in df['Url'].tolist() if "finance.yahoo" in url]
    # filtered_urls = df[df['Url'].str.contains("finance.yahoo", na=False)]
    # filtered_ticker_list = []
    # for url, ticker in zip(filtered_urls['Url'], filtered_urls['Ticker']):
    #     filtered_ticker_list.append(ticker)

    print("Retrieved Columns:", df.columns.tolist())
    print("First few rows:\n", df.head())
    #return filtered_url_list, filtered_ticker_list
    expected_columns = {"Url", "Ticker", "Date", "Category"}
    if not expected_columns.issubset(df.columns):
        raise KeyError("One or more expected columns are missing. Check API Key.")

    # Filter only finance.yahoo articles
    filtered_df = df[df["Url"].str.contains("finance.yahoo", na=False)]

    # Extract individual lists
    urls = filtered_df["Url"].tolist()
    tickers = filtered_df["Ticker"].tolist()
    dates = filtered_df["Date"].tolist()
    categories = filtered_df["Category"].tolist()

    return urls, tickers, dates, categories
