import os

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
    filtered_url_list = [url for url in df['Url'].tolist() if "finance.yahoo" in url]
    filtered_urls = df[df['Url'].str.contains("finance.yahoo", na=False)]
    filtered_ticker_list = []
    for url, ticker in zip(filtered_urls['Url'], filtered_urls['Ticker']):
        filtered_ticker_list.append(ticker)

    return filtered_url_list, filtered_ticker_list
